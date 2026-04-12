import json
import re
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def normalize_text(text: str) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\u00bd": "1/2",
        "\u2714": " ",
        "\u2705": " ",
        "âœ…": " ",
        "â€“": "-",
        "â€”": "-",
        "â€œ": '"',
        "â€\u200c": '"',
        "â€™": "'",
        "€™": "'",
        "آ½": "1/2",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_paragraphs(docx_path: Path):
    with zipfile.ZipFile(docx_path) as zf:
        xml_bytes = zf.read("word/document.xml")
    root = ET.fromstring(xml_bytes)
    paragraphs = []
    for para in root.findall(".//w:body/w:p", NS):
        texts = [node.text or "" for node in para.findall(".//w:t", NS)]
        line = normalize_text("".join(texts))
        if line:
            paragraphs.append(line)
    return paragraphs


QUESTION_SPLIT_RE = re.compile(r"(?=(?:^|\s)(\d{1,3})\s*[\.\-\)])")
OPTION_RE = re.compile(
    r"^\s*(?P<question>.*?)\s+"
    r"A[\.\)]\s*(?P<a>.*?)\s+"
    r"B[\.\)]\s*(?P<b>.*?)\s+"
    r"C[\.\)]\s*(?P<c>.*?)\s+"
    r"D[\.\)]\s*(?P<d_and_answer>.*)$",
    re.IGNORECASE | re.DOTALL,
)


def split_question_blocks(text: str):
    matches = list(re.finditer(r"(\d{1,3})\s*[\.\-\)]", text))
    blocks = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append(text[start:end].strip())
    return blocks


def parse_question_block(block: str):
    number_match = re.match(r"^\s*(\d{1,3})\s*[\.\-\)]\s*(.*)$", block, re.DOTALL)
    if not number_match:
        return None

    number = int(number_match.group(1))
    body = normalize_text(number_match.group(2))

    body = re.sub(r"\s+Answer\s*[:：]\s*([ABCDabcd])(?:[\.\)]\s*)?.*$", r" Answer: \1", body)
    match = OPTION_RE.match(body)
    if not match:
        return None

    parts = {key: normalize_text(value or "") for key, value in match.groupdict().items()}
    d_and_answer = parts["d_and_answer"]
    answer_match = re.search(r"\bAnswer\s*[:：]\s*([ABCDabcd])\b", d_and_answer, re.IGNORECASE)
    answer = answer_match.group(1).upper() if answer_match else ""
    d_text = re.sub(r"\bAnswer\s*[:：]\s*[ABCDabcd]\b.*$", "", d_and_answer, flags=re.IGNORECASE).strip()

    item = {
        "num": number,
        "question": parts["question"],
        "a": parts["a"],
        "b": parts["b"],
        "c": parts["c"],
        "d": normalize_text(d_text),
        "answer": answer if answer in {"A", "B", "C", "D"} else "",
        "source_line": block,
    }
    return item


def parse_questions(paragraphs):
    whole_text = normalize_text(" ".join(paragraphs))
    blocks = split_question_blocks(whole_text)
    questions = []
    unmatched = []

    for block in blocks:
        parsed = parse_question_block(block)
        if parsed:
            questions.append(parsed)
        else:
            unmatched.append(block)

    return questions, unmatched


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    payload = []
    for raw_path in args.paths:
        path = Path(raw_path)
        paragraphs = extract_paragraphs(path)
        questions, unmatched = parse_questions(paragraphs)
        payload.append(
            {
                "file": str(path),
                "paragraphs": paragraphs,
                "questions": questions,
                "unmatched": unmatched,
            }
        )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
