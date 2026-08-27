import pandas as pd


class BookingAnalyzer:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def cancellation_rate(self) -> float:
        return float(self.data["is_canceled"].mean() * 100)

    def cancellation_summary(self) -> dict[str, int | float]:
        total_bookings = len(self.data)
        total_canceled = int(self.data["is_canceled"].sum())
        total_not_canceled = total_bookings - total_canceled
        return {
            "total_bookings": total_bookings,
            "total_canceled": total_canceled,
            "total_not_canceled": total_not_canceled,
            "cancellation_rate": self.cancellation_rate(),
        }

    def cancellation_rate_by_hotel(self) -> pd.DataFrame:
        result = (
            self.data.groupby("hotel")
            .agg(
                total_bookings=("is_canceled", "size"),
                canceled_bookings=("is_canceled", "sum"),
            )
            .reset_index()
        )

        result["cancellation_rate"] = (
            result["canceled_bookings"] / result["total_bookings"] * 100
        )

        return result

    def cancellation_rate_by_market_segment(self) -> pd.DataFrame:
        result = (
            self.data.groupby("market_segment")
            .agg(
                total_bookings=("is_canceled", "size"),
                canceled_bookings=("is_canceled", "sum"),
            )
            .reset_index()
        )

        result["cancellation_rate"] = (
            result["canceled_bookings"] / result["total_bookings"] * 100
        )

        return result

    def cancellation_rate_by_deposit_type(self) -> pd.DataFrame:
        result = (
            self.data.groupby("deposit_type")
            .agg(
                total_bookings=("is_canceled", "size"),
                canceled_bookings=("is_canceled", "sum"),
            )
            .reset_index()
        )

        result["cancellation_rate"] = (
            result["canceled_bookings"] / result["total_bookings"] * 100
        )

        return result

    def cancellation_rate_by_customer_type(self) -> pd.DataFrame:
        result = (
            self.data.groupby("customer_type")
            .agg(
                total_bookings=("is_canceled", "size"),
                canceled_bookings=("is_canceled", "sum"),
            )
            .reset_index()
        )

        result["cancellation_rate"] = (
            result["canceled_bookings"] / result["total_bookings"] * 100
        )

        return result
