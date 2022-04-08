from starlink.transform_data import load_starlink_data, transform_starlink_historical_data
from starlink.coordinates_api import _get_closest_distance

def test_loading():
    df = load_starlink_data("starlink_historical_data.json")
    
    assert df.empty == False

def test_transform():
    df = load_starlink_data("starlink_historical_data.json")
    df = transform_starlink_historical_data(df)
    
    assert list(df.columns) == ["creation_date", "longitude", "latitude"]
    assert df['creation_date'].dtype == 'datetime64[ns]'
    assert df.index.name == "id"

def test_closest_distance():
    received_coordinates = (32,	-53.09619548496887)
    point1 = ("example_id_1", "2021-01-26 02:30:00.000", 109, 25.453949445394215)
    point2 = ("example_id_2", "2021-01-26 02:30:00.000", 11, -20.297919368213044)
    
    nearest_row = (0, 0, 0, 0, 9**9)
    for result in [point1, point2]:
        nearest_row = _get_closest_distance(
            result, received_coordinates, nearest_row
    )

    assert nearest_row[0] == point2[0]