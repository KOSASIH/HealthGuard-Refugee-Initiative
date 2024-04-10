from flask import abort

health_data_schema = HealthDataSchema()

@app.route('/health', methods=['GET'])
def get_health_data():
    data = HealthData.query.order_by(HealthData.timestamp.desc()).first()
    if data is None:
        abort(404, description="No health data found")
    return jsonify(health_data_schema.dump(data))

@app.route('/health', methods=['POST'])
def update_health_data():
    data = request.get_json()
    errors = health_data_schema.validate(data)
    if errors:
        abort(400, description=errors)
    health_data = HealthData(heart_rate=data['heart_rate'],
                             blood_pressure=data['blood_pressure'],
                             temperature=data['temperature'])
    db.session.add(health_data)
    db.session.commit()
    return jsonify(health_data_schema.dump(health_data))
