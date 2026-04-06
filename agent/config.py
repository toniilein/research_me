"""Topic configuration for the Daily Research Agent."""

from pathlib import Path

# === PATHS ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SITE_DIR = PROJECT_ROOT / "site"

# === MODEL ===
MODEL = "claude-sonnet-4-20250514"

# === TOPICS ===
# Add new topics by appending a dict with "name", "slug", and "focus_areas".

TOPICS = [
    {
        "name": "Tokenisierung & RWA",
        "slug": "tokenisierung-rwa",
        "focus_areas": [
            "Tokenisierte Anleihen und Treasuries (BlackRock BUIDL, Franklin Templeton, Ondo)",
            "Real World Asset Protokolle (Centrifuge, Maple, Goldfinch)",
            "Institutionelle Adoption (TradFi Partnerschaften, regulatorische Entwicklungen)",
            "Tokenisierte Fonds und ETFs",
            "Infrastruktur (Chainlink CCIP, LayerZero für Cross-Chain RWA)",
            "Marktvolumen und TVL-Entwicklung",
            "Regulierung (MiCA, SEC, BaFin Einordnungen)",
        ],
    },
    # === ADD NEW TOPICS BELOW ===
    # {
    #     "name": "ILS & Catastrophe Bonds",
    #     "slug": "ils-cat-bonds",
    #     "focus_areas": [
    #         "Neue Cat Bond Emissionen",
    #         "Artemis.bm News",
    #         "Parametrische Versicherung",
    #         "Climate Risk Modelling",
    #         "ILS Fund Performance",
    #     ],
    # },
]
