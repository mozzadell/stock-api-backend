from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route('/api/stock-data', methods=['POST'])
def get_stock_data():
    try:
        data = request.json
        ticker = data.get('ticker')
        start_date = data.get('startDate')
        end_date = data.get('endDate', datetime.now().strftime('%Y-%m-%d'))
        
        print(f"Fetching data for {ticker} from {start_date} to {end_date}")
        
        # Fetch stock data using yfinance
        stock = yf.Ticker(ticker)
        
        # Get historical data with dividends and stock splits
        hist = stock.history(start=start_date, end=end_date, actions=True)
        
        if hist.empty:
            return jsonify({'error': f'No data found for ticker {ticker}'}), 404
        
        # Format data for frontend
        result = []
        for date, row in hist.iterrows():
            result.append({
                'date': date.strftime('%Y-%m-%d'),
                'close': float(row['Close']),
                'dividend': float(row.get('Dividends', 0))
            })
        
        print(f"Returning {len(result)} data points")
        return jsonify(result)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)