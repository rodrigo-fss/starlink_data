## Running the project

To run the project (instantiate database, insert data into it and provide the API through localhost:80):
`make run`

To run the tests:
`make test`

## The Task (Part 1):

Stand up your favorite kind of database (and ideally it would be in a form that would be runnable by us, via something like docker-compose).

**Solution:**

Using Postgres 13 image - added health check to guarantee that the containers that depend on it will start properly

## The Task (Part 2):

Write a script (in whatever language that you prefer, though Ruby, Python, or Javascript would be ideal for us) to import the relevant fields in Starlink_historical_data.JSON as a time series. The relevant fields are:
    - spaceTrack.creation_date (represents the time that the lat/lon records were recorded)
    - longitude
    - latitude
    - ID (this is the starlink satellite id)
Again, the goal is that we want to be able to query the database for the last known position for a given starlink satellite.
Don't hesitate to use any tools/tricks you know to load data quickly and easily!

**Solution**

The solution can be found in the `starlink/transform_data.py` file. It reads the data, transforms it and inserts it into the postgres database container.

Both `load_starlink_data` and `transform_starlink_historical_data` are being tested.

## The Task (Part 3):

Write a query to fetch the last known position of a satellite (by ID), given a time T. Include this query in your README or somewhere in the project submission

**Solution**

```sql
    select * 
    from starlink_data 
    where 
        id = '$id' and 
        creation_date <= '$timeT'
    order by creation_date desc 
    limit 1;
```

## Bonus Task (Part 4):

Write some logic (via a combination of query + application logic, most likely) to fetch from the database the _closest_ satellite at a given time T, and a given a position on a globe as a (latitude, longitude) coordinate.

No need to derive any fancy match for distances for a point on the globe to a position above the earth. You can just use the Haversine formula. Example libraries to help here:

For Python: https://github.com/mapado/haversine

**Solution**

You'll be able to query the closest satellite at a given time T through the API available at `localhost:80`

All you need to do to spin up the database, insert the data into it and have the API available is run:

`make run`

querying the closest satellite to 
- latitude: 1493
- longitude: -456
at
- snapshot_time: 2021-01-25 2012:00:00

would look like this:
`http://localhost/closest_satelite/?latitude=1493&longitude=-456&snapshop_time=2021-01-25%2012:00:00`

The `_get_closest_distance` is being tested as well


## Possible improvements

Error handling, test improvement, move credentials to a vault
