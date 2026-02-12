# -*- coding: utf-8 -*-
"""
ILD YÇBT Patern Tanımları ve Skorlama Kriterleri
2025 ERS/ATS Güncellemesi (Ryerson CJ et al. Eur Respir J 2025;66(6):2500158)
+ 2025 ATS ILA Klinik Bildirisi (Podolanczuk AJ et al. Am J Respir Crit Care Med 2025;211:1132-1155)

2025 Nomenklatur Değişiklikleri:
  - DIP → AMP (Alveoler Makrofaj Pnömonisi)
  - HP (patern olarak) → BIP (Bronşiyolosentrik İnterstisyel Pnömoni)
    * HP yalnızca multidisipliner tanı olarak kalır
  - AIP → DAD (Diffüz Alveoler Hasar)

2025 Sınıflama Yapısı:
  İnterstisyel Bozukluklar:
    - Fibrotik: UIP, Fibrotik NSIP, Fibrotik BIP
    - Nonfibrotik: Nonfibrotik NSIP, Nonfibrotik BIP
  Alveoler Dolum Bozuklukları:
    - OP, RB-ILD, AMP (eski DIP)
    - Nadir: AEP, CEP, LP, PAP

Her patern:
  - name: Patern adı
  - required_findings: Tanı için gerekli bulgular (en az biri)
  - supportive_findings: Tanıyı destekleyen bulgular
  - against_findings: Tanıya karşı olan bulgular
  - distribution: Tipik dağılım paterni
  - base_score: Temel skor (0-100)
  - associated_diagnoses: İlişkili klinik tanılar
  - clinical_modifiers: Klinik bağlam modifiyerleri
  - category_2025: 2025 sınıflama kategorisi
"""

