from flask import jsonify, request
from app import app
from .services import get_weather, get_forecast, get_locations, add_location, remove_location, get_settings, update_settings

@app.route('/api/weather/<location>')
def api_weather(location):
    return jsonify(get_weather(location))

@app.route('/api/forecast/<location>')
def api_forecast(location):
    return jsonify(get_forecast(location))

@app.route('/api/locations')
def api_locations():
    return jsonify(get_locations())

@app.route('/api/locations', methods=['POST'])
def api_add_location():
    data = request.json
    return jsonify(add_location(data))

@app.route('/api/locations/<location>', methods=['DELETE'])
def api_remove_location(location):
    return jsonify(remove_location(location))

@app.route('/api/settings', methods=['GET'])
def api_get_settings():
    return jsonify(get_settings())

@app.route('/api/settings/<setting_name>', methods=['PUT'])
def api_update_settings(setting_name):
    data = request.json
    return jsonify(update_settings(setting_name, data))
