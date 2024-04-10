from flask import Flask, request, jsonify
from database import Session
from datetime import datetime

# Import your models here, e.g.
# from models import HealthData

# ...

# Replace this line:
# db = SQLAlchemy(app)

# With this line:
session_factory = Session()
session = session_factory()

# ...

# Replace this line:
# health_data = HealthData(heart_rate=data['heart_rate'], ...)

# With this line:
health_data = HealthData(heart_rate=data['heart_rate'], ..., timestamp=datetime.utcnow())

# Add this line after creating the health_data object:
session.add(health_data)

# Replace this line:
# db.session.commit()

# With this line:
session.commit()

# ...

# Replace this line:
# data = HealthData.query.order_by(HealthData.timestamp.desc()).first()

# With this line:
data = session.query(HealthData).order_by(HealthData.timestamp.desc()).first()

# ...

# Replace this line:
# db.session.delete(health_data)

# With this line:
session.delete(health_data)

# Replace this line:
# db.session.commit()

# With this line:
session.commit()

# ...

# Replace this line:
# session.close()

# With this line:
session.remove()
