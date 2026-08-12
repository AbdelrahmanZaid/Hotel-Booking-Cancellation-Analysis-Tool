from .loader import load_booking_data
from .validator import validate_booking_data
from .cleaner import clean_booking_data

def main() -> None:

    data = load_booking_data()

    validation = validate_booking_data(data)

    cleaned_data = clean_booking_data(data)

    print("Hotel Booking Cancellation Analysis Tool:\n")

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

if __name__ == "__main__":
    main()