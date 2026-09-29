# Hotel Booking Cancellation Analysis Tool

Python command line application to analyze hotel booking cancellation, customer behavior, market channels, guest origin and Average Daily Rate (ADR) of the hotel.

The tool analyzes past hotel booking information and delivers numerical summaries and visualisations to help understand hotel booking patterns.

## Features

Tool can analyze:

- Overall booking cancellations
- Cancellation rates by hotel
- Cancellation rates by market segment
- Cancellation rates by deposit type
- Cancellation rates by customer type
- Repeated guest behavior
- Special requests
- Room assignment changes
- Distribution channels
- Top guest-origin countries
- Average Daily Rate (ADR) by hotel
- Monthly ADR trends
- Automatic generation of analysis visualizations

## Dataset and Preparation

The data used for the project is in the Hotel Booking dataset found in data/hotel_bookings.csv.

There are 119,390 records in the dataset, and 32 original columns. The dataset is directly included within the repository, because it is below approximately 50 MB, following the project requirements.

Before performing the analysis, the data is validated and prepared. Values for children are filled in with the median value if missing and values for country are filled in with "Unknown" if missing. Any agent or company that were not present in the booking will not be deleted because these may be related to an agent or company not having been associated with the booking.

It also converts date information into correct date format and adds extra columns to be used in analysis such as total_nights, total_guests, room_changed, has_agent, has_company and arrival_date.

Duplicated-looking rows are not automatically deleted as there is no unique booking identifier in the dataset. So there can be two rows identical but representing different bookings.

## Installation and Usage

### Installation:
Download and clone the repository, and open the project folder.
It requires Python 3.10 or newer is required.
Install the package in editable mode via:
uv pip install -e .

### Usage:
Use the following to run the application:
To run the Hotel Booking Cancellation Analysis Tool, you use the command uv run -m hotel_booking_cancellation_analysis_tool <command>

### Available commands:

- summary:
Displays the total number of bookings, cancelled bookings, non-cancelled bookings and the overall cancellation rate.

- cancellations:

Displays cancellation analysis for hotels, market segments, deposit type and customer type.

- customers:

Displays repeated guest behaviour, special requests and room changes.

- market:

Displays booking distribution channels and countries from which guests are coming.

- adr: 

Reports average and median Average Daily Rate by hotel and by month.

- visualize: 

Creates and stores all project visualisations in the outputs folder.

### Examples:

- uv run -m hotel_booking_cancellation_analysis_tool summary
- uv run -m hotel_booking_cancellation_analysis_tool cancellations
- uv run -m hotel_booking_cancellation_analysis_tool visualize


## Testing and Code Quality:

Tests for the primary data loading, validation, cleaning and analysis are included in the project.

### Perform the tests with the following:

- uv run pytest

Use the following to check code:

- uv run ruff check .
- uv run ruff format --check .

Ruff is code linter & formatter.