# -*- coding: utf-8 -*-
"""
ILD BT Bulguları Taksonomisi
2025 ERS/ATS Kılavuzu Uyumlu (Ryerson CJ et al. Eur Respir J 2025)
"""

# =============================================
# DAĞILIM BULGULARI
# =============================================
DISTRIBUTION_FINDINGS = {
    "basal_predominant": {
        "label": "Bazal predominant dağılım",
        "description": "Alt lob ağırlıklı tutulum. UIP paterni için tipiktir.",
        "category": "distribution",
    },
    "peripheral_predominant": {
        "label": "Periferik (subplevral) predominant",
        "description": "Subplevral alanlarda yoğunlaşan dağılım. UIP ve NSIP'te görülür.",
        "category": "distribution",
    },
    "upper_predominant": {
        "label": "Üst lob predominant dağılım",
        "description": "Üst lob ağırlıklı tutulum. HP, sarkoidoz ve PLCH'de tipiktir.",
        "category": "distribution",
    },
    "peribronchovascular": {
        "label": "Peribronovasküler dağılım",
        "description": "Bronkovasküler demet çevresinde tutulum. NSIP ve OP'de görülür.",
        "category": "distribution",
    },
    "diffuse": {
        "label": "Diffüz dağılım",
        "description": "Homojen, yaygın tutulum. DIP, PAP ve diffüz hemoraji düşündürür.",
        "category": "distribution",
    },
    "random": {
        "label": "Rastgele (random) dağılım",
        "description": "Belirli bir anatomik predileksiyon göstermeyen dağılım.",
        "category": "distribution",
    },
    "unilateral": {
        "label": "Unilateral veya asimetrik",
        "description": "Tek taraflı veya belirgin asimetrik tutulum. Atipik bir dağılımdır.",
        "category": "distribution",
    },
}

# =============================================
# FİBROTİK BULGULAR
# =============================================
FIBROTIC_FINDINGS = {
    "honeycombing": {
        "label": "Bal peteği (Honeycombing)",
        "description": "Subplevral kümelenmiş kistik hava boşlukları (3-10 mm). UIP için en spesifik bulgudur.",
        "category": "fibrotic",
    },
    "traction_bronchiectasis": {
        "label": "Traksiyon bronşektazisi",
        "description": "Fibrozise bağlı bronşiyal dilatasyon. İleri evre fibrozis göstergesidir.",
        "category": "fibrotic",
    },
    "traction_bronchiolectasis": {
        "label": "Traksiyon bronşiolektazisi",
        "description": "Periferik hava yollarında fibrozise bağlı dilatasyon.",
        "category": "fibrotic",
    },
    "reticulation": {
        "label": "Retiküler patern",
        "description": "İnterlobüler ve intralobüler septal kalınlaşma oluşturan ağ benzeri patern.",
        "category": "fibrotic",
    },
    "architectural_distortion": {
        "label": "Yapısal distorsiyon",
        "description": "Normal akciğer mimarisinin bozulması. Fibrozis göstergesidir.",
        "category": "fibrotic",
    },
    "volume_loss": {
        "label": "Volüm kaybı",
        "description": "Fibrozise bağlı lober veya segmental volüm azalması.",
        "category": "fibrotic",
    },
    "irregular_interfaces": {
        "label": "İrregüler plevral/mediastinal arayüz",
        "description": "Subplevral fibrozise bağlı düzensiz kontur.",
        "category": "fibrotic",
    },
}

# =============================================
# NON-FİBROTİK BULGULAR
# =============================================
NON_FIBROTIC_FINDINGS = {
    "ground_glass": {
        "label": "Buzlu cam opasitesi (GGO)",
        "description": "Altta yatan yapıları silmeyen artmış dansitede alan. Aktif inflamasyon veya erken fibrozis düşündürür.",
        "category": "non_fibrotic",
    },
    "consolidation": {
        "label": "Konsolidasyon",
        "description": "Hava bronkogramı içerebilen homojen dansite artışı. OP ve enfeksiyon düşündürür.",
        "category": "non_fibrotic",
    },
    "centrilobular_nodules": {
        "label": "Sentrilübüler nodüller",
        "description": "Lobül merkezinde küçük nodüller. HP ve RB-ILD düşündürür.",
        "category": "non_fibrotic",
    },
    "mosaic_attenuation": {
        "label": "Mozaik atenüasyon",
        "description": "Farklı dansite alanlarının bir arada bulunması. Air trapping veya vasküler patoloji düşündürür.",
        "category": "non_fibrotic",
    },
    "air_trapping": {
        "label": "Hava hapsi (Air trapping)",
        "description": "Ekspiratuar kesitlerde lobüler düzeyde hava hapsi. HP ve obliteratif bronşiolit düşündürür.",
        "category": "non_fibrotic",
    },
    "crazy_paving": {
        "label": "Kaldırım taşı paterni (Crazy paving)",
        "description": "GGO zemininde süperpoze retiküler patern. PAP, hemoraji ve enfeksiyon düşündürür.",
        "category": "non_fibrotic",
    },
    "tree_in_bud": {
        "label": "Tomurcuklanan ağaç (Tree-in-bud)",
        "description": "Sentrilübüler dallanan lineer ve nodüler opasiteler. Enfeksiyon ve aspirasyon düşündürür.",
        "category": "non_fibrotic",
    },
    "septal_thickening": {
        "label": "İnterlobüler septal kalınlaşma",
        "description": "Lobüller arası septa kalınlaşması. Lenfanjitik yayılım, ödem ve PAP düşündürür.",
        "category": "non_fibrotic",
    },
}

