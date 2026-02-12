# -*- coding: utf-8 -*-
"""
ILD Karar Destek Motoru
2025 ERS/ATS Güncellemesi Uyumlu Patern Tanıma ve Güven Skoru Hesaplama
(Ryerson CJ et al. Eur Respir J 2025;66(6):2500158)

2025 Nomenklatur: DIP→AMP, HP(patern)→BIP, AIP→DAD
NSIP: Fibrotik/Nonfibrotik ayrımı
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from config.pattern_definitions import (
    PATTERN_CATEGORIES,
    NOMENCLATURE_2025_MAP,
    FINDING_IMPLICATIONS,
    COOCCURRENCE_RULES,
)


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

    2025 Nomenklatur uyumlu: DIP→AMP, HP→BIP, AIP→DAD
    """

    def __init__(self):
        self.patterns = PATTERN_CATEGORIES
        self._legacy_map = NOMENCLATURE_2025_MAP

    def resolve_pattern_key(self, key: str) -> str:
        """Eski patern anahtarını 2025 nomenklaturuna çevir."""
        return self._legacy_map.get(key, key)

    @staticmethod
    def _calculate_cooccurrence_modifiers(
        expanded_findings: List[str],
    ) -> Dict[str, float]:
        """
        Birlikte-görülme kurallarını değerlendir.

        Belirli bulguların birlikteliği klinik anlam taşır.
        Örn: sentrilobüler nodüller + tree-in-bud → enfeksiyon, BIP değil.

        Returns:
            Dict[pattern_key, toplam_modifier]
        """
        modifiers: Dict[str, float] = {}
        findings_set = set(expanded_findings)

        for rule in COOCCURRENCE_RULES:
            trigger = set(rule["trigger_findings"])
            if trigger.issubset(findings_set):
                for pattern_key, mod_value in rule["pattern_modifiers"].items():
                    modifiers[pattern_key] = modifiers.get(pattern_key, 0) + mod_value

        return modifiers

    @staticmethod
    def _expand_findings(selected_findings: List[str]) -> List[str]:
        """
        Kompozit bulgulardan bileşenlerini otomatik çıkar.

        Örnek: head_cheese_sign seçildiğinde centrilobular_nodules,
        mosaic_attenuation ve air_trapping otomatik olarak eklenir.
        Bu, klinik olarak doğrudur çünkü head-cheese bulgusu
        bu üç bileşenin birlikte varlığını tanımlar.
        """
        expanded = set(selected_findings)
        for finding in selected_findings:
            if finding in FINDING_IMPLICATIONS:
                expanded.update(FINDING_IMPLICATIONS[finding])
        return list(expanded)

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

        # Kompozit bulgulardan bileşenleri çıkar
        # Örn: head_cheese_sign → centrilobular_nodules + mosaic + air_trapping
        expanded_findings = self._expand_findings(selected_findings)

        results = []
        for pattern_key, pattern_def in self.patterns.items():
            result = self._score_pattern(
                pattern_key, pattern_def, expanded_findings, clinical_context
            )
            results.append(result)

        # Birlikte-görülme kurallarını uygula
        # Örn: sentrilobüler nodül + tree-in-bud → BIP cezası
        cooccurrence_mods = self._calculate_cooccurrence_modifiers(expanded_findings)
        for result in results:
            if result.pattern_key in cooccurrence_mods:
                mod = cooccurrence_mods[result.pattern_key]
                result.final_score = max(0, min(100, result.final_score + mod))
                result.clinical_modifier_score += mod  # İzlenebilirlik

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
        """
        Tek bir patern için skor hesapla.

        Tetikleme mantığı (2025 güncel):
        1. required_findings kontrol edilir (orijinal yol)
        2. Eğer required karşılanmazsa → alternative_required_sets kontrol edilir
           Bu, elementer bulgulardan patern çıkarımı sağlar.
           Örn: üst lob + GGO + air trapping → BIP çıkarımı
        3. Alternatif set üzerinden tetiklenen paternlere %90 güven
           katsayısı uygulanır (doğrudan bulgu yerine çıkarıma dayandığı için)
        """

        required = pattern_def.get("required_findings", [])
        alt_sets = pattern_def.get("alternative_required_sets", [])
        supportive = pattern_def.get("supportive_findings", [])
        against = pattern_def.get("against_findings", [])
        distribution = pattern_def.get("distribution", [])
        base_score = pattern_def.get("base_score", 50)
        modifiers = pattern_def.get("clinical_modifiers", {})

        # --- Required findings: birincil veya alternatif yol ---
        matched_required = [f for f in required if f in selected_findings]
        used_alternative = False
        inference_factor = 1.0  # Doğrudan bulgu = tam güven

        if not matched_required:
            # Alternatif setleri kontrol et
            best_alt_match = []
            for alt_set in alt_sets:
                alt_matched = [f for f in alt_set if f in selected_findings]
                if len(alt_matched) == len(alt_set):
                    # Tam eşleşme — en uzun seti tercih et (daha spesifik)
                    if len(alt_matched) > len(best_alt_match):
                        best_alt_match = alt_matched

            if best_alt_match:
                matched_required = best_alt_match
                used_alternative = True
                inference_factor = 0.90  # Çıkarıma dayalı → %90 güven
            else:
                # Ne birincil ne de alternatif tetiklendi
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

        # Required bulgu skoru
        if used_alternative:
            # Alternatif set: eşleşen eleman sayısına göre kademeli skor
            req_ratio = len(matched_required) / max(len(matched_required), 1)
            finding_score = base_score * (0.6 + 0.4 * req_ratio) * inference_factor
        else:
            req_ratio = len(matched_required) / max(len(required), 1)
            finding_score = base_score * (0.6 + 0.4 * req_ratio)

        # --- Supportive findings ---
        # Alternatif setle tetiklendiyse, alternatif setteki bulgular
        # supportive olarak tekrar sayılmaz (çift puan önleme)
        if used_alternative:
            already_counted = set(matched_required)
            matched_supportive = [
                f for f in supportive
                if f in selected_findings and f not in already_counted
            ]
        else:
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
        if "acute_presentation" in modifiers and "Akut" in presentation:
            clinical_mod += modifiers["acute_presentation"]

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

        # --- Karşıt bulgu kontrolü (tüm paternler için öncelikli) ---
        if len(primary.matched_against) > 0:
            return True, (
                f"Primer paternle uyumsuz bulgu(lar) mevcuttur: "
                f"{', '.join(primary.matched_against)}. "
                "Atipik özellikler nedeniyle MDD önerilir."
            )

        # --- Kesin UIP ve yüksek güven → MDD gerekmez ---
        # (Yalnızca karşıt bulgu yoksa buraya ulaşılır)
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
