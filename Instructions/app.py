import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"<h3>Available Routes:</h3>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD(start_date)<br/>"
        f"/api/v1.0/YYYY-MM-DD(start_date)/YYYY-MM-DD(end_date)<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)
    return jsonify(all_precip)
###############################################################
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)
###############################################################
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date.desc()).all()
    session.close()
    all_tobs = list(np.ravel(results))
    return jsonify(all_tobs)

###############################################################
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= f"{start}").filter(Measurement.date <= '2017-08-23').all()
    session.close()
    all_start = list(np.ravel(results))
    return jsonify(all_start)

###############################################################
@app.route("/api/v1.0/<start>/<end>")
def end_date(start,end):    
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= f"{start}").filter(Measurement.date <= f"{end}").all()
    session.close()
    all_end = list(np.ravel(results))
    return jsonify(all_end)

if __name__ == '__main__':
    app.run(debug=True)