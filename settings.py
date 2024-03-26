from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
DOWNLOADS = PROJECT_ROOT / "downloads"
DATABASE_FRESHNESS_DAYS = 1 # (download the db every x days)
