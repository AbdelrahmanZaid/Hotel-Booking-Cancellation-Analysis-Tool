from dataclasses import dataclass
import pandas as pd

REQUIRED_COLUMNS = {
    "hotel",
    "is_canceled",
    "lead_time",
    "arrival_date_year",
    "arrival_date_month",
    "arrival_date_week_number",
    "arrival_date_day_of_month",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "children",
    "babies",
    "meal",
    "country",
    "market_segment",
    "distribution_channel",
    "is_repeated_guest",
    "previous_cancellations",
    "previous_bookings_not_canceled",
    "reserved_room_type",
    "assigned_room_type",
    "booking_changes",
    "deposit_type",
    "agent",
    "company",
    "days_in_waiting_list",
    "customer_type",
    "adr",
    "required_car_parking_spaces",
    "total_of_special_requests",
    "reservation_status",
    "reservation_status_date",
}


NON_NEGATIVE_COLUMNS = [
    "lead_time",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "children",
    "babies",
    "previous_cancellations",
    "previous_bookings_not_canceled",
    "booking_changes",
    "days_in_waiting_list",
    "required_car_parking_spaces",
    "total_of_special_requests",
]


@dataclass
class ValidationResult:

    errors: list[str]
    warnings: list[str]

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


def validate_booking_data(data: pd.DataFrame) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if data.empty:
        errors.append("The dataset is empty.")
        return ValidationResult(errors, warnings)

    missing_columns = REQUIRED_COLUMNS - set(data.columns)

    if missing_columns:
        errors.append(
            "Missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

        return ValidationResult(errors, warnings)

    invalid_cancellation_values = set(data["is_canceled"].dropna().unique()) - {0, 1}

    if invalid_cancellation_values:
        errors.append(
            f"Values are invalid in is_canceled: "
            f"{sorted(invalid_cancellation_values)}"
        )

    invalid_repeated_guest_values = (
        set(data["is_repeated_guest"].dropna().unique()) - {0, 1}
    )

    if invalid_repeated_guest_values:
        errors.append(
            f"Values are invalid in is_repeated_guest: "
            f"{sorted(invalid_repeated_guest_values)}"
        )

    valid_hotels = {"City Hotel", "Resort Hotel"}

    invalid_hotels = set(data["hotel"].dropna().unique()) - valid_hotels

    if invalid_hotels:
        errors.append(
            f"Hotel unknown type: {sorted(invalid_hotels)}"
        )

    for column in NON_NEGATIVE_COLUMNS:
        negative_count = (data[column].dropna() < 0).sum()

        if negative_count > 0:
            errors.append(
                f"{column} has {negative_count} negative values."
            )

    missing_values = data.isna().sum()
    missing_values = missing_values[missing_values > 0]

    for column, count in missing_values.items():
        warnings.append(
            f"{column} has {count:,} missing values."
        )

    duplicate_count = data.duplicated().sum()

    if duplicate_count > 0:
        warnings.append(
            f"{duplicate_count:,} rows have duplicated values."
        )

    return ValidationResult(errors, warnings)