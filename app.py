from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
from datetime import datetime
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/api/stock-data', methods=['POST'])
def get_stock_data():
    try:
        data = request.json
        ticker = data.get('ticker')
        start_date = data.get('startDate')
        end_date = data.get('endDate', datetime.now().strftime('%Y-%m-%d'))
        
        print(f"Fetching data for {ticker} from {start_date} to {end_date}")
        
        stock = yf.Ticker(ticker)
        
        # Get with auto_adjust=True for adjusted close prices
        hist = stock.history(start=start_date, end=end_date, auto_adjust=False)
        
        if hist.empty:
            return jsonify({'error': f'No data found for ticker {ticker}'}), 404
        
        result = []
        for index, row in hist.iterrows():
            result.append({
                'date': index.strftime('%Y-%m-%d'),
                'close': float(row['Close']),  # This is now adjusted close
                'dividend': float(row['Dividends']) if pd.notna(row['Dividends']) else 0.0
            })
        
        print(f"Returning {len(result)} data points")
        
        div_count = sum(1 for r in result if r['dividend'] > 0)
        print(f"Found {div_count} dividend payments")
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)