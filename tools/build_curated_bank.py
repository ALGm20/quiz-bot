import json
import re
from collections import defaultdict
from pathlib import Path


RAW_PATH = Path(r"C:\Users\Yasser\Documents\New project\plant_quiz_bot\analysis\raw_docx_questions.json")
OUT_PATH = Path(r"C:\Users\Yasser\Documents\New project\plant_quiz_bot\data\plant_question_bank.json")
ANSWER_KEY_PATH = Path(r"C:\Users\Yasser\Documents\New project\plant_quiz_bot\analysis\plant_mcq_answer_key.md")


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def normalize_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def parse_answer_pairs(text: str):
    mapping = {}
    for token in text.split():
        num, answer = token.split(":")
        mapping[int(num)] = answer.strip().upper()
    return mapping


MANUAL_ANSWERS = {
    "Choose the correct -Diyala (2).docx": parse_answer_pairs(
        """
        1:C 2:B 3:B 4:C 5:C 6:B 7:B 8:B 9:B 10:B 11:B 12:B 13:B 14:A 15:B 16:B 17:B 18:B 19:D 20:B
        21:B 22:B 23:C 24:B 25:B 26:C 27:B 28:B 29:D 30:B 31:B 32:B 33:B 34:B 35:A 36:B 37:B 38:C 39:B 40:C
        41:B 42:B 43:B 44:C 45:A 46:B 47:D 48:B 49:B 50:D 51:B 52:B 53:B 54:B 55:B 56:B 57:B 58:B 59:A 60:B
        61:C 62:D 63:B 64:C 65:A 66:B 67:B 68:A 69:B 70:B 71:A 72:A 73:B 74:D 75:B 76:B 77:A 78:C 79:B 80:C
        81:B 82:B 83:D 84:B 85:C 86:B 87:D 88:B 89:D 90:B 91:D 92:B 93:D 94:A 95:D 96:A 97:D 98:D 99:A 100:A
        101:D 102:C 103:A 104:C 105:A 106:B 107:B 108:B 109:B 110:A 111:C 112:A 113:B 114:B 115:B 116:A 117:B 118:B 119:C 120:B
        121:B 122:A 123:C 124:A 125:A 126:B 127:C 128:B 129:B 130:B 131:A 132:B 133:B 134:B 135:B 136:C 137:A 138:B 139:C 140:B
        141:B 142:A 143:A 144:A 145:B 146:A 147:A 148:A 149:B 150:A 151:A 152:A 153:B 154:A 155:A 156:B 157:A 158:B 159:B 160:B
        161:A 162:A 163:B 164:A 165:A 166:A 167:C 168:B 169:A 170:B 171:A 172:C 173:A 174:B 175:A 176:A 177:A 178:B 179:A 180:A
        181:C 182:A 183:A 184:A 185:A 186:A 187:C 188:B 189:B 190:A 191:C 192:B 193:C 194:B 195:B 196:A 197:C 198:A 199:B 200:B
        201:A 202:A 203:A 204:A 205:A 206:B 207:A 208:A 209:A 210:A 211:A 212:C 213:A
        """
    ),
    "MCQ TX 2.docx": parse_answer_pairs(
        """
        1:C 2:B 3:C 4:B 5:C 6:D 7:C 8:B 9:B 10:C
        11:B 12:B 13:C 14:C 15:C 16:C 17:D 18:B 19:B 20:B
        """
    ),
    "MCQ-3.docx": parse_answer_pairs(
        """
        1:B 2:C 3:A 4:B 5:B 6:B 7:B 8:B 9:A 10:C
        11:A 12:B 13:A 14:B 15:A 16:B 17:C 18:C 19:A 20:A
        21:B 22:C 23:B 24:A 25:C
        """
    ),
    "MCQ TX-1 HW (2).docx": parse_answer_pairs("16:C 24:C"),
    "MCQ TX-1 HW.docx": parse_answer_pairs("16:C 24:C"),
    "Training 1          MCQ (2).docx": parse_answer_pairs("9:B"),
}


