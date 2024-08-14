# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
from pathlib import Path

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
database_path = Path("Resources/hawaii.sqlite")
engine = create_engine(f"sqlite:///{database_path}")

# Reflect the database tables into ORM classes
Base = automap_base()
Base.prepare(autoload_with=database_path)

# Map the ORM classes to the reflected tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session to interact with the database
db_session = Session(database_path)

#################################################
# Flask Application Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Calculate the date one year ago from the most recent measurement date
latest_date = db_session.query(Measurement.date).order_by(Measurement.date.desc()).first()
latest_date_str = latest_date[0]
latest_date = dt.date(2017, 8, 23)
year_ago = latest_date - dt.timedelta(days=365)

@app.route("/")
def home():
    print("Request received for the 'Home' page.")
    """List all available API routes."""
    return (
        "Available Routes:<br/><br/>"
        "* /api/v1.0/precipitation<br/>"
        "* /api/v1.0/stations<br/>"
        "* /api/v1.0/tobs<br/>"
        "* /api/v1.0/start<br/>"
        "* /api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Retrieve precipitation data for the past year
    precip_data = db_session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    # Format data into a list of dictionaries
    precip_list = [{"date": date, "prcp": prcp} for date, prcp in precip_data]

    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def stations():
    # Retrieve station data
    station_data = db_session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    # Format data into a list of dictionaries
    station_list = [
        {
            "station": station,
            "name": name,
            "latitude": lat,
            "longitude": lng,
            "elevation": elev
        }
        for station, name, lat, lng, elev in station_data
    ]

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temperature_observations():
    # Find the most active station
    most_active_station = db_session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    most_active_station_id = most_active_station[0]

    # Retrieve temperature observations for the past year from the most active station
    temp_data = db_session.query(Measurement.tobs).filter(Measurement.station == most_active_station_id).filter(Measurement.date >= year_ago).all()

    # Format data into a list of dictionaries
    temp_list = [{"date": date, "tobs": tobs} for date, tobs in temp_data]

    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def temperature_stats_start(start):
    # Query temperature statistics from a start date
    stats = db_session.query(
        func.min(Measurement.tobs).label('TMIN'),
        func.max(Measurement.tobs).label('TMAX'),
        func.avg(Measurement.tobs).label('TAVG')
    ).filter(Measurement.date >= start).all()

    # Extract statistics from the query result
    min_temp, avg_temp, max_temp = stats[0]

    return jsonify({
        'TMIN': min_temp,
        'TAVG': avg_temp,
        'TMAX': max_temp
    })

@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_start_end(start, end):
    # Query temperature statistics between start and end dates
    stats = db_session.query(
        func.min(Measurement.tobs).label('TMIN'),
        func.max(Measurement.tobs).label('TMAX'),
        func.avg(Measurement.tobs).label('TAVG')
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Extract statistics from the query result
    min_temp, avg_temp, max_temp = stats[0]

    return jsonify({
        'TMIN': min_temp,
        'TAVG': avg_temp,
        'TMAX': max_temp
    })

# Close the session when the app is stopped
@app.teardown_appcontext
def teardown_session(exception):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)