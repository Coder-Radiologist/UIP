# -*- coding: utf-8 -*-
"""
ILD YÇBT Patern Tanımları ve Skorlama Kriterleri
2022 ATS/ERS/JRS/ALAT + 2025 ERS/ATS Güncellemesi

Her patern:
  - name: Patern adı
  - required_findings: Tanı için gerekli bulgular (en az biri)
  - supportive_findings: Tanıyı destekleyen bulgular
  - against_findings: Tanıya karşı olan bulgular
  - distribution: Tipik dağılım paterni
  - base_score: Temel skor (0-100)
  - associated_diagnoses: İlişkili klinik tanılar
  - clinical_modifiers: Klinik bağlam modifiyerleri
"""

PATTERN_CATEGORIES = {
    # ====================================================
    # UIP (Usual Interstitial Pneumonia)
    # ====================================================
    "uip_definite": {
        "name": "Kesin UIP (Definite UIP)",
        "required_findings": ["honeycombing"],
        "supportive_findings": [
            "traction_bronchiectasis",
            "traction_bronchiolectasis",
            "reticulation",
            "basal_predominant",
            "peripheral_predominant",
            "architectural_distortion",
            "volume_loss",
            "irregular_interfaces",
        ],
        "against_findings": [
            "upper_predominant",
            "peribronchovascular",
            "consolidation",
            "ground_glass",
            "centrilobular_nodules",
            "cysts",
            "mosaic_attenuation",
            "subpleural_sparing",
        ],
        "distribution": ["basal_predominant", "peripheral_predominant"],
        "base_score": 95,
        "associated_diagnoses": [
            "İdiyopatik pulmoner fibrozis (IPF)",
            "CTD-UIP (RA-UIP, SSc-UIP vb.)",
            "Kronik hipersensitivite pnömonisi (fibrotik HP)",
            "Ailesel pulmoner fibrozis",
            "Asbest ilişkili pulmoner fibrozis",
        ],
        "clinical_modifiers": {
            "age_over_60": 5,
            "male": 3,
            "smoking_history": 2,
            "ctd_present": -10,  # CTD varsa IPF olasılığı azalır
            "exposure_present": -5,  # Maruziyet varsa HP düşün
        },
    },

    "uip_probable": {
        "name": "Olası UIP (Probable UIP)",
        "required_findings": ["traction_bronchiectasis", "reticulation"],
        "supportive_findings": [
            "traction_bronchiolectasis",
            "basal_predominant",
            "peripheral_predominant",
            "architectural_distortion",
            "volume_loss",
        ],
        "against_findings": [
            "honeycombing",
            "upper_predominant",
            "peribronchovascular",
            "consolidation",
            "centrilobular_nodules",
            "subpleural_sparing",
        ],
        "distribution": ["basal_predominant", "peripheral_predominant"],
        "base_score": 75,
        "associated_diagnoses": [
            "İdiyopatik pulmoner fibrozis (IPF)",
            "CTD-UIP",
            "Kronik HP (fibrotik)",
        ],
        "clinical_modifiers": {
            "age_over_60": 5,
            "male": 3,
            "smoking_history": 2,
        },
    },

    "uip_indeterminate": {
        "name": "UIP için belirsiz (Indeterminate for UIP)",
        "required_findings": ["reticulation"],
        "supportive_findings": [
            "ground_glass",
            "traction_bronchiectasis",
            "basal_predominant",
        ],
        "against_findings": [
            "honeycombing",
            "centrilobular_nodules",
            "consolidation",
        ],
        "distribution": ["basal_predominant", "peripheral_predominant"],
        "base_score": 45,
        "associated_diagnoses": [
            "İdiyopatik pulmoner fibrozis (IPF)",
            "Fibrotik NSIP",
            "Erken evre UIP",
        ],
        "clinical_modifiers": {
            "age_over_60": 5,
        },
    },

    # ====================================================
    # NSIP (Nonspecific Interstitial Pneumonia)
    # ====================================================
    "nsip": {
        "name": "NSIP (Nonspesifik İnterstisyel Pnömoni)",
        "required_findings": ["ground_glass"],
        "supportive_findings": [
            "reticulation",
            "traction_bronchiectasis",
            "subpleural_sparing",
            "basal_predominant",
            "peribronchovascular",
            "volume_loss",
        ],
        "against_findings": [
            "honeycombing",
            "centrilobular_nodules",
            "air_trapping",
            "upper_predominant",
        ],
        "distribution": ["basal_predominant", "peribronchovascular"],
        "base_score": 70,
        "associated_diagnoses": [
            "İdiyopatik NSIP",
            "CTD-NSIP (SSc, PM/DM, Sjögren)",
            "İlaç ilişkili NSIP",
            "HP (sellüler faz)",
        ],
        "clinical_modifiers": {
            "ctd_present": 15,
            "female": 5,
            "age_under_50": 5,
        },
    },

    # ====================================================
    # Organizing Pneumonia (OP)
    # ====================================================
    "op": {
        "name": "Organize Pnömoni (OP)",
        "required_findings": ["consolidation"],
        "supportive_findings": [
            "ground_glass",
            "peribronchovascular",
            "perilobular_pattern",
            "reversed_halo",
        ],
        "against_findings": [
            "honeycombing",
            "traction_bronchiectasis",
            "reticulation",
            "centrilobular_nodules",
        ],
        "distribution": ["peribronchovascular", "peripheral_predominant"],
        "base_score": 70,
        "associated_diagnoses": [
            "Kriptojenik organize pnömoni (COP)",
            "CTD ilişkili OP",
            "İlaç ilişkili OP",
            "Enfeksiyon sonrası OP",
            "Radyasyon pnömonisi",
        ],
        "clinical_modifiers": {
            "subacute_presentation": 10,
            "ctd_present": 5,
        },
    },

    # ====================================================
    # Hipersensitivite Pnömonisi (HP)
    # ====================================================
    "hp_nonfibrotic": {
        "name": "Non-fibrotik HP (Hipersensitivite Pnömonisi)",
        "required_findings": ["centrilobular_nodules"],
        "supportive_findings": [
            "ground_glass",
            "mosaic_attenuation",
            "air_trapping",
            "head_cheese_sign",
            "upper_predominant",
            "diffuse",
        ],
        "against_findings": [
            "honeycombing",
            "traction_bronchiectasis",
            "peripheral_predominant",
        ],
        "distribution": ["upper_predominant", "diffuse"],
        "base_score": 70,
        "associated_diagnoses": [
            "Kuş besleyici akciğeri",
            "Çiftçi akciğeri",
            "Kimyasal HP",
            "Ev içi küf maruziyeti",
        ],
        "clinical_modifiers": {
            "exposure_present": 20,
            "subacute_presentation": 5,
        },
    },

    "hp_fibrotic": {
        "name": "Fibrotik HP",
        "required_findings": ["traction_bronchiectasis", "centrilobular_nodules"],
        "supportive_findings": [
            "ground_glass",
            "mosaic_attenuation",
            "air_trapping",
            "reticulation",
            "head_cheese_sign",
            "upper_predominant",
        ],
        "against_findings": [
            "peripheral_predominant",
        ],
        "distribution": ["upper_predominant", "diffuse", "random"],
        "base_score": 65,
        "associated_diagnoses": [
            "Kronik HP (fibrotik faz)",
            "Fibrotik HP — UIP-benzeri patern",
        ],
        "clinical_modifiers": {
            "exposure_present": 20,
        },
    },

    # ====================================================
    # Sarkoidoz
    # ====================================================
    "sarcoidosis": {
        "name": "Sarkoidoz",
        "required_findings": ["lymphadenopathy"],
        "supportive_findings": [
            "centrilobular_nodules",
            "upper_predominant",
            "peribronchovascular",
            "ground_glass",
            "consolidation",
            "reticulation",
        ],
        "against_findings": [
            "honeycombing",
            "basal_predominant",
            "tree_in_bud",
        ],
        "distribution": ["upper_predominant", "peribronchovascular"],
        "base_score": 65,
        "associated_diagnoses": [
            "Pulmoner sarkoidoz",
            "Fibrotik sarkoidoz (Evre IV)",
        ],
        "clinical_modifiers": {
            "age_under_50": 5,
        },
    },

    # ====================================================
    # LIP (Lenfositik İnterstisyel Pnömoni)
    # ====================================================
    "lip": {
        "name": "LIP (Lenfositik İnterstisyel Pnömoni)",
        "required_findings": ["cysts"],
        "supportive_findings": [
            "ground_glass",
            "centrilobular_nodules",
            "septal_thickening",
            "diffuse",
        ],
        "against_findings": [
            "honeycombing",
            "traction_bronchiectasis",
        ],
        "distribution": ["diffuse"],
        "base_score": 55,
        "associated_diagnoses": [
            "LIP (Sjögren ilişkili)",
            "LIP (HIV ilişkili)",
            "İdiyopatik LIP",
        ],
        "clinical_modifiers": {
            "ctd_present": 15,
        },
    },

    # ====================================================
    # DIP (Deskuamatif İnterstisyel Pnömoni)
    # ====================================================
    "dip": {
        "name": "DIP (Deskuamatif İnterstisyel Pnömoni)",
        "required_findings": ["ground_glass"],
        "supportive_findings": [
            "basal_predominant",
            "peripheral_predominant",
            "diffuse",
            "cysts",
        ],
        "against_findings": [
            "honeycombing",
            "consolidation",
            "centrilobular_nodules",
            "upper_predominant",
        ],
        "distribution": ["basal_predominant", "diffuse"],
        "base_score": 50,
        "associated_diagnoses": [
            "DIP (sigara ilişkili)",
            "RB-ILD (Respiratuar bronşiyolit-ILD)",
        ],
        "clinical_modifiers": {
            "smoking_history": 20,
        },
    },

    # ====================================================
    # PLCH (Pulmoner Langerhans Hücreli Histiyositoz)
    # ====================================================
    "plch": {
        "name": "PLCH (Pulmoner Langerhans Hücreli Histiyositoz)",
        "required_findings": ["cysts"],
        "supportive_findings": [
            "centrilobular_nodules",
            "upper_predominant",
        ],
        "against_findings": [
            "honeycombing",
            "basal_predominant",
            "ground_glass",
            "consolidation",
        ],
        "distribution": ["upper_predominant"],
        "base_score": 60,
        "associated_diagnoses": [
            "Pulmoner Langerhans hücreli histiyositoz",
        ],
        "clinical_modifiers": {
            "smoking_history": 20,
            "age_under_50": 5,
        },
    },

    # ====================================================
    # PPFE
    # ====================================================
    "ppfe": {
        "name": "PPFE (Plöroparankimal Fibroelastozis)",
        "required_findings": ["pleuroparenchymal_fibroelastosis"],
        "supportive_findings": [
            "upper_predominant",
            "pleural_thickening",
            "volume_loss",
            "architectural_distortion",
        ],
        "against_findings": [
            "ground_glass",
            "consolidation",
            "centrilobular_nodules",
        ],
        "distribution": ["upper_predominant"],
        "base_score": 70,
        "associated_diagnoses": [
            "İdiyopatik PPFE",
            "Post-transplant PPFE",
            "CTD ilişkili PPFE",
        ],
        "clinical_modifiers": {},
    },
}
