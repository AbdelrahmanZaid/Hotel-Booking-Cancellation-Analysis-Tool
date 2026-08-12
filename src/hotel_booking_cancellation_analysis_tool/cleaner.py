import pandas as pd


def clean_booking_data(data: pd.DataFrame) -> pd.DataFrame:

    cleaned_data = data.copy()

    cleaned_data["children"] = (
        cleaned_data["children"]
        .fillna(0)
        .astype("int64")
    )

    cleaned_data["country"] = (
        cleaned_data["country"]
        .fillna("Unknown")
    )

    cleaned_data["agent"] = (
        cleaned_data["agent"]
        .astype("Int64")
    )

    cleaned_data["company"] = (
        cleaned_data["company"]
        .astype("Int64")
    )

    cleaned_data["reservation_status_date"] = pd.to_datetime(
        cleaned_data["reservation_status_date"],
        errors="coerce",
    )

    arrival_date_text = (cleaned_data["arrival_date_year"].astype(str) + "-"
        + cleaned_data["arrival_date_month"] + "-" 
        + cleaned_data["arrival_date_day_of_month"].astype(str)
    )

    cleaned_data["arrival_date"] = pd.to_datetime(
        arrival_date_text,
        format="%Y-%B-%d",
        errors="coerce",
    )

    cleaned_data["total_nights"] = ( cleaned_data["stays_in_weekend_nights"]
        + cleaned_data["stays_in_week_nights"])

    cleaned_data["total_guests"] = (cleaned_data["adults"]
        + cleaned_data["children"]
        + cleaned_data["babies"]
    )

    cleaned_data["room_changed"] = ( cleaned_data["reserved_room_type"] 
                                    != cleaned_data["assigned_room_type"])

    cleaned_data["has_agent"] = cleaned_data["agent"].notna()
    cleaned_data["has_company"] = cleaned_data["company"].notna()

    return cleaned_data