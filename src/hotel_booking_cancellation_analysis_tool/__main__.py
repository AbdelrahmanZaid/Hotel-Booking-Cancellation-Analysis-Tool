from .loader import load_booking_data
from .validator import validate_booking_data
from .cleaner import clean_booking_data
from .analyzer import BookingAnalyzer


def main() -> None:

    data = load_booking_data()

    validation = validate_booking_data(data)

    cleaned_data = clean_booking_data(data)

    analyzer = BookingAnalyzer(cleaned_data)

    cancellation_summary = analyzer.cancellation_summary()

    cancellation_by_hotel = analyzer.cancellation_rate_by_hotel()

    cancellation_by_market_segment = analyzer.cancellation_rate_by_market_segment()

    cancellation_by_deposit_type = analyzer.cancellation_rate_by_deposit_type()

    cancellation_by_customer_type = analyzer.cancellation_rate_by_customer_type()

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

    print(f"Total bookings: {cancellation_summary['total_bookings']:,}\n")

    print(f"Canceled bookings: {cancellation_summary['total_canceled']:,}\n")

    print(f"Not canceled bookings: {cancellation_summary['total_not_canceled']:,}\n")

    print(f"Cancellation rate: {cancellation_summary['cancellation_rate']:.2f}%\n")

    print("\nCancellation rate by hotel:")
    print(cancellation_by_hotel)

    print("\nCancellation rate by market segment:")
    print(cancellation_by_market_segment)

    print("\nCancellation rate by deposit type:")
    print(cancellation_by_deposit_type)

    print("\nCancellation rate by customer type:")
    print(cancellation_by_customer_type)


if __name__ == "__main__":
    main()
