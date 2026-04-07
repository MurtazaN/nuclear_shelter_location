"""Data cleaning and processed-file generation utilities."""

import pandas as pd
import pgeocode

from src.data_loader import (
    CENSUS_PROCESSED_PATH,
    NUCLEAR_TARGETS_PROCESSED_PATH,
    PROCESSED_DATA_DIR,
    URBAN_AREAS_PROCESSED_PATH,
    load_raw_census_data,
    load_raw_nuclear_targets_data,
    load_raw_urban_areas_data,
)


def parse_yield_kt(yield_str: str) -> float:
    """Parse target yield values into kilotons."""
    if not isinstance(yield_str, str):
        return 0.0
    cleaned_yield = yield_str.strip().lower().replace(" ", "").replace("\xa0", "")
    if cleaned_yield.endswith("mt"):
        return float(cleaned_yield[:-2]) * 1000
    if cleaned_yield.endswith("kt"):
        return float(cleaned_yield[:-2])
    try:
        return float(cleaned_yield)
    except ValueError:
        return 0.0


def normalize_burst_type(burst_type_str: str) -> str:
    """Normalize burst type labels to Air Burst or Surface Burst."""
    if not isinstance(burst_type_str, str):
        return "Surface Burst"
    normalized_burst_type = burst_type_str.replace("\xa0", " ").strip().lower()
    if "air" in normalized_burst_type:
        return "Air Burst"
    return "Surface Burst"


def clean_census_data(census_raw_df: pd.DataFrame) -> pd.DataFrame:
    """Create ZIP-level census data using base population rows only."""
    census_clean_df = census_raw_df.copy()
    census_clean_df.columns = census_clean_df.columns.str.strip().str.lower()

    required_columns = {"population", "minimum_age", "maximum_age", "gender", "zipcode"}
    missing_columns = required_columns - set(census_clean_df.columns)
    if missing_columns:
        raise ValueError(f"Census data is missing required columns: {sorted(missing_columns)}")

    # Match total_pop.py logic exactly: blank age/gender fields count as null.
    for column_name in ["minimum_age", "maximum_age", "gender"]:
        census_clean_df[column_name] = census_clean_df[column_name].replace(r"^\s*$", pd.NA, regex=True)

    base_population_mask = (
        census_clean_df["minimum_age"].isna()
        & census_clean_df["maximum_age"].isna()
        & census_clean_df["gender"].isna()
    )

    census_clean_df = census_clean_df.loc[base_population_mask, ["zipcode", "population"]].copy()
    census_clean_df["zip_code"] = census_clean_df["zipcode"].astype(str).str.strip().str.zfill(5)
    census_clean_df["population"] = pd.to_numeric(census_clean_df["population"], errors="coerce")
    census_clean_df = census_clean_df.dropna(subset=["zip_code", "population"])
    census_clean_df = census_clean_df[census_clean_df["population"] > 0].copy()
    census_clean_df["population"] = census_clean_df["population"].astype(int)

    rows_before_dedup = len(census_clean_df)
    census_clean_df = census_clean_df.drop_duplicates(subset=["zip_code"], keep="first").reset_index(drop=True)
    rows_removed = rows_before_dedup - len(census_clean_df)
    print(f"  Census base rows: {rows_before_dedup:,} | duplicate ZIP rows removed: {rows_removed:,}")

    geocoder = pgeocode.Nominatim("US")
    geocoded_df = geocoder.query_postal_code(census_clean_df["zip_code"].tolist())
    census_clean_df["lat"] = geocoded_df["latitude"].values
    census_clean_df["lon"] = geocoded_df["longitude"].values

    rows_before_geo_drop = len(census_clean_df)
    census_clean_df = census_clean_df.dropna(subset=["lat", "lon"]).reset_index(drop=True)
    geo_rows_removed = rows_before_geo_drop - len(census_clean_df)
    print(f"  ZIP rows removed due to missing coordinates: {geo_rows_removed:,}")

    census_processed_df = census_clean_df[["zip_code", "population", "lat", "lon"]].copy()
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    census_processed_df.to_csv(CENSUS_PROCESSED_PATH, index=False)
    return census_processed_df


