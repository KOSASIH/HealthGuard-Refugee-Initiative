from flask import Flask, request, jsonify
from datetime import datetime
from database import session_factory, HealthData

app = Flask(__name__)

# Create a route for the root endpoint
@app.route('/')
def index():
    return "Welcome to the HealthGuard Refugee Initiative backend!"

# Create a route for the health data endpoint
@app.route('/health', methods=['GET'])
def get_health_data():
    # Retrieve the most recent health data from the database
    data = session_factory().query(HealthData).order_by(HealthData.timestamp.desc()).first()
    if data is None:
        return jsonify({"error": "No health data found"}), 404

    # Serialize the health data as JSON
    health_data = {
        "heart_rate": data.heart_rate,
        "blood_pressure": data.blood_pressure,
        "temperature": data.temperature,
        "timestamp": data.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(health_data)

# Create a route for updating health data
@app.route('/health', methods=['POST'])
def update_health_data():
    # Validate the request data
    data = request.get_json()
    if not data or 'heart_rate' not in data or 'blood_pressure' not in data or 'temperature' not in data:
        return jsonify({"error": "Invalid request data"}), 400

    # Create a new health data object
    health_data = HealthData(heart_rate=data['heart_rate'],
                             blood_pressure=data['blood_pressure'],
                             temperature=data['temperature'],
                             timestamp=datetime.utcnow())

    # Add the health data object to the database session
    session_factory().add(health_data)

    # Commit the transaction
    session_factory().commit()

    # Serialize the health data as JSON
    health_data = {
        "heart_rate": health_data.heart_rate,
        "blood_pressure": health_data.blood_pressure,
        "temperature": health_data.temperature,
        "timestamp": health_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(health_data), 201

# Create a route for deleting health data
@app.route('/health', methods=['DELETE'])
def delete_health_data():
    # Retrieve the most recent health data from the database
    data = session_factory().query(HealthData).order_by(HealthData.timestamp.desc()).first()
    if data is None:
        return jsonify({"error": "No health data found"}), 404

    # Delete the health data object from the database session
    session_factory().delete(data)

    # Commit the transaction
    session_factory().commit()

    return jsonify({"message": "Health data deleted"})

# Close the database session when the application shuts down
@app.teardown_appcontext
def shutdown_session(exception=None):
    session_factory().remove()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
