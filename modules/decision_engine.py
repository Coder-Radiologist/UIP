# -*- coding: utf-8 -*-
"""
ILD Karar Destek Motoru
2025 ERS/ATS Kılavuzu Uyumlu Patern Tanıma ve Güven Skoru Hesaplama
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from config.pattern_definitions import PATTERN_CATEGORIES


@dataclass
class PatternResult:
    """Tek bir patern için analiz sonucu."""
    pattern_key: str
    pattern_name: str
    base_score: float
    finding_score: float
    distribution_score: float
    clinical_modifier_score: float
    penalty_score: float
    final_score: float
    matched_required: List[str] = field(default_factory=list)
    matched_supportive: List[str] = field(default_factory=list)
    matched_against: List[str] = field(default_factory=list)
    associated_diagnoses: List[str] = field(default_factory=list)

    @property
    def confidence_level(self) -> Dict[str, str]:
        """Güven düzeyini renk kodu ile döndür."""
        if self.final_score >= 90:
            return {
                "label": "Yüksek Güven — Tipik Patern",
                "color": "green",
                "description": "BT bulguları bu patern için yüksek güvenle uyumludur. Uygun klinik bağlamda tek başına tanısal olabilir.",
            }
        elif self.final_score >= 70:
            return {
                "label": "Orta-Yüksek Güven — Olası Patern",
                "color": "green",
                "description": "BT bulguları bu paterni kuvvetle düşündürmektedir. Klinik korelasyon önerilir.",
            }
        elif self.final_score >= 51:
            return {
                "label": "Orta Güven — Uyumlu Patern",
                "color": "orange",
                "description": "BT bulguları bu paternle uyumlu olmakla birlikte ayırıcı tanılar mevcuttur. MDD önerilir.",
            }
        elif self.final_score >= 30:
            return {
                "label": "Düşük-Orta Güven — Belirsiz",
                "color": "orange",
                "description": "BT bulguları birden fazla paternle örtüşmektedir. Biyopsi veya ileri tetkik gerekebilir.",
            }
        else:
            return {
                "label": "Düşük Güven — Alternatif Tanı",
                "color": "red",
                "description": "BT bulguları bu patern için yeterli değildir. Alternatif tanılar değerlendirilmelidir.",
            }


@dataclass
class DiagnosticResult:
    """Tüm analiz sonucu."""
    primary_pattern: Optional[PatternResult]
    ranked_patterns: List[PatternResult]
    mdd_recommended: bool
    mdd_reason: str
    selected_findings: List[str] = field(default_factory=list)


class ILDDecisionEngine:
    """
    ILD YÇBT patern analiz motoru.
    Seçilen BT bulgularını ve klinik bağlamı değerlendirerek
    en olası YÇBT paternini ve güven skorunu hesaplar.
    """

    def __init__(self):
        self.patterns = PATTERN_CATEGORIES

    def analyze(
        self,
        selected_findings: List[str],
        clinical_context: Dict,
    ) -> DiagnosticResult:
        """
        Ana analiz fonksiyonu.

        Args:
            selected_findings: Seçilen BT bulgu key listesi
            clinical_context: Klinik bağlam dict'i

        Returns:
            DiagnosticResult objesi
        """
        if not selected_findings:
            return DiagnosticResult(
                primary_pattern=None,
                ranked_patterns=[],
                mdd_recommended=False,
                mdd_reason="Bulgu seçilmediği için değerlendirme yapılamadı.",
                selected_findings=[],
            )

        results = []
        for pattern_key, pattern_def in self.patterns.items():
            result = self._score_pattern(
                pattern_key, pattern_def, selected_findings, clinical_context
            )
            results.append(result)

        # Skora göre sırala
        results.sort(key=lambda x: x.final_score, reverse=True)

        primary = results[0] if results and results[0].final_score > 0 else None

        # MDD kararı
        mdd_recommended, mdd_reason = self._evaluate_mdd(primary, results)

        return DiagnosticResult(
            primary_pattern=primary,
            ranked_patterns=results,
            mdd_recommended=mdd_recommended,
            mdd_reason=mdd_reason,
            selected_findings=selected_findings,
        )

    def _score_pattern(
        self,
        pattern_key: str,
        pattern_def: Dict,
        selected_findings: List[str],
        clinical_context: Dict,
    ) -> PatternResult:
        """Tek bir patern için skor hesapla."""

        required = pattern_def.get("required_findings", [])
        supportive = pattern_def.get("supportive_findings", [])
        against = pattern_def.get("against_findings", [])
        distribution = pattern_def.get("distribution", [])
        base_score = pattern_def.get("base_score", 50)
        modifiers = pattern_def.get("clinical_modifiers", {})

        # --- Required findings ---
        matched_required = [f for f in required if f in selected_findings]
        if not matched_required:
            # Gerekli bulgu yoksa skor çok düşük
            return PatternResult(
                pattern_key=pattern_key,
                pattern_name=pattern_def["name"],
                base_score=base_score,
                finding_score=0,
                distribution_score=0,
                clinical_modifier_score=0,
                penalty_score=0,
                final_score=0,
                matched_required=[],
                matched_supportive=[],
                matched_against=[],
                associated_diagnoses=pattern_def.get("associated_diagnoses", []),
            )

        # Required bulgu skoru: en az biri varsa baz skorun %60'ı
        # Birden fazla required varsa ve hepsi seçildiyse tam baz skor
        req_ratio = len(matched_required) / max(len(required), 1)
        finding_score = base_score * (0.6 + 0.4 * req_ratio)

        # --- Supportive findings ---
        matched_supportive = [f for f in supportive if f in selected_findings]
        support_bonus = min(len(matched_supportive) * 3, 15)  # Max +15
        finding_score += support_bonus

        # --- Distribution match ---
        matched_dist = [f for f in distribution if f in selected_findings]
        distribution_score = 5 if matched_dist else 0
        finding_score += distribution_score

        # --- Against findings penalty ---
        matched_against = [f for f in against if f in selected_findings]
        penalty = len(matched_against) * 8  # Her karşıt bulgu -8
        finding_score -= penalty

        # --- Clinical modifiers ---
        clinical_mod = 0
        age = clinical_context.get("age", 55)
        sex = clinical_context.get("sex", "Erkek")
        smoking = clinical_context.get("smoking", "Hiç içmemiş")
        ctd = clinical_context.get("ctd", "Yok")
        exposure = clinical_context.get("exposure", "Yok")
        presentation = clinical_context.get("presentation", "Kronik (>3 ay)")

        if "age_over_60" in modifiers and age > 60:
            clinical_mod += modifiers["age_over_60"]
        if "age_under_50" in modifiers and age < 50:
            clinical_mod += modifiers["age_under_50"]
        if "male" in modifiers and sex == "Erkek":
            clinical_mod += modifiers["male"]
        if "female" in modifiers and sex == "Kadın":
            clinical_mod += modifiers["female"]
        if "smoking_history" in modifiers and smoking != "Hiç içmemiş":
            clinical_mod += modifiers["smoking_history"]
        if "ctd_present" in modifiers and ctd != "Yok":
            clinical_mod += modifiers["ctd_present"]
        if "exposure_present" in modifiers and exposure != "Yok":
            clinical_mod += modifiers["exposure_present"]
        if "subacute_presentation" in modifiers and "Subakut" in presentation:
            clinical_mod += modifiers["subacute_presentation"]

        final_score = max(0, min(100, finding_score + clinical_mod))

        return PatternResult(
            pattern_key=pattern_key,
            pattern_name=pattern_def["name"],
            base_score=base_score,
            finding_score=finding_score,
            distribution_score=distribution_score,
            clinical_modifier_score=clinical_mod,
            penalty_score=penalty,
            final_score=final_score,
            matched_required=matched_required,
            matched_supportive=matched_supportive,
            matched_against=matched_against,
            associated_diagnoses=pattern_def.get("associated_diagnoses", []),
        )

    def _evaluate_mdd(
        self,
        primary: Optional[PatternResult],
        ranked: List[PatternResult],
    ) -> tuple:
        """MDD gereksinimi değerlendir."""
        if primary is None:
            return False, "Yeterli bulgu seçilmediği için değerlendirme yapılamadı."

        # Kesin UIP ve yüksek güven → MDD gerekmez
        if primary.pattern_key == "uip_definite" and primary.final_score >= 90:
            return False, (
                "Kesin UIP paterni yüksek güvenle saptanmıştır. "
                "2025 ERS/ATS kılavuzuna göre, uygun klinik bağlamda "
                "kesin UIP paterni IPF tanısı için yeterlidir."
            )

        # İlk iki patern arası fark çok az → MDD önerilir
        if len(ranked) >= 2:
            diff = ranked[0].final_score - ranked[1].final_score
            if diff < 15 and ranked[1].final_score > 20:
                return True, (
                    f"İlk iki patern arasındaki skor farkı düşüktür "
                    f"({ranked[0].pattern_name}: %{ranked[0].final_score:.0f} vs "
                    f"{ranked[1].pattern_name}: %{ranked[1].final_score:.0f}). "
                    f"Ayırıcı tanı için MDD önerilir."
                )

        # Düşük-orta güven → MDD önerilir
        if primary.final_score < 70:
            return True, (
                f"Tanısal güven düzeyi orta-düşüktür (%{primary.final_score:.0f}). "
                "Kesin tanı için MDD, serolojik tetkikler ve/veya biyopsi değerlendirilmelidir."
            )

        # Karşıt bulgu varsa → MDD önerilir
        if len(primary.matched_against) > 0:
            return True, (
                f"Primer paternle uyumsuz bulgu(lar) mevcuttur: "
                f"{', '.join(primary.matched_against)}. "
                "Atipik özellikler nedeniyle MDD önerilir."
            )

        # Olası UIP → MDD hâlâ faydalı olabilir
        if primary.pattern_key == "uip_probable":
            return True, (
                "Olası UIP paterni saptanmıştır. 2025 ERS/ATS kılavuzuna göre, "
                "olası UIP durumunda IPF tanısı konulabilir; ancak belirsiz olgularda "
                "MDD tanısal güveni artırabilir."
            )

        return False, (
            f"{primary.pattern_name} paterni yeterli güvenle saptanmıştır (%{primary.final_score:.0f}). "
            "Rutin MDD gerekmemekle birlikte, klinik şüphe durumunda değerlendirilebilir."
        )
