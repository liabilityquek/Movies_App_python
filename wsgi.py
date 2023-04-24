from app import app
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    host = os.getenv('HOST', '0.0.0.0')
    app.run(host=host)
