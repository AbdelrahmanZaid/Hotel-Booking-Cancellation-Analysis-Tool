from .loader import load_booking_data
from .validator import validate_booking_data
from .cleaner import clean_booking_data
from .analyzer import BookingAnalyzer


def main() -> None:
    data = load_booking_data()

    print(f"Booking data {len(data):,}\n")
    print(f"Columns: {len(data.columns)}\n")

    validation = validate_booking_data(data)

    print("Validation status:")

    if not validation.is_valid:
        print("Dataset is invalid\n")

        if validation.errors:
            print("Errors found:")
            for error in validation.errors:
                print(error)

        return

    print("Dataset is valid\n")

    if validation.warnings:
        print("Warnings found:")
        for warning in validation.warnings:
            print(warning)

    cleaned_data = clean_booking_data(data)

    print("\nData preparation complete\n")
    print(f"Prepared bookings: {len(cleaned_data):,}")
    print(f"Prepared columns: {len(cleaned_data.columns)}\n")

    analyzer = BookingAnalyzer(cleaned_data)

    cancellation_summary = analyzer.cancellation_summary()

    cancellation_by_hotel = analyzer.cancellation_rate_by_hotel()

    cancellation_by_market_segment = analyzer.cancellation_rate_by_market_segment()

    cancellation_by_deposit_type = analyzer.cancellation_rate_by_deposit_type()

    cancellation_by_customer_type = analyzer.cancellation_rate_by_customer_type()

    arrival_bookings_by_month = analyzer.arrival_bookings_by_month()

    arrival_bookings_by_month_and_hotel = analyzer.arrival_bookings_by_month_and_hotel()

    repeated_guest_analysis = analyzer.repeated_guest_analysis()

    total_of_special_requests_analysis = analyzer.total_of_special_requests_analysis()

    room_change_analysis = analyzer.room_change_analysis()

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

    print("\nArrival bookings by month:")
    print(arrival_bookings_by_month)

    print("\nArrival bookings by month and hotel:")
    print(arrival_bookings_by_month_and_hotel)

    print("\nRepeated guest analysis:")
    print(repeated_guest_analysis)

    print("\nTotal of special requests analysis:")
    print(total_of_special_requests_analysis)

    print("\nRoom change analysis:")
    print(f"Total bookings: {room_change_analysis['total_bookings']:,}")
    print(f"Changed rooms: {room_change_analysis['total_rooms_changed']:,}")
    print(f"Unchanged rooms: {room_change_analysis['total_rooms_unchanged']:,}")
    print(
        f"Percentage changed: {room_change_analysis['percentage_rooms_changed']:.2f}%"
    )
    print(
        f"Percentage unchanged: {room_change_analysis['percentage_rooms_unchanged']:.2f}%"
    )


if __name__ == "__main__":
    main()
