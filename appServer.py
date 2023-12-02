# ----- Before the import, you should install Flask:
# ----- pip install Flask
# ----- pip install plotly
# ----- pip install pandas
# ----- For running the Web server:
# ----- python app.py
# ----- http://127.0.0.1:5000/

from flask import Flask, jsonify, render_template, send_from_directory, request
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import os, requests

# ----- Here we add our Key's CoinGecko API key
# ----- The CoinGecko API allows limited access without an API key
COINGECKO_API_KEY = 'YOUR_API_KEY'
DOGECOIN_ID = 'dogecoin'


app = Flask(__name__)

# ----- Data (Of course generated with ChatGPT)
# ----- Remember when you turn off the server, all the beers that you added desapear

beers = [
  {
    "id": 1,
    "name": "Crafty IPA",
    "description": "A hoppy India Pale Ale with citrus and floral notes."
  },
  {
    "id": 2,
    "name": "Golden Lager",
    "description": "A smooth and crisp lager with a touch of malt sweetness."
  },
  {
    "id": 3,
    "name": "Stout Expedition",
    "description": "A rich and robust stout with hints of chocolate and coffee."
  },
  {
    "id": 4,
    "name": "Wheat Harmony",
    "description": "A refreshing wheat beer with a subtle fruity aroma."
  },
  {
    "id": 5,
    "name": "Amber Ale Elegance",
    "description": "An amber ale with a perfect balance of caramel malt and hop bitterness."
  }
]

# ----- Define a simple route
@app.route('/')
def home():
    return render_template("home.html")
    
# ----- Route with out JSON response
@app.route("/about")
def about():
    return render_template("about.html")

# ----- Route with out JSON response
@app.route("/services")
def services():
    return render_template("services.html")

# ----- Define a route with JSON response
@app.route('/api/data', methods=['GET'])
def getData():
    data = {'message': 'Welcome to the API!', 'status': 'success'}
    return jsonify(data)

# ----- Add our favicon
# ----- Still don't work :( 
@app.route('/favicon')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# ----- Route for serving the logo
@app.route('/logo')
def logo():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'logo.png', mimetype='image/png')

# ----- Endpoint to get all beers
@app.route('/beers', methods=['GET'])
def getBeers():
    return jsonify({'beers': beers})

# ----- Endpoint to get a specific beer by ID
@app.route('/beers/<int:beerId>', methods=['GET'])
def getBeer(beerId):
    beer = next((beer for beer in beers if beer['id'] == beerId), None)
    if beer is None:
        return jsonify({'error': 'Beer not found'}), 404
    return jsonify({'beer': beer})

# ----- Endpoint to create a new Beer
@app.route('/beers', methods=['POST'])
def createBeer():
    if not request.json or 'name' not in request.json or 'description' not in request.json:
        return jsonify({'error': 'Name and Description are required'}), 400

    newBeer = {
        'id': beers[-1]['id'] + 1,
        'name': request.json['name'],
        'description': request.json['description']
    }
    beers.append(newBeer)
    return jsonify({'beer': newBeer}), 201

# ----- Endpoint to update a Beer by ID
@app.route('/beers/<int:beerId>', methods=['PUT'])
def updateBeer(beerId):
    beer = next((beer for beer in beers if beer['id'] == beerId), None)
    if beer is None:
        return jsonify({'error': 'Beer not found'}), 404

    if 'name' in request.json:
        beer['name'] = request.json['name']
    if 'description' in request.json:
        beer['description'] = request.json['description']

    return jsonify({'beer': beer})

# ----- Endpoint to delete a Beer by ID
@app.route('/beers/<int:beerId>', methods=['DELETE'])
def deleteBeer(beerId):
    beer = next((beer for beer in beers if beer['id'] == beerId), None)
    if beer is None:
        return jsonify({'error': 'Beer not found'}), 404

    beers.remove(beer)
    return jsonify({'result': 'Beer deleted successfully'})

# ----- We create a section to see the Dogecoin Price :)
@app.route('/dogecoin')
def dogecoinPrice():
    # ----- Fetch Dogecoin price data from CoinGecko
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={DOGECOIN_ID}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()

    # ----- Extract Dogecoin price
    dogecoinPrice = data[DOGECOIN_ID]['usd']

    return render_template('dogecoin.html', dogecoinPrice=dogecoinPrice)

# ----- We create a section to see the Historical Dogecoin Price :)
@app.route('/dogecoinHistorical')
def dogecoinHistorical():
    try:
        # ----- Fetch historical Dogecoin price data from CoinGecko
        # ----- https://www.coingecko.com/api/documentation
        url = f'https://api.coingecko.com/api/v3/coins/{DOGECOIN_ID}/market_chart?vs_currency=usd&days=7'
        response = requests.get(url)
        # ----- Raise an error for bad responses (4xx or 5xx)
        response.raise_for_status()
        data = response.json()

        # Extract labels (timestamps) and prices from the response
        labels = [point[0] for point in data['prices']]
        prices = [point[1] for point in data['prices']]

        # Create a Plotly line chart
        trace = go.Scatter(x=labels, y=prices, mode='lines+markers', name='Dogecoin Prices (USD)',line=dict(color='blue'))
        layout = go.Layout(title='Dogecoin Historical Prices', xaxis=dict(title='Date (Soon)'), yaxis=dict(title='Price (USD)'))
        chart = go.Figure(data=[trace], layout=layout)
        chart_html = chart.to_html(full_html=False)

        return render_template('dogecoinHistorical.html', chart_html=chart_html)
    except requests.exceptions.RequestException as e:
        app.logger.error(f'Error fetching historical prices: {e}')
        return jsonify({'error': 'Failed to fetch historical prices'}), 500  # Return 500 Internal Server Error

if __name__ == '__main__':
# ----- Run the application on port 5000
    app.run(debug=True)