PATTERN_CATEGORIES = {
    # ====================================================
    # İNTERSTİSYEL BOZUKLUKLAR — FİBROTİK
    # ====================================================

    # ---- UIP (Usual Interstitial Pneumonia) ----
    "uip_definite": {
        "name": "Kesin UIP (Definite UIP)",
        "category_2025": "İnterstisyel — Fibrotik",
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
            "Kronik BIP — UIP-benzeri patern (eski: fibrotik HP)",
            "Ailesel pulmoner fibrozis",
            "Asbest ilişkili pulmoner fibrozis",
        ],
        "clinical_modifiers": {
            "age_over_60": 5,
            "male": 3,
            "smoking_history": 2,
            "ctd_present": -10,
            "exposure_present": -5,
        },
    },

    "uip_probable": {
        "name": "Olası UIP (Probable UIP)",
        "category_2025": "İnterstisyel — Fibrotik",
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
            "Kronik BIP — UIP-benzeri patern (eski: fibrotik HP)",
        ],
        "clinical_modifiers": {
            "age_over_60": 5,
            "male": 3,
            "smoking_history": 2,
        },
    },

    "uip_indeterminate": {
        "name": "UIP için belirsiz (Indeterminate for UIP)",
        "category_2025": "İnterstisyel — Fibrotik",
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

    # ---- NSIP — Fibrotik ----
    "nsip_fibrotic": {
        "name": "Fibrotik NSIP",
        "category_2025": "İnterstisyel — Fibrotik",
        "required_findings": ["ground_glass", "reticulation"],
        "supportive_findings": [
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
            "İdiyopatik fibrotik NSIP",
            "CTD-NSIP (SSc, PM/DM, Sjögren, SLE)",
            "İlaç ilişkili fibrotik NSIP",
            "Fibrotik BIP — NSIP paterni (eski: fibrotik HP-NSIP overlap)",
        ],
        "clinical_modifiers": {
            "ctd_present": 15,
            "female": 5,
            "age_under_50": 5,
        },
    },

    # ====================================================
    # İNTERSTİSYEL BOZUKLUKLAR — NONFİBROTİK
    # ====================================================

    # ---- NSIP — Nonfibrotik (Sellüler) ----
    "nsip_nonfibrotic": {
        "name": "Nonfibrotik NSIP (Sellüler NSIP)",
        "category_2025": "İnterstisyel — Nonfibrotik",
        "required_findings": ["ground_glass"],
        "supportive_findings": [
            "subpleural_sparing",
            "basal_predominant",
            "peribronchovascular",
        ],
        "against_findings": [
            "honeycombing",
            "traction_bronchiectasis",
            "reticulation",
            "centrilobular_nodules",
            "air_trapping",
            "upper_predominant",
        ],
        "distribution": ["basal_predominant", "peribronchovascular"],
        "base_score": 65,
        "associated_diagnoses": [
            "İdiyopatik sellüler NSIP",
            "CTD-NSIP (SSc, PM/DM, Sjögren)",
            "İlaç ilişkili NSIP",
        ],
        "clinical_modifiers": {
            "ctd_present": 15,
            "female": 5,
            "age_under_50": 5,
        },
    },

    # ---- BIP — Nonfibrotik (eski: Nonfibrotik HP) ----
    # 2025: HP yerine patern olarak BIP kullanılır
    # HP yalnızca multidisipliner tanı olarak kalır
    #
    # BIP tanısı iki yoldan tetiklenebilir:
    #   1. Doğrudan: centrilobular_nodules veya head_cheese_sign seçimi
    #   2. Elementer çıkarım: Üst lob + GGO + air trapping gibi
    #      bireysel bulguların birlikteliği BIP'i düşündürür
    #
    # DİKKAT: tree_in_bud eşliği → enfeksiyon düşündürür, BIP'e karşı
    "bip_nonfibrotic": {
        "name": "Nonfibrotik BIP (eski: Nonfibrotik HP)",
        "category_2025": "İnterstisyel — Nonfibrotik",
        "required_findings": ["centrilobular_nodules"],
        "alternative_required_sets": [
            # Üç-dansite paterni (headcheese eşdeğeri, etiket bilinmeden)
            # GGO + air trapping + mozaik = hava yolu merkezli hastalık
            ["ground_glass", "air_trapping", "mosaic_attenuation"],
            # Üst lob + GGO + hava hapsi → hava yolu tutulumu
            ["ground_glass", "air_trapping", "upper_predominant"],
            # Üst lob + GGO + mozaik → BIP düşündürür
            ["ground_glass", "mosaic_attenuation", "upper_predominant"],
        ],
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
            "tree_in_bud",
            "centrilobular_nodules_solid",
        ],
        "distribution": ["upper_predominant", "diffuse"],
        "base_score": 70,
        "associated_diagnoses": [
            "Hipersensitivite pnömonisi (MDD tanısı)",
            "CTD-ILD — BIP paterni",
            "Aspirasyon ilişkili BIP",
            "İlaç ilişkili BIP",
        ],
        "clinical_modifiers": {
            "exposure_present": 20,
            "subacute_presentation": 5,
        },
    },

    # ---- BIP — Fibrotik (eski: Fibrotik HP) ----
    #
    # Fibrotik BIP tetikleme yolları:
    #   1. Doğrudan: traksiyon + sentrilobüler nodüller
    #   2. Elementer: Üst lob fibrozis (traksiyon/honeycombing/retikülasyon)
    #      + hava yolu belirteci (air trapping/mozaik) → kronik fibrotik BIP
    #      Bu, eski "kronik fibrotik HP" senaryolarını yakalar
    "bip_fibrotic": {
        "name": "Fibrotik BIP (eski: Fibrotik HP)",
        "category_2025": "İnterstisyel — Fibrotik",
        "required_findings": ["traction_bronchiectasis", "centrilobular_nodules"],
        "alternative_required_sets": [
            # Üst lob fibrozis + hava yolu → fibrotik BIP
            # Senaryo: üst lob + retikülasyon + traksiyon + air trapping
            ["traction_bronchiectasis", "upper_predominant", "air_trapping"],
            ["traction_bronchiectasis", "upper_predominant", "mosaic_attenuation"],
            # İleri fibrotik BIP (honeycombing ile)
            ["honeycombing", "upper_predominant", "air_trapping"],
            ["honeycombing", "upper_predominant", "mosaic_attenuation"],
            # Retikülasyon + traksiyon + üst lob + hava yolu
            ["reticulation", "traction_bronchiectasis", "upper_predominant", "air_trapping"],
            ["reticulation", "traction_bronchiectasis", "upper_predominant", "mosaic_attenuation"],
        ],
        "supportive_findings": [
            "ground_glass",
            "mosaic_attenuation",
            "air_trapping",
            "reticulation",
            "head_cheese_sign",
            "upper_predominant",
            "honeycombing",
        ],
        "against_findings": [
            "peripheral_predominant",
            "tree_in_bud",
            "centrilobular_nodules_solid",
        ],
        "distribution": ["upper_predominant", "diffuse", "random"],
        "base_score": 65,
        "associated_diagnoses": [
            "Kronik hipersensitivite pnömonisi — fibrotik (MDD tanısı)",
            "Fibrotik BIP — UIP-benzeri patern",
            "CTD-ILD — fibrotik BIP paterni",
        ],
        "clinical_modifiers": {
            "exposure_present": 20,
        },
    },

    # ====================================================
    # ALVEOLER DOLUM BOZUKLUKLARI
    # ====================================================

    # ---- OP (Organize Pnömoni) ----
    "op": {
        "name": "Organize Pnömoni (OP)",
        "category_2025": "Alveoler Dolum Bozukluğu",
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

    # ---- AMP (eski: DIP) ----
    # 2025: DIP yerine AMP kullanılır
    "amp": {
        "name": "AMP (Alveoler Makrofaj Pnömonisi, eski: DIP)",
        "category_2025": "Alveoler Dolum Bozukluğu",
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
            "AMP — sigara ilişkili (eski: DIP)",
            "RB-ILD (Respiratuar bronşiyolit-ILD)",
            "CTD ilişkili AMP",
            "Mesleki maruziyet ilişkili AMP",
            "Sürfaktan metabolizma bozuklukları",
        ],
        "clinical_modifiers": {
            "smoking_history": 20,
        },
    },

    # ---- DAD (eski: AIP) ----
    # 2025: AIP yerine DAD kullanılır
    "dad": {
        "name": "DAD (Diffüz Alveoler Hasar, eski: AIP)",
        "category_2025": "Alveoler Dolum Bozukluğu",
        "required_findings": ["ground_glass", "consolidation"],
        "supportive_findings": [
            "diffuse",
            "septal_thickening",
        ],
        "against_findings": [
            "honeycombing",
            "centrilobular_nodules",
            "upper_predominant",
            "cysts",
        ],
        "distribution": ["diffuse"],
        "base_score": 60,
        "associated_diagnoses": [
            "İdiyopatik DAD (eski: AIP)",
            "ILD akut alevlenmesi (AE-ILD)",
            "İlaç ilişkili DAD",
            "Enfeksiyon ilişkili DAD",
        ],
        "clinical_modifiers": {
            "acute_presentation": 20,
        },
    },

    # ====================================================
    # DİĞER İNTERSTİSYEL PATERNLER
    # ====================================================

    # ---- Sarkoidoz ----
    "sarcoidosis": {
        "name": "Sarkoidoz",
        "category_2025": "Diğer İnterstisyel Patern",
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

    # ---- LIP ----
    "lip": {
        "name": "LIP (Lenfositik İnterstisyel Pnömoni)",
        "category_2025": "Diğer İnterstisyel Patern",
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

    # ---- PLCH ----
    "plch": {
        "name": "PLCH (Pulmoner Langerhans Hücreli Histiyositoz)",
        "category_2025": "Diğer İnterstisyel Patern",
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

    # ---- PPFE ----
    "ppfe": {
        "name": "PPFE (Plöroparankimal Fibroelastozis)",
        "category_2025": "Diğer İnterstisyel Patern",
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


# ====================================================
# 2025 NOMENKLATUR UYUMLULUK HARİTASI
# ====================================================
# Eski terimlerden yenilerine eşleme (geriye uyumluluk için)
NOMENCLATURE_2025_MAP = {
    # Eski anahtar → Yeni anahtar
    "dip": "amp",
    "hp_nonfibrotic": "bip_nonfibrotic",
    "hp_fibrotic": "bip_fibrotic",
    "aip": "dad",
    # NSIP artık fibrotik/nonfibrotik olarak ayrılır
    "nsip": "nsip_fibrotic",  # Varsayılan olarak fibrotik NSIP'e yönlendirilir
}

# Eski terimden yeni terime görüntüleme adı eşlemesi
DISPLAY_NAME_MAP = {
    "DIP": "AMP (Alveoler Makrofaj Pnömonisi)",
    "Deskuamatif İnterstisyel Pnömoni": "AMP (Alveoler Makrofaj Pnömonisi)",
    "Non-fibrotik HP": "Nonfibrotik BIP (Bronşiyolosentrik İnterstisyel Pnömoni)",
    "Fibrotik HP": "Fibrotik BIP (Bronşiyolosentrik İnterstisyel Pnömoni)",
    "Hipersensitivite Pnömonisi": "BIP (patern) / HP (MDD tanısı)",
    "AIP": "DAD (Diffüz Alveoler Hasar)",
    "Akut İnterstisyel Pnömoni": "DAD (Diffüz Alveoler Hasar)",
}

# ====================================================
# BULGU ÇIKARIM HARİTASI (Finding Implications)
# ====================================================
# Kompozit bulgular, bileşenlerini otomatik olarak içerir.
# Bu sayede head-cheese seçildiğinde sentrilobüler nodüller
# otomatik olarak değerlendirmeye dahil olur.
FINDING_IMPLICATIONS = {
    # Head-cheese sign = GGO + normal akciğer + lobüler air trapping + sentrilobüler komponent
    "head_cheese_sign": [
        "centrilobular_nodules",
        "mosaic_attenuation",
        "air_trapping",
    ],
    # Honeycombing ileri evre fibrozis — retiküler patern ve distorsiyon içerir
    "honeycombing": [
        "reticulation",
        "architectural_distortion",
    ],
    # Crazy paving = GGO + süperpoze retiküler patern
    "crazy_paving": [
        "ground_glass",
        "septal_thickening",
    ],
    # Reversed halo → konsolidasyon + GGO komponentleri
    "reversed_halo": [
        "consolidation",
        "ground_glass",
    ],
}


# ====================================================
# BULGU BİRLİKTE-GÖRÜLME KURALLARI (Co-occurrence Rules)
# ====================================================
# Belirli bulguların birlikteliği, bazı paternlere ek ceza
# veya bonus uygular. Bu, klinik bağlamı daha iyi yansıtır.
#
# Örnek: sentrilobüler nodüller + tree-in-bud = enfeksiyon
# Bu durumda BIP büyük ceza almalı çünkü HP/BIP'te
# tree-in-bud beklenmez; nodüller solid/enfektif karakter taşır.
COOCCURRENCE_RULES = [
    {
        "name": "Enfektif sentrilobüler patern",
        "trigger_findings": ["centrilobular_nodules", "tree_in_bud"],
        "description": "Tree-in-bud eşlikli sentrilobüler nodüller enfeksiyonu "
                        "düşündürür, HP/BIP ile uyumsuz.",
        "pattern_modifiers": {
            "bip_nonfibrotic": -20,
            "bip_fibrotic": -20,
        },
    },
    {
        "name": "Solid nodül + enfeksiyon",
        "trigger_findings": ["centrilobular_nodules_solid", "tree_in_bud"],
        "description": "Solid sentrilobüler nodüller ve tree-in-bud: "
                        "yüksek olasılıkla enfeksiyon.",
        "pattern_modifiers": {
            "bip_nonfibrotic": -25,
            "bip_fibrotic": -25,
        },
    },
    {
        "name": "Solid nodül ↔ GGO nodül çatışması",
        "trigger_findings": ["centrilobular_nodules", "centrilobular_nodules_solid"],
        "description": "Hem buzlu cam hem solid sentrilobüler nodüller seçilmiş. "
                        "Mikst patern: enfeksiyon + BIP süperpoze olabilir; MDD önerilir.",
        "pattern_modifiers": {
            "bip_nonfibrotic": -10,
            "bip_fibrotic": -10,
        },
    },
    {
        "name": "Subplevral koruma + bazal GGO → NSIP güçlendirme",
        "trigger_findings": ["subpleural_sparing", "ground_glass", "basal_predominant"],
        "description": "Subplevral koruma ile bazal GGO birlikteliği "
                        "NSIP'i güçlü şekilde destekler.",
        "pattern_modifiers": {
            "nsip_fibrotic": 10,
            "nsip_nonfibrotic": 10,
        },
    },
]


# 2025 Sınıflama kategorileri
CLASSIFICATION_2025 = {
    "interstisyel_fibrotik": {
        "label": "İnterstisyel Bozukluklar — Fibrotik",
        "patterns": ["uip_definite", "uip_probable", "uip_indeterminate",
                     "nsip_fibrotic", "bip_fibrotic"],
    },
    "interstisyel_nonfibrotik": {
        "label": "İnterstisyel Bozukluklar — Nonfibrotik",
        "patterns": ["nsip_nonfibrotic", "bip_nonfibrotic"],
    },
    "alveoler_dolum": {
        "label": "Alveoler Dolum Bozuklukları",
        "patterns": ["op", "amp", "dad"],
    },
    "diger": {
        "label": "Diğer İnterstisyel Paternler",
        "patterns": ["sarcoidosis", "lip", "plch", "ppfe"],
    },
}
