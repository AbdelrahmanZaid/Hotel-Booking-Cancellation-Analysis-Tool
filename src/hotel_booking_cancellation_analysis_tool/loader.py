from pathlib import Path 
import pandas as pd

DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "hotel_bookings.csv"
)

def load_booking_data(file_path: str | Path | None = None,) -> pd.DataFrame:
    path = Path(file_path) if file_path is not None else DATA_PATH

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    data = pd.read_csv(path)

    if data.empty:
        raise ValueError("The dataset is empty.")

    return data