import pandas as pd

class BookingAnalyzer:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def cancellation_rate(self) -> pd.DataFrame:
        return self.data["is_canceled"].mean()*100
    
    def overall_summary(self) -> dict[str,int | float]:
        total_bookings = len(self.data)
        total_cancelled = int(self.data["is_canceled"].sum())
        total_not_cancelled = total_bookings - total_cancelled
        return {
            "total_bookings": total_bookings,
            "total_cancelled": total_cancelled,
            "total_not_cancelled": total_not_cancelled,
            "cancellation_rate": self.cancellation_rate()
        }