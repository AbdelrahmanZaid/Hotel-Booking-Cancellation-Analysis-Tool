import argparse
from pathlib import Path
from .analyzer import BookingAnalyzer
from .cleaner import clean_booking_data
from .loader import load_booking_data
from .validator import validate_booking_data
from .visualizer import BookingVisualizer

def _prepare_data(file_path: Path | None = None) -> BookingAnalyzer:
    data = load_booking_data(file_path)

    validation = validate_booking_data(data)

    if not validation.is_valid:
        raise ValueError("Dataset is not valid")

    cleaned_data = clean_booking_data(data)

    return BookingAnalyzer(cleaned_data)


def _print_summary(analyzer: BookingAnalyzer) -> None:
    summary = analyzer.cancellation_summary()
    print(f"Total bookings: {summary['total_bookings']:,}")
    print(f"Canceled bookings: {summary['total_canceled']:,}")
    print(f"Not canceled bookings: {summary['total_not_canceled']:,}")
    print(f"Cancellation rate: {summary['cancellation_rate']:.2f}%")


def _print_cancellations(analyzer: BookingAnalyzer) -> None:
    hotel = analyzer.cancellation_rate_by_hotel()
    market_segment = analyzer.cancellation_rate_by_market_segment()
    deposit_type = analyzer.cancellation_rate_by_deposit_type()
    customer_type = analyzer.cancellation_rate_by_customer_type()

    print("\nCancellation rate by hotel:")
    print(hotel.round({"cancellation_rate": 2}).to_string(index=False))

    print("\nCancellation rate by market segment:")
    print(market_segment.round({"cancellation_rate": 2}).to_string(index=False))

    print("\nCancellation rate by deposit type:")
    print(deposit_type.round({"cancellation_rate": 2}).to_string(index=False))

    print("\nCancellation rate by customer type:")
    print(customer_type.round({"cancellation_rate": 2}).to_string(index=False))


def _print_arrival_bookings(analyzer: BookingAnalyzer) -> None:
    arrival_bookings_by_month = analyzer.arrival_bookings_by_month()
    arrival_bookings_by_month_and_hotel = analyzer.arrival_bookings_by_month_and_hotel()
    print("\nArrival bookings by month:\n")
    print(arrival_bookings_by_month.to_string(index=False))

    print("\nArrival bookings by month and hotel:\n")
    print(arrival_bookings_by_month_and_hotel.to_string(index=False))


def _print_customer_analysis(analyzer: BookingAnalyzer) -> None:
    repeated_guests = analyzer.repeated_guest_analysis()
    special_requests = analyzer.total_of_special_requests_analysis()
    room_changes = analyzer.room_change_analysis()
    print("\nRepeated guests analysis:\n")
    print(repeated_guests.to_string(index=False))
    print("\nSpecial requests analysis:\n")
    print(
        special_requests.to_string(
            index=False, formatters={"booking_percentage": lambda x: f"{x:.2f}%"}
        )
    )
    print("\nRoom changes analysis:\n")
    print(
        f"Total bookings: {room_changes['total_bookings']:,}",
        f"\nRooms unchanged: {room_changes['total_rooms_unchanged']:,}",
        f"\nRooms unchanged percentage: {room_changes['percentage_rooms_unchanged']:.2f}%",
        f"\nRooms changed: {room_changes['total_rooms_changed']:,}",
        f"\nRooms changed percentage: {room_changes['percentage_rooms_changed']:.2f}%",
    )


def _print_market(analyzer: BookingAnalyzer) -> None:
    distribution_channel_analysis = analyzer.distribution_channel_analysis()
    top_countries_by_bookings = analyzer.top_countries_by_bookings(15)

    print("\nDistribution channel analysis:\n")
    print(distribution_channel_analysis.to_string(index=False))

    print("\nTop countries by bookings:\n")
    print(top_countries_by_bookings.to_string(index=False))


def _print_average_daily_rate_analysis(analyzer: BookingAnalyzer) -> None:
    adr_by_hotel = analyzer.average_daily_rate_hotel_analysis()
    adr_by_month = analyzer.average_daily_rate_month_analysis()

    print("\nAverage daily rate by hotel:\n")
    print(
        adr_by_hotel.to_string(
            index=False,
            formatters={
                "median_adr": lambda x: f"{x:.2f}",
                "average_adr": lambda x: f"{x:.2f}",
            },
        )
    )
    print("\nAverage daily rate by month:\n")
    print(
        adr_by_month.round({"average_daily_rate": 2}).to_string(
            index=False, formatters={"average_daily_rate": lambda x: f"{x:.2f}"}
        )
    )

def _create_visualizations(analyzer: BookingAnalyzer) -> None:
    visualizer: BookingVisualizer = BookingVisualizer()
    cancellation_summary = analyzer.cancellation_summary()
    cancellation_by_hotel = analyzer.cancellation_rate_by_hotel()
    cancellation_by_market = (
        analyzer.cancellation_rate_by_market_segment()
    )
    cancellation_by_deposit = (
        analyzer.cancellation_rate_by_deposit_type()
    )

    distribution_channels = analyzer.distribution_channel_analysis()

    arrivals_by_month = analyzer.arrival_bookings_by_month()
    arrivals_by_hotel = (analyzer.arrival_bookings_by_month_and_hotel())

    top_countries = analyzer.top_countries_by_bookings(15)
    adr_by_month = analyzer.average_daily_rate_month_analysis()

    visualizer.plot_cancellation_summary(cancellation_summary)
    visualizer.plot_cancellation_by_hotel(cancellation_by_hotel)
    visualizer.plot_cancellation_by_market_segment(cancellation_by_market)
    visualizer.plot_cancellation_by_deposit_type(cancellation_by_deposit)
    visualizer.plot_distribution_channels(distribution_channels)
    visualizer.plot_arrival_bookings_by_month(arrivals_by_month)
    visualizer.plot_arrival_bookings_by_hotel_and_month(arrivals_by_hotel)
    visualizer.plot_top_countries(top_countries)
    visualizer.plot_adr_by_month(adr_by_month)
    print("\nVisualizations have been created successfully")

def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Hotel Booking Cancellation Analysis Tool"
    )
    parser.add_argument(
        "--data",
        type=Path,
        help="Path to CSV file that contains hotel booking data",
    )
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )
    subparsers.add_parser(
        "summary",
        help="Show summary of hotel bookings",
    )
    subparsers.add_parser(
        "cancellations",
        help="Show cancellation rates analysis",
    )
    subparsers.add_parser(
        "arrivals",
        help="Show arrival bookings analysis",
    )
    subparsers.add_parser(
        "customers",
        help="Show customer analysis",
    )
    subparsers.add_parser(
        "market",
        help="Show market analysis",
    )
    subparsers.add_parser(
        "adr",
        help="Show average daily rate analysis",
    )
    subparsers.add_parser(
        "visualize",
        help="Create visualizations of the data"
    )
    return parser

def main() -> None:
    parser = build_argument_parser()
    args = parser.parse_args()
    try:
        analyzer = _prepare_data(args.data)

        if args.command == "summary":
            _print_summary(analyzer)
        elif args.command == "cancellations":
            _print_cancellations(analyzer)
        elif args.command == "arrivals":
            _print_arrival_bookings(analyzer)
        elif args.command == "customers":
            _print_customer_analysis(analyzer)
        elif args.command == "market":
            _print_market(analyzer)
        elif args.command == "adr":
            _print_average_daily_rate_analysis(analyzer)
        elif args.command == "visualize":
            _create_visualizations(analyzer)
    except ValueError as e:
        print(f"Error: {e}")
