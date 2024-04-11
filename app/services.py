import datetime

import requests
import mysql.connector
from mysql.connector import Error

# Initialize MySQL database connection
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Arons@5849',
        database='locations_db'
    )

    if conn.is_connected():
        print('Connected to MySQL database')

except Error as e:
    print(f"Error connecting to MySQL database: {e}")
    # Handle error or exit the script if connection fails

# Function to retrieve a list of supported locations from the database
def get_locations():
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM locations')
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except Error as e:
        print(f"Error retrieving locations from database: {e}")
        return []

# Function to add a new location to the list of supported locations in the database
def add_location(location_data):
    location_name = location_data.get('name')  # Extract location name from JSON data
    if location_name:
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO locations (name) VALUES (%s)', (location_name,))
            conn.commit()
            return {'message': f'Location "{location_name}" added successfully'}
        except mysql.connector.IntegrityError:
            return {'error': f'Location "{location_name}" already exists'}
        finally:
            cursor.close()  # Close the cursor after use
    else:
        return {'error': 'Location name not provided in the request'}

# Function to remove a location from the list of supported locations in the database
def remove_location(location):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM locations WHERE name = %s', (location,))
        conn.commit()
        if cursor.rowcount > 0:
            return {'message': f'Location "{location}" removed successfully'}
        else:
            return {'error': f'Location "{location}" not found'}
    except Error as e:
        print(f"Error removing location from database: {e}")
        return {'error': f'Unable to remove location "{location}"'}
    finally:
        cursor.close()  # Close the cursor after use

# Close database connection when the module is unloaded
def __del__():
    if conn.is_connected():
        conn.close()
        print('MySQL database connection closed')

# Function to fetch current weather data for a specific location from an external weather API
def get_weather(location):
    api_key = '5d1d25a7eb0f27e31f408dde7b2f718a'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            recorded_time = datetime.datetime.utcfromtimestamp(data['dt']).strftime(
                '%Y-%m-%d %H:%M:%S')  # Convert Unix timestamp to human-readable format
            weather = {
                'location': data['name'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'recorded_time': recorded_time
            }
            return weather
        else:
            return {'error': 'Unable to fetch weather data'}
    except requests.exceptions.RequestException as e:
        return {'error': f'An error occurred: {e}'}

# Function to fetch weather forecast for a specific location from an external weather API
def get_forecast(location):
    api_key = '5d1d25a7eb0f27e31f408dde7b2f718a'
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Extract relevant forecast data (e.g., next 5 days)
            forecast = []
            for item in data['list']:
                timestamp = datetime.datetime.utcfromtimestamp(item['dt']).strftime(
                    '%Y-%m-%d %H:%M:%S')  # Convert Unix timestamp to human-readable format
                forecast.append({
                    'timestamp': timestamp,
                    'temperature': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed']
                })
            return forecast
        else:
            return {'error': 'Unable to fetch forecast data'}
    except requests.exceptions.RequestException as e:
        return {'error': f'An error occurred: {e}'}

def get_settings():
    # Simulated data for current application settings
    current_settings = {
        'units': 'metric',
        'language': 'en',
        'notifications': True
    }
    return current_settings

def update_settings(setting_name, new_value):
    # Simulated logic to update application settings
    current_settings = get_settings()
    if setting_name in current_settings:
        current_settings[setting_name] = new_value
        # Simulated logic to save updated settings to database or configuration file
        # For now, just return the updated settings
        return {'message': f'Setting "{setting_name}" updated successfully', 'new_value': new_value}
    else:
        return {'error': f'Setting "{setting_name}" not found'}
