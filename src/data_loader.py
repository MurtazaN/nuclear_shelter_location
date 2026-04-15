"""Dataset loaders for raw and processed files."""

from pathlib import Path

import pandas as pd


# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_DATA_DIR = BASE_DATA_DIR / "raw"
PROCESSED_DATA_DIR = BASE_DATA_DIR / "processed"

CENSUS_2010_RAW_PATH = RAW_DATA_DIR / "population_by_zip_2010.csv"
NUCLEAR_TARGETS_RAW_PATH = RAW_DATA_DIR / "usa_nuclear_targets.csv"
URBAN_AREAS_RAW_PATH = RAW_DATA_DIR / "usa_urban_areas.csv"

CENSUS_PROCESSED_PATH = PROCESSED_DATA_DIR / "census_by_zip_processed.csv"
NUCLEAR_TARGETS_PROCESSED_PATH = PROCESSED_DATA_DIR / "nuclear_targets_processed.csv"
URBAN_AREAS_PROCESSED_PATH = PROCESSED_DATA_DIR / "urban_areas_processed.csv"


def _require_file(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(
            f"{label} not found at {path}. Processed files do not exist."
        )


# ── Raw loaders ──────────────────────────────────────────────────────────────
def load_raw_census_data() -> pd.DataFrame:
    print("Loading raw Census data...")
    return pd.read_csv(CENSUS_2010_RAW_PATH, dtype=str)


def load_raw_nuclear_targets_data() -> pd.DataFrame:
    print("Loading raw Nuclear Targets data...")
    return pd.read_csv(NUCLEAR_TARGETS_RAW_PATH)


def load_raw_urban_areas_data() -> pd.DataFrame:
    print("Loading raw Urban Areas data...")
    return pd.read_csv(URBAN_AREAS_RAW_PATH, dtype=str)


# ── Processed loaders ────────────────────────────────────────────────────────
def load_processed_census_data() -> pd.DataFrame:
    _require_file(CENSUS_PROCESSED_PATH, "Processed census file")
    census_processed_df = pd.read_csv(CENSUS_PROCESSED_PATH, dtype={"zip_code": str})
    return census_processed_df


def load_processed_nuclear_targets_data() -> pd.DataFrame:
    _require_file(NUCLEAR_TARGETS_PROCESSED_PATH, "Processed nuclear targets file")
    nuclear_targets_processed_df = pd.read_csv(NUCLEAR_TARGETS_PROCESSED_PATH)
    return nuclear_targets_processed_df


def load_processed_urban_areas_data() -> pd.DataFrame:
    _require_file(URBAN_AREAS_PROCESSED_PATH, "Processed urban areas file")
    urban_areas_processed_df = pd.read_csv(URBAN_AREAS_PROCESSED_PATH)
    return urban_areas_processed_df


def load_all_raw() -> dict:
    return {
        "census": load_raw_census_data(),
        "targets": load_raw_nuclear_targets_data(),
        "urban_areas": load_raw_urban_areas_data(),
    }


def load_all_processed() -> dict:
    return {
        "census": load_processed_census_data(),
        "targets": load_processed_nuclear_targets_data(),
        "urban_areas": load_processed_urban_areas_data(),
    }

