from app import app, db
from flask import render_template, jsonify, request
from app.models import Divvy
from sqlalchemy.sql import func
import datetime


@app.route('/calculate')
def calculate():
  start = request.args.get('start') or datetime.datetime.now()
  end = request.args.get('end') or datetime.datetime.now()
  from_station_id = request.args.get('from_station_id')
  if(from_station_id):
    stationid = Divvy.query.filter(Divvy.from_station_id == from_station_id).all()
    if len(stationid) > 0:
      result = Divvy.query.with_entities(func.avg(Divvy.trip_duration)).filter(Divvy.starttime >= start, Divvy.stoptime <= end, Divvy.from_station_id == from_station_id).one()
      return jsonify({ "averageDuration": float(result[0] or 0), "fromStationId" : from_station_id, "fromStationName": Divvy.query.filter(Divvy.from_station_id == from_station_id).first().from_station_name})
    else:
      return "Invalid Station ID"
  else:
    dates = Divvy.query.filter(Divvy.starttime >= start, Divvy.stoptime <= end).all()
    if len(dates) > 0:
      result = Divvy.query.with_entities(func.avg(Divvy.trip_duration)).filter(Divvy.starttime >= start, Divvy.stoptime <= end).one()
      return jsonify({ "averageDuration": float(result[0] or 0)})
    else:
      return "Date out of range"
  
  