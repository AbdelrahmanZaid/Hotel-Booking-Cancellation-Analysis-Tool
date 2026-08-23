from .loader import load_booking_data
from .validator import validate_booking_data
from .cleaner import clean_booking_data
from .analyzer import BookingAnalyzer
from hotel_booking_cancellation_analysis_tool import analyzer


def main() -> None:

    data = load_booking_data()

    validation = validate_booking_data(data)

    cleaned_data = clean_booking_data(data)

    analyzer = BookingAnalyzer(cleaned_data)

    cancellation_summary = analyzer.cancellation_summary()

    cancellation_by_hotel = analyzer.cancellation_rate_by_hotel()

    print(f"Booking data loaded with {len(data)} records\n")

    print(f"Columns: {len(data.columns)}\n")

    print("Validation status:")
    if validation.is_valid:
        print("Dataset is valid\n")
    else:
        print("Dataset is invalid\n")

    if validation.errors:
        print("Errors found:")
        for error in validation.errors:
            print(f"{error}")

    if validation.warnings:
        print("Warnings found:")
        for warning in validation.warnings:
            print(f"{warning}")

    print("Data preparation complete\n")
    print(f"Prepared bookings: {len(cleaned_data):,}")
    print(f"Prepared columns: {len(cleaned_data.columns)}")

    print("Data preparation complete \n")
    print(f"Total bookings: {cancellation_summary['total_bookings']:,}\n")
    print(f"Canceled bookings: {cancellation_summary['total_canceled']:,}\n")
    print(f"Not canceled bookings: {cancellation_summary['total_not_canceled']:,}\n")
    print(f"Cancellation rate: {cancellation_summary['cancellation_rate']:.2f}%\n")
    print("\n Cancellation rate by hotel:")
    print(cancellation_by_hotel)


if __name__ == "__main__":
    main()