# =============================================
# SPESİFİK BULGULAR
# =============================================
SPECIFIC_FINDINGS = {
    "cysts": {
        "label": "Kistler",
        "description": "İnce duvarlı hava boşlukları. LIP, PLCH ve LAM düşündürür.",
        "category": "specific",
    },
    "lymphadenopathy": {
        "label": "Mediastinal/hiler lenfadenopati",
        "description": "Büyümüş lenf nodları. Sarkoidoz, enfeksiyon ve malignite düşündürür.",
        "category": "specific",
    },
    "pleural_thickening": {
        "label": "Plevral kalınlaşma",
        "description": "Visseral veya parietal plevral kalınlaşma. Asbest maruziyeti ve CTD-ILD düşündürür.",
        "category": "specific",
    },
    "pleural_effusion": {
        "label": "Plevral efüzyon",
        "description": "Plevral sıvı. CTD-ILD ve kardiyak patoloji düşündürür.",
        "category": "specific",
    },
    "perilobular_pattern": {
        "label": "Perilübüler patern",
        "description": "Sekonder lobül periferinde arkuat opasiteler. OP için tipiktir.",
        "category": "specific",
    },
    "reversed_halo": {
        "label": "Ters halo bulgusu (Atoll sign)",
        "description": "GGO çevresinde konsolidasyon halkası. OP ve sarkoidoz düşündürür.",
        "category": "specific",
    },
    "subpleural_sparing": {
        "label": "Subplevral koruma (sparing)",
        "description": "Subplevral alanın korunması. NSIP için karakteristik bulgudur.",
        "category": "specific",
    },
    "head_cheese_sign": {
        "label": "Head-cheese bulgusu",
        "description": "GGO, normal akciğer ve lobüler air trapping bir arada. HP için tipiktir.",
        "category": "specific",
    },
    "pleuroparenchymal_fibroelastosis": {
        "label": "Plöroparankimal fibroelastozis (PPFE)",
        "description": "Üst lob apikal plevral ve subplevral yoğunlaşma ile volüm kaybı.",
        "category": "specific",
    },
    "esophageal_dilatation": {
        "label": "Özofagus dilatasyonu",
        "description": "Genişlemiş özofagus lümeni. Sistemik skleroz (SSc) düşündürür.",
        "category": "specific",
    },
}

# =============================================
# ILA BULGULARI (Interstitial Lung Abnormalities)
# =============================================
ILA_FINDINGS = {
    "ila_ground_glass": {
        "label": "Buzlu cam opasitesi",
        "description": "Non-dependent buzlu cam alanları.",
    },
    "ila_reticulation": {
        "label": "Retiküler patern",
        "description": "İnce retiküler opasiteler.",
    },
    "ila_traction_bronchiectasis": {
        "label": "Traksiyon bronşektazisi",
        "description": "ILA zemininde traksiyon bronşektazisi — ileri ILA düşündürür.",
    },
    "ila_honeycombing": {
        "label": "Bal peteği",
        "description": "ILA zemininde honeycombing — ileri ILA, ILD'ye progresyon riski yüksek.",
    },
    "ila_nonadipose_atelectasis": {
        "label": "Nonadipöz atelektazi",
        "description": "Yağ dokusu ile ilişkili olmayan subplevral atelektazi.",
    },
    "ila_centrilobular_nodules": {
        "label": "Sentrilübüler nodüller",
        "description": "ILA kapsamında sentrilübüler nodüller.",
    },
}

# =============================================
# ŞİDDET VE YAYGINLIK SEÇENEKLERİ
# =============================================
SEVERITY_OPTIONS = {
    "extent": {
        "label": "Hastalık yaygınlığı (toplam akciğer)",
        "options": ["< %5", "%5-15", "%15-25", "%25-50", "> %50"],
    },
    "progression": {
        "label": "Değişim durumu",
        "options": [
            "İlk tetkik",
            "Stabil (önceki tetkikle karşılaştırıldığında)",
            "Progresif (artmış yaygınlık veya yeni bulgular)",
            "Regresif (azalmış yaygınlık)",
        ],
    },
}

# =============================================
# TÜM BULGU GRUPLARI (Sıralı dict)
# =============================================
ALL_FINDING_GROUPS = {
    "📍 Dağılım Bulguları": DISTRIBUTION_FINDINGS,
    "🔗 Fibrotik Bulgular": FIBROTIC_FINDINGS,
    "☁️ Non-Fibrotik Bulgular": NON_FIBROTIC_FINDINGS,
    "🔬 Spesifik Bulgular": SPECIFIC_FINDINGS,
}
