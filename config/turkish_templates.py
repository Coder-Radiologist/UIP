# -*- coding: utf-8 -*-
"""
ILD Rapor Sistemi — Türkçe Arayüz Şablonları
"""

PAGE_TITLES = {
    "page1": "Hasta Bilgileri",
    "page2": "BT Bulguları",
    "page3": "ILA Tarama",
    "page4": "Rapor & Karar Desteği",
}

PATIENT_FORM = {
    "name": "Hasta Adı / Protokol No",
    "age": "Yaş",
    "sex": "Cinsiyet",
    "sex_options": ["Erkek", "Kadın"],
    "smoking": "Sigara öyküsü",
    "smoking_options": [
        "Hiç içmemiş",
        "Aktif içici",
        "Bırakmış (ex-smoker)",
    ],
    "pack_years": "Paket-yıl",
    "exposure": "Çevresel / Mesleki maruziyet",
    "exposure_options": [
        "Yok",
        "Asbest",
        "Silika",
        "Kuş antijeni (güvercin, muhabbet kuşu vb.)",
        "Küf / Nem",
        "Metal tozu",
        "Tahıl / Saman tozu",
        "İlaç ilişkili (amiodaron, metotreksat, nitrofurantoin vb.)",
        "Radyoterapi",
        "Diğer (belirtiniz)",
    ],
    "ctd": "Bağ dokusu hastalığı (CTD)",
    "ctd_options": [
        "Yok",
        "Romatoid artrit (RA)",
        "Sistemik skleroz (SSc)",
        "Sjögren sendromu",
        "Polimiyozit / Dermatomiyozit",
        "Sistemik lupus eritematozus (SLE)",
        "Mikst bağ dokusu hastalığı (MCTD)",
        "ANCA ilişkili vaskülit",
        "Ankilozan spondilit",
        "Sınıflandırılamamış CTD (UCTD / IPAF)",
        "Diğer",
    ],
    "presentation": "Klinik prezentasyon",
    "presentation_options": [
        "Kronik (>3 ay)",
        "Subakut (1-3 ay)",
        "Akut (<1 ay)",
        "Asemptomatik (insidental bulgu)",
    ],
    "indication": "BT endikasyonu",
    "indication_options": [
        "ILD değerlendirme",
        "Dispne araştırma",
        "Akciğer kanseri taraması",
        "CTD akciğer tutulumu",
        "İlaç toksisitesi",
        "Mesleki hastalık",
        "Takip BT",
        "Alevlenme değerlendirmesi",
        "Transplantasyon öncesi değerlendirme",
        "Diğer",
    ],
}

FINDINGS_UI = {
    "instruction": "YÇBT'de saptanan bulguları seçiniz. Her bulgunun yanında kısa açıklaması yer almaktadır.",
    "severity_header": "Yaygınlık ve Değişim Değerlendirmesi",
}

ILA_UI = {
    "ila_present": "İnterstisyel Akciğer Anormallikleri (ILA) saptandı",
    "ila_extent": "ILA tutulum yaygınlığı",
    "ila_findings": "ILA Bulguları",
}

UI_TEXTS = {
    "sidebar_info": "2025 ERS/ATS kılavuzuna uyumlu interstisyel akciğer hastalığı yapısal raporlama ve karar destek sistemi.",
    "next_button": "İleri ➡️",
    "back_button": "⬅️ Geri",
    "no_findings": "Henüz BT bulgusu seçilmemiştir. Lütfen BT Bulguları sayfasına dönerek en az bir bulgu seçiniz.",
    "confidence_label": "Tanısal Güven Düzeyi",
    "differential": "Ayırıcı Tanı Sıralaması",
    "mdd_title": "Multidisipliner Tartışma (MDD) Önerisi",
    "report_title": "Yapısal Radyoloji Raporu",
    "new_report": "Yeni Rapor Başlat",
    "footer": "ILD Rapor Sistemi v1.0 — 2025 ERS/ATS Kılavuzu Uyumlu | Ryerson CJ et al. Eur Respir J 2025 | Klinik karar desteği amaçlıdır, kesin tanı yerine geçmez.",
}
