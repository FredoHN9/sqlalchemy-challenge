# Climate Data Analysis and API with SQLAlchemy, Matplotlib, and Flask

## Overview

This project involves analyzing climate data from a SQLite database using SQLAlchemy for database interaction, Matplotlib for data visualization, and Flask for creating a RESTful API. The data includes precipitation and temperature observations from various weather stations in Hawaii.

## Features

1. **Database Setup**: Connect to a SQLite database and reflect its tables using SQLAlchemy.
2. **Exploratory Precipitation Analysis**: Retrieve and analyze precipitation data.
3. **Exploratory Station Analysis**: Analyze data from weather stations including finding the most active stations and their temperature statistics.
4. **Data Visualization**: Plot precipitation and temperature data using Matplotlib.
5. **Database Operations**: Insert new data and list tables within the database using SQLite.
6. **RESTful API**: Create a Flask application to serve climate data through various API endpoints.

## How It Works

### Database Setup

1. **Connect to Database**: Use SQLAlchemy to connect to the `hawaii.sqlite` database.
2. **Reflect Tables**: Reflect the database tables into SQLAlchemy ORM classes for easy querying.

### Exploratory Precipitation Analysis

1. **Retrieve Precipitation Data**: Query the last 12 months of precipitation data from the most recent date in the dataset.
2. **Store in DataFrame**: Save the query results into a Pandas DataFrame.
3. **Plot Data**: Plot the precipitation data using Matplotlib.
4. **Summary Statistics**: Calculate summary statistics for the precipitation data.

### Exploratory Station Analysis

1. **Total Number of Stations**: Query the total number of weather stations in the dataset.
2. **Most Active Stations**: Identify the most active stations by counting the number of observations for each station.
3. **Temperature Statistics**: Calculate the lowest, highest, and average temperature for the most active station.
4. **Temperature Histogram**: Query the last 12 months of temperature data for the most active station and plot a histogram.

### Data Visualization

1. **Plot Precipitation Data**: Create a line plot for precipitation data over the last 12 months.
2. **Plot Temperature Data**: Create a histogram for temperature observations from the most active station.

### Database Operations

1. **List Tables**: List all tables in the SQLite database.
2. **Insert Example Data**: Insert new example data into the `measurement` and `station` tables.
3. **Commit Changes**: Commit the changes to the database and close the connection.

### RESTful API

1. **Flask Application Setup**: Set up a Flask application to serve the climate data.
2. **API Endpoints**:
    - `/api/v1.0/precipitation`: Retrieve precipitation data for the past year.
    - `/api/v1.0/stations`: Retrieve data for all weather stations.
    - `/api/v1.0/tobs`: Retrieve temperature observations for the past year from the most active station.
    - `/api/v1.0/<start>`: Retrieve temperature statistics from a start date.
    - `/api/v1.0/<start>/<end>`: Retrieve temperature statistics between start and end dates.

## Usage

To use this code:
1. Ensure you have the necessary Python packages installed: `SQLAlchemy`, `Pandas`, `Matplotlib`, `Flask`, and `SQLite3`.
2. Place the `hawaii.sqlite` database file in the `Resources` directory.
3. Execute the code in a Python environment that supports Flask and inline plotting with Matplotlib.

## Code Execution

### Database Setup

```python
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Map the classes
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)