SKIP_SOURCE_NUMS = {
    ("Choose the correct -Diyala (2).docx", 7),
    ("Choose the correct -Diyala (2).docx", 88),
    ("Choose the correct -Diyala (2).docx", 96),
    ("Choose the correct -Diyala (2).docx", 134),
    ("Choose the correct -Diyala (2).docx", 135),
    ("Choose the correct -Diyala (2).docx", 201),
    ("Choose the correct -Diyala (2).docx", 208),
    ("Choose the correct -Diyala (2).docx", 209),
    ("Choose the correct -Diyala (2).docx", 210),
    ("Choose the correct -Diyala (2).docx", 211),
    ("MCQ TX-1 (2).docx", 753),
    ("MCQ TX-1 HW (2).docx", 753),
    ("MCQ TX-1 HW.docx", 753),
}


TEXT_OVERRIDES = {
    ("Choose the correct -Diyala (2).docx", 104): {
        "question": "Which term describes a leaf margin with sharp teeth pointing upward like a saw?",
    },
    ("Choose the correct -Diyala (2).docx", 179): {
        "question": "A leaf with a cirrhose apex is seen in:",
    },
    ("Choose the correct -Diyala (2).docx", 203): {
        "question": "A flower with a spurred corolla is:",
    },
    ("MCQ-3.docx", 17): {
        "d": "Terminal bud",
    },
    ("MCQ TX-1 HW (2).docx", 16): {
        "question": "In writing scientific names, the genus starts with:",
    },
    ("MCQ TX-1 HW.docx", 16): {
        "question": "In writing scientific names, the genus starts with:",
    },
}


MANUAL_QUESTIONS = [
    {
        "file": "Choose the correct -Diyala (2).docx",
        "num": 170,
        "question": "Which leaf type has four leaflets?",
        "a": "Trifoliate",
        "b": "Quadrifoliate",
        "c": "Multifoliate",
        "d": "Bifoliate",
        "answer": "B",
    },
    {
        "file": "MCQ TX-1 (2).docx",
        "num": 30,
        "question": 'The book "Species Plantarum" (1753) was published by:',
        "a": "De Candolle",
        "b": "Bentham",
        "c": "Linnaeus",
        "d": "Eichler",
        "answer": "C",
    },
    {
        "file": "MCQ TX-1 HW (2).docx",
        "num": 30,
        "question": 'The book "Species Plantarum" (1753) was published by:',
        "a": "De Candolle",
        "b": "Bentham",
        "c": "Linnaeus",
        "d": "Eichler",
        "answer": "C",
    },
    {
        "file": "MCQ TX-1 HW.docx",
        "num": 30,
        "question": 'The book "Species Plantarum" (1753) was published by:',
        "a": "De Candolle",
        "b": "Bentham",
        "c": "Linnaeus",
        "d": "Eichler",
        "answer": "C",
    },
]


SECTION_ORDER = [
    "التصنيف النباتي والنظاميات",
    "مورفولوجيا النبات العامة",
    "العادات النباتية ودورة الحياة",
    "الجذور وتحوّراتها",
    "الساق وتحوّراته",
    "الأوراق",
    "الأزهار والتكاثر الزهري",
    "البيئات النباتية والتكيفات البيئية",
]


SECTION_EMOJI = {
    "التصنيف النباتي والنظاميات": "🧭",
    "مورفولوجيا النبات العامة": "🌱",
    "العادات النباتية ودورة الحياة": "🌿",
    "الجذور وتحوّراتها": "🌰",
    "الساق وتحوّراته": "🌾",
    "الأوراق": "🍃",
    "الأزهار والتكاثر الزهري": "🌸",
    "البيئات النباتية والتكيفات البيئية": "🌍",
}


