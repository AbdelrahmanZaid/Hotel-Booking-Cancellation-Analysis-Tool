from .loader import load_booking_data


def main() -> None:

    data = load_booking_data()


    print("Hotel Booking Cancellation Analysis Tool:\n")

    print(f"Booking data loaded with {len(data)} records\n")

    print(f"Columns: {len(data.columns)}\n")

if __name__ == "__main__":
    main()