from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers import authenticate 

# Instantiate our Node
app = Flask(__name__)
CORS(app)

# Simple route for basic testing
@app.route('/', methods=['GET'])
def home():
	return "Hello World"

# Unprotected end-point
@app.route('/authenticate', methods=['POST'])
def profile():
	response, code = authenticate_route(request)
	return jsonify(response), code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

