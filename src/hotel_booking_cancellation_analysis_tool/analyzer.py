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

    def arrival_bookings_by_month(self) -> pd.DataFrame:
        data_with_month = self.data.assign(
            arrival_month=self.data["arrival_date"].dt.to_period("M").astype(str)
        )

        result = (
            data_with_month.groupby("arrival_month")
            .agg(
                total_bookings=("is_canceled", "size"),
                canceled_bookings=("is_canceled", "sum"),
            )
            .reset_index()
        )

        result["non_canceled_bookings"] = (
            result["total_bookings"] - result["canceled_bookings"]
        )

        return result

    def arrival_bookings_by_month_and_hotel(self) -> pd.DataFrame:
        data_with_month = self.data.assign(
            arrival_month=self.data["arrival_date"].dt.to_period("M").astype(str)
        )

        result = (
            data_with_month.groupby(["hotel", "arrival_month"])
            .agg(
                total_bookings=("is_canceled", "size"),
                canceled_bookings=("is_canceled", "sum"),
            )
            .reset_index()
        )

        result["non_canceled_bookings"] = (
            result["total_bookings"] - result["canceled_bookings"]
        )

        return result

    def repeated_guest_analysis(self) -> pd.DataFrame:
        result = (
            self.data.groupby("is_repeated_guest")
            .agg(
                total_bookings=("is_repeated_guest", "size"),
                average_lead_time=("lead_time", "mean"),
                average_total_nights=("total_nights", "mean"),
                average_guests=("total_guests", "mean"),
                average_special_requests=(
                    "total_of_special_requests",
                    "mean",
                ),
            )
            .reset_index()
        )

        result["guest_type"] = result["is_repeated_guest"].map(
            {
                0: "Not repeated",
                1: "Repeated",
            }
        )
        result = result[
            [
                "guest_type",
                "total_bookings",
                "average_lead_time",
                "average_total_nights",
                "average_guests",
                "average_special_requests",
            ]
        ]
        result = result.round(
            {
                "average_lead_time": 2,
                "average_total_nights": 2,
                "average_guests": 2,
                "average_special_requests": 2,
            }
        )

        return result

    def total_of_special_requests_analysis(self) -> pd.DataFrame:
        result = (
            self.data.groupby("total_of_special_requests")
            .agg(
                total_bookings=("total_of_special_requests", "size"),
            )
            .reset_index()
        )

        result["booking_percentage"] = result["total_bookings"] / len(self.data) * 100
        result = result.round({"booking_percentage": 3})
        return result

    def room_change_analysis(self) -> dict[str, int | float]:
        total_bookings = len(self.data)
        total_rooms_changed = int(self.data["room_changed"].sum())
        total_rooms_unchanged = total_bookings - total_rooms_changed

        percentage_rooms_changed = round(
            (total_rooms_changed / total_bookings) * 100, 2
        )
        percentage_rooms_unchanged = round(
            (total_rooms_unchanged / total_bookings) * 100, 2
        )

        return {
            "total_bookings": total_bookings,
            "total_rooms_changed": total_rooms_changed,
            "total_rooms_unchanged": total_rooms_unchanged,
            "percentage_rooms_changed": percentage_rooms_changed,
            "percentage_rooms_unchanged": percentage_rooms_unchanged,
        }

    def distribution_channel_analysis(self) -> pd.DataFrame:
        result = (
            self.data.groupby("distribution_channel")
            .size()
            .reset_index(name="total_bookings")
        )

        result["percentage_of_bookings"] = (
            result["total_bookings"] / len(self.data) * 100
        )

        result = result.sort_values(
            "total_bookings",
            ascending=False,
        ).reset_index(drop=True)

        result = result.round({"percentage_of_bookings": 3})
        return result

    def top_countries_by_bookings(self, top_n: int = 15) -> pd.DataFrame:
        result = (
            self.data.groupby("country")
            .size()
            .reset_index(name="total_bookings")
            .sort_values("total_bookings", ascending=False)
            .head(top_n)
            .reset_index(drop=True)
        )
        result.index = result.index + 1
        result["percentage_of_bookings"] = (
            result["total_bookings"] / len(self.data) * 100
        )
        result = result.round({"percentage_of_bookings": 3})
        return result

    def average_daily_rate_hotel_analysis(self) -> pd.DataFrame:
        result = (
            self.data.groupby("hotel")
            .agg(
                total_bookings=("adr", "size"),
                median_adr=("adr", "median"),
                average_adr=("adr", "mean"),
            )
            .reset_index()
        )

        result = result.round(
            {
                "median_adr": 2,
                "average_adr": 2,
            }
        )
        return result

    def average_daily_rate_month_analysis(self) -> pd.DataFrame:
        data_with_month = self.data.assign(
            arrival_month=self.data["arrival_date"].dt.to_period("M").astype(str)
        )
        result = (
            data_with_month.groupby("arrival_month")
            .agg(
                total_bookings=("adr", "size"),
                median_adr=("adr", "median"),
                average_adr=("adr", "mean"),
            )
            .reset_index()
        )

        result = result.round(
            {
                "median_adr": 2,
                "average_adr": 2,
            }
        )
        return result
