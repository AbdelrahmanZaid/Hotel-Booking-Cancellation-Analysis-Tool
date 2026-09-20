import pandas as pd
import pytest

from hotel_booking_cancellation_analysis_tool.analyzer import BookingAnalyzer
from hotel_booking_cancellation_analysis_tool.cleaner import clean_booking_data
from hotel_booking_cancellation_analysis_tool.loader import load_booking_data
from hotel_booking_cancellation_analysis_tool.validator import validate_booking_data


def test_load_booking_data(tmp_path):

    file_path = tmp_path / "bookings.csv"

    pd.DataFrame(
        {
            "hotel": ["Resort Hotel"],
            "is_canceled": [0],
        }
    ).to_csv(file_path, index=False)

    data = load_booking_data(file_path)

    assert len(data) == 1
    assert data.loc[0, "hotel"] == "Resort Hotel"
    assert data.loc[0, "is_canceled"] == 0


def test_missing_file_raises_error(tmp_path):
    file_path = tmp_path / "not_found.csv"

    with pytest.raises(
        FileNotFoundError,
        match="Dataset not found",
    ):
        load_booking_data(file_path)


def test_empty_dataset_raises_error(tmp_path):
    file_path = tmp_path / "empty.csv"

    pd.DataFrame(columns=["hotel", "is_canceled"]).to_csv(file_path, index=False)

    with pytest.raises(
        ValueError,
        match="dataset is empty",
    ):
        load_booking_data(file_path)


def test_valid_dataset():

    data = load_booking_data()

    result = validate_booking_data(data)

    assert result.is_valid
    assert result.errors == []


def test_missing_required_column():
    data = load_booking_data()
    data = data.drop(columns=["hotel"])

    result = validate_booking_data(data)

    assert not result.is_valid
    assert any("hotel" in error.lower() for error in result.errors)


def test_invalid_cancellation_value():
    data = load_booking_data()
    data.loc[0, "is_canceled"] = 2

    result = validate_booking_data(data)

    assert not result.is_valid
    assert any("is_canceled" in error.lower() for error in result.errors)


def test_invalid_repeated_guest_value():

    data = load_booking_data()
    data.loc[0, "is_repeated_guest"] = 3

    result = validate_booking_data(data)

    assert not result.is_valid
    assert any("is_repeated_guest" in error.lower() for error in result.errors)


def test_duplicate_rows_create_warning():

    data = load_booking_data()

    result = validate_booking_data(data)

    assert any("duplicated" in warning.lower() for warning in result.warnings)


def _sample_data() -> pd.DataFrame:

    return pd.DataFrame(
        {
            "children": [1.0, None, 3.0],
            "country": ["FRA", None, "CHE"],
            "agent": [3.0, None, 10.0],
            "company": [None, 3.0, None],
            "reservation_status_date": [
                "2017-07-16",
                "2017-07-17",
                "2017-07-18",
            ],
            "arrival_date_year": [2017, 2017, 2017],
            "arrival_date_month": ["July", "July", "July"],
            "arrival_date_day_of_month": [15, 16, 17],
            "stays_in_weekend_nights": [3, 0, 2],
            "stays_in_week_nights": [2, 3, 0],
            "adults": [4, 2, 1],
            "babies": [1, 1, 0],
            "reserved_room_type": ["A", "B", "C"],
            "assigned_room_type": ["A", "C", "C"],
        }
    )


def test_cleaner_creates_derived_columns():

    cleaned = clean_booking_data(_sample_data())

    assert cleaned.loc[0, "total_nights"] == 5
    assert cleaned.loc[1, "total_nights"] == 3

    assert cleaned.loc[0, "total_guests"] == 6
    assert cleaned.loc[1, "total_guests"] == 5

    assert not cleaned.loc[0, "room_changed"]
    assert cleaned.loc[1, "room_changed"]

    assert cleaned.loc[0, "has_agent"]
    assert not cleaned.loc[1, "has_agent"]

    assert not cleaned.loc[0, "has_company"]
    assert cleaned.loc[1, "has_company"]


