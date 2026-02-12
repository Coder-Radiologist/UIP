# -*- coding: utf-8 -*-
"""
ILA (Interstitial Lung Abnormalities) Sınıflandırıcı
Fleischner Society 2020 + 2025 ERS/ATS Güncellemesi

Sınıflandırma:
  - Non-subplevral ILA
  - Subplevral non-fibrotik ILA
  - Subplevral fibrotik ILA

Risk düzeyleri:
  - Düşük: <%5 tutulum, non-fibrotik
  - Orta: %5-15 veya subplevral non-fibrotik
  - Yüksek: Fibrotik bulgular veya >%15 tutulum
"""

from dataclasses import dataclass
from typing import List


# Fibrotik ILA bulguları
_FIBROTIC_ILA_FINDINGS = {
    "ila_traction_bronchiectasis",
    "ila_honeycombing",
}


@dataclass
class ILAResult:
    """ILA sınıflandırma sonucu."""
    ila_present: bool
    category: str          # non_subpleural, subpleural_nonfibrotic, subpleural_fibrotic
    category_label: str    # Türkçe etiket
    risk_level: str        # Düşük, Orta, Yüksek
    extent_percent: float
    has_fibrotic_features: bool
    is_subpleural: bool
    follow_up: str
    selected_findings: List[str]


class ILAClassifier:
    """
    ILA bulgularını sınıflandırır ve risk düzeyi belirler.
    """

    def classify(
        self,
        ila_present: bool,
        is_subpleural: bool,
        extent_percent: float,
        selected_ila_findings: List[str],
    ) -> ILAResult:
        """
        ILA sınıflandırması yap.

        Args:
            ila_present: ILA bulgusu var mı
            is_subpleural: Subplevral dağılım mevcut mu
            extent_percent: Tutulum yüzdesi
            selected_ila_findings: Seçilen ILA bulguları

        Returns:
            ILAResult objesi
        """
        if not ila_present:
            return ILAResult(
                ila_present=False,
                category="none",
                category_label="ILA saptanmadı",
                risk_level="Düşük",
                extent_percent=0,
                has_fibrotic_features=False,
                is_subpleural=False,
                follow_up="ILA bulgusu yoktur. Rutin takip yeterlidir.",
                selected_findings=[],
            )

        # Fibrotik özellik var mı?
        has_fibrotic = bool(
            set(selected_ila_findings) & _FIBROTIC_ILA_FINDINGS
        )

        # Kategori belirleme
        if has_fibrotic and is_subpleural:
            category = "subpleural_fibrotic"
            category_label = "Subplevral Fibrotik ILA"
        elif is_subpleural:
            category = "subpleural_nonfibrotic"
            category_label = "Subplevral Non-fibrotik ILA"
        else:
            category = "non_subpleural"
            category_label = "Non-subplevral ILA"

        # Risk düzeyi
        risk_level = self._determine_risk(
            category, extent_percent, has_fibrotic, len(selected_ila_findings)
        )

        # Takip önerisi
        follow_up = self._generate_follow_up(category, risk_level, extent_percent)

        return ILAResult(
            ila_present=True,
            category=category,
            category_label=category_label,
            risk_level=risk_level,
            extent_percent=extent_percent,
            has_fibrotic_features=has_fibrotic,
            is_subpleural=is_subpleural,
            follow_up=follow_up,
            selected_findings=selected_ila_findings,
        )

    def _determine_risk(
        self,
        category: str,
        extent: float,
        has_fibrotic: bool,
        finding_count: int,
    ) -> str:
        """Risk düzeyi hesapla."""
        # Fibrotik ILA → her zaman yüksek risk
        if has_fibrotic:
            return "Yüksek"

        # Yaygınlık bazlı
        if extent > 15:
            return "Yüksek"
        elif extent > 5:
            if category == "subpleural_nonfibrotic":
                return "Orta"
            elif category == "non_subpleural":
                return "Orta"
            else:
                return "Orta"
        else:
            # <%5
            if category == "non_subpleural":
                return "Düşük"
            else:
                return "Düşük" if finding_count <= 1 else "Orta"

    def _generate_follow_up(
        self,
        category: str,
        risk_level: str,
        extent: float,
    ) -> str:
        """Takip önerisi oluştur."""
        recommendations = {
            ("subpleural_fibrotic", "Yüksek"): (
                "Fibrotik ILA saptanmıştır — ILD'ye progresyon riski yüksektir. "
                "Solunum fonksiyon testleri (SFT) ve 3-6 ay içinde kontrol YÇBT önerilir. "
                "Semptomatik ise göğüs hastalıkları konsültasyonu ve MDD değerlendirilmelidir."
            ),
            ("subpleural_nonfibrotic", "Orta"): (
                "Subplevral non-fibrotik ILA saptanmıştır. "
                "12 ay içinde kontrol YÇBT ile progresyon değerlendirmesi önerilir. "
                "SFT bazal değerlendirme yapılmalıdır."
            ),
            ("subpleural_nonfibrotic", "Düşük"): (
                "Minimal subplevral ILA saptanmıştır. "
                "12-24 ay içinde kontrol YÇBT düşünülebilir. "
                "Klinik semptomlar gelişirse erken kontrol önerilir."
            ),
            ("non_subpleural", "Orta"): (
                "Non-subplevral ILA saptanmıştır. "
                "Etiyoloji araştırması (maruziyet öyküsü, otoimmün belirteçler) düşünülmelidir. "
                "12 ay içinde kontrol YÇBT önerilir."
            ),
            ("non_subpleural", "Düşük"): (
                "Minimal non-subplevral ILA saptanmıştır. "
                "Klinik önemi belirsizdir; semptom gelişirse değerlendirilmelidir."
            ),
        }

        key = (category, risk_level)
        if key in recommendations:
            return recommendations[key]

        # Yüksek risk genel
        if risk_level == "Yüksek":
            return (
                f"ILA yaygınlığı %{extent:.0f} olup progresyon riski yüksektir. "
                "SFT, göğüs hastalıkları konsültasyonu ve 3-6 ay içinde kontrol YÇBT önerilir."
            )

        return "ILA saptanmıştır. Klinik değerlendirme ve takip önerilir."
