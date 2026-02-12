# -*- coding: utf-8 -*-
"""
ILD Yapısal Radyoloji Raporu Oluşturucu
PACS/RIS uyumlu düz metin rapor formatı
"""

from typing import Dict, List, Optional
from datetime import datetime

from config.findings_taxonomy import (
    DISTRIBUTION_FINDINGS,
    FIBROTIC_FINDINGS,
    NON_FIBROTIC_FINDINGS,
    SPECIFIC_FINDINGS,
    ILA_FINDINGS,
)


# Tüm bulgular tek sözlükte
_ALL_FINDINGS = {}
_ALL_FINDINGS.update(DISTRIBUTION_FINDINGS)
_ALL_FINDINGS.update(FIBROTIC_FINDINGS)
_ALL_FINDINGS.update(NON_FIBROTIC_FINDINGS)
_ALL_FINDINGS.update(SPECIFIC_FINDINGS)


class ReportGenerator:
    """Yapısal radyoloji raporu oluşturur."""

    def generate_full_report(
        self,
        patient_info: Dict,
        clinical_context: Dict,
        selected_findings: List[str],
        diagnostic_result,
        ila_result=None,
    ) -> str:
        """
        Tam yapısal rapor metni oluştur.

        Args:
            patient_info: Hasta bilgileri dict
            clinical_context: Klinik bağlam dict
            selected_findings: Seçilen bulgu key listesi
            diagnostic_result: DiagnosticResult objesi
            ila_result: ILAResult objesi (opsiyonel)

        Returns:
            PACS/RIS'e kopyalanabilir rapor metni
        """
        sections = []

        # --- Başlık ---
        sections.append("=" * 60)
        sections.append("YÜKSEK ÇÖZÜNÜRLÜKLÜ BT - İNTERSTİSYEL AKCİĞER HASTALIKLARI")
        sections.append("YAPISAL RAPOR")
        sections.append("=" * 60)
        sections.append("")

        # --- Klinik Bilgi ---
        sections.append("KLİNİK BİLGİ:")
        sections.append("-" * 40)
        name = patient_info.get("name", "")
        if name:
            sections.append(f"  Hasta: {name}")
        sections.append(f"  Yaş/Cinsiyet: {patient_info.get('age', '')}/{patient_info.get('sex', '')}")
        sections.append(f"  Endikasyon: {clinical_context.get('indication', '')}")
        sections.append(f"  Prezentasyon: {clinical_context.get('presentation', '')}")

        smoking = clinical_context.get("smoking", "Hiç içmemiş")
        pack_years = clinical_context.get("pack_years", 0)
        if smoking != "Hiç içmemiş" and pack_years > 0:
            sections.append(f"  Sigara: {smoking} ({pack_years} paket-yıl)")
        else:
            sections.append(f"  Sigara: {smoking}")

        exposure = clinical_context.get("exposure", "Yok")
        if exposure != "Yok":
            sections.append(f"  Maruziyet: {exposure}")

        ctd = clinical_context.get("ctd", "Yok")
        if ctd != "Yok":
            sections.append(f"  CTD: {ctd}")
        sections.append("")

        # --- BT Bulguları ---
        sections.append("BT BULGULARI:")
        sections.append("-" * 40)

        if not selected_findings:
            sections.append("  İnterstisyel akciğer hastalığı ile uyumlu bulgu saptanmamıştır.")
        else:
            # Bulguları kategorilere göre grupla
            dist_findings = []
            fibrotic_findings = []
            nonfibrotic_findings = []
            specific_findings = []

            for f_key in selected_findings:
                info = _ALL_FINDINGS.get(f_key)
                if not info:
                    continue
                cat = info.get("category", "")
                label = info["label"]
                if cat == "distribution":
                    dist_findings.append(label)
                elif cat == "fibrotic":
                    fibrotic_findings.append(label)
                elif cat == "non_fibrotic":
                    nonfibrotic_findings.append(label)
                elif cat == "specific":
                    specific_findings.append(label)

            if dist_findings:
                sections.append(f"  Dağılım: {', '.join(dist_findings)}")
            if fibrotic_findings:
                sections.append(f"  Fibrotik bulgular: {', '.join(fibrotic_findings)}")
            if nonfibrotic_findings:
                sections.append(f"  Non-fibrotik bulgular: {', '.join(nonfibrotic_findings)}")
            if specific_findings:
                sections.append(f"  Spesifik bulgular: {', '.join(specific_findings)}")
        sections.append("")

        # --- Tanısal Değerlendirme ---
        sections.append("TANISAL DEĞERLENDİRME:")
        sections.append("-" * 40)

        if diagnostic_result and diagnostic_result.primary_pattern:
            primary = diagnostic_result.primary_pattern
            conf = primary.confidence_level

            sections.append(f"  Primer YÇBT paterni: {primary.pattern_name}")
            sections.append(f"  Tanısal güven: %{primary.final_score:.0f} — {conf['label']}")
            sections.append("")

            # Ayırıcı tanı
            top = [
                p for p in diagnostic_result.ranked_patterns[:3]
                if p.final_score > 10 and p.pattern_key != primary.pattern_key
            ]
            if top:
                sections.append("  Ayırıcı tanı:")
                for i, p in enumerate(top, 1):
                    sections.append(f"    {i}. {p.pattern_name} (%{p.final_score:.0f})")
                sections.append("")

            # İlişkili klinik tanılar
            if primary.associated_diagnoses:
                sections.append("  İlişkili klinik tanılar:")
                for diag in primary.associated_diagnoses:
                    sections.append(f"    - {diag}")
                sections.append("")
        else:
            sections.append("  Spesifik bir YÇBT paterni tanımlanamamıştır.")
            sections.append("  Klinik korelasyon ve ileri değerlendirme önerilir.")
            sections.append("")

        # --- ILA Değerlendirmesi ---
        if ila_result and ila_result.ila_present:
            sections.append("ILA DEĞERLENDİRMESİ:")
            sections.append("-" * 40)
            sections.append(f"  Kategori: {ila_result.category_label}")
            sections.append(f"  Risk düzeyi: {ila_result.risk_level}")
            sections.append(f"  Tutulum yaygınlığı: %{ila_result.extent_percent:.0f}")
            sections.append(f"  Fibrotik özellik: {'Var' if ila_result.has_fibrotic_features else 'Yok'}")
            sections.append(f"  Takip: {ila_result.follow_up}")
            sections.append("")

        # --- MDD Önerisi ---
        if diagnostic_result:
            sections.append("MULTİDİSİPLİNER TARTIŞMA (MDD):")
            sections.append("-" * 40)
            if diagnostic_result.mdd_recommended:
                sections.append("  >> MDD ÖNERİLİR")
            else:
                sections.append("  MDD rutin olarak gerekmemektedir.")
            sections.append(f"  Gerekçe: {diagnostic_result.mdd_reason}")
            sections.append("")

        # --- Sonuç ---
        sections.append("SONUÇ:")
        sections.append("-" * 40)
        if diagnostic_result and diagnostic_result.primary_pattern:
            primary = diagnostic_result.primary_pattern
            sections.append(
                f"  YÇBT bulguları {primary.pattern_name} ile uyumludur "
                f"(güven: %{primary.final_score:.0f})."
            )
            if diagnostic_result.mdd_recommended:
                sections.append("  Multidisipliner tartışma (MDD) önerilmektedir.")
        else:
            sections.append("  Spesifik ILD paterni tanımlanamamıştır. Klinik korelasyon önerilir.")

        if ila_result and ila_result.ila_present:
            sections.append(
                f"  ILA: {ila_result.category_label} — "
                f"Risk: {ila_result.risk_level}"
            )

        sections.append("")
        sections.append("=" * 60)
        sections.append(
            f"Rapor tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )
        sections.append(
            "2025 ERS/ATS Kılavuzu uyumlu yapısal raporlama sistemi"
        )
        sections.append(
            "Klinik karar desteği amaçlıdır, kesin tanı yerine geçmez."
        )
        sections.append("=" * 60)

        return "\n".join(sections)