def test_cleaner_creates_dates():
    cleaned = clean_booking_data(_sample_data())

    assert pd.api.types.is_datetime64_any_dtype(cleaned["reservation_status_date"])

    assert pd.api.types.is_datetime64_any_dtype(cleaned["arrival_date"])

    assert cleaned.loc[0, "arrival_date"] == pd.Timestamp("2017-07-15")


def test_cleaner_does_not_modify_original_data():

    original = _sample_data()

    clean_booking_data(original)

    assert "total_nights" not in original.columns
    assert "arrival_date" not in original.columns
    assert pd.isna(original.loc[1, "children"])


def _sample_analysis_data() -> pd.DataFrame:

    return pd.DataFrame(
        {
            "hotel": [
                "City Hotel",
                "City Hotel",
                "Resort Hotel",
                "Resort Hotel",
                "City Hotel",
                "Resort Hotel",
            ],
            "is_canceled": [1, 0, 0, 1, 1, 0],
            "is_repeated_guest": [0, 0, 1, 1, 0, 1],
            "arrival_date": pd.to_datetime(
                [
                    "2017-01-05",
                    "2017-01-10",
                    "2017-01-20",
                    "2017-02-05",
                    "2017-02-10",
                    "2017-02-20",
                ]
            ),
        }
    )


def test_cancellation_summary():

    analyzer = BookingAnalyzer(_sample_analysis_data())

    summary = analyzer.cancellation_summary()

    assert summary["total_bookings"] == 6
    assert summary["total_canceled"] == 3
    assert summary["total_not_canceled"] == 3
    assert summary["cancellation_rate"] == pytest.approx(50.0)


def test_cancellation_rate_by_hotel():

    analyzer = BookingAnalyzer(_sample_analysis_data())

    result = analyzer.cancellation_rate_by_hotel()

    city = result[result["hotel"] == "City Hotel"].iloc[0]
    resort = result[result["hotel"] == "Resort Hotel"].iloc[0]

    assert city["total_bookings"] == 3
    assert city["canceled_bookings"] == 2
    assert city["cancellation_rate"] == pytest.approx(66.6667, rel=1e-3)

    assert resort["total_bookings"] == 3
    assert resort["canceled_bookings"] == 1
    assert resort["cancellation_rate"] == pytest.approx(33.3333, rel=1e-3)


def test_arrival_bookings_by_month():
    analyzer = BookingAnalyzer(_sample_analysis_data())

    result = analyzer.arrival_bookings_by_month()

    january = result[result["arrival_month"].astype(str) == "2017-01"].iloc[0]

    february = result[result["arrival_month"].astype(str) == "2017-02"].iloc[0]

    assert january["total_bookings"] == 3
    assert january["canceled_bookings"] == 1
    assert january["non_canceled_bookings"] == 2

    assert february["total_bookings"] == 3
    assert february["canceled_bookings"] == 2
    assert february["non_canceled_bookings"] == 1


def test_adr_by_hotel():
    data = pd.DataFrame(
        {
            "hotel": [
                "City Hotel",
                "City Hotel",
                "Resort Hotel",
                "Resort Hotel",
            ],
            "adr": [100.0, 120.0, 80.0, 100.0],
        }
    )

    analyzer = BookingAnalyzer(data)

    result = analyzer.average_daily_rate_hotel_analysis()

    city = result[result["hotel"] == "City Hotel"].iloc[0]
    resort = result[result["hotel"] == "Resort Hotel"].iloc[0]

    assert city["total_bookings"] == 2
    assert city["average_adr"] == pytest.approx(110.0)
    assert city["median_adr"] == pytest.approx(110.0)

    assert resort["total_bookings"] == 2
    assert resort["average_adr"] == pytest.approx(90.0)
    assert resort["median_adr"] == pytest.approx(90.0)
