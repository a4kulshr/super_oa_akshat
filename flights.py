import pandas as pd
import numpy as np
import re


def get_raw_flight_data():
    """
    Provides the raw flight data as a single string.

    In a real-world application, this data might be fetched from a file,
    a database, or an API endpoint.
    """
    return (
        'Airline Code;DelayTimes;FlightCodes;To_From\n'
        'Air Canada (!);[21, 40];20015.0;WAterLoo_NEwYork\n'
        '<Air France> (12);[];;Montreal_TORONTO\n'
        '(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n'
        '12. Air France;[78, 66];;Ottawa_VANcouvER\n'
        'Lufthansa;[12, 33];20055.0;london_MONtreal\n'
    )


def parse_flight_data_string(data_string):
    """
    Parses the multiline string of flight data into a DataFrame.

    Args:
        data_string: A string where each line is a record and fields are
                     separated by semicolons.

    Returns:
        A pandas DataFrame containing the flight data.
    """
    lines = data_string.strip().split('\n')
    header = lines[0].split(';')
    data_rows = [line.split(';') for line in lines[1:]]
    return pd.DataFrame(data_rows, columns=header)


def clean_and_prepare_data(flights_df):
    """
    Applies a series of cleaning and transformation steps to the flight data.
    """
    # Clean up the 'Airline Code' by removing special characters and numbers.
    flights_df['Airline Code'] = (
        flights_df['Airline Code']
        .str.replace(r'[^\w\s]|\d', '', regex=True)
        .str.strip()
    )

    # Fill in missing flight codes. They are expected to increment by 10 for each row.
    flights_df['FlightCodes'] = flights_df['FlightCodes'].replace('', np.nan)
    numeric_codes = pd.to_numeric(flights_df['FlightCodes'], errors='coerce')
    start_code = int(numeric_codes.dropna().iloc[0])
    flights_df['FlightCodes'] = [start_code + 10 * i for i in range(len(flights_df))]

    # Split 'To_From' into separate 'From' and 'To' columns and capitalize them.
    route_split = flights_df['To_From'].str.split('_', expand=True)
    flights_df['From'] = route_split[0].str.upper()
    flights_df['To'] = route_split[1].str.upper()
    flights_df = flights_df.drop(columns=['To_From'])

    # Parse the 'DelayTimes' string into a list of integers.
    flights_df['DelayTimes'] = (
        flights_df['DelayTimes']
        .str.findall(r'\d+')
        .apply(lambda x: [int(i) for i in x])
    )
    
    return flights_df


def main():
    """
    The main entry point for the script. It orchestrates the process of
    reading, cleaning, and saving the flight data.
    """
    print("Processing flight data...")

    # Load the initial data
    raw_data = get_raw_flight_data()
    flights_df = parse_flight_data_string(raw_data)

    # Apply all transformations
    cleaned_flights = clean_and_prepare_data(flights_df.copy())

    # Reorder columns for the final output
    final_columns = ['Airline Code', 'From', 'To', 'FlightCodes', 'DelayTimes']
    final_df = cleaned_flights[final_columns]

    # Display the result in the console
    print("\n--- Transformed Flight Data ---")
    print(final_df.to_string())

    # Save the cleaned data to a CSV file
    output_filename = 'Cleaned_Airline_Data.csv'
    final_df.to_csv(output_filename, index=False)
    print(f"\nSuccessfully saved the transformed data to '{output_filename}'.")


if __name__ == "__main__":
    main() 