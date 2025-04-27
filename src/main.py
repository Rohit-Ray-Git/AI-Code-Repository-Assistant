from flask import Flask, request, jsonify
from flask_cors import CORS
from .api.routes import register_routes

app = Flask(__name__)
CORS(app)

# Register routes
register_routes(app)

@app.route("/")
def root():
    return jsonify({"message": "Welcome to AI Code Repository Assistant"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True) 