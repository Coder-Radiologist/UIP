
import streamlit as st
import sys
import os

# Proje kök dizinini path'e ekle
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

from config.findings_taxonomy import (
    DISTRIBUTION_FINDINGS,
    FIBROTIC_FINDINGS,
    NON_FIBROTIC_FINDINGS,
    SPECIFIC_FINDINGS,
    ILA_FINDINGS,
    SEVERITY_OPTIONS,
    ALL_FINDING_GROUPS,
)
from config.turkish_templates import (
    PAGE_TITLES,
    PATIENT_FORM,
    FINDINGS_UI,
    ILA_UI,
    UI_TEXTS,
)
from config.pattern_definitions import PATTERN_CATEGORIES
from modules.decision_engine import ILDDecisionEngine
from modules.ila_classifier import ILAClassifier
from modules.report_generator import ReportGenerator


# =============================================
# SAYFA YAPIPLANDIRMASI
# =============================================
st.set_page_config(
    page_title="ILD Rapor Sistemi 2025",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS yükle
css_path = os.path.join(ROOT_DIR, "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# =============================================
# SESSION STATE BAŞLATMA
# =============================================
def init_session_state():
    """Session state değişkenlerini başlat."""
    defaults = {
        "current_page": 1,
        # Hasta bilgileri
        "patient_name": "",
        "patient_age": 55,
        "patient_sex": "Erkek",
        "smoking": "Hiç içmemiş",
        "pack_years": 0,
        "exposure": "Yok",
        "exposure_other": "",
        "ctd": "Yok",
        "presentation": "Kronik (>3 ay)",
        "indication": "ILD değerlendirme",
        # BT Bulguları
        "selected_findings": [],
        "extent": "< %5",
        "progression": "İlk tetkik",
        # ILA
        "ila_present": False,
        "ila_subpleural": False,
        "ila_extent": 5,
        "ila_findings": [],
        # Sonuçlar
        "diagnostic_result": None,
        "ila_result": None,
        "report_text": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# =============================================
# SIDEBAR — NAVİGASYON
# =============================================
with st.sidebar:
    st.markdown("## 🫁 ILD Rapor Sistemi")
    st.caption(UI_TEXTS["sidebar_info"])
    st.markdown("---")

    pages = {
        1: "📋 Hasta Bilgileri",
        2: "🔍 BT Bulguları",
        3: "🏥 ILA Tarama",
        4: "📄 Rapor & Karar Desteği",
    }

    for page_num, page_name in pages.items():
        if st.button(
            page_name,
            key=f"nav_{page_num}",
            use_container_width=True,
            type="primary" if st.session_state.current_page == page_num else "secondary",
        ):
            st.session_state.current_page = page_num
            st.rerun()

    st.markdown("---")
    st.caption("v1.0 — 2025 ERS/ATS Uyumlu")
    st.caption("Ryerson CJ et al. Eur Respir J 2025")

    # Yeni rapor butonu
    if st.button("🔄 Yeni Rapor Başlat", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key != "current_page":
                del st.session_state[key]
        st.session_state.current_page = 1
        init_session_state()
        st.rerun()


# =============================================
# SAYFA 1: HASTA BİLGİLERİ
# =============================================
def page_patient_info():
    st.title("📋 " + PAGE_TITLES["page1"])
    st.markdown("Hasta demografik ve klinik bilgilerini giriniz. Bu bilgiler tanısal güven hesaplamasında kullanılacaktır.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Demografik Bilgiler")
        st.session_state.patient_name = st.text_input(
            PATIENT_FORM["name"],
            value=st.session_state.patient_name,
        )
        st.session_state.patient_age = st.number_input(
            PATIENT_FORM["age"],
            min_value=0, max_value=120,
            value=st.session_state.patient_age,
        )
        st.session_state.patient_sex = st.radio(
            PATIENT_FORM["sex"],
            PATIENT_FORM["sex_options"],
            index=PATIENT_FORM["sex_options"].index(st.session_state.patient_sex),
            horizontal=True,
        )

    with col2:
        st.subheader("Klinik Bağlam")
        st.session_state.smoking = st.selectbox(
            PATIENT_FORM["smoking"],
            PATIENT_FORM["smoking_options"],
            index=PATIENT_FORM["smoking_options"].index(st.session_state.smoking),
        )
        if st.session_state.smoking != "Hiç içmemiş":
            st.session_state.pack_years = st.number_input(
                PATIENT_FORM["pack_years"],
                min_value=0, max_value=200,
                value=st.session_state.pack_years,
            )

        st.session_state.exposure = st.selectbox(
            PATIENT_FORM["exposure"],
            PATIENT_FORM["exposure_options"],
            index=PATIENT_FORM["exposure_options"].index(st.session_state.exposure)
            if st.session_state.exposure in PATIENT_FORM["exposure_options"] else 0,
        )
        if st.session_state.exposure == "Diğer (belirtiniz)":
            st.session_state.exposure_other = st.text_input("Maruziyet detayı")

    st.markdown("---")

    col3, col4 = st.columns(2)
    with col3:
        st.session_state.ctd = st.selectbox(
            PATIENT_FORM["ctd"],
            PATIENT_FORM["ctd_options"],
            index=PATIENT_FORM["ctd_options"].index(st.session_state.ctd)
            if st.session_state.ctd in PATIENT_FORM["ctd_options"] else 0,
        )

    with col4:
        st.session_state.presentation = st.selectbox(
            PATIENT_FORM["presentation"],
            PATIENT_FORM["presentation_options"],
            index=PATIENT_FORM["presentation_options"].index(st.session_state.presentation),
        )
        st.session_state.indication = st.selectbox(
            PATIENT_FORM["indication"],
            PATIENT_FORM["indication_options"],
            index=PATIENT_FORM["indication_options"].index(st.session_state.indication)
            if st.session_state.indication in PATIENT_FORM["indication_options"] else 0,
        )

    # İleri butonu
    st.markdown("---")
    if st.button(UI_TEXTS["next_button"], type="primary", use_container_width=True):
        st.session_state.current_page = 2
        st.rerun()


# =============================================
# SAYFA 2: BT BULGULARI
# =============================================
def page_ct_findings():
    st.title("🔍 " + PAGE_TITLES["page2"])
    st.markdown(FINDINGS_UI["instruction"])
    st.markdown("---")

    # Tüm bulgu gruplarını göster
    for group_name, findings_dict in ALL_FINDING_GROUPS.items():
        st.subheader(group_name)
        cols = st.columns(2)
        for i, (key, info) in enumerate(findings_dict.items()):
            with cols[i % 2]:
                checked = key in st.session_state.selected_findings
                if st.checkbox(
                    info["label"],
                    value=checked,
                    key=f"finding_{key}",
                    help=info["description"],
                ):
                    if key not in st.session_state.selected_findings:
                        st.session_state.selected_findings.append(key)
                else:
                    if key in st.session_state.selected_findings:
                        st.session_state.selected_findings.remove(key)

    # Yaygınlık ve değişim
    st.markdown("---")
    st.subheader(FINDINGS_UI["severity_header"])
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.extent = st.select_slider(
            SEVERITY_OPTIONS["extent"]["label"],
            options=SEVERITY_OPTIONS["extent"]["options"],
            value=st.session_state.extent,
        )
    with col2:
        st.session_state.progression = st.selectbox(
            SEVERITY_OPTIONS["progression"]["label"],
            SEVERITY_OPTIONS["progression"]["options"],
            index=SEVERITY_OPTIONS["progression"]["options"].index(st.session_state.progression),
        )

    # Seçilen bulgular özeti
    if st.session_state.selected_findings:
        st.markdown("---")
        st.info(f"**Seçilen bulgu sayısı:** {len(st.session_state.selected_findings)}")

    # Navigasyon
    st.markdown("---")
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button(UI_TEXTS["back_button"], use_container_width=True):
            st.session_state.current_page = 1
            st.rerun()
    with col_nav2:
        if st.button(UI_TEXTS["next_button"], type="primary", use_container_width=True):
            st.session_state.current_page = 3
            st.rerun()


# =============================================
# SAYFA 3: ILA TARAMA
# =============================================
def page_ila_screening():
    st.title("🏥 " + PAGE_TITLES["page3"])
    st.markdown("Akciğer kanseri taraması veya diğer endikasyonlarla çekilen BT'de saptanan ILA bulgularını değerlendiriniz.")
    st.markdown("---")

    st.session_state.ila_present = st.checkbox(
        ILA_UI["ila_present"],
        value=st.session_state.ila_present,
    )

    if st.session_state.ila_present:
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            st.session_state.ila_extent = st.slider(
                ILA_UI["ila_extent"] + " (%)",
                min_value=1, max_value=100,
                value=st.session_state.ila_extent,
            )

            st.session_state.ila_subpleural = st.checkbox(
                "Subplevral dağılım mevcut",
                value=st.session_state.ila_subpleural,
            )

        with col2:
            st.subheader(ILA_UI["ila_findings"])
            for key, info in ILA_FINDINGS.items():
                checked = key in st.session_state.ila_findings
                if st.checkbox(
                    info["label"],
                    value=checked,
                    key=f"ila_{key}",
                    help=info["description"],
                ):
                    if key not in st.session_state.ila_findings:
                        st.session_state.ila_findings.append(key)
                else:
                    if key in st.session_state.ila_findings:
                        st.session_state.ila_findings.remove(key)

        # Anlık ILA sınıflandırma önizlemesi
        if st.session_state.ila_findings:
            classifier = ILAClassifier()
            preview = classifier.classify(
                ila_present=True,
                is_subpleural=st.session_state.ila_subpleural,
                extent_percent=st.session_state.ila_extent,
                selected_ila_findings=st.session_state.ila_findings,
            )
            st.markdown("---")
            risk_color = {"Düşük": "🟢", "Orta": "🟡", "Yüksek": "🔴"}.get(preview.risk_level, "⚪")
            st.success(
                f"**ILA Kategorisi:** {preview.category_label}  \n"
                f"**Risk Düzeyi:** {risk_color} {preview.risk_level}  \n"
                f"**Takip:** {preview.follow_up}"
            )
    else:
        st.info("ILA bulgusu saptanmadıysa bu bölümü atlayabilirsiniz.")

    # Navigasyon
    st.markdown("---")
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button(UI_TEXTS["back_button"], use_container_width=True):
            st.session_state.current_page = 2
            st.rerun()
    with col_nav2:
        if st.button(UI_TEXTS["next_button"] + " (Rapor Oluştur)", type="primary", use_container_width=True):
            # Analiz çalıştır
            _run_analysis()
            st.session_state.current_page = 4
            st.rerun()


# =============================================
# ANALİZ ÇALIŞTIR
# =============================================
def _run_analysis():
    """Karar destek motorunu ve rapor üreticiyi çalıştır."""
    # Klinik bağlam
    clinical_context = {
        "age": st.session_state.patient_age,
        "sex": st.session_state.patient_sex,
        "smoking": st.session_state.smoking,
        "pack_years": st.session_state.pack_years,
        "ctd": st.session_state.ctd,
        "exposure": st.session_state.exposure,
        "presentation": st.session_state.presentation,
        "indication": st.session_state.indication,
    }

    # Karar destek motoru
    engine = ILDDecisionEngine()
    diagnostic_result = engine.analyze(
        selected_findings=st.session_state.selected_findings,
        clinical_context=clinical_context,
    )
    st.session_state.diagnostic_result = diagnostic_result

    # ILA sınıflandırma
    if st.session_state.ila_present:
        classifier = ILAClassifier()
        ila_result = classifier.classify(
            ila_present=True,
            is_subpleural=st.session_state.ila_subpleural,
            extent_percent=st.session_state.ila_extent,
            selected_ila_findings=st.session_state.ila_findings,
        )
        st.session_state.ila_result = ila_result
    else:
        st.session_state.ila_result = None

    # Rapor oluştur
    patient_info = {
        "name": st.session_state.patient_name,
        "age": st.session_state.patient_age,
        "sex": st.session_state.patient_sex,
    }
    generator = ReportGenerator()
    report_text = generator.generate_full_report(
        patient_info=patient_info,
        clinical_context=clinical_context,
        selected_findings=st.session_state.selected_findings,
        diagnostic_result=diagnostic_result,
        ila_result=st.session_state.ila_result,
    )
    st.session_state.report_text = report_text


# =============================================
# SAYFA 4: RAPOR & KARAR DESTEĞİ
# =============================================
def page_report():
    st.title("📄 " + PAGE_TITLES["page4"])

    # Eğer analiz henüz yapılmadıysa çalıştır
    if st.session_state.diagnostic_result is None:
        _run_analysis()

    result = st.session_state.diagnostic_result

    if not result or not result.primary_pattern:
        st.warning(UI_TEXTS["no_findings"])
        if st.button(UI_TEXTS["back_button"]):
            st.session_state.current_page = 2
            st.rerun()
        return

    # ---- TANISAL GÜVEN DÜZEYİ ----
    st.markdown("---")
    st.subheader("🎯 " + UI_TEXTS["confidence_label"])

    primary = result.primary_pattern
    conf_level = primary.confidence_level

    # Renk kodlu güven göstergesi
    color_map = {"green": "confidence-high", "orange": "confidence-medium", "red": "confidence-low"}
    css_class = color_map.get(conf_level["color"], "confidence-medium")
    emoji_map = {"green": "🟢", "orange": "🟡", "red": "🔴"}
    emoji = emoji_map.get(conf_level["color"], "⚪")

    col_conf1, col_conf2 = st.columns([2, 3])
    with col_conf1:
        st.metric(
            label="Primer Patern",
            value=primary.pattern_name.split("(")[0].strip(),
            delta=f"%{primary.final_score:.0f} güven",
        )
    with col_conf2:
        st.markdown(
            f"<div class='{css_class}'>{emoji} {conf_level['label']} — %{primary.final_score:.0f}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"*{conf_level['description']}*")

    # ---- AYIRICI TANI SIRALAMASI ----
    st.markdown("---")
    st.subheader("📊 " + UI_TEXTS["differential"])

    # İlk 5 patern
    top_patterns = [p for p in result.ranked_patterns[:5] if p.final_score > 5]
    for i, pattern in enumerate(top_patterns):
        conf_pct = pattern.final_score
        bar_color = "🟢" if conf_pct >= 90 else ("🟡" if conf_pct >= 51 else "🔴")

        col_a, col_b = st.columns([3, 7])
        with col_a:
            st.markdown(f"**{i+1}. {pattern.pattern_name.split('(')[0].strip()}**")
        with col_b:
            st.progress(min(conf_pct / 100, 1.0))
            st.caption(f"{bar_color} %{conf_pct:.0f} — {pattern.confidence_level['label']}")

    # İlişkili klinik tanılar
    if primary.associated_diagnoses:
        st.markdown("---")
        st.subheader("🏷️ İlişkili Klinik Tanılar")
        for i, diag in enumerate(primary.associated_diagnoses, 1):
            st.markdown(f"  {i}. {diag}")

    # ---- MDD ÖNERİSİ ----
    st.markdown("---")
    st.subheader("👥 " + UI_TEXTS["mdd_title"])

    if result.mdd_recommended:
        st.warning(f"**MDD ÖNERİLİR** — {result.mdd_reason}")
    else:
        st.success(f"**MDD rutin olarak gerekmemektedir** — {result.mdd_reason}")

    # ---- ILA SONUÇLARI ----
    ila = st.session_state.ila_result
    if ila and ila.ila_present:
        st.markdown("---")
        st.subheader("🔬 ILA Değerlendirmesi")
        risk_emoji = {"Düşük": "🟢", "Orta": "🟡", "Yüksek": "🔴"}.get(ila.risk_level, "⚪")
        col_ila1, col_ila2, col_ila3 = st.columns(3)
        with col_ila1:
            st.metric("Kategori", ila.category_label)
        with col_ila2:
            st.metric("Risk Düzeyi", f"{risk_emoji} {ila.risk_level}")
        with col_ila3:
            st.metric("Tutulum", f"%{ila.extent_percent:.0f}")
        st.info(ila.follow_up)

    # ---- RAPOR METNİ ----
    st.markdown("---")
    st.subheader("📝 " + UI_TEXTS["report_title"])
    st.markdown("Aşağıdaki rapor metni PACS/RIS'e kopyalanabilir formattadır:")

    # Rapor kutusu
    st.text_area(
        "Rapor",
        value=st.session_state.report_text,
        height=500,
        label_visibility="collapsed",
    )

    # Kopyala butonu (Streamlit native)
    st.code(st.session_state.report_text, language=None)

    # Navigasyon
    st.markdown("---")
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button(UI_TEXTS["back_button"], use_container_width=True):
            st.session_state.current_page = 3
            st.rerun()
    with col_nav2:
        if st.button("🔄 " + UI_TEXTS["new_report"], type="primary", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key != "current_page":
                    del st.session_state[key]
            st.session_state.current_page = 1
            init_session_state()
            st.rerun()


# =============================================
# SAYFA YÖNLENDİRME
# =============================================
page_map = {
    1: page_patient_info,
    2: page_ct_findings,
    3: page_ila_screening,
    4: page_report,
}

current_page = st.session_state.get("current_page", 1)
page_func = page_map.get(current_page, page_patient_info)
page_func()

# Footer
st.markdown("---")
st.markdown(
    f"<div class='footer-text'>{UI_TEXTS['footer']}</div>",
    unsafe_allow_html=True,
)

