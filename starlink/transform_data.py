import json

import pandas as pd
from pip import main
from sqlalchemy import create_engine, DateTime


def load_starlink_data(file_name: str) -> pd.DataFrame:
    '''Function created to load Starlink JSON data
    couldn't just pd.read_json because it's a nested file'''

    with open(file_name) as data_file:
        starlink_data = json.load(data_file)

    df = pd.json_normalize(starlink_data, max_level=1)
    return df


def transform_starlink_historical_data(df: pd.DataFrame) -> pd.DataFrame:
    # Keeping only the relevant columns and renaming them
    df = df[["spaceTrack.CREATION_DATE", "longitude", "latitude", "id"]]
    df.columns = ["creation_date", "longitude", "latitude", "id"]

    # Parsing type to insure it'll be inserted as a timestime in the database
    df["creation_date"] = pd.to_datetime(df["creation_date"])

    # Setting index to be created inside the database
    df.set_index("id", inplace=True)
    return df


def insert_starlink_data(connection_string: str, df: pd.DataFrame) -> None:
    engine = create_engine(connection_string)
    with engine.connect() as connection:
        df.to_sql(
            'starlink_data',
            engine,
            if_exists="replace",
            dtype={
                "creation_date": DateTime
            }
        )



if __name__ == "__main__":
    df = load_starlink_data("../starlink_historical_data.json")
    df = transform_starlink_historical_data(df)
    insert_starlink_data(
        'postgresql://postgres:local@postgres:5432/local', df
    )
