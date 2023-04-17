from flask_mongoengine import MongoEngine
import os

db = MongoEngine()

def init_database(app):
    app.config["MONGODB_SETTINGS"] = {
        "db": "test",
        "host": os.environ.get("DATABASE_URL"),
        "alias": "default",
        "tlsAllowInvalidCertificates": True
    }

    db.init_app(app)
    
    print("MongoDB running")
