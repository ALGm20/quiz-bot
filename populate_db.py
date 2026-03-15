"""
populate_db.py — تعبئة الأسئلة (بدون قائمة طلاب مسبقة)
شغّله مرة واحدة عند البداية
"""
import os
from database import Database
os.makedirs("/data", exist_ok=True)
db = Database("/data/quiz_bot.db")

# امسح الأسئلة القديمة لتجنب التكرار عند إعادة التشغيل
with db._connect() as c:
    c.execute("DELETE FROM questions")
    c.execute("DELETE FROM sections")
print("🗑️ تم مسح الأسئلة القديمة")

QUESTIONS = [

    # ══════════════════════════════════════════════════════════════
    # المجموعة 1 — أساسيات الفيروسات (من virology_100_mcq)
    # ══════════════════════════════════════════════════════════════
    {
        "section": "الفيروسات",
        "section_emoji": "🦠",
        "section_description": "جميع أسئلة الفيروسات — البنية، التصنيف، دورات الحياة، آلية العمل",
        "question": "The term 'virus' means:",
        "a": "Cell", "b": "Poison", "c": "Protein", "d": "Parasite",
        "answer": "B",
        "explanation": "The word 'virus' is derived from Latin meaning poison."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses are considered:",
        "a": "Cellular organisms", "b": "Acellular particles",
        "c": "Prokaryotic cells", "d": "Eukaryotic cells",
        "answer": "B",
        "explanation": "Viruses are acellular — they have no cell structure, organelles, or cytoplasm."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses contain:",
        "a": "DNA only", "b": "RNA only", "c": "DNA and RNA", "d": "DNA or RNA",
        "answer": "D",
        "explanation": "A virus contains either DNA or RNA as its genome — never both at the same time."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses reproduce:",
        "a": "Outside cells", "b": "Inside living cells", "c": "In soil", "d": "In water",
        "answer": "B",
        "explanation": "Viruses can only replicate inside living host cells using the host's machinery."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses are obligate intracellular parasites because they:",
        "a": "Replicate only inside host cells", "b": "Live in water",
        "c": "Produce toxins", "d": "Are large organisms",
        "answer": "A",
        "explanation": "Viruses lack the machinery for independent replication and must use living host cells."
    },
    {
        "section": "الفيروسات",
        "question": "The protein coat of a virus is called:",
        "a": "Capsule", "b": "Capsid", "c": "Membrane", "d": "Cytoplasm",
        "answer": "B",
        "explanation": "The capsid is the protein shell that surrounds and protects the viral genome."
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
        "explanation": "Capsomeres are the individual protein subunits that assemble to form the capsid."
    },
    {
        "section": "الفيروسات",
        "question": "Capsomeres combine to form:",
        "a": "Viral capsid", "b": "Cell membrane", "c": "Nucleus", "d": "Cytoplasm",
        "answer": "A",
        "explanation": "Multiple capsomeres assemble together to form the complete viral capsid."
    },
    {
        "section": "الفيروسات",
        "question": "Capsid plus nucleic acid is called:",
        "a": "Envelope", "b": "Nucleocapsid", "c": "Ribosome", "d": "Cytoplasm",
        "answer": "B",
        "explanation": "The nucleocapsid = capsid + the enclosed nucleic acid (genome)."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses that have a lipid membrane are called:",
        "a": "Naked viruses", "b": "Enveloped viruses",
        "c": "Complex viruses", "d": "RNA viruses",
        "answer": "B",
        "explanation": "Enveloped viruses have a lipid bilayer derived from the host cell membrane surrounding the nucleocapsid."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses without an envelope are called:",
        "a": "Naked viruses", "b": "Enveloped viruses",
        "c": "Complex viruses", "d": "Helical viruses",
        "answer": "A",
        "explanation": "Non-enveloped viruses are called naked viruses — they have only a capsid with no lipid membrane."
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
        "explanation": "Viruses have no ribosomes — they depend entirely on the host cell's ribosomes for protein synthesis."
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
        "explanation": "Most viruses range from 20 to 200 nm — much smaller than bacteria (~1000 nm)."
    },
    {
        "section": "الفيروسات",
        "question": "Viruses infect:",
        "a": "Animals", "b": "Plants", "c": "Bacteria", "d": "All of the above",
        "answer": "D",
        "explanation": "Viruses can infect all types of living organisms: animals, plants, fungi, and bacteria."
    },
    {
        "section": "الفيروسات",
        "question": "Bacteriophages infect:",
        "a": "Animals", "b": "Plants", "c": "Bacteria", "d": "Fungi",
        "answer": "C",
        "explanation": "Bacteriophages (phages) are viruses that specifically infect bacteria."
    },
    {
        "section": "الفيروسات",
        "question": "Poxviruses are classified as:",
        "a": "Naked viruses", "b": "Complex viruses",
        "c": "RNA viruses", "d": "Icosahedral viruses",
        "answer": "B",
        "explanation": "Poxviruses have a complex irregular structure — neither purely icosahedral nor helical."
    },
    {
        "section": "الفيروسات",
        "question": "The main role of the capsid is:",
        "a": "Energy production", "b": "Protect viral genome",
        "c": "DNA synthesis", "d": "Protein digestion",
        "answer": "B",
        "explanation": "The capsid protects the viral nucleic acid from enzymes, UV radiation, and harsh environments."
    },

    # ══════════════════════════════════════════════════════════════
    # المجموعة 2 — من أسئلة التراث (فيروسات فقط)
    # ══════════════════════════════════════════════════════════════
    {
        "section": "الفيروسات",
        "question": "What is the origin of the word 'virus'?",
        "a": "Latin for germ", "b": "Greek for poison",
        "c": "Latin for infectious", "d": "Word for toxoplasma",
        "answer": "B",
        "explanation": "The word 'virus' originates from Latin/Greek meaning poison or venom."
    },
    {
        "section": "الفيروسات",
        "question": "Viral classification is primarily based on:",
        "a": "Cell wall composition", "b": "Nucleic acid type and structure",
        "c": "Method of binary fission", "d": "Color under an electron microscope",
        "answer": "B",
        "explanation": "Viruses are primarily classified by their nucleic acid type (DNA/RNA), structure, and replication strategy."
    },
    {
        "section": "الفيروسات",
        "question": "What distinguishes enveloped viruses from non-enveloped viruses?",
        "a": "Presence of a lipid membrane derived from the host cell",
        "b": "Having only DNA as genetic material",
        "c": "Their ability to replicate outside living cells",
        "d": "The absence of a protein capsid",
        "answer": "A",
        "explanation": "Enveloped viruses have a host-derived lipid bilayer surrounding the nucleocapsid."
    },
    {
        "section": "الفيروسات",
        "question": "Which of the following viruses infects bacteria?",
        "a": "Influenza virus", "b": "HIV",
        "c": "Bacteriophage", "d": "Poliovirus",
        "answer": "C",
        "explanation": "Bacteriophages are viruses that specifically infect and replicate inside bacteria."
    },

    # ══════════════════════════════════════════════════════════════
    # المجموعة 3 — من حل المرشحات (صور + اسئلة مكتوبة)
    # ══════════════════════════════════════════════════════════════
    {
        "section": "الفيروسات",
        "question": "What is a virus composed of?",
        "a": "DNA only", "b": "RNA only",
        "c": "Genetic material and a protein shell", "d": "Lipids and carbohydrates",
        "answer": "C",
        "explanation": "All viruses consist of nucleic acid (DNA or RNA) enclosed within a protein coat (capsid)."
    },
    {
        "section": "الفيروسات",
        "question": "Which of the following is NOT a basic viral form?",
        "a": "Complex", "b": "Naked", "c": "Filamentous", "d": "Enveloped",
        "answer": "C",
        "explanation": "The three basic viral morphologies are icosahedral, helical, and complex. Filamentous is not a standard viral form category."
    },
    {
        "section": "الفيروسات",
        "question": "What is the function of the viral capsid?",
        "a": "It contains ribosomes", "b": "It protects the viral genetic material",
        "c": "It produces viral proteins", "d": "It helps in DNA replication",
        "answer": "B",
        "explanation": "The capsid's primary function is to protect the viral genome from degradation."
    },
    {
        "section": "الفيروسات",
        "question": "Which classification system is used for viruses?",
        "a": "Bergey's Manual", "b": "Linnaean System",
        "c": "Hierarchical Classification (Order, Family, Genus, Species)",
        "d": "Whittaker's Five Kingdom Classification",
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
        "explanation": "Viruses are obligate intracellular parasites — they can only reproduce inside living host cells."
    },
    {
        "section": "الفيروسات",
        "question": "Which scientist is credited with the first description of viruses?",
        "a": "Louis Pasteur", "b": "Edward Jenner",
        "c": "Robert Koch", "d": "Alexander Fleming",
        "answer": "A",
        "explanation": "Louis Pasteur contributed foundational work to virology. Dmitri Ivanovsky also described tobacco mosaic virus."
    },
    {
        "section": "الفيروسات",
        "question": "What is the main function of the viral envelope?",
        "a": "To protect the capsid",
        "b": "To facilitate entry into host cells",
        "c": "To replicate viral DNA",
        "d": "To produce viral proteins",
        "answer": "B",
        "explanation": "Viral envelope glycoproteins bind to host cell receptors and facilitate membrane fusion for viral entry."
    },
    {
        "section": "الفيروسات",
        "question": "Which of the following is an RNA virus?",
        "a": "Herpesvirus", "b": "Adenovirus",
        "c": "Retrovirus", "d": "Poxvirus",
        "answer": "C",
        "explanation": "Retroviruses (like HIV) have an RNA genome converted to DNA by reverse transcriptase."
    },
    {
        "section": "الفيروسات",
        "question": "How do bacteriophages primarily infect bacterial cells?",
        "a": "By direct fusion with the bacterial membrane",
        "b": "By injecting their genetic material into the host",
        "c": "By endocytosis",
        "d": "By lysing the host cell first",
        "answer": "B",
        "explanation": "Phages attach to the bacterial surface and inject their DNA into the host, leaving the empty capsid outside."
    },
    {
        "section": "الفيروسات",
        "question": "Which method is commonly used to cultivate viruses in the laboratory?",
        "a": "Agar plate culture", "b": "Nutrient broth culture",
        "c": "Cell culture", "d": "Streak plate method",
        "answer": "C",
        "explanation": "Viruses require living cells for replication, so cell (tissue) culture is used in the laboratory."
    },
    {
        "section": "الفيروسات",
        "question": "Which of the following viruses has a double-stranded RNA genome?",
        "a": "Retrovirus", "b": "Reovirus",
        "c": "Picornavirus", "d": "Herpesvirus",
        "answer": "B",
        "explanation": "Reoviruses (including Rotaviruses) have a segmented double-stranded RNA (dsRNA) genome."
    },
    {
        "section": "الفيروسات",
        "question": "What is the function of viral hemagglutinin in influenza viruses?",
        "a": "Aids in viral entry into host cells",
        "b": "Assists in viral genome replication",
        "c": "Stimulates host immune response",
        "d": "Facilitates viral exit from host cells",
        "answer": "A",
        "explanation": "Hemagglutinin (H) binds to sialic acid receptors on respiratory epithelial cells, mediating viral attachment and entry."
    },
    {
        "section": "الفيروسات",
        "question": "Which type of viral infection leads to immediate destruction of the host cell?",
        "a": "Lysogenic infection", "b": "Latent infection",
        "c": "Lytic infection", "d": "Chronic infection",
        "answer": "C",
        "explanation": "In the lytic cycle, the virus replicates rapidly inside the host cell and lyses (destroys) it upon release of new virions."
    },
    {
        "section": "الفيروسات",
        "question": "Which enzyme allows retroviruses to integrate their genome into the host DNA?",
        "a": "DNA polymerase", "b": "RNA polymerase",
        "c": "Reverse transcriptase", "d": "Integrase",
        "answer": "C",
        "explanation": "Reverse transcriptase converts the viral RNA genome into DNA which is then integrated into the host genome."
    },
    {
        "section": "الفيروسات",
        "question": "What is the primary mode of transmission for arboviruses?",
        "a": "Respiratory droplets", "b": "Contaminated food",
        "c": "Insect vectors", "d": "Direct human contact",
        "answer": "C",
        "explanation": "Arboviruses (arthropod-borne viruses) like dengue and Zika are transmitted through insect bites (mosquitoes, ticks)."
    },
    {
        "section": "الفيروسات",
        "question": "Which is NOT a method of viral classification?",
        "a": "Shape", "b": "Mode of replication",
        "c": "Size of the host cell", "d": "Type of nucleic acid",
        "answer": "C",
        "explanation": "Viral classification uses shape, replication mode, and nucleic acid type — NOT the size of the host cell."
    },
    {
        "section": "الفيروسات",
        "question": "What is a key characteristic of viruses?",
        "a": "They have a nuclear membrane",
        "b": "They possess metabolic enzymes",
        "c": "They lack an external cell wall",
        "d": "They can replicate independently",
        "answer": "C",
        "explanation": "Viruses have no cell wall, no nucleus, no cytoplasm, and no metabolic machinery — they are not cells."
    },
    {
        "section": "الفيروسات",
        "question": "During which stage of the viral life cycle does receptor-mediated endocytosis occur?",
        "a": "Adsorption", "b": "Penetration",
        "c": "Replication", "d": "Assembly",
        "answer": "B",
        "explanation": "Receptor-mediated endocytosis is a mechanism of viral penetration into the host cell."
    },
    {
        "section": "الفيروسات",
        "question": "In viral taxonomy, what suffix is commonly used for virus families?",
        "a": "-virus", "b": "-pathogen", "c": "-viridae", "d": "-bacteria",
        "answer": "C",
        "explanation": "Virus family names end in -viridae (e.g., Herpesviridae, Retroviridae, Picornaviridae)."
    },

    # ══════════════════════════════════════════════════════════════
    # المجموعة 4 — الأسئلة المتقدمة (من النص المرسل)
    # ══════════════════════════════════════════════════════════════
    {
        "section": "الفيروسات",
        "question": "Which viral structure is primarily responsible for attachment to host cell receptors?",
        "a": "Capsomere", "b": "Matrix protein",
        "c": "Viral spikes (glycoproteins)", "d": "Viral polymerase",
        "answer": "C",
        "explanation": "Viral surface glycoproteins (spikes) bind to specific receptors on host cells — this determines host tropism."
    },
    {
        "section": "الفيروسات",
        "question": "Which of the following viruses replicates entirely in the cytoplasm?",
        "a": "Herpesvirus", "b": "Adenovirus",
        "c": "Poxvirus", "d": "Papillomavirus",
        "answer": "C",
        "explanation": "Poxviruses are unique among DNA viruses — they encode their own RNA polymerase and replicate entirely in the cytoplasm."
    },
    {
        "section": "الفيروسات",
        "question": "Which viral genome type requires reverse transcriptase during replication?",
        "a": "dsDNA viruses", "b": "(+) ssRNA viruses",
        "c": "Retroviruses", "d": "dsRNA viruses",
        "answer": "C",
        "explanation": "Retroviruses use reverse transcriptase to convert their RNA genome into DNA, which is then integrated into the host genome."
    },
    {
        "section": "الفيروسات",
        "question": "The icosahedral symmetry of viruses provides:",
        "a": "Maximum stability with minimal genetic coding",
        "b": "Increased lipid envelope protection",
        "c": "Higher mutation rate",
        "d": "Ability to replicate outside cells",
        "answer": "A",
        "explanation": "Icosahedral symmetry is energetically optimal — it encloses maximum volume with minimal protein subunits."
    },
    {
        "section": "الفيروسات",
        "question": "Which of the following viruses is most resistant to environmental conditions?",
        "a": "Enveloped viruses", "b": "Naked viruses",
        "c": "RNA viruses", "d": "Retroviruses",
        "answer": "B",
        "explanation": "Naked (non-enveloped) viruses are more resistant to heat, desiccation, detergents, and chemical disinfectants than enveloped viruses."
    },
    {
        "section": "الفيروسات",
        "question": "Which enzyme is commonly carried by negative-sense RNA viruses?",
        "a": "DNA polymerase",
        "b": "RNA-dependent RNA polymerase",
        "c": "Reverse transcriptase",
        "d": "Integrase",
        "answer": "B",
        "explanation": "Negative-sense RNA cannot serve as mRNA directly — these viruses must carry RNA-dependent RNA polymerase (RdRp) to transcribe their genome."
    },
    {
        "section": "الفيروسات",
        "question": "During viral replication, the stage called 'uncoating' refers to:",
        "a": "Release of virions from the host cell",
        "b": "Removal of viral envelope only",
        "c": "Release of viral genome into host cell",
        "d": "Assembly of capsid proteins",
        "answer": "C",
        "explanation": "Uncoating is the process of removing the capsid (and envelope if present) to release the viral genome into the host cell cytoplasm."
    },
    {
        "section": "الفيروسات",
        "question": "Which viral family contains segmented RNA genomes?",
        "a": "Picornaviridae", "b": "Orthomyxoviridae",
        "c": "Herpesviridae", "d": "Adenoviridae",
        "answer": "B",
        "explanation": "Orthomyxoviridae (influenza viruses) have 8 segments of negative-sense RNA — this segmentation allows genetic reassortment."
    },
    {
        "section": "الفيروسات",
        "question": "The process by which viruses obtain their envelope from host membranes is called:",
        "a": "Lysis", "b": "Budding", "c": "Integration", "d": "Fusion",
        "answer": "B",
        "explanation": "During budding, the nucleocapsid pushes through the host cell membrane, acquiring a lipid envelope as it exits."
    },
    {
        "section": "الفيروسات",
        "question": "Which viral component determines host specificity (tropism)?",
        "a": "Capsid size", "b": "Viral receptor-binding proteins",
        "c": "Genome length", "d": "Viral polymerase",
        "answer": "B",
        "explanation": "Viral tropism is determined by the specific interaction between viral surface proteins and receptors on host cells."
    },
    {
        "section": "الفيروسات",
        "question": "Which virus has a double-stranded RNA genome?",
        "a": "Rotavirus", "b": "Poliovirus",
        "c": "Influenza virus", "d": "HIV",
        "answer": "A",
        "explanation": "Rotavirus (family Reoviridae) has an 11-segment double-stranded RNA genome."
    },
    {
        "section": "الفيروسات",
        "question": "Which stage of viral replication involves synthesis of viral proteins and nucleic acids?",
        "a": "Attachment", "b": "Penetration",
        "c": "Biosynthesis", "d": "Release",
        "answer": "C",
        "explanation": "The biosynthesis (eclipse) stage is when viral proteins and nucleic acids are produced using host cell machinery."
    },
    {
        "section": "الفيروسات",
        "question": "Which virus integrates its genome into the host DNA as a provirus?",
        "a": "Influenza virus", "b": "HIV",
        "c": "Rabies virus", "d": "Rotavirus",
        "answer": "B",
        "explanation": "HIV integrates its DNA copy into the host genome as a provirus, which can remain latent for years before activation."
    },
    {
        "section": "الفيروسات",
        "question": "Which viral infection cycle results in destruction of the host cell?",
        "a": "Lysogenic cycle", "b": "Latent cycle",
        "c": "Lytic cycle", "d": "Persistent cycle",
        "answer": "C",
        "explanation": "In the lytic cycle, new virions accumulate until the host cell lyses, releasing hundreds of new virus particles."
    },
    {
        "section": "الفيروسات",
        "question": "Which viral component protects the genome and assists in viral assembly?",
        "a": "Envelope", "b": "Capsid",
        "c": "Glycoprotein spikes", "d": "Matrix protein",
        "answer": "B",
        "explanation": "The capsid both protects the viral genome and provides structural scaffolding for viral assembly."
    },
]

db.import_questions(QUESTIONS)
print(f"\n✅ تم إضافة {len(QUESTIONS)} سؤال في سكشن الفيروسات 🦠")
print(f"\n🚀 شغّل البوت الآن: python bot.py")
