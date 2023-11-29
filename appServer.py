# ----- Before the import, you should install Flask
# ----- pip install Flask

from flask import Flask, jsonify, render_template

app = Flask(__name__)

# ----- Define a simple route
@app.route('/')
def home():
    return render_template("home.html")

# ----- Route with out JSON response
@app.route("/buenosAires")
def buenosAires():
    return render_template("buenosAires.html")
    
# ----- Route with out JSON response
@app.route("/about")
def about():
    return render_template("about.html")

# ----- Define a route with JSON response
@app.route('/api/data', methods=['GET'])
def getData():
    data = {'message': 'Welcome to the API!', 'status': 'success'}
    return jsonify(data)

if __name__ == '__main__':
# ----- Run the application on port 5000
    app.run(debug=True)
