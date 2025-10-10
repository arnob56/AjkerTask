# api/index.py
from app.wsgi import app  # Import your Flask app instance

# Optional test route to verify deployment
@app.route("/ping")
def ping():
    return {"message": "pong"}

# Local run support
if __name__ == "__main__":
    app.run(debug=True)
