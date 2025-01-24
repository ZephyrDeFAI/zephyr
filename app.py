from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Import routes
from routes import auth_routes, model_routes, data_routes

# Register blueprints
app.register_blueprint(auth_routes.bp)
app.register_blueprint(model_routes.bp)
app.register_blueprint(data_routes.bp)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
