"""
أسئلة العمليات الأيضية — كل الأشكال محوّلة لـ MCQ
43 MCQ + 8 T/F + 11 فراغ + Matching + نفس الأسئلة بأشكال 3
"""

METABOLISM_QUESTIONS = [

    # ══════════════════════════════════════════════════════════════
    # SECTION 1: MCQ الأصلية (43 سؤال)
    # ══════════════════════════════════════════════════════════════

    {"section":"العمليات الأيضية","section_emoji":"⚗️",
     "section_description":"Metabolism, Enzymes, Glycolysis, Krebs, ETC, Fermentation, Photosynthesis",
     "question":"Which of the following is an energy-releasing process?",
     "a":"Anabolism","b":"Catabolism","c":"Fermentation","d":"Endocytosis",
     "answer":"B","explanation":"Catabolism breaks down complex molecules to release energy."},

    {"section":"العمليات الأيضية",
     "question":"What is the final electron acceptor in aerobic respiration?",
     "a":"Nitrogen","b":"Sulfur","c":"Oxygen","d":"Carbon dioxide",
     "answer":"C","explanation":"O2 is the final electron acceptor in aerobic respiration, forming water."},

    {"section":"العمليات الأيضية",
     "question":"Which metabolic pathway produces ATP through substrate-level phosphorylation?",
     "a":"Glycolysis","b":"Electron Transport Chain","c":"Krebs Cycle","d":"Photosynthesis",
     "answer":"A","explanation":"Glycolysis produces 2 ATP net via substrate-level phosphorylation."},

    {"section":"العمليات الأيضية",
     "question":"What is the main function of the electron transport chain?",
     "a":"DNA replication","b":"ATP production","c":"Protein synthesis","d":"Lipid breakdown",
     "answer":"B","explanation":"The ETC generates ATP through oxidative phosphorylation."},

    {"section":"العمليات الأيضية",
     "question":"What type of fermentation produces only lactic acid?",
     "a":"Alcohol fermentation","b":"Mixed acid fermentation","c":"Homolactic fermentation","d":"Heterolactic fermentation",
     "answer":"C","explanation":"Homolactic fermentation produces lactic acid only."},

    {"section":"العمليات الأيضية",
     "question":"What does the term 'metabolism' refer to in microbiology?",
     "a":"The sum of all chemical reactions in an organism","b":"The process of cellular division",
     "c":"The energy storage in cells","d":"The synthesis of proteins only",
     "answer":"A","explanation":"Metabolism = the sum of all chemical reactions (catabolism + anabolism)."},

    {"section":"العمليات الأيضية",
     "question":"Enzymes are best described as:",
     "a":"Inhibitors of chemical reactions",
     "b":"Biological catalysts that lower the activation energy of reactions",
     "c":"Structural components of cell walls","d":"Energy storage molecules",
     "answer":"B","explanation":"Enzymes are biological catalysts that lower activation energy without being consumed."},

    {"section":"العمليات الأيضية",
     "question":"The protein part of an enzyme, without its cofactor, is known as the:",
     "a":"Holoenzyme","b":"Coenzyme","c":"Apoenzyme","d":"Substrate",
     "answer":"C","explanation":"Apoenzyme = protein portion of an enzyme (inactive without cofactor)."},

    {"section":"العمليات الأيضية",
     "question":"When an apoenzyme binds with its cofactor, the complete active enzyme is called a:",
     "a":"Holoenzyme","b":"Metalloenzyme","c":"Isoenzyme","d":"Subenzyme",
     "answer":"A","explanation":"Holoenzyme = apoenzyme + cofactor (fully active enzyme)."},

    {"section":"العمليات الأيضية",
     "question":"Which of the following is NOT one of the six major classes of enzymes?",
     "a":"Oxidoreductase","b":"Transferase","c":"Polymerase","d":"Lyase",
     "answer":"C","explanation":"The 6 classes are: Oxidoreductase, Transferase, Hydrolase, Lyase, Isomerase, Ligase. Polymerase is not one of them."},

    {"section":"العمليات الأيضية",
     "question":"The process that converts glucose into pyruvic acid in the cytoplasm is known as:",
     "a":"Krebs cycle","b":"Electron transport chain","c":"Glycolysis","d":"Fermentation",
     "answer":"C","explanation":"Glycolysis occurs in the cytoplasm and converts glucose to pyruvic acid."},

    {"section":"العمليات الأيضية",
     "question":"What is the net gain of ATP molecules produced during glycolysis from one molecule of glucose?",
     "a":"2 ATP","b":"4 ATP","c":"36 ATP","d":"38 ATP",
     "answer":"A","explanation":"Net gain = 2 ATP (4 produced - 2 used = 2 net)."},

    {"section":"العمليات الأيضية",
     "question":"Which metabolic cycle oxidizes acetyl CoA to produce NADH and FADH2?",
     "a":"Glycolysis","b":"Krebs cycle","c":"Calvin cycle","d":"Urea cycle",
     "answer":"B","explanation":"The Krebs (citric acid) cycle oxidizes acetyl CoA producing NADH, FADH2, and ATP."},

    {"section":"العمليات الأيضية",
     "question":"In aerobic respiration, what serves as the final electron acceptor in the electron transport chain?",
     "a":"NADH","b":"FADH2","c":"Oxygen (O2)","d":"Carbon dioxide (CO2)",
     "answer":"C","explanation":"O2 is the final electron acceptor in aerobic respiration, reduced to H2O."},

    {"section":"العمليات الأيضية",
     "question":"Compared to aerobic respiration, anaerobic respiration generally yields:",
     "a":"More ATP","b":"The same amount of ATP","c":"Less ATP","d":"No ATP",
     "answer":"C","explanation":"Anaerobic respiration yields less ATP because only part of the Krebs cycle operates."},

    {"section":"العمليات الأيضية",
     "question":"During fermentation, the final electron acceptor is typically:",
     "a":"Oxygen","b":"An organic molecule","c":"Nitrogen","d":"Water",
     "answer":"B","explanation":"Fermentation uses organic molecules as final electron acceptors, not O2."},

    {"section":"العمليات الأيضية",
     "question":"Alcohol fermentation results in the production of:",
     "a":"Lactic acid","b":"Ethanol and CO2","c":"Acetic acid","d":"Water and CO2",
     "answer":"B","explanation":"Alcohol fermentation produces ethyl alcohol (ethanol) + CO2."},

    {"section":"العمليات الأيضية",
     "question":"Lactic acid fermentation (in its homolactic form) produces:",
     "a":"Ethanol","b":"Lactic acid only","c":"A mixture of lactic acid and ethanol","d":"Acetic acid",
     "answer":"B","explanation":"Homolactic fermentation produces ONLY lactic acid."},

    {"section":"العمليات الأيضية",
     "question":"The light-dependent reactions of photosynthesis occur in the:",
     "a":"Stroma of chloroplasts","b":"Thylakoid membranes","c":"Cytoplasm","d":"Mitochondrial matrix",
     "answer":"B","explanation":"Light-dependent reactions occur in the thylakoid membranes of chloroplasts."},

    {"section":"العمليات الأيضية",
     "question":"The Calvin-Benson cycle is also known as the:",
     "a":"Krebs cycle","b":"Dark (light-independent) reactions of photosynthesis",
     "c":"Light reactions of photosynthesis","d":"Electron transport chain",
     "answer":"B","explanation":"Calvin-Benson cycle = light-independent (dark) reactions that fix CO2."},

    {"section":"العمليات الأيضية",
     "question":"Phototrophs obtain energy primarily from:",
     "a":"Chemical compounds","b":"Light","c":"Inorganic substances","d":"Organic compounds",
     "answer":"B","explanation":"Phototrophs use light as their energy source through photosynthesis."},

    {"section":"العمليات الأيضية",
     "question":"Chemotrophs derive energy from:",
     "a":"Sunlight","b":"Chemical compounds","c":"Water","d":"Carbon dioxide",
     "answer":"B","explanation":"Chemotrophs obtain energy by oxidizing chemical compounds."},

    {"section":"العمليات الأيضية",
     "question":"Which of the following increases the rate of chemical reactions in microbial metabolism?",
     "a":"Decreased temperature","b":"Lower substrate concentration",
     "c":"The presence of enzymes","d":"Higher activation energy",
     "answer":"C","explanation":"Enzymes lower activation energy and increase reaction rate."},

    {"section":"العمليات الأيضية",
     "question":"In enzyme function, a coenzyme primarily assists by:",
     "a":"Becoming a permanent part of the enzyme","b":"Providing direct energy for the reaction",
     "c":"Enhancing the enzyme's catalytic activity","d":"Acting as a substrate for the enzyme",
     "answer":"C","explanation":"Coenzymes are organic cofactors (NAD+, FAD) that enhance enzyme catalytic activity."},

    {"section":"العمليات الأيضية",
     "question":"Chemolithotrophs obtain energy by oxidizing inorganic compounds such as:",
     "a":"Sunlight","b":"Organic sugars","c":"Hydrogen sulfide","d":"Water",
     "answer":"C","explanation":"Chemolithotrophs oxidize inorganic compounds like H2S, NH3, or Fe2+."},

    {"section":"العمليات الأيضية",
     "question":"Which of the following metabolic processes is catabolic?",
     "a":"Protein synthesis","b":"Breakdown of glucose for energy","c":"Lipid biosynthesis","d":"DNA replication",
     "answer":"B","explanation":"Catabolism breaks down molecules (like glucose) to release energy."},

    {"section":"العمليات الأيضية",
     "question":"What is the primary enzyme responsible for catalyzing the first step of glycolysis?",
     "a":"Lipase","b":"Amylase","c":"Hexokinase","d":"DNA polymerase",
     "answer":"C","explanation":"Hexokinase phosphorylates glucose to glucose-6-phosphate, the first step of glycolysis."},

    {"section":"العمليات الأيضية",
     "question":"Which of the following does NOT influence enzyme activity?",
     "a":"Substrate concentration","b":"pH level","c":"Nucleic acid composition","d":"Temperature",
     "answer":"C","explanation":"Enzyme activity is affected by temperature, pH, and substrate concentration — NOT nucleic acid composition."},

    {"section":"العمليات الأيضية",
     "question":"A coenzyme is a:",
     "a":"Type of ribosome","b":"Non-protein molecule that assists enzyme function",
     "c":"Polymer of nucleic acids","d":"Type of DNA polymerase",
     "answer":"B","explanation":"Coenzymes are non-protein organic molecules (NAD+, FAD) that assist enzymes."},

    {"section":"العمليات الأيضية",
     "question":"Which of the following categories of microorganisms uses light as an energy source?",
     "a":"Chemotrophs","b":"Phototrophs","c":"Chemoorganotrophs","d":"Chemolithotrophs",
     "answer":"B","explanation":"Phototrophs use light energy (photosynthesis) as their primary energy source."},

    {"section":"العمليات الأيضية",
     "question":"What can denature enzymes?",
     "a":"Light exposure","b":"Temperature and pH changes","c":"Enzyme inhibitors","d":"None of the above",
     "answer":"B","explanation":"High temperature and extreme pH disrupt enzyme 3D structure causing denaturation."},

    {"section":"العمليات الأيضية",
     "question":"Which of the following occurs during fermentation?",
     "a":"Uses the Krebs cycle","b":"Uses oxygen as an electron acceptor",
     "c":"Does not require oxygen","d":"Generates ATP through oxidative phosphorylation",
     "answer":"C","explanation":"Fermentation is anaerobic — does not require oxygen and does not use ETC or Krebs cycle."},

    {"section":"العمليات الأيضية",
     "question":"Chemolithotrophs derive their energy from:",
     "a":"Organic compounds","b":"Light","c":"Inorganic compounds","d":"Fermentation",
     "answer":"C","explanation":"Chemolithotrophs oxidize inorganic compounds (H2S, Fe2+, NH3) for energy."},

    {"section":"العمليات الأيضية",
     "question":"Which enzyme classification involves the transfer of functional groups?",
     "a":"Oxidoreductase","b":"Transferase","c":"Hydrolase","d":"Ligase",
     "answer":"B","explanation":"Transferase enzymes transfer functional groups from one molecule to another."},

    {"section":"العمليات الأيضية",
     "question":"Glycolysis results in the production of:",
     "a":"2 ATP, 2 pyruvic acid, and 2 NADH","b":"4 ATP, 2 pyruvic acid, and 2 NADPH",
     "c":"6 ATP, 2 pyruvic acid, and 2 FADH2","d":"2 ATP, 4 pyruvic acid, and 2 NADH",
     "answer":"A","explanation":"Glycolysis: 1 glucose → 2 pyruvate + 2 ATP (net) + 2 NADH."},

    {"section":"العمليات الأيضية",
     "question":"Which metabolic process does NOT require oxygen and does NOT involve the Krebs cycle or ETC?",
     "a":"Aerobic respiration","b":"Fermentation","c":"Anaerobic respiration","d":"Oxidative phosphorylation",
     "answer":"B","explanation":"Fermentation: no O2, no Krebs cycle, no ETC — uses organic final electron acceptor."},

    {"section":"العمليات الأيضية",
     "question":"What is catabolism?",
     "a":"The energy-using processes","b":"The process that forms new enzymes",
     "c":"The energy-releasing processes that provide building blocks for anabolism","d":"A metabolic pathway that produces vitamins",
     "answer":"C","explanation":"Catabolism = energy-releasing breakdown of complex molecules."},

    {"section":"العمليات الأيضية",
     "question":"In microbial metabolism, which statement best describes enzyme catalysis?",
     "a":"Enzymes increase activation energy to stabilize reactions",
     "b":"Enzymes lower activation energy and increase reaction rate",
     "c":"Enzymes are consumed during reactions",
     "d":"Enzymes function independently of substrate specificity",
     "answer":"B","explanation":"Enzymes lower activation energy → faster reactions, and are NOT consumed."},

    {"section":"العمليات الأيضية",
     "question":"Which enzyme class is responsible for oxidation-reduction reactions?",
     "a":"Transferase","b":"Hydrolase","c":"Oxidoreductase","d":"Isomerase",
     "answer":"C","explanation":"Oxidoreductase catalyzes oxidation-reduction (redox) reactions."},

    {"section":"العمليات الأيضية",
     "question":"Which enzyme class catalyzes the rearrangement of atoms within a molecule?",
     "a":"Transferase","b":"Ligase","c":"Lyase","d":"Isomerase",
     "answer":"D","explanation":"Isomerase rearranges atoms within a molecule to form isomers."},

    {"section":"العمليات الأيضية",
     "question":"Which enzyme class joins molecules together using ATP?",
     "a":"Hydrolase","b":"Lyase","c":"Isomerase","d":"Ligase",
     "answer":"D","explanation":"Ligase joins molecules together and requires ATP."},

    {"section":"العمليات الأيضية",
     "question":"Which enzyme class catalyzes removal of atoms without hydrolysis?",
     "a":"Isomerase","b":"Lyase","c":"Hydrolase","d":"Ligase",
     "answer":"B","explanation":"Lyase removes atoms without hydrolysis, forming double bonds."},

    {"section":"العمليات الأيضية",
     "question":"How many ATPs are produced from complete oxidation of one glucose in aerobic respiration?",
     "a":"2 ATP","b":"4 ATP","c":"18 ATP","d":"36 ATP",
     "answer":"D","explanation":"Complete aerobic respiration yields 36 ATP from one glucose molecule."},

    {"section":"العمليات الأيضية",
     "question":"The three major processes of carbohydrate catabolism are:",
     "a":"Glycolysis, Krebs cycle, Electron transport chain",
     "b":"Glycolysis, Fermentation, Photosynthesis",
     "c":"Krebs cycle, Calvin cycle, Fermentation",
     "d":"Electron transport chain, Fermentation, Glycolysis",
     "answer":"A","explanation":"Carbohydrate catabolism: 1) Glycolysis 2) Krebs cycle 3) Electron transport chain."},

    # ══════════════════════════════════════════════════════════════
    # SECTION 2: T/F محوّلة لـ MCQ (8 أسئلة × 2 شكل)
    # ══════════════════════════════════════════════════════════════

    # T/F 1 — Anabolism
    {"section":"العمليات الأيضية",
     "question":"Which of the following correctly describes anabolism?",
     "a":"It is the energy-releasing process in cells",
     "b":"It is the energy-USING process that builds complex molecules",
     "c":"It breaks down glucose to produce ATP",
     "d":"It is another name for catabolism",
     "answer":"B","explanation":"Anabolism uses energy to BUILD complex molecules. Catabolism RELEASES energy."},

    {"section":"العمليات الأيضية",
     "question":"True or False: Anabolism is the process that releases energy in cells.",
     "a":"True — anabolism releases energy","b":"False — anabolism USES energy, catabolism releases it",
     "c":"True — anabolism and catabolism both release energy","d":"False — neither releases energy",
     "answer":"B","explanation":"Anabolism = energy-USING (builds molecules). Catabolism = energy-RELEASING."},

    # T/F 2 — Holoenzyme
    {"section":"العمليات الأيضية",
     "question":"Which statement about holoenzyme is CORRECT?",
     "a":"A holoenzyme consists only of the apoenzyme protein",
     "b":"A holoenzyme consists of an apoenzyme AND a cofactor",
     "c":"A holoenzyme is the cofactor alone","d":"A holoenzyme does not require a cofactor",
     "answer":"B","explanation":"Holoenzyme = apoenzyme (protein) + cofactor (non-protein) = fully active enzyme."},

    {"section":"العمليات الأيضية",
     "question":"True or False: A holoenzyme consists of an apoenzyme and a cofactor.",
     "a":"True — holoenzyme = apoenzyme + cofactor","b":"False — holoenzyme = apoenzyme only",
     "c":"False — holoenzyme = cofactor only","d":"True — but only when the cofactor is organic",
     "answer":"A","explanation":"Holoenzyme = apoenzyme + cofactor. This statement is TRUE."},

    # T/F 3 — Enzymes & activation energy
    {"section":"العمليات الأيضية",
     "question":"How do enzymes affect activation energy?",
     "a":"They increase activation energy","b":"They decrease (lower) activation energy",
     "c":"They have no effect on activation energy","d":"They convert activation energy to ATP",
     "answer":"B","explanation":"Enzymes LOWER activation energy → faster reaction rate."},

    {"section":"العمليات الأيضية",
     "question":"True or False: Enzymes increase reaction rates by INCREASING activation energy.",
     "a":"True — they increase activation energy","b":"False — enzymes LOWER activation energy",
     "c":"True — higher energy = faster reactions","d":"False — enzymes have no effect on energy",
     "answer":"B","explanation":"This statement is FALSE. Enzymes LOWER (decrease) activation energy."},

    # T/F 5 — High temperature denatures enzymes
    {"section":"العمليات الأيضية",
     "question":"What happens to enzyme function at very high temperatures?",
     "a":"Enzyme activity increases indefinitely","b":"Enzyme becomes more specific",
     "c":"Enzyme is denatured and loses its function","d":"Enzyme converts to a coenzyme",
     "answer":"C","explanation":"High temperature disrupts the 3D structure of enzymes → denaturation → loss of function."},

    {"section":"العمليات الأيضية",
     "question":"True or False: High temperatures can denature enzymes, leading to loss of their function.",
     "a":"True — high temperature causes denaturation and loss of function",
     "b":"False — enzymes are resistant to all temperatures",
     "c":"True — but only at temperatures above 100°C",
     "d":"False — high temperature only slows enzymes, doesn't stop them",
     "answer":"A","explanation":"TRUE. High temperatures disrupt hydrogen bonds → denaturation → enzyme loses function."},

    # T/F 6 — Glycolysis
    {"section":"العمليات الأيضية",
     "question":"Which statement about glycolysis is CORRECT?",
     "a":"Glycolysis requires oxygen to proceed",
     "b":"Glycolysis is the first step and does NOT require oxygen",
     "c":"Glycolysis occurs in the mitochondria","d":"Glycolysis produces FADH2",
     "answer":"B","explanation":"Glycolysis is the first step of carbohydrate catabolism, occurs in cytoplasm, requires NO oxygen."},

    {"section":"العمليات الأيضية",
     "question":"True or False: Glycolysis is the first step in carbohydrate catabolism and does not require oxygen.",
     "a":"True — glycolysis is first and is anaerobic","b":"False — glycolysis requires oxygen",
     "c":"True — but glycolysis occurs in the mitochondria","d":"False — glycolysis is not the first step",
     "answer":"A","explanation":"TRUE. Glycolysis: first step, occurs in cytoplasm, anaerobic (no O2 needed)."},

    # T/F 7 — Anaerobic respiration
    {"section":"العمليات الأيضية",
     "question":"In anaerobic respiration, what is the final electron acceptor?",
     "a":"Oxygen (O2)","b":"Carbon dioxide","c":"NOT oxygen — an inorganic molecule other than O2",
     "d":"Water",
     "answer":"C","explanation":"Anaerobic respiration uses inorganic molecules other than O2 (e.g., NO3-, SO4-) as final electron acceptors."},

    {"section":"العمليات الأيضية",
     "question":"True or False: In anaerobic respiration, oxygen is the final electron acceptor.",
     "a":"True — oxygen is always the final acceptor","b":"False — in anaerobic respiration the acceptor is NOT oxygen",
     "c":"True — both aerobic and anaerobic use oxygen","d":"False — there is no electron acceptor in anaerobic respiration",
     "answer":"B","explanation":"FALSE. In AEROBIC respiration O2 is the acceptor. In ANAEROBIC it is NOT O2."},

    # T/F 8 — Alcohol fermentation
    {"section":"العمليات الأيضية",
     "question":"What are the products of alcohol fermentation?",
     "a":"Lactic acid only","b":"Ethyl alcohol and carbon dioxide (CO2)",
     "c":"Acetic acid and water","d":"ATP and oxygen",
     "answer":"B","explanation":"Alcohol fermentation produces ethanol (ethyl alcohol) + CO2."},

    {"section":"العمليات الأيضية",
     "question":"True or False: Alcohol fermentation produces ethyl alcohol and carbon dioxide.",
     "a":"True — products are ethanol + CO2","b":"False — it produces only lactic acid",
     "c":"True — but only in eukaryotes","d":"False — it produces acetic acid",
     "answer":"A","explanation":"TRUE. Alcohol fermentation: pyruvate → acetaldehyde → ethanol + CO2."},

    # ══════════════════════════════════════════════════════════════
    # SECTION 3: فراغات محوّلة لـ MCQ (11 سؤال × 2 شكل)
    # ══════════════════════════════════════════════════════════════

    {"section":"العمليات الأيضية",
     "question":"Fill in: Removal of atoms WITHOUT hydrolysis is catalyzed by ___.",
     "a":"Hydrolase","b":"Lyase","c":"Isomerase","d":"Ligase",
     "answer":"B","explanation":"Lyase removes atoms without hydrolysis, often creating double bonds."},

    {"section":"العمليات الأيضية",
     "question":"The breakdown of carbohydrates to release energy is carried out through ___ major processes.",
     "a":"Two","b":"Three","c":"Four","d":"Five",
     "answer":"B","explanation":"Three major processes: 1) Glycolysis 2) Krebs cycle 3) Electron transport chain."},

    {"section":"العمليات الأيضية",
     "question":"Complete oxidation of one glucose using aerobic respiration produces ___ ATPs.",
     "a":"18 ATP","b":"28 ATP","c":"36 ATP","d":"48 ATP",
     "answer":"C","explanation":"Complete aerobic oxidation of glucose yields 36 ATP."},

    {"section":"العمليات الأيضية",
     "question":"Fill in: Alcohol fermentation produces ___ + CO2.",
     "a":"Lactic acid","b":"Acetic acid","c":"Ethyl alcohol (ethanol)","d":"Pyruvic acid",
     "answer":"C","explanation":"Alcohol fermentation: glucose → ethanol + CO2."},

    {"section":"العمليات الأيضية",
     "question":"The energy-releasing processes in metabolism are collectively called ___.",
     "a":"Anabolism","b":"Catabolism","c":"Photosynthesis","d":"Fermentation",
     "answer":"B","explanation":"Catabolism = all energy-RELEASING metabolic processes."},

    {"section":"العمليات الأيضية",
     "question":"Fill in: Apoenzyme is the ___ component of an enzyme.",
     "a":"Non-protein (cofactor)","b":"Inorganic","c":"Protein","d":"Lipid",
     "answer":"C","explanation":"Apoenzyme = the protein portion of an enzyme (inactive without its cofactor)."},

    {"section":"العمليات الأيضية",
     "question":"Fill in: Isomerase catalyzes the ___ of atoms within a molecule.",
     "a":"Joining","b":"Removal","c":"Transfer","d":"Rearrangement",
     "answer":"D","explanation":"Isomerase = rearrangement of atoms to form isomers."},

    {"section":"العمليات الأيضية",
     "question":"A metabolic pathway is a sequence of ___ catalyzed chemical reactions in a cell.",
     "a":"Randomly","b":"Enzymatically","c":"Chemically","d":"Physically",
     "answer":"B","explanation":"Metabolic pathways are sequences of ENZYMATICALLY catalyzed reactions."},

    {"section":"العمليات الأيضية",
     "question":"___ is the minimum amount of energy required to start a chemical reaction.",
     "a":"Kinetic energy","b":"Potential energy","c":"Activation energy","d":"Thermal energy",
     "answer":"C","explanation":"Activation energy = minimum energy required to initiate a chemical reaction."},

    {"section":"العمليات الأيضية",
     "question":"A ___ is a non-protein component required for the activity of an enzyme.",
     "a":"Substrate","b":"Cofactor","c":"Apoenzyme","d":"Holoenzyme",
     "answer":"B","explanation":"Cofactor = non-protein component (can be organic=coenzyme or inorganic=metal ion)."},

    {"section":"العمليات الأيضية",
     "question":"Which of the following is an organic cofactor (coenzyme)?",
     "a":"Fe2+","b":"Mg2+","c":"NAD+","d":"Zn2+",
     "answer":"C","explanation":"NAD+ (and NADP+, FAD, CoA) are organic cofactors = coenzymes."},

    # ══════════════════════════════════════════════════════════════
    # SECTION 4: Matching محوّلة لـ MCQ
    # ══════════════════════════════════════════════════════════════

    {"section":"العمليات الأيضية",
     "question":"Match: Which enzyme class is responsible for HYDROLYSIS reactions?",
     "a":"Oxidoreductase","b":"Transferase","c":"Hydrolase","d":"Ligase",
     "answer":"C","explanation":"Hydrolase catalyzes hydrolysis — breaking bonds using water."},

    {"section":"العمليات الأيضية",
     "question":"Match: The term 'Catabolism' is best matched with:",
     "a":"Energy-using processes","b":"Energy-releasing processes",
     "c":"Protein synthesis","d":"DNA replication",
     "answer":"B","explanation":"Catabolism = energy-RELEASING breakdown of complex molecules."},

    {"section":"العمليات الأيضية",
     "question":"Match: The term 'Anabolism' is best matched with:",
     "a":"Energy-releasing processes","b":"Oxidation reactions",
     "c":"Energy-using processes","d":"Fermentation",
     "answer":"C","explanation":"Anabolism = energy-USING synthesis of complex molecules."},

    {"section":"العمليات الأيضية",
     "question":"Match: 'Cofactor' is best matched with:",
     "a":"Protein component of an enzyme","b":"Complete active enzyme",
     "c":"Non-protein component of an enzyme","d":"Product of glycolysis",
     "answer":"C","explanation":"Cofactor = non-protein component required for enzyme activity."},

    {"section":"العمليات الأيضية",
     "question":"Match: 'Oxidoreductase' is matched with which function?",
     "a":"Transfer functional groups","b":"Hydrolysis",
     "c":"Rearrangement of atoms","d":"Oxidation-reduction reactions",
     "answer":"D","explanation":"Oxidoreductase catalyzes oxidation-reduction (redox) reactions."},

    # ══════════════════════════════════════════════════════════════
    # SECTION 5: Short Answer → MCQ
    # ══════════════════════════════════════════════════════════════

    {"section":"العمليات الأيضية",
     "question":"According to the collision theory, chemical reactions occur when:",
     "a":"Molecules are at rest","b":"Atoms, ions, and molecules collide with sufficient energy",
     "c":"Temperature drops below 0°C","d":"Enzymes are absent",
     "answer":"B","explanation":"Collision theory: reactions occur when particles collide with enough energy (≥ activation energy)."},

    {"section":"العمليات الأيضية",
     "question":"The Key-Lock theory of enzyme activity states that:",
     "a":"Any enzyme can catalyze any reaction","b":"Enzymes change shape to fit any substrate",
     "c":"The enzyme's active site is specifically shaped to fit a particular substrate",
     "d":"Substrates are used up during the reaction",
     "answer":"C","explanation":"Key-Lock theory: enzyme active site = specific shape that fits ONLY its substrate (like key-lock)."},

    {"section":"العمليات الأيضية",
     "question":"Which of the following is an example of a coenzyme?",
     "a":"Hexokinase","b":"Lipase","c":"NAD+","d":"Holoenzyme",
     "answer":"C","explanation":"NAD+, NADP+, FAD, and Coenzyme A are all coenzymes (organic cofactors)."},

    {"section":"العمليات الأيضية",
     "question":"What is produced by the oxidation of glucose during glycolysis?",
     "a":"Acetyl CoA and FADH2","b":"ATP and NADH (and pyruvic acid)",
     "c":"CO2 and water","d":"Ethanol and lactic acid",
     "answer":"B","explanation":"Glycolysis: glucose → 2 pyruvate + 2 ATP (net) + 2 NADH."},

    {"section":"العمليات الأيضية",
     "question":"What does the Krebs cycle oxidize to produce NADH and FADH2?",
     "a":"Glucose","b":"Pyruvic acid","c":"Acetyl CoA","d":"Lactic acid",
     "answer":"C","explanation":"Krebs cycle oxidizes acetyl CoA → NADH, FADH2, CO2, and 1 ATP per turn."},

    {"section":"العمليات الأيضية",
     "question":"In photosynthesis, what is the main difference between oxygenic and anoxygenic photosynthesis?",
     "a":"Oxygenic uses CO2, anoxygenic does not","b":"Oxygenic produces O2, anoxygenic does not produce O2",
     "c":"They are identical processes","d":"Anoxygenic requires more light",
     "answer":"B","explanation":"Oxygenic (plants, cyanobacteria) produces O2. Anoxygenic (green/purple bacteria) does NOT produce O2."},

    {"section":"العمليات الأيضية",
     "question":"Which process involves fixing carbon into organic molecules using light energy?",
     "a":"Glycolysis","b":"Fermentation","c":"Photosynthesis (dark reaction / Calvin cycle)","d":"ETC",
     "answer":"C","explanation":"Photosynthesis dark reactions (Calvin-Benson cycle) fix CO2 into organic molecules."},

    {"section":"العمليات الأيضية",
     "question":"What type of organism is Chemoautotroph?",
     "a":"Uses light, CO2 as carbon source","b":"Uses chemical energy, CO as carbon source",
     "c":"Uses light, organic compounds as carbon source","d":"Uses chemical energy, organic compounds as carbon source",
     "answer":"B","explanation":"Chemoautotroph: energy from chemicals, carbon from CO2/inorganic sources. Example: iron-oxidizing bacteria."},

]

print(f"✅ إجمالي الأسئلة: {len(METABOLISM_QUESTIONS)}")
from collections import Counter
print(f"السكشن: العمليات الأيضية")

if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from database import Database
    os.makedirs("/data", exist_ok=True)
    db = Database("/data/quiz_bot.db")

    # امسح أسئلة هذا السكشن فقط قبل الإضافة لتجنب التكرار
    with db._connect() as c:
        c.execute("PRAGMA foreign_keys = OFF")
        # احذف أسئلة سكشن العمليات الأيضية فقط
        c.execute("""DELETE FROM questions WHERE section_id IN (
            SELECT id FROM sections WHERE name='العمليات الأيضية'
        )""")
        c.execute("DELETE FROM sections WHERE name='العمليات الأيضية'")
        c.execute("PRAGMA foreign_keys = ON")
    print("🗑️ تم مسح الأسئلة القديمة للعمليات الأيضية")

    db.import_questions(METABOLISM_QUESTIONS)
    print(f"✅ تم إضافة {len(METABOLISM_QUESTIONS)} سؤال في سكشن العمليات الأيضية")
