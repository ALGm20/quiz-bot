"""
populate_db.py — تعبئة الأسئلة فقط (لا حاجة لقائمة طلاب)
شغّله مرة واحدة عند البداية
"""
from database import Database
db = Database("quiz_bot.db")

QUESTIONS = [
    {
        "section": "الفيروسات",
        "section_emoji": "🦠",
        "section_description": "بنية الفيروسات، تصنيفها، دورات حياتها، آلية عملها",
        "question": "The term 'virus' means:",
        "a": "Cell", "b": "Poison", "c": "Protein", "d": "Parasite",
        "answer": "B",
        "explanation": "The word virus is derived from Latin meaning poison."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses are considered:",
        "a": "Cellular organisms", "b": "Acellular particles",
        "c": "Prokaryotic cells", "d": "Eukaryotic cells",
        "answer": "B",
        "explanation": "Viruses are acellular — they have no cell structure."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses contain:",
        "a": "DNA only", "b": "RNA only", "c": "DNA and RNA", "d": "DNA or RNA",
        "answer": "D",
        "explanation": "A virus contains either DNA or RNA — never both."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses reproduce:",
        "a": "Outside cells", "b": "Inside living cells", "c": "In soil", "d": "In water",
        "answer": "B",
        "explanation": "Viruses can only replicate inside living host cells."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses are obligate intracellular parasites because they:",
        "a": "Replicate only inside host cells", "b": "Live in water",
        "c": "Produce toxins", "d": "Are large organisms",
        "answer": "A",
        "explanation": "Viruses cannot replicate outside a living host cell."
    },
    {
        "section": "الفيروسات",
        "question": "The protein coat of a virus is called:",
        "a": "Capsule", "b": "Capsid", "c": "Membrane", "d": "Cytoplasm",
        "answer": "B",
        "explanation": "The capsid is the protein shell that surrounds the viral genome."
    },
    {
        "section": "الفيروسات",
        "question": "Capsids are composed mainly of:",
        "a": "Lipids", "b": "Proteins", "c": "Carbohydrates", "d": "Minerals",
        "answer": "B",
        "explanation": "Capsids are made of protein subunits called capsomeres."
    },
    {
        "section": "الفيروسات",
        "question": "Capsid subunits are called:",
        "a": "Ribosomes", "b": "Capsomeres", "c": "Lysosomes", "d": "Chromosomes",
        "answer": "B",
        "explanation": "Capsomeres are the protein subunits that assemble to form the capsid."
    },
    {
        "section": "الفيروسات",
        "question": "Capsomeres combine to form:",
        "a": "Viral capsid", "b": "Cell membrane", "c": "Nucleus", "d": "Cytoplasm",
        "answer": "A",
        "explanation": "Multiple capsomeres assemble to form the complete viral capsid."
    },
    {
        "section": "الفيروسات",
        "question": "Capsid plus nucleic acid is called:",
        "a": "Envelope", "b": "Nucleocapsid", "c": "Ribosome", "d": "Cytoplasm",
        "answer": "B",
        "explanation": "Nucleocapsid = capsid + enclosed nucleic acid."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses that have a lipid membrane are called:",
        "a": "Naked viruses", "b": "Enveloped viruses",
        "c": "Complex viruses", "d": "RNA viruses",
        "answer": "B",
        "explanation": "Enveloped viruses have a lipid bilayer from the host cell membrane."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses without an envelope are called:",
        "a": "Naked viruses", "b": "Enveloped viruses",
        "c": "Complex viruses", "d": "Helical viruses",
        "answer": "A",
        "explanation": "Non-enveloped viruses are called naked viruses."
    },
    {
        "section": "الفيروسات",
        "question": "The viral envelope originates from:",
        "a": "Viral proteins", "b": "Host cell membrane", "c": "DNA", "d": "RNA",
        "answer": "B",
        "explanation": "Enveloped viruses acquire their lipid envelope from the host cell membrane during budding."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses lack:",
        "a": "Genetic material", "b": "Ribosomes", "c": "Capsid", "d": "Proteins",
        "answer": "B",
        "explanation": "Viruses have no ribosomes — they depend on the host cell's ribosomes."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses depend on host cells for:",
        "a": "Energy", "b": "Protein synthesis", "c": "Replication", "d": "All of the above",
        "answer": "D",
        "explanation": "Viruses are completely dependent on the host for energy, protein synthesis, and replication."
    },
    {
        "section": "الفيروسات",
        "question": "Typical virus size is:",
        "a": "1–5 nm", "b": "20–200 nm", "c": "1000 nm", "d": "5 µm",
        "answer": "B",
        "explanation": "Most viruses range from 20 to 200 nm."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses infect:",
        "a": "Animals", "b": "Plants", "c": "Bacteria", "d": "All of the above",
        "answer": "D",
        "explanation": "Viruses can infect all types of living organisms."
    },
    {
        "section": "الفيروسات",
        "question": "Bacteriophages infect:",
        "a": "Animals", "b": "Plants", "c": "Bacteria", "d": "Fungi",
        "answer": "C",
        "explanation": "Bacteriophages are viruses that specifically infect bacteria."
    },
    {
        "section": "الفيروسات",
        "question": "Poxviruses are classified as:",
        "a": "Naked viruses", "b": "Complex viruses",
        "c": "RNA viruses", "d": "Icosahedral viruses",
        "answer": "B",
        "explanation": "Poxviruses have a complex irregular structure."
    },
    {
        "section": "الفيروسات",
        "question": "The main role of the capsid is:",
        "a": "Energy production", "b": "Protect viral genome",
        "c": "DNA synthesis", "d": "Protein digestion",
        "answer": "B",
        "explanation": "The capsid protects the viral nucleic acid."
    },
    {
        "section": "الفيروسات",
        "question": "What is the origin of the word 'virus'?",
        "a": "Latin for germ", "b": "Greek for poison",
        "c": "Latin for infectious", "d": "Word for toxoplasma",
        "answer": "B",
        "explanation": "Virus comes from Latin/Greek meaning poison."
    },
    {
        "section": "الفيروسات",
        "question": "Viral classification is primarily based on:",
        "a": "Cell wall composition", "b": "Nucleic acid type and structure",
        "c": "Method of binary fission", "d": "Color under electron microscope",
        "answer": "B",
        "explanation": "Viruses are classified by nucleic acid type, structure, and replication strategy."
    },
    {
        "section": "الفيروسات",
        "question": "What distinguishes enveloped from non-enveloped viruses?",
        "a": "Presence of a lipid membrane derived from the host cell",
        "b": "Having only DNA as genetic material",
        "c": "Ability to replicate outside living cells",
        "d": "Absence of a protein capsid",
        "answer": "A",
        "explanation": "Enveloped viruses have a host-derived lipid bilayer."
    },
    {
        "section": "الفيروسات",
        "question": "Which of the following viruses infects bacteria?",
        "a": "Influenza virus", "b": "HIV",
        "c": "Bacteriophage", "d": "Poliovirus",
        "answer": "C",
        "explanation": "Bacteriophages infect and replicate inside bacteria."
    },
    {
        "section": "الفيروسات",
        "question": "What is a virus composed of?",
        "a": "DNA only", "b": "RNA only",
        "c": "Genetic material and a protein shell", "d": "Lipids and carbohydrates",
        "answer": "C",
        "explanation": "All viruses consist of nucleic acid enclosed in a protein coat (capsid)."
    },
    {
        "section": "الفيروسات",
        "question": "Which of the following is NOT a basic viral form?",
        "a": "Complex", "b": "Naked", "c": "Filamentous", "d": "Enveloped",
        "answer": "C",
        "explanation": "Basic viral forms are icosahedral, helical, and complex."
    },
    {
        "section": "الفيروسات",
        "question": "What is the function of the viral capsid?",
        "a": "It contains ribosomes",
        "b": "It protects the viral genetic material",
        "c": "It produces viral proteins",
        "d": "It helps in DNA replication",
        "answer": "B",
        "explanation": "The capsid protects the viral genome from degradation."
    },
    {
        "section": "الفيروسات",
        "question": "Which classification system is used for viruses?",
        "a": "Bergey's Manual", "b": "Linnaean System",
        "c": "Hierarchical Classification (Order, Family, Genus, Species)",
        "d": "Whittaker's Five Kingdom",
        "answer": "C",
        "explanation": "Viruses use hierarchical classification: Order → Family → Genus → Species."
    },
    {
        "section": "الفيروسات",
        "question": "What is a bacteriophage?",
        "a": "A virus that infects bacteria", "b": "A virus that infects humans",
        "c": "A type of antibiotic", "d": "A bacterial toxin",
        "answer": "A",
        "explanation": "A bacteriophage is a virus that infects and replicates within bacteria."
    },
    {
        "section": "الفيروسات",
        "question": "Which of the following statements about viruses is true?",
        "a": "Viruses cannot reproduce outside of a host cell",
        "b": "Protozoa have rigid cell walls",
        "c": "Fungi are plants",
        "d": "Bacteria cannot move",
        "answer": "A",
        "explanation": "Viruses are obligate intracellular parasites."
    },
    {
        "section": "الفيروسات",
        "question": "What is the main function of the viral envelope?",
        "a": "To protect the capsid",
        "b": "To facilitate entry into host cells",
        "c": "To replicate viral DNA",
        "d": "To produce viral proteins",
        "answer": "B",
        "explanation": "Viral envelope glycoproteins facilitate attachment and entry into host cells."
    },
    {
        "section": "الفيروسات",
        "question": "Which of the following is an RNA virus?",
        "a": "Herpesvirus", "b": "Adenovirus", "c": "Retrovirus", "d": "Poxvirus",
        "answer": "C",
        "explanation": "Retroviruses (like HIV) have an RNA genome."
    },
    {
        "section": "الفيروسات",
        "question": "How do bacteriophages primarily infect bacterial cells?",
        "a": "By direct fusion with the bacterial membrane",
        "b": "By injecting their genetic material into the host",
        "c": "By endocytosis",
        "d": "By lysing the host cell first",
        "answer": "B",
        "explanation": "Phages inject their DNA into the host, leaving the capsid outside."
    },
    {
        "section": "الفيروسات",
        "question": "Which method is commonly used to cultivate viruses in the laboratory?",
        "a": "Agar plate culture", "b": "Nutrient broth culture",
        "c": "Cell culture", "d": "Streak plate method",
        "answer": "C",
        "explanation": "Cell (tissue) culture is used since viruses require living cells."
    },
    {
        "section": "الفيروسات",
        "question": "Which virus has a double-stranded RNA genome?",
        "a": "Retrovirus", "b": "Reovirus", "c": "Picornavirus", "d": "Herpesvirus",
        "answer": "B",
        "explanation": "Reoviruses (including Rotaviruses) have segmented dsRNA genomes."
    },
    {
        "section": "الفيروسات",
        "question": "What is the function of viral hemagglutinin in influenza?",
        "a": "Aids in viral entry into host cells",
        "b": "Assists in viral genome replication",
        "c": "Stimulates host immune response",
        "d": "Facilitates viral exit from host cells",
        "answer": "A",
        "explanation": "Hemagglutinin (H) binds to sialic acid receptors, mediating entry."
    },
    {
        "section": "الفيروسات",
        "question": "Which type of viral infection leads to immediate destruction of the host cell?",
        "a": "Lysogenic infection", "b": "Latent infection",
        "c": "Lytic infection", "d": "Chronic infection",
        "answer": "C",
        "explanation": "In the lytic cycle, the host cell is destroyed upon virus release."
    },
    {
        "section": "الفيروسات",
        "question": "Which enzyme allows retroviruses to integrate their genome into host DNA?",
        "a": "DNA polymerase", "b": "RNA polymerase",
        "c": "Reverse transcriptase", "d": "Integrase",
        "answer": "C",
        "explanation": "Reverse transcriptase converts viral RNA into DNA for integration."
    },
    {
        "section": "الفيروسات",
        "question": "What is the primary mode of transmission for arboviruses?",
        "a": "Respiratory droplets", "b": "Contaminated food",
        "c": "Insect vectors", "d": "Direct human contact",
        "answer": "C",
        "explanation": "Arboviruses are transmitted through insect bites (mosquitoes, ticks)."
    },
    {
        "section": "الفيروسات",
        "question": "Which viral structure is responsible for attachment to host cell receptors?",
        "a": "Capsomere", "b": "Matrix protein",
        "c": "Viral spikes (glycoproteins)", "d": "Viral polymerase",
        "answer": "C",
        "explanation": "Viral surface glycoproteins bind to specific receptors on host cells."
    },
    {
        "section": "الفيروسات",
        "question": "Which virus replicates entirely in the cytoplasm?",
        "a": "Herpesvirus", "b": "Adenovirus", "c": "Poxvirus", "d": "Papillomavirus",
        "answer": "C",
        "explanation": "Poxviruses encode their own RNA polymerase and replicate in the cytoplasm."
    },
    {
        "section": "الفيروسات",
        "question": "Which viral genome type requires reverse transcriptase?",
        "a": "dsDNA viruses", "b": "(+) ssRNA viruses",
        "c": "Retroviruses", "d": "dsRNA viruses",
        "answer": "C",
        "explanation": "Retroviruses use reverse transcriptase to convert RNA to DNA."
    },
    {
        "section": "الفيروسات",
        "question": "The icosahedral symmetry of viruses provides:",
        "a": "Maximum stability with minimal genetic coding",
        "b": "Increased lipid envelope protection",
        "c": "Higher mutation rate",
        "d": "Ability to replicate outside cells",
        "answer": "A",
        "explanation": "Icosahedral symmetry encloses maximum volume with minimal protein subunits."
    },
    {
        "section": "الفيروسات",
        "question": "Which viruses are most resistant to environmental conditions?",
        "a": "Enveloped viruses", "b": "Naked viruses",
        "c": "RNA viruses", "d": "Retroviruses",
        "answer": "B",
        "explanation": "Naked viruses are more resistant to heat, desiccation, and disinfectants."
    },
    {
        "section": "الفيروسات",
        "question": "Which enzyme is carried by negative-sense RNA viruses?",
        "a": "DNA polymerase", "b": "RNA-dependent RNA polymerase",
        "c": "Reverse transcriptase", "d": "Integrase",
        "answer": "B",
        "explanation": "Negative-sense RNA viruses carry RdRp to transcribe their genome into mRNA."
    },
    {
        "section": "الفيروسات",
        "question": "During viral replication, 'uncoating' refers to:",
        "a": "Release of virions from the host cell",
        "b": "Removal of viral envelope only",
        "c": "Release of viral genome into host cell",
        "d": "Assembly of capsid proteins",
        "answer": "C",
        "explanation": "Uncoating releases the viral genome into the host cell cytoplasm."
    },
    {
        "section": "الفيروسات",
        "question": "Which viral family contains segmented RNA genomes?",
        "a": "Picornaviridae", "b": "Orthomyxoviridae",
        "c": "Herpesviridae", "d": "Adenoviridae",
        "answer": "B",
        "explanation": "Influenza viruses (Orthomyxoviridae) have 8 RNA segments."
    },
    {
        "section": "الفيروسات",
        "question": "The process by which viruses obtain their envelope is called:",
        "a": "Lysis", "b": "Budding", "c": "Integration", "d": "Fusion",
        "answer": "B",
        "explanation": "During budding, the nucleocapsid acquires a lipid envelope from the host cell."
    },
    {
        "section": "الفيروسات",
        "question": "Which viral component determines host specificity (tropism)?",
        "a": "Capsid size", "b": "Viral receptor-binding proteins",
        "c": "Genome length", "d": "Viral polymerase",
        "answer": "B",
        "explanation": "Viral tropism is determined by surface proteins and their host cell receptors."
    },
    {
        "section": "الفيروسات",
        "question": "Which stage of viral replication involves synthesis of viral proteins?",
        "a": "Attachment", "b": "Penetration", "c": "Biosynthesis", "d": "Release",
        "answer": "C",
        "explanation": "The biosynthesis stage is when viral proteins and nucleic acids are produced."
    },
    {
        "section": "الفيروسات",
        "question": "Which virus integrates its genome into the host DNA as a provirus?",
        "a": "Influenza virus", "b": "HIV", "c": "Rabies virus", "d": "Rotavirus",
        "answer": "B",
        "explanation": "HIV integrates its DNA copy into the host genome as a provirus."
    },
    {
        "section": "الفيروسات",
        "question": "Which viral infection cycle results in destruction of the host cell?",
        "a": "Lysogenic cycle", "b": "Latent cycle",
        "c": "Lytic cycle", "d": "Persistent cycle",
        "answer": "C",
        "explanation": "In the lytic cycle, new virions accumulate until the host cell lyses."
    },
    {
        "section": "الفيروسات",
        "question": "Which viral component protects the genome and assists in viral assembly?",
        "a": "Envelope", "b": "Capsid",
        "c": "Glycoprotein spikes", "d": "Matrix protein",
        "answer": "B",
        "explanation": "The capsid protects the genome and provides scaffolding for assembly."
    },
    {
        "section": "الفيروسات",
        "question": "Which is NOT a method of viral classification?",
        "a": "Shape", "b": "Mode of replication",
        "c": "Size of the host cell", "d": "Type of nucleic acid",
        "answer": "C",
        "explanation": "Viral classification does not use the size of the host cell."
    },
    {
        "section": "الفيروسات",
        "question": "What is a key characteristic of viruses?",
        "a": "They have a nuclear membrane",
        "b": "They possess metabolic enzymes",
        "c": "They lack an external cell wall",
        "d": "They can replicate independently",
        "answer": "C",
        "explanation": "Viruses have no cell wall, no nucleus, and no metabolic machinery."
    },
    {
        "section": "الفيروسات",
        "question": "During which stage does receptor-mediated endocytosis occur?",
        "a": "Adsorption", "b": "Penetration",
        "c": "Replication", "d": "Assembly",
        "answer": "B",
        "explanation": "Receptor-mediated endocytosis is a mechanism of viral penetration."
    },
    {
        "section": "الفيروسات",
        "question": "In viral taxonomy, what suffix is used for virus families?",
        "a": "-virus", "b": "-pathogen", "c": "-viridae", "d": "-bacteria",
        "answer": "C",
        "explanation": "Virus family names end in -viridae (e.g., Herpesviridae, Retroviridae)."
    },
]

db.import_questions(QUESTIONS)

from collections import Counter
counts = Counter(q["section"] for q in QUESTIONS)
print(f"\n✅ تم إضافة {len(QUESTIONS)} سؤال في {len(counts)} سكشن:")
for sec, cnt in counts.items():
    emoji = next((q.get("section_emoji","📖") for q in QUESTIONS if q["section"]==sec),"📖")
    print(f"   {emoji} {sec}: {cnt} سؤال")

print(f"\n📊 قاعدة البيانات:")
st = db.stats()
print(f"   ❓ أسئلة: {st['questions']}")
print(f"   📦 سكشنات: {st['sections']}")
print("\n🚀 شغّل البوت: python run.py")
