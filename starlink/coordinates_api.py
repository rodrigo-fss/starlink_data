from opcode import HAVE_ARGUMENT
import psycopg2
from haversine import haversine
from flask import Flask, request

app = Flask(__name__)


def _get_db_connection():
    conn = psycopg2.connect(host="postgres",
                            database="local",
                            user="postgres",
                            password="local")
    return conn


def _get_closest_distance(db_row: tuple, received_coordinates: tuple, previous_closest_row: tuple) -> tuple:
    '''Receives a row and compare it's distance with the previous closest,
    if the new one has a shorter distance, returns it as the new closest'''

    # The distance will be the 4th item on the tuple
    previous_closest_distance = previous_closest_row[4]
    db_coordinates = (db_row[2], db_row[3])

    distance = haversine(db_coordinates, received_coordinates)

    if distance < previous_closest_distance:
        # Append distance to the row data
        return db_row + (distance,)
    else:
        return previous_closest_row


def _query_most_recent_coordinates(snapshot_time: str) -> list:
    with _get_db_connection().cursor() as cursor:
        # Given a time, get the most recent record for each ID
        cursor.execute(f'''
            with coordinates_at_that_time as (
                select * from starlink_data 
                where creation_date <= '{snapshot_time}'
            ), -- filtering only the records prior to the given date
            rank_coordinates as ( 
                select *, 
                    rank() over(
                        partition by id
                        order by creation_date desc
                    ) c_rank 
                from coordinates_at_that_time
            ) -- descending ranking ids by creation_date
            select id, creation_date, latitude, longitude
            from rank_coordinates where 
                c_rank = 1 -- getting only the most recent record for each ID
                and latitude is not null 
                and longitude is not null 
            order by id
            '''
                       )
        results = cursor.fetchall()
        return results


@app.route("/")
def hello_world():
    return ('''
        <p>Use the /closest_satelite/ endpoint to get the coordinates of the nearest satelite in a given time.</p>
        <p>You should use the following params:<p>
                <ul>
                    <li>latitude: <b>Int</b></li>
                    <li>longitude: <b>Int</b></li>
                    <li>snapshot_time: <b>String</b> (format: Y-m-d H:m:s)</li>
                </ul>
        <p> The request should look like this: 
        http://localhost/closest_satelite?latitude=1493&longitude=-456&snapshop_time=2021-01-25%2012:00:00</p>
        ''')


@app.route("/closest_satelite/", methods=["GET"])
def get_closest_satelite():
    latitude = int(request.args.get("latitude"))
    longitude = int(request.args.get("longitude"))
    received_coordinates = (latitude, longitude)

    if request.args.get("snapshot_time"):
        snapshot_time = request.args.get("snapshot_time")
    else:
        snapshot_time = '2022-01-01'

    results = _query_most_recent_coordinates(snapshot_time)

    # Arbitrary values to start the _get_closes_distance
    nearest_row = (0, 0, 0, 0, 9**9)
    for result in results:
        nearest_row = _get_closest_distance(
            result, received_coordinates, nearest_row
        )

    return f'''
    <p> ID: {nearest_row[0]}</p>
    <p> Creation Date: {nearest_row[1]}</p>
    <p> Latitude: {nearest_row[2]}</p>
    <p> Longitude: {nearest_row[3]}</p> 
    <p> Distance: {nearest_row[4]}</p>
    '''