def clean_nuclear_targets(nuclear_targets_raw_df: pd.DataFrame) -> pd.DataFrame:
    """Normalize nuclear target columns and parse yield/burst metadata."""
    nuclear_targets_clean_df = nuclear_targets_raw_df.copy()
    nuclear_targets_clean_df.columns = nuclear_targets_clean_df.columns.str.strip().str.lower()

    column_rename_map = {}
    if "target" in nuclear_targets_clean_df.columns:
        column_rename_map["target"] = "name"
    if "lng" in nuclear_targets_clean_df.columns:
        column_rename_map["lng"] = "lon"
    nuclear_targets_clean_df = nuclear_targets_clean_df.rename(columns=column_rename_map)

    nuclear_targets_clean_df["lat"] = pd.to_numeric(nuclear_targets_clean_df["lat"], errors="coerce")
    nuclear_targets_clean_df["lon"] = pd.to_numeric(nuclear_targets_clean_df["lon"], errors="coerce")
    nuclear_targets_clean_df = nuclear_targets_clean_df.dropna(subset=["lat", "lon"]).reset_index(drop=True)

    if "yield" in nuclear_targets_clean_df.columns:
        nuclear_targets_clean_df["yield_kt"] = nuclear_targets_clean_df["yield"].apply(parse_yield_kt)
    else:
        nuclear_targets_clean_df["yield_kt"] = 500.0

    if "type" in nuclear_targets_clean_df.columns:
        nuclear_targets_clean_df["burst_type"] = nuclear_targets_clean_df["type"].apply(normalize_burst_type)
    else:
        nuclear_targets_clean_df["burst_type"] = "Surface Burst"

    output_columns = ["name", "lat", "lon", "yield_kt", "burst_type"]
    if "category" in nuclear_targets_clean_df.columns:
        output_columns.append("category")

    nuclear_targets_processed_df = nuclear_targets_clean_df[output_columns].copy()
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    nuclear_targets_processed_df.to_csv(NUCLEAR_TARGETS_PROCESSED_PATH, index=False)
    return nuclear_targets_processed_df


def clean_urban_areas(urban_areas_raw_df: pd.DataFrame) -> pd.DataFrame:
    """Normalize urban area centroids to name/lat/lon columns."""
    urban_areas_clean_df = urban_areas_raw_df.copy()
    urban_areas_clean_df.columns = urban_areas_clean_df.columns.str.strip().str.lower()

    column_rename_map = {}
    for column_alias in ["name10", "namelsad10", "name"]:
        if column_alias in urban_areas_clean_df.columns:
            column_rename_map[column_alias] = "name"
            break
    for column_alias in ["intptlat10", "lat", "latitude"]:
        if column_alias in urban_areas_clean_df.columns:
            column_rename_map[column_alias] = "lat"
            break
    for column_alias in ["intptlon10", "lon", "lng", "longitude"]:
        if column_alias in urban_areas_clean_df.columns:
            column_rename_map[column_alias] = "lon"
            break

    urban_areas_clean_df = urban_areas_clean_df.rename(columns=column_rename_map)
    urban_areas_clean_df["lat"] = pd.to_numeric(urban_areas_clean_df["lat"], errors="coerce")
    urban_areas_clean_df["lon"] = pd.to_numeric(urban_areas_clean_df["lon"], errors="coerce")
    urban_areas_clean_df = urban_areas_clean_df.dropna(subset=["lat", "lon"]).reset_index(drop=True)

    urban_areas_processed_df = urban_areas_clean_df[["name", "lat", "lon"]].copy()
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    urban_areas_processed_df.to_csv(URBAN_AREAS_PROCESSED_PATH, index=False)
    return urban_areas_processed_df


if __name__ == "__main__":
    clean_census_data(load_raw_census_data())
    clean_nuclear_targets(load_raw_nuclear_targets_data())
    clean_urban_areas(load_raw_urban_areas_data())
