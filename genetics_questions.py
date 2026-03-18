"""
genetics_questions.py — سكشن الوراثة والجينات
جميع الأسئلة محوّلة لـ MCQ بـ 3 أشكال
"""

GENETICS_QUESTIONS = [

    # ══════════════════════════════════════════════════════════════
    # SECTION 1: MCQ الأصلية (Q1-Q60)
    # ══════════════════════════════════════════════════════════════

    {"section":"الوراثة والجينات","section_emoji":"🧬",
     "section_description":"Genetics, DNA, Replication, Transcription, Translation, Mutations",
     "question":"Genetics is defined as the study of:",
     "a":"Cell metabolism","b":"Genes and how information is carried, expressed, and replicated",
     "c":"Protein synthesis only","d":"Cell membrane structure",
     "answer":"B","explanation":"Genetics studies genes: what they are, how they carry info, how expressed, and how replicated."},

    {"section":"الوراثة والجينات",
     "question":"A gene is:",
     "a":"RNA molecule","b":"Segment of DNA that encodes a functional product",
     "c":"Protein enzyme","d":"Lipid structure",
     "answer":"B","explanation":"A gene = a segment of DNA that encodes a functional product, usually a protein."},

    {"section":"الوراثة والجينات",
     "question":"Genome refers to:",
     "a":"One gene","b":"RNA molecules","c":"All genetic material in a cell","d":"Ribosomes",
     "answer":"C","explanation":"Genome = ALL genetic material in a cell."},

    {"section":"الوراثة والجينات",
     "question":"Genomics is:",
     "a":"Study of proteins","b":"Molecular study of genomes","c":"Study of RNA","d":"Study of mutations only",
     "answer":"B","explanation":"Genomics = the molecular study of genomes and their functions."},

    {"section":"الوراثة والجينات",
     "question":"Genotype refers to:",
     "a":"Physical characteristics","b":"Genetic composition of an organism","c":"RNA sequence","d":"Protein type",
     "answer":"B","explanation":"Genotype = the genes of an organism (its genetic makeup)."},

    {"section":"الوراثة والجينات",
     "question":"Phenotype represents:",
     "a":"DNA structure","b":"Expression of genes","c":"RNA sequence","d":"Chromosome number",
     "answer":"B","explanation":"Phenotype = the physical expression of genes (observable characteristics)."},

    {"section":"الوراثة والجينات",
     "question":"DNA is a polymer of:",
     "a":"Amino acids","b":"Nucleotides","c":"Lipids","d":"Sugars",
     "answer":"B","explanation":"DNA is a polymer made of nucleotide subunits (adenine, thymine, cytosine, guanine)."},

    {"section":"الوراثة والجينات",
     "question":"The bases in DNA are:",
     "a":"Adenine, Uracil, Cytosine, Guanine","b":"Adenine, Thymine, Cytosine, Guanine",
     "c":"Adenine, Thymine, Cytosine, Uracil","d":"Adenine, Uracil, Guanine, Cytosine",
     "answer":"B","explanation":"DNA bases: Adenine (A), Thymine (T), Cytosine (C), Guanine (G). RNA uses Uracil instead of Thymine."},

    {"section":"الوراثة والجينات",
     "question":"DNA structure is described as:",
     "a":"Single helix","b":"Double helix","c":"Triple helix","d":"Linear strand",
     "answer":"B","explanation":"DNA has a double helix structure — two antiparallel strands wound around each other."},

    {"section":"الوراثة والجينات",
     "question":"DNA strands are held together by:",
     "a":"Covalent bonds","b":"Hydrogen bonds","c":"Ionic bonds","d":"Peptide bonds",
     "answer":"B","explanation":"Hydrogen bonds between complementary base pairs (A-T: 2 H-bonds, G-C: 3 H-bonds) hold DNA strands together."},

    {"section":"الوراثة والجينات",
     "question":"DNA strands are described as:",
     "a":"Parallel","b":"Antiparallel","c":"Perpendicular","d":"Random",
     "answer":"B","explanation":"DNA strands are antiparallel — one runs 5'→3' while the other runs 3'→5'."},

    {"section":"الوراثة والجينات",
     "question":"DNA backbone consists of:",
     "a":"Amino acids and lipids","b":"Deoxyribose-phosphate","c":"Ribose-phosphate","d":"Glucose-phosphate",
     "answer":"B","explanation":"The DNA backbone is made of alternating deoxyribose sugar and phosphate groups."},

    {"section":"الوراثة والجينات",
     "question":"DNA replication is described as:",
     "a":"Conservative","b":"Semiconservative","c":"Dispersive","d":"Random",
     "answer":"B","explanation":"DNA replication is semiconservative: each new DNA molecule contains one original strand and one new strand."},

    {"section":"الوراثة والجينات",
     "question":"DNA replication direction is:",
     "a":"3'→5'","b":"5'→3'","c":"Both directions simultaneously","d":"Random direction",
     "answer":"B","explanation":"DNA synthesis always proceeds in the 5'→3' direction."},

    {"section":"الوراثة والجينات",
     "question":"DNA replication is initiated by:",
     "a":"DNA polymerase","b":"RNA primer","c":"Ligase","d":"Helicase",
     "answer":"B","explanation":"DNA replication is initiated by an RNA primer synthesized by primase."},

    {"section":"الوراثة والجينات",
     "question":"The leading strand is synthesized:",
     "a":"Discontinuously","b":"Continuously","c":"In short fragments","d":"From 3'→5'",
     "answer":"B","explanation":"The leading strand is synthesized continuously in the 5'→3' direction."},

    {"section":"الوراثة والجينات",
     "question":"The lagging strand is synthesized:",
     "a":"Continuously","b":"Discontinuously (Okazaki fragments)","c":"In one piece","d":"From 5'→3' continuously",
     "answer":"B","explanation":"The lagging strand is synthesized discontinuously as Okazaki fragments."},

    {"section":"الوراثة والجينات",
     "question":"Okazaki fragments are joined by:",
     "a":"Helicase","b":"DNA ligase","c":"RNA polymerase","d":"Primase",
     "answer":"B","explanation":"DNA ligase seals the nicks between Okazaki fragments on the lagging strand."},

    {"section":"الوراثة والجينات",
     "question":"Transcription is:",
     "a":"DNA to protein","b":"DNA to RNA","c":"RNA to protein","d":"RNA to DNA",
     "answer":"B","explanation":"Transcription = the process of making RNA from a DNA template."},

    {"section":"الوراثة والجينات",
     "question":"Transcription is carried out by:",
     "a":"DNA polymerase","b":"RNA polymerase","c":"Ligase","d":"Helicase",
     "answer":"B","explanation":"RNA polymerase binds to the promoter and synthesizes mRNA from the DNA template."},

    {"section":"الوراثة والجينات",
     "question":"Transcription begins when RNA polymerase binds to:",
     "a":"Start codon","b":"Promoter","c":"Terminator","d":"Ribosome",
     "answer":"B","explanation":"Transcription begins when RNA polymerase binds to the promoter sequence on DNA."},

    {"section":"الوراثة والجينات",
     "question":"Transcription ends at:",
     "a":"Start codon","b":"Terminator sequence","c":"Promoter","d":"Ribosome",
     "answer":"B","explanation":"Transcription ends when RNA polymerase reaches the terminator sequence."},

    {"section":"الوراثة والجينات",
     "question":"Translation is:",
     "a":"DNA to RNA","b":"mRNA to protein","c":"RNA to DNA","d":"DNA to protein directly",
     "answer":"B","explanation":"Translation = decoding mRNA to synthesize a protein at the ribosome."},

    {"section":"الوراثة والجينات",
     "question":"Translation occurs at:",
     "a":"Nucleus","b":"Ribosome","c":"Mitochondria","d":"Golgi apparatus",
     "answer":"B","explanation":"Translation occurs at ribosomes, which read the mRNA codons."},

    {"section":"الوراثة والجينات",
     "question":"A codon consists of:",
     "a":"2 nucleotides","b":"3 nucleotides","c":"4 nucleotides","d":"1 nucleotide",
     "answer":"B","explanation":"A codon = 3 consecutive nucleotides on mRNA that specify one amino acid."},

    {"section":"الوراثة والجينات",
     "question":"The start codon is:",
     "a":"UAA","b":"AUG","c":"UAG","d":"UGA",
     "answer":"B","explanation":"AUG is the universal start codon — it codes for methionine."},

    {"section":"الوراثة والجينات",
     "question":"Stop codons are:",
     "a":"AUG, UAA, UAG","b":"UAA, UAG, UGA","c":"UGA, AUG, UAA","d":"GUA, CAU, ACG",
     "answer":"B","explanation":"The three stop codons are UAA, UAG, and UGA — they signal termination of translation."},

    {"section":"الوراثة والجينات",
     "question":"Amino acids are carried to ribosomes by:",
     "a":"mRNA","b":"tRNA","c":"rRNA","d":"DNA",
     "answer":"B","explanation":"tRNA (transfer RNA) carries specific amino acids to the ribosome during translation."},

    {"section":"الوراثة والجينات",
     "question":"mRNA is read in the direction:",
     "a":"3'→5'","b":"5'→3'","c":"Random","d":"Bidirectional",
     "answer":"B","explanation":"mRNA is read 5'→3' by the ribosome during translation."},

    {"section":"الوراثة والجينات",
     "question":"Ribosome mainly consists of:",
     "a":"DNA and protein","b":"rRNA and protein","c":"Lipids","d":"Carbohydrates",
     "answer":"B","explanation":"Ribosomes are made of ribosomal RNA (rRNA) and proteins."},

    {"section":"الوراثة والجينات",
     "question":"The template for protein synthesis is:",
     "a":"DNA","b":"mRNA","c":"tRNA","d":"rRNA",
     "answer":"B","explanation":"mRNA serves as the template during translation."},

    {"section":"الوراثة والجينات",
     "question":"The central dogma of molecular biology is:",
     "a":"RNA→DNA→Protein","b":"DNA→RNA→Protein","c":"Protein→DNA→RNA","d":"RNA→Protein→DNA",
     "answer":"B","explanation":"Central dogma: DNA→(Transcription)→RNA→(Translation)→Protein."},

    {"section":"الوراثة والجينات",
     "question":"Reverse transcription occurs in:",
     "a":"Bacteria","b":"Plants","c":"Some viruses (retroviruses)","d":"Animals only",
     "answer":"C","explanation":"Reverse transcription (RNA→DNA) occurs in retroviruses like HIV, using reverse transcriptase."},

    {"section":"الوراثة والجينات",
     "question":"DNA replication results in:",
     "a":"Two identical DNA molecules","b":"RNA molecules","c":"Protein molecules","d":"Mutated DNA",
     "answer":"A","explanation":"DNA replication produces two identical DNA molecules — each with one original and one new strand."},

    {"section":"الوراثة والجينات",
     "question":"Genetic information is stored in:",
     "a":"Proteins","b":"DNA base sequence","c":"Lipids","d":"Carbohydrates",
     "answer":"B","explanation":"Genetic information is encoded in the specific sequence of DNA bases (A, T, C, G)."},

    {"section":"الوراثة والجينات",
     "question":"Translation ends when:",
     "a":"Ribosome meets promoter","b":"Stop codon appears","c":"RNA polymerase stops","d":"DNA replication begins",
     "answer":"B","explanation":"Translation terminates when the ribosome encounters a stop codon (UAA, UAG, or UGA)."},

    {"section":"الوراثة والجينات",
     "question":"Gene expression involves:",
     "a":"Replication only","b":"Transcription and translation","c":"Mutation only","d":"Protein folding",
     "answer":"B","explanation":"Gene expression = transcription (DNA→mRNA) + translation (mRNA→protein)."},

    {"section":"الوراثة والجينات",
     "question":"DNA replication ensures:",
     "a":"Energy production","b":"Genetic continuity","c":"Protein folding","d":"Mutation",
     "answer":"B","explanation":"DNA replication ensures genetic continuity by passing identical genetic information to daughter cells."},

    # ── Mutations ────────────────────────────────────────────────

    {"section":"الوراثة والجينات",
     "question":"A mutation is defined as:",
     "a":"Normal DNA replication","b":"Change in DNA base sequence","c":"Protein synthesis error","d":"RNA degradation",
     "answer":"B","explanation":"A mutation = any change in the DNA base sequence."},

    {"section":"الوراثة والجينات",
     "question":"Spontaneous mutations occur:",
     "a":"Due to radiation","b":"Without mutagens (mistakes in DNA replication)","c":"From chemicals","d":"Only in bacteria",
     "answer":"B","explanation":"Spontaneous mutations arise without external mutagens — they occur due to errors during DNA replication."},

    {"section":"الوراثة والجينات",
     "question":"Induced mutations are caused by:",
     "a":"Normal cell division","b":"Mutagens (chemicals or radiation)","c":"Protein synthesis","d":"Ribosome activity",
     "answer":"B","explanation":"Induced mutations are caused by mutagens: chemical agents or radiation."},

    {"section":"الوراثة والجينات",
     "question":"Nitrous acid causes mutation by:",
     "a":"Inserting between bases","b":"Altering adenine to pair with cytosine instead of thymine",
     "c":"Breaking chromosomes","d":"Forming thymine dimers",
     "answer":"B","explanation":"Nitrous acid deaminates adenine → hypoxanthine → pairs with C instead of T → mutation."},

    {"section":"الوراثة والجينات",
     "question":"Ethidium bromide causes mutation by:",
     "a":"Breaking chromosomes","b":"Inserting between bases causing frameshift",
     "c":"Forming thymine dimers","d":"Altering base pairing",
     "answer":"B","explanation":"Ethidium bromide is an intercalating agent that inserts between DNA bases → frameshift mutation."},

    {"section":"الوراثة والجينات",
     "question":"Ionizing radiation (X-rays, gamma rays) causes:",
     "a":"Base substitution only","b":"Chromosomal breaks","c":"Protein synthesis","d":"RNA degradation",
     "answer":"B","explanation":"Ionizing radiation causes chromosomal breaks and double-strand DNA breaks."},

    {"section":"الوراثة والجينات",
     "question":"UV radiation causes:",
     "a":"DNA deletion","b":"Thymine dimers","c":"Protein damage","d":"RNA mutation",
     "answer":"B","explanation":"UV radiation causes thymine dimers — adjacent thymine bases bond together, blocking replication."},

    {"section":"الوراثة والجينات",
     "question":"Base substitution mutation is also called:",
     "a":"Frameshift mutation","b":"Point mutation","c":"Deletion mutation","d":"Inversion",
     "answer":"B","explanation":"Base substitution = point mutation — one base is replaced by another."},

    {"section":"الوراثة والجينات",
     "question":"Missense mutation results in:",
     "a":"No amino acid change","b":"Change in amino acid","c":"Stop codon","d":"DNA deletion",
     "answer":"B","explanation":"Missense mutation changes one base → different amino acid is incorporated into the protein."},

    {"section":"الوراثة والجينات",
     "question":"Nonsense mutation results in:",
     "a":"Amino acid change","b":"Stop codon formation (premature)","c":"Frameshift","d":"Duplication",
     "answer":"B","explanation":"Nonsense mutation changes a codon to a stop codon → premature termination of translation."},

    {"section":"الوراثة والجينات",
     "question":"Frameshift mutation occurs due to:",
     "a":"Base substitution","b":"Insertion or deletion of nucleotides","c":"Stop codon","d":"Protein folding",
     "answer":"B","explanation":"Frameshift mutation: insertion or deletion of nucleotides (not in multiples of 3) shifts the reading frame."},

    {"section":"الوراثة والجينات",
     "question":"Frameshift mutation affects:",
     "a":"One codon only","b":"Entire reading frame downstream","c":"One nucleotide","d":"One amino acid",
     "answer":"B","explanation":"Frameshift shifts ALL codons downstream → usually produces a non-functional protein."},

    # ── Section 2: Example MCQ ───────────────────────────────────

    {"section":"الوراثة والجينات",
     "question":"The process of copying DNA prior to cell division is called:",
     "a":"Transcription","b":"Translation","c":"DNA replication","d":"Mutation",
     "answer":"C","explanation":"DNA replication copies the DNA before cell division to ensure each daughter cell receives a complete genome."},

    {"section":"الوراثة والجينات",
     "question":"During DNA replication, which strand is synthesized continuously?",
     "a":"Lagging strand","b":"Leading strand","c":"Both strands equally","d":"Neither strand",
     "answer":"B","explanation":"The leading strand is synthesized continuously in the 5'→3' direction toward the replication fork."},

    {"section":"الوراثة والجينات",
     "question":"The process by which mRNA is synthesized from a DNA template is known as:",
     "a":"Translation","b":"Replication","c":"Transcription","d":"Mutation",
     "answer":"C","explanation":"Transcription = synthesis of RNA from a DNA template by RNA polymerase."},

    {"section":"الوراثة والجينات",
     "question":"A mutation that results in the substitution of one amino acid for another is called a:",
     "a":"Nonsense mutation","b":"Frameshift mutation","c":"Missense mutation","d":"Silent mutation",
     "answer":"C","explanation":"Missense mutation: base change → different amino acid. Nonsense = stop codon. Silent = no change."},

    {"section":"الوراثة والجينات",
     "question":"Which type of mutation involves insertion or deletion that shifts the reading frame?",
     "a":"Missense mutation","b":"Nonsense mutation","c":"Frameshift mutation","d":"Silent mutation",
     "answer":"C","explanation":"Frameshift mutation: insertion/deletion shifts reading frame → all downstream codons change."},

    {"section":"الوراثة والجينات",
     "question":"A mutation that does NOT change the amino acid sequence is referred to as a:",
     "a":"Silent mutation","b":"Missense mutation","c":"Nonsense mutation","d":"Frameshift mutation",
     "answer":"A","explanation":"Silent mutation: base change → same amino acid (due to degeneracy of the genetic code)."},

    {"section":"الوراثة والجينات",
     "question":"Which statement about microbial genetics is TRUE?",
     "a":"The genome consists only of genes that encode proteins",
     "b":"Transcription synthesizes DNA from RNA",
     "c":"Translation decodes mRNA to synthesize proteins",
     "d":"DNA replication occurs during translation",
     "answer":"C","explanation":"Translation = decoding mRNA codons → protein synthesis at ribosomes. Central dogma."},

    # ── Section 3: Photos ─────────────────────────────────────────

    {"section":"الوراثة والجينات",
     "question":"Which RNA molecule carries amino acids to the ribosome during protein synthesis?",
     "a":"mRNA","b":"rRNA","c":"tRNA","d":"siRNA",
     "answer":"C","explanation":"tRNA carries specific amino acids to the ribosome and matches them to mRNA codons (anticodon-codon)."},

    {"section":"الوراثة والجينات",
     "question":"What is the primary role of mRNA in a cell?",
     "a":"Transporting amino acids for protein synthesis",
     "b":"Carrying genetic instructions from DNA to ribosomes",
     "c":"Regulating gene expression only",
     "d":"Storing genetic information permanently",
     "answer":"B","explanation":"mRNA carries the genetic code from DNA in the nucleus to ribosomes in the cytoplasm."},

    {"section":"الوراثة والجينات",
     "question":"A frameshift mutation is caused by:",
     "a":"Substituting one nucleotide for another","b":"Adding or deleting a single nucleotide",
     "c":"Breaking a chromosome","d":"Doubling the genome",
     "answer":"B","explanation":"Frameshift = insertion or deletion of nucleotides (shifts the reading frame of all downstream codons)."},

    # ══════════════════════════════════════════════════════════════
    # SECTION 5: T/F + Choose محوّلة لـ MCQ (شكلين لكل واحدة)
    # ══════════════════════════════════════════════════════════════

    # T/F 75 — Leading strand
    {"section":"الوراثة والجينات",
     "question":"How is the leading strand synthesized during DNA replication?",
     "a":"Discontinuously as Okazaki fragments","b":"Continuously in the 5'→3' direction",
     "c":"From 3'→5' direction","d":"Using RNA ligase",
     "answer":"B","explanation":"The leading strand is synthesized CONTINUOUSLY — it follows the replication fork in 5'→3' direction."},

    {"section":"الوراثة والجينات",
     "question":"True or False: The leading strand in DNA replication is synthesized discontinuously.",
     "a":"True — it is synthesized in Okazaki fragments",
     "b":"False — the leading strand is synthesized CONTINUOUSLY",
     "c":"True — both strands are discontinuous",
     "d":"False — it is synthesized from 3'→5'",
     "answer":"B","explanation":"FALSE. The LAGGING strand is discontinuous. The LEADING strand is synthesized continuously."},

    # T/F 76 — Genotype vs Phenotype
    {"section":"الوراثة والجينات",
     "question":"Which term refers to the PHYSICAL expression of an organism's genes?",
     "a":"Genotype","b":"Phenotype","c":"Genome","d":"Genomics",
     "answer":"B","explanation":"Phenotype = physical/observable expression of genes. Genotype = the actual genes."},

    {"section":"الوراثة والجينات",
     "question":"True or False: The genotype of an organism refers to the PHYSICAL expression of its genes.",
     "a":"True — genotype and phenotype are the same",
     "b":"False — that is the PHENOTYPE; genotype is the genetic composition",
     "c":"True — genotype describes physical traits","d":"False — genotype refers to RNA sequence",
     "answer":"B","explanation":"FALSE. Genotype = genetic composition. PHENOTYPE = physical expression of genes."},

    # T/F 77 — Hydrogen bonds
    {"section":"الوراثة والجينات",
     "question":"What type of bonds hold DNA strands together?",
     "a":"Covalent bonds between bases","b":"Hydrogen bonds between AT and GC base pairs",
     "c":"Ionic bonds between phosphates","d":"Peptide bonds between nucleotides",
     "answer":"B","explanation":"Hydrogen bonds hold the two DNA strands together: A=T (2 H-bonds), G≡C (3 H-bonds)."},

    {"section":"الوراثة والجينات",
     "question":"True or False: DNA strands are held together by hydrogen bonds between AT and CG pairs.",
     "a":"True — hydrogen bonds hold complementary base pairs together",
     "b":"False — covalent bonds hold DNA strands together",
     "c":"True — but only between GC pairs","d":"False — ionic bonds connect the strands",
     "answer":"A","explanation":"TRUE. Hydrogen bonds: A-T (2 bonds), G-C (3 bonds) hold the two antiparallel strands together."},

    # Choose 78 — Replication direction
    {"section":"الوراثة والجينات",
     "question":"DNA replication proceeds in which direction?",
     "a":"3'→5' direction","b":"5'→3' direction","c":"Both 3'→5' and 5'→3'","d":"No specific direction",
     "answer":"B","explanation":"DNA synthesis always proceeds 5'→3' — DNA polymerase adds nucleotides to the 3' end."},

    # Choose 79 — Phenotype
    {"section":"الوراثة والجينات",
     "question":"Fill in: Expression of the genes = ___",
     "a":"Genotype","b":"Phenotype","c":"Genome","d":"Genomics",
     "answer":"B","explanation":"Phenotype = the observable expression of genes (physical, biochemical, behavioral traits)."},

    # Choose 80 — Genome
    {"section":"الوراثة والجينات",
     "question":"Fill in: All of the genetic material in a cell = ___",
     "a":"Gene","b":"Genomics","c":"Genome","d":"Genotype",
     "answer":"C","explanation":"Genome = ALL genetic material in a cell (all chromosomes + plasmids + organelle DNA)."},

    # Choose 81 — Antiparallel
    {"section":"الوراثة والجينات",
     "question":"DNA strands are ___ to each other.",
     "a":"Parallel","b":"Antiparallel","c":"Perpendicular","d":"Identical in direction",
     "answer":"B","explanation":"DNA strands are antiparallel: one runs 5'→3', the other 3'→5'."},

    {"section":"الوراثة والجينات",
     "question":"True or False: DNA strands run in the same direction (parallel) to each other.",
     "a":"True — both strands run 5'→3'","b":"False — DNA strands are ANTIPARALLEL",
     "c":"True — both run 3'→5'","d":"False — they run perpendicular to each other",
     "answer":"B","explanation":"FALSE. DNA strands are ANTIPARALLEL — one 5'→3', the other 3'→5'."},

    # Choose 82 — Transcription direction
    {"section":"الوراثة والجينات",
     "question":"Transcription proceeds in which direction?",
     "a":"3'→5' direction","b":"5'→3' direction","c":"Bidirectional","d":"No specific direction",
     "answer":"B","explanation":"RNA synthesis during transcription proceeds 5'→3', reading the template strand 3'→5'."},

    # Choose 83 — Start codon
    {"section":"الوراثة والجينات",
     "question":"Translation of mRNA begins at the start codon:",
     "a":"UAG","b":"UGA","c":"UAA","d":"AUG",
     "answer":"D","explanation":"AUG is the universal start codon that initiates translation and codes for methionine."},

    # Choose 84 — Ethidium bromide
    {"section":"الوراثة والجينات",
     "question":"Ethidium bromide inserts between bases causing:",
     "a":"Thymine dimers","b":"Frameshift mutation","c":"Chromosomal breaks","d":"Base substitution",
     "answer":"B","explanation":"Ethidium bromide is an intercalating agent — inserts between DNA bases → frameshift mutation."},

    # T/F 85 — UV and thymine dimers
    {"section":"الوراثة والجينات",
     "question":"What type of mutation does UV radiation induce?",
     "a":"Frameshift mutation","b":"Thymine dimers","c":"Chromosomal breaks","d":"Base deletion",
     "answer":"B","explanation":"UV radiation causes thymine dimers — covalent bonds form between adjacent thymine bases → blocks replication."},

    {"section":"الوراثة والجينات",
     "question":"True or False: UV radiation induces formation of thymine dimers.",
     "a":"True — UV causes thymine dimers that block DNA replication",
     "b":"False — UV causes chromosomal breaks only",
     "c":"True — but only in prokaryotes","d":"False — UV causes base substitution",
     "answer":"A","explanation":"TRUE. UV radiation induces thymine dimer formation (adjacent T-T covalent bonds) → blocks DNA replication."},

    # Choose 86 — Spontaneous mutations
    {"section":"الوراثة والجينات",
     "question":"Mutations due to occasional mistakes in DNA replication are called:",
     "a":"Induced mutations","b":"Spontaneous mutations","c":"Chemical mutations","d":"Radiation mutations",
     "answer":"B","explanation":"Spontaneous mutations occur without mutagens — they arise from errors during DNA replication."},

    {"section":"الوراثة والجينات",
     "question":"True or False: Spontaneous mutations are caused by mutagens like radiation.",
     "a":"True — all mutations need a mutagen","b":"False — spontaneous mutations occur WITHOUT mutagens",
     "c":"True — radiation is always involved","d":"False — spontaneous mutations don't occur in nature",
     "answer":"B","explanation":"FALSE. Spontaneous mutations occur WITHOUT mutagens — they are random errors in DNA replication."},

    # ══════════════════════════════════════════════════════════════
    # SECTION 6: Short Answer → MCQ
    # ══════════════════════════════════════════════════════════════

    {"section":"الوراثة والجينات",
     "question":"Which of the following correctly describes the structure of DNA?",
     "a":"Single strand of amino acids with ribose backbone",
     "b":"Double helix of nucleotides with deoxyribose-phosphate backbone, antiparallel strands held by H-bonds",
     "c":"Single helix with ribose-phosphate backbone","d":"Double helix with covalent bonds between bases",
     "answer":"B","explanation":"DNA: double helix, nucleotide polymer, deoxyribose-phosphate backbone, antiparallel, H-bonds between bases."},

    {"section":"الوراثة والجينات",
     "question":"What does 'semiconservative replication' mean?",
     "a":"Both strands are newly synthesized","b":"Each new DNA molecule has one original + one new strand",
     "c":"Only one DNA molecule is produced","d":"The original DNA is destroyed",
     "answer":"B","explanation":"Semiconservative: each daughter DNA retains one original (parental) strand and one newly synthesized strand."},

    {"section":"الوراثة والجينات",
     "question":"Which of the following correctly describes DNA replication?",
     "a":"Conservative, 3'→5', no primer needed",
     "b":"Semiconservative, 5'→3', initiated by RNA primer, leading strand continuous, lagging strand discontinuous",
     "c":"Dispersive, bidirectional, no Okazaki fragments",
     "d":"Semiconservative, 3'→5', leading strand discontinuous",
     "answer":"B","explanation":"DNA replication: semiconservative, 5'→3', RNA primer, leading (continuous), lagging (Okazaki fragments), joined by ligase."},

    {"section":"الوراثة والجينات",
     "question":"Which correctly compares missense, nonsense, and frameshift mutations?",
     "a":"All three cause stop codons","b":"All three change only one amino acid",
     "c":"Missense=amino acid change, Nonsense=stop codon, Frameshift=reading frame shift",
     "d":"Missense=stop codon, Nonsense=frameshift, Frameshift=amino acid change",
     "answer":"C","explanation":"Missense: different AA; Nonsense: premature stop codon; Frameshift: shifts entire reading frame downstream."},

    {"section":"الوراثة والجينات",
     "question":"What are the two types of mutations based on their cause?",
     "a":"Missense and nonsense","b":"Spontaneous (no mutagen) and induced (by mutagens)",
     "c":"Chemical and thermal","d":"DNA and RNA mutations",
     "answer":"B","explanation":"Spontaneous mutations: random replication errors. Induced mutations: caused by mutagens (chemicals or radiation)."},

    {"section":"الوراثة والجينات",
     "question":"Reverse transcription (RNA→DNA) occurs in which organisms?",
     "a":"All bacteria","b":"All plants","c":"Retroviruses like HIV","d":"All eukaryotes",
     "answer":"C","explanation":"Reverse transcription occurs in retroviruses (like HIV) using the enzyme reverse transcriptase."},

    {"section":"الوراثة والجينات",
     "question":"What is the role of DNA ligase in DNA replication?",
     "a":"Unwinds the double helix","b":"Synthesizes RNA primers",
     "c":"Joins Okazaki fragments on the lagging strand","d":"Adds nucleotides to leading strand",
     "answer":"C","explanation":"DNA ligase seals the nicks between Okazaki fragments on the lagging strand to create a continuous DNA strand."},

    {"section":"الوراثة والجينات",
     "question":"Chromosome map represents:",
     "a":"Protein structure","b":"Gene locations on chromosomes","c":"RNA sequence","d":"Membrane structure",
     "answer":"B","explanation":"A chromosome map (genetic map) shows the locations and relative distances of genes on chromosomes."},

    # ── إضافي — أشكال مختلفة من نفس المعلومات ──────────────────

    {"section":"الوراثة والجينات",
     "question":"Fill in: A segment of DNA encoding a functional product = ___",
     "a":"Genome","b":"Gene","c":"Genotype","d":"Codon",
     "answer":"B","explanation":"A gene = a specific segment of DNA that encodes a functional product (usually a protein)."},

    {"section":"الوراثة والجينات",
     "question":"Fill in: The molecular study of genomes = ___",
     "a":"Genetics","b":"Genomics","c":"Proteomics","d":"Metabolomics",
     "answer":"B","explanation":"Genomics = the molecular study of genomes, including sequencing and functional analysis."},

    {"section":"الوراثة والجينات",
     "question":"True or False: Genotype refers to the physical characteristics of an organism.",
     "a":"True — genotype describes physical traits",
     "b":"False — genotype is the genetic makeup; phenotype describes physical traits",
     "c":"True — genotype and phenotype are identical","d":"False — genotype refers to RNA",
     "answer":"B","explanation":"FALSE. Genotype = genetic composition (genes). Phenotype = physical expression of those genes."},

    {"section":"الوراثة والجينات",
     "question":"Fill in: The process DNA→RNA is called ___",
     "a":"Translation","b":"Replication","c":"Transcription","d":"Reverse transcription",
     "answer":"C","explanation":"Transcription = DNA→RNA, carried out by RNA polymerase."},

    {"section":"الوراثة والجينات",
     "question":"Fill in: The process RNA→Protein is called ___",
     "a":"Transcription","b":"Replication","c":"Translation","d":"Reverse transcription",
     "answer":"C","explanation":"Translation = mRNA→Protein, occurs at ribosomes."},

    {"section":"الوراثة والجينات",
     "question":"Which chemical mutagen alters adenine causing it to pair with cytosine instead of thymine?",
     "a":"Ethidium bromide","b":"UV radiation","c":"Nitrous acid","d":"X-rays",
     "answer":"C","explanation":"Nitrous acid deaminates adenine → hypoxanthine, which base-pairs with cytosine → A:T to G:C transition."},

    {"section":"الوراثة والجينات",
     "question":"True or False: Nonsense mutation changes one amino acid to a different amino acid.",
     "a":"True — it changes one amino acid","b":"False — nonsense mutation creates a STOP CODON, not an amino acid change",
     "c":"True — all point mutations change amino acids","d":"False — nonsense mutation causes frameshift",
     "answer":"B","explanation":"FALSE. Nonsense mutation → STOP codon (premature termination). Missense mutation changes one amino acid."},

    {"section":"الوراثة والجينات",
     "question":"Silent mutation results in:",
     "a":"Change in amino acid","b":"Premature stop codon",
     "c":"No change in amino acid (same protein)","d":"Frameshift of reading frame",
     "answer":"C","explanation":"Silent (synonymous) mutation: base change → different codon but SAME amino acid due to codon degeneracy."},

    {"section":"الوراثة والجينات",
     "question":"Which of the following correctly describes the central dogma?",
     "a":"Proteins can be converted back to DNA","b":"RNA can replicate independently",
     "c":"Genetic information flows: DNA→RNA→Protein","d":"Translation produces DNA",
     "answer":"C","explanation":"Central dogma: DNA (replication)→DNA (transcription)→RNA (translation)→Protein. Information flows one way."},

]

print(f"✅ إجمالي الأسئلة: {len(GENETICS_QUESTIONS)}")

if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from database import Database
    os.makedirs("/data", exist_ok=True)
    db = Database("/data/quiz_bot.db")

    # امسح السكشن القديم أولاً لتجنب التكرار
    with db._connect() as c:
        c.execute("PRAGMA foreign_keys = OFF")
        c.execute("""DELETE FROM questions WHERE section_id IN (
            SELECT id FROM sections WHERE name='الوراثة والجينات'
        )""")
        c.execute("DELETE FROM sections WHERE name='الوراثة والجينات'")
        c.execute("PRAGMA foreign_keys = ON")
    print("🗑️ تم مسح الأسئلة القديمة")

    db.import_questions(GENETICS_QUESTIONS)
    print(f"✅ تم إضافة {len(GENETICS_QUESTIONS)} سؤال في سكشن الوراثة والجينات 🧬")
