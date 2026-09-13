from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


class BookingVisualizer:

    def __init__(
        self,
        output_dir: str | Path = "outputs",
    ) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def plot_cancellation_summary(
        self,
        data: dict[str, int | float],
    ) -> Path:

        labels = ["Canceled", "Not canceled"]
        values = [
            data["total_canceled"],
            data["total_not_canceled"],
        ]

        fig, ax = plt.subplots(figsize=(7, 5))

        ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
        )

        ax.set_title("Overall Booking Cancellation Summary")

        fig.tight_layout()

        output_path = self.output_dir / "cancellation_summary.png"
        fig.savefig(output_path, dpi=150)

        plt.close(fig)

        return output_path

    def plot_cancellation_by_hotel(
        self,
        data: pd.DataFrame,
    ) -> Path:

        fig, ax = plt.subplots()

        bars = ax.bar(
            data["hotel"],
            data["cancellation_rate"],
        )

        ax.set_title("Cancellation Rate by Hotel")
        ax.set_xlabel("Hotel")
        ax.set_ylabel("Cancellation Rate (%)")

        ax.bar_label(
            bars,
            fmt="%.2f%%",
            padding=3,
        )
        ax.set_ylim(0, 100)

        fig.tight_layout()

        output_path = self.output_dir / "cancellation_by_hotel.png"

        fig.savefig(
            output_path,
            dpi=150,
        )

        plt.close(fig)

        return output_path

    def plot_cancellation_by_market_segment(
        self,
        data: pd.DataFrame,
    ) -> Path:

        plot_data = data[data["market_segment"] != "Undefined"].sort_values(
            "cancellation_rate",
            ascending=True,
        )

        fig, ax = plt.subplots(figsize=(9, 5))

        bars = ax.bar(
            plot_data["market_segment"],
            plot_data["cancellation_rate"],
        )

        ax.set_title("Cancellation Rate by Market Segment")
        ax.set_xlabel("Market Segment")
        ax.set_ylabel("Cancellation Rate (%)")

        ax.bar_label(
            bars,
            fmt="%.2f%%",
            padding=3,
        )

        ax.set_ylim(0, 105)

        fig.tight_layout()

        output_path = self.output_dir / "cancellation_by_market_segment.png"

        fig.savefig(
            output_path,
            dpi=150,
        )

        plt.close(fig)

        return output_path

    def plot_cancellation_by_deposit_type(
        self,
        data: pd.DataFrame,
    ) -> Path:

        fig, ax = plt.subplots(figsize=(7, 5))

        bars = ax.bar(
            data["deposit_type"],
            data["cancellation_rate"],
        )

        ax.set_title("Cancellation Rate by Deposit Type")
        ax.set_xlabel("Deposit Type")
        ax.set_ylabel("Cancellation Rate (%)")

        ax.bar_label(
            bars,
            fmt="%.2f%%",
            padding=3,
        )

        ax.set_ylim(0, 105)

        fig.tight_layout()

        output_path = self.output_dir / "cancellation_by_deposit_type.png"

        fig.savefig(
            output_path,
            dpi=150,
        )

        plt.close(fig)

        return output_path

    def plot_distribution_channels(
        self,
        data: pd.DataFrame,
    ) -> Path:

        plot_data = data[data["distribution_channel"] != "Undefined"].sort_values(
            "percentage_of_bookings",
            ascending=True,
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        bars = ax.barh(
            plot_data["distribution_channel"],
            plot_data["percentage_of_bookings"],
        )

        ax.set_title("Booking Distribution by Channel")
        ax.set_xlabel("Percentage of Bookings (%)")
        ax.set_ylabel("Distribution Channel")

        ax.bar_label(
            bars,
            fmt="%.2f%%",
            padding=3,
        )

        ax.set_xlim(0, 90)

        fig.tight_layout()

        output_path = self.output_dir / "distribution_channels.png"

        fig.savefig(output_path, dpi=150)
        plt.close(fig)

        return output_path

    def plot_arrival_bookings_by_month(
        self,
        data: pd.DataFrame,
    ) -> Path:
        fig, ax = plt.subplots(figsize=(11, 5))

        ax.plot(
            data["arrival_month"],
            data["non_canceled_bookings"],
            marker="o",
            label="Non-canceled bookings",
        )

        ax.plot(
            data["arrival_month"],
            data["canceled_bookings"],
            marker="o",
            label="Canceled bookings",
        )

        ax.set_title("Monthly Arrival Bookings")
        ax.set_xlabel("Arrival Month")
        ax.set_ylabel("Number of Bookings")

        ax.legend()

        ax.tick_params(
            axis="x",
            rotation=45,
        )

        fig.tight_layout()

        output_path = self.output_dir / "arrival_bookings_by_month.png"

        fig.savefig(
            output_path,
            dpi=150,
        )

        plt.close(fig)

        return output_path

    def plot_arrival_bookings_by_hotel_and_month(
        self,
        data: pd.DataFrame,
    ) -> Path:

        fig, ax = plt.subplots(figsize=(11, 5))

        for hotel, hotel_data in data.groupby("hotel"):
            ax.plot(
                hotel_data["arrival_month"],
                hotel_data["total_bookings"],
                marker="o",
                label=hotel,
            )

        ax.set_title("Monthly Arrival Bookings by Hotel")
        ax.set_xlabel("Arrival Month")
        ax.set_ylabel("Number of Bookings")

        ax.legend()

        ax.tick_params(
            axis="x",
            rotation=45,
        )

        fig.tight_layout()

        output_path = self.output_dir / "arrival_bookings_by_hotel_and_month.png"

        fig.savefig(
            output_path,
            dpi=150,
        )

        plt.close(fig)

        return output_path

    def plot_top_countries(
        self,
        data: pd.DataFrame,
    ) -> Path:

        plot_data = data.sort_values(
            "total_bookings",
            ascending=True,
        )

        fig, ax = plt.subplots(figsize=(9, 6))

        bars = ax.barh(
            plot_data["country"],
            plot_data["total_bookings"],
        )

        ax.set_title("Top Countries by Bookings")
        ax.set_xlabel("Total Bookings")
        ax.set_ylabel("Country")

        ax.bar_label(
            bars,
            fmt="%.0f",
            padding=3,
        )

        fig.tight_layout()

        output_path = self.output_dir / "top_countries.png"
        fig.savefig(output_path, dpi=150)

        plt.close(fig)

        return output_path

    def plot_adr_by_month(
        self,
        data: pd.DataFrame,
    ) -> Path:

        fig, ax = plt.subplots(figsize=(11, 5))

        ax.plot(
            data["arrival_month"],
            data["average_adr"],
            marker="o",
            label="Average ADR",
        )

        ax.plot(
            data["arrival_month"],
            data["median_adr"],
            marker="o",
            label="Median ADR",
        )

        ax.set_title("Monthly Average Daily Rate (ADR) Analysis")
        ax.set_xlabel("Arrival Month")
        ax.set_ylabel("Average Daily Rate")

        ax.legend()

        ax.tick_params(
            axis="x",
            rotation=45,
        )

        fig.tight_layout()

        output_path = self.output_dir / "adr_by_month.png"

        fig.savefig(output_path, dpi=150)

        plt.close(fig)

        return output_path
