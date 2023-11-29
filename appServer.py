# ----- Before the import, you should install Flask
# ----- pip install Flask

from flask import Flask, jsonify

app = Flask(__name__)

# ----- Define a simple route
@app.route('/')
def homeSite():
    return 'Hello, World! This is your API server.'

# ----- Define a route with JSON response
@app.route('/api/data', methods=['GET'])
def getData():
    data = {'message': 'Welcome to the API!', 'status': 'success'}
    return jsonify(data)

if __name__ == '__main__':
# ----- Run the application on port 5000
    app.run(debug=True)