def assign_section(question: str, source_file: str) -> str:
    q = question.lower()

    taxonomy_terms = [
        "taxonomy",
        "systematics",
        "biosystematics",
        "nomenclature",
        "taxon",
        "classification",
        "binomial",
        "dichotomous key",
        "polyclave",
        "apg",
        "alpha taxonomy",
        "beta taxonomy",
        "gamma taxonomy",
        "omega taxonomy",
        "species plantarum",
        "icbn",
        "icnafp",
        "phyletic",
        "cladistic",
        "theophrastus",
    ]
    if any(term in q for term in taxonomy_terms):
        return "التصنيف النباتي والنظاميات"

    flower_terms = [
        "flower",
        "floral",
        "sepal",
        "petal",
        "corolla",
        "calyx",
        "androecium",
        "gynoecium",
        "pistil",
        "stamen",
        "anther",
        "stigma",
        "ovary",
        "perianth",
        "pappus",
        "spathe",
        "bilabiate",
        "papilionaceous",
        "campanulate",
        "ligulate",
        "urceolate",
        "zygomorphic",
        "actinomorphic",
        "monoecious",
        "dioecious",
    ]
    if any(term in q for term in flower_terms) or "flower" in source_file.lower():
        return "الأزهار والتكاثر الزهري"

    leaf_terms = [
        "leaf",
        "leaves",
        "petiole",
        "phyllotaxy",
        "stipule",
        "venation",
        "margin",
        "apex",
        "leaflet",
        "pinnate",
        "palmate",
        "glabrous",
        "sericeous",
        "tomentose",
        "villous",
        "rugose",
        "reniform",
        "cordate",
        "auriculate",
        "amplexicaul",
        "ciliate",
        "peltate",
    ]
    if any(term in q for term in leaf_terms) or "leaves" in source_file.lower():
        return "الأوراق"

    root_terms = [
        "root",
        "roots",
        "taproot",
        "fibrous",
        "fusiform",
        "conical",
        "napiform",
        "haustoria",
        "haustorial",
        "pneumatophore",
        "pneumatophores",
        "velamen",
        "buttress roots",
        "prop roots",
        "contractile roots",
    ]
    if any(term in q for term in root_terms):
        return "الجذور وتحوّراتها"

    stem_terms = [
        "stem",
        "node",
        "internode",
        "rhizome",
        "tuber",
        "bulb",
        "corm",
        "subaerial",
        "runner",
        "stolon",
        "phylloclade",
        "thorn",
        "tendril",
        "decumbent",
        "winged stem",
        "quadrangular stem",
        "cylindrical stem",
        "hollow cylindrical stem",
        "tree with a single main stem",
        "excurrent",
    ]
    if any(term in q for term in stem_terms):
        return "الساق وتحوّراته"

    ecology_terms = [
        "halophyte",
        "hydrophyte",
        "xerophyte",
        "mesophyte",
        "psammophyte",
        "psammophytes",
        "epiphyte",
        "epiphytes",
        "lithophyte",
        "saprophyte",
        "helophyte",
        "geophyte",
        "oxyphyte",
        "oxylophyte",
        "liana",
        "saline habitats",
        "aquatic",
        "decaying organic matter",
        "rocks",
        "sand",
        "water",
        "marshes",
        "mangroves",
    ]
    if any(term in q for term in ecology_terms):
        return "البيئات النباتية والتكيفات البيئية"

    habit_terms = [
        "annual",
        "biennial",
        "perennial",
        "ephemeral",
        "monocarpic",
        "shrub",
        "tree",
        "herb",
        "herbaceous",
        "vine",
        "subshrub",
        "suffrutescent",
        "woody",
        "life cycle",
        "angiosperm",
        "gymnosperm",
        "monocot",
        "dicot",
        "vegetative organ",
        "reproductive organ",
        "qualitative traits",
        "quantitative traits",
    ]
    if any(term in q for term in habit_terms):
        return "العادات النباتية ودورة الحياة"

    return "مورفولوجيا النبات العامة"


