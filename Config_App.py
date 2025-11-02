patient_history_columns = ["Test_date", "STI", "Test_type", "Result", "Location", "Notes", "Entry_ts"]

stis_full_list = [
    "HIV",
    "Syphilis",
    "Gonorrhea",
    "Chlamydia",
    "Hepatitis A",
    "Hepatitis B",
    "Hepatitis C",
    "Genital herpes",
    "Human papillomavirus (HPV)",
    "Mycoplasma genitalium",
    "Trichomoniasis",
    "LGV (Lymphogranuloma venereum)"
]

profile_tags_full_list = [
    "MSM (Men who have sex with men)",
    "WSW (Women who have sex with women)",
    "Bisexual",
    "Trans woman",
    "Trans man",
    "Non-binary",
    "PrEP user",
    "PEP user",
    "Living with HIV",
    "Multiple partners",
    "Casual partners",
    "Chemsex",
    "Sex work",
    "Serodiscordant couple",
    "Vaccinated Hepatitis A/B",
    "Vaccinated HPV"
]

sti_test_types = {
    "HIV": [
        "Ag/Ab 4th generation (ELISA)",
        "Rapid antibody test",
        "Western blot",
        "PCR (RNA viral load)",
        "Self-test (oral fluid)",
        "Other / Don’t know",
    ],
    "Syphilis": [
        "VDRL (Venereal Disease Research Laboratory)",
        "RPR (Rapid Plasma Reagin)",
        "TPHA (Treponema pallidum hemagglutination)",
        "FTA-ABS (Fluorescent treponemal antibody absorption)",
        "Rapid treponemal test",
        "Other / Don’t know",
    ],
    "Gonorrhea": [
        "PCR / NAAT (urine or swab)",
        "Culture test (Neisseria gonorrhoeae)",
        "Gram stain (urethral swab)",
        "Other / Don’t know",
    ],
    "Chlamydia": [
        "PCR / NAAT (urine or swab)",
        "Culture test",
        "Rapid antigen test",
        "Other / Don’t know",
    ],
    "Hepatitis A": [
        "HAV IgM antibody (acute infection)",
        "HAV total antibodies (immunity check)",
        "Other / Don’t know",
    ],
    "Hepatitis B": [
        "HBsAg (surface antigen)",
        "Anti-HBs (surface antibody)",
        "Anti-HBc (core antibody)",
        "HBV DNA (viral load PCR)",
        "Other / Don’t know",
    ],
    "Hepatitis C": [
        "Anti-HCV antibody",
        "HCV RNA PCR (viral load)",
        "HCV genotype test",
        "Other / Don’t know",
    ],
    "Genital herpes": [
        "HSV-1/HSV-2 PCR (swab)",
        "Viral culture",
        "HSV IgG/IgM serology",
        "Other / Don’t know",
    ],
    "Human papillomavirus (HPV)": [
        "HPV DNA test (PCR)",
        "Pap smear (cytology)",
        "Visual inspection with acetic acid (VIA)",
        "Other / Don’t know",
    ],
    "Mycoplasma genitalium": [
        "PCR / NAAT (urine or swab)",
        "Antibiotic resistance PCR",
        "Other / Don’t know",
    ],
    "Trichomoniasis": [
        "Wet mount microscopy",
        "PCR / NAAT",
        "Antigen test (rapid test)",
        "Other / Don’t know",
    ],
    "LGV (Lymphogranuloma venereum)": [
        "Chlamydia trachomatis L1–L3 genotyping (PCR)",
        "NAAT with LGV confirmation",
        "Other / Don’t know",
    ],
}

sti_result_options = {
    "HIV": ["Negative / Non-reactive", "Positive / Reactive", "Indeterminate", "Other / Don’t know"],
    "Syphilis": ["Non-reactive", "Reactive", "Inconclusive", "Other / Don’t know"],
    "Gonorrhea": ["Detected", "Not detected", "Inconclusive", "Other / Don’t know"],
    "Chlamydia": ["Detected", "Not detected", "Inconclusive", "Other / Don’t know"],
    "Hepatitis A": ["IgM positive", "IgM negative", "Immune (total Ab+)", "Other / Don’t know"],
    "Hepatitis B": ["HBsAg positive", "HBsAg negative", "Immune (anti-HBs+)", "Other / Don’t know"],
    "Hepatitis C": ["Antibody positive", "Antibody negative", "RNA detected", "RNA not detected", "Other / Don’t know"],
    "Genital herpes": ["HSV detected", "Not detected", "Serology positive", "Serology negative", "Other / Don’t know"],
    "Human papillomavirus (HPV)": ["HPV detected", "HPV not detected", "Abnormal cytology", "Normal cytology", "Other / Don’t know"],
    "Mycoplasma genitalium": ["Detected", "Not detected", "Other / Don’t know"],
    "Trichomoniasis": ["Detected", "Not detected", "Other / Don’t know"],
    "LGV (Lymphogranuloma venereum)": ["LGV detected", "Not detected", "Other / Don’t know"],
}

common_results = ["Negative / Non-reactive", "Positive / Reactive", "Not detected", "Inconclusive", "Other / Don’t know"]