def load_questions():
    raw_data = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    items = []

    for entry in raw_data:
        source_file = Path(entry["file"]).name
        for question in entry["questions"]:
            if (source_file, question["num"]) in SKIP_SOURCE_NUMS:
                continue

            item = {
                "file": source_file,
                "num": int(question["num"]),
                "question": normalize_text(question["question"]),
                "a": normalize_text(question["a"]),
                "b": normalize_text(question["b"]),
                "c": normalize_text(question["c"]),
                "d": normalize_text(question["d"]),
                "answer": (question.get("answer") or "").strip().upper(),
            }

            override = TEXT_OVERRIDES.get((source_file, item["num"]))
            if override:
                item.update({key: normalize_text(value) for key, value in override.items()})

            if not item["answer"]:
                item["answer"] = MANUAL_ANSWERS.get(source_file, {}).get(item["num"], "")

            items.append(item)

    for question in MANUAL_QUESTIONS:
        if (question["file"], question["num"]) in SKIP_SOURCE_NUMS:
            continue
        items.append(dict(question))

    return items


def build_bank():
    items = load_questions()
    groups = defaultdict(list)

    for item in items:
        key = "|".join(
            [
                normalize_key(item["question"]),
                normalize_key(item["a"]),
                normalize_key(item["b"]),
                normalize_key(item["c"]),
                normalize_key(item["d"]),
            ]
        )
        groups[key].append(item)

    curated = []
    unresolved = []

    for group_items in groups.values():
        answered = [item for item in group_items if item["answer"] in {"A", "B", "C", "D"}]
        rep = dict(answered[0] if answered else group_items[0])
        if not rep["answer"]:
            unresolved.append(rep)
            continue

        rep["section"] = assign_section(rep["question"], rep["file"])
        rep["sources"] = sorted({f"{item['file']}#{item['num']}" for item in group_items})
        curated.append(rep)

    if unresolved:
        lines = []
        for item in sorted(unresolved, key=lambda q: (q["file"], q["num"])):
            lines.append(
                f"{item['file']}#{item['num']} | {item['question']} | "
                f"A={item['a']} | B={item['b']} | C={item['c']} | D={item['d']}"
            )
        raise SystemExit("Unresolved answers remain:\n" + "\n".join(lines))

    section_buckets = {name: [] for name in SECTION_ORDER}
    for item in curated:
        section_buckets[item["section"]].append(item)

    result = []
    for section_index, section_name in enumerate(SECTION_ORDER, start=1):
        questions = sorted(section_buckets[section_name], key=lambda q: (q["file"], q["num"], q["question"]))
        for order, question in enumerate(questions, start=1):
            result.append(
                {
                    "section": section_name,
                    "section_order": section_index,
                    "section_emoji": SECTION_EMOJI[section_name],
                    "question": question["question"],
                    "a": question["a"],
                    "b": question["b"],
                    "c": question["c"],
                    "d": question["d"],
                    "answer": question["answer"],
                    "order": order,
                    "source_files": question["sources"],
                }
            )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    answer_lines = ["# Plant MCQ Answer Key", ""]
    for section_name in SECTION_ORDER:
        answer_lines.append(f"## {section_name}")
        answer_lines.append("")
        section_items = [item for item in result if item["section"] == section_name]
        for index, item in enumerate(section_items, start=1):
            correct_text = item[item["answer"].lower()]
            answer_lines.append(f"{index}. {item['question']}")
            answer_lines.append(f"   Answer: {item['answer']}) {correct_text}")
        answer_lines.append("")
    ANSWER_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    ANSWER_KEY_PATH.write_text("\n".join(answer_lines), encoding="utf-8")

    counts = defaultdict(int)
    for item in result:
        counts[item["section"]] += 1

    print(f"Built {len(result)} curated questions.")
    for section_name in SECTION_ORDER:
        print(f"{section_name}: {counts[section_name]}")


if __name__ == "__main__":
    build_bank()
