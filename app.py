from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from flask_cors import CORS
import os
import json
import threading
import time
from datetime import datetime
import pandas as pd
from Search_Agent import get_apartment_data, save_to_excel
from Classify_Agent import classify_excel_addresses
import logging

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production
CORS(app)

# Global variables to track scraping status
scraping_status = {
    'running': False,
    'progress': 0,
    'message': '',
    'results_file': None,
    'classified_file': None,
    'total_apartments': 0,
    'error': None
}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Main page with the search form."""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def start_search():
    """Start the apartment search process."""
    global scraping_status
    
    if scraping_status['running']:
        return jsonify({'error': 'Search already in progress'}), 400
    
    try:
        # Get form data
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['city', 'state', 'max_price', 'bedroom_types', 'max_pages']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Reset status
        scraping_status = {
            'running': True,
            'progress': 0,
            'message': 'Starting search...',
            'results_file': None,
            'classified_file': None,
            'total_apartments': 0,
            'error': None
        }
        
        # Start scraping in a separate thread
        search_params = {
            'city': data['city'],
            'state': data['state'],
            'max_price': int(data['max_price']),
            'bedroom_types': data['bedroom_types'],
            'max_pages': int(data['max_pages']),
            'openai_key': data.get('openai_key', ''),
            'classify': data.get('classify', False)
        }
        
        thread = threading.Thread(target=run_search, args=(search_params,))
        thread.daemon = True
        thread.start()
        
        return jsonify({'message': 'Search started successfully'})
        
    except Exception as e:
        logger.error(f"Error starting search: {str(e)}")
        scraping_status['running'] = False
        scraping_status['error'] = str(e)
        return jsonify({'error': str(e)}), 500

def update_progress_during_scraping(max_pages):
    """Update progress while scraping is happening."""
    global scraping_status
    
    # Estimate time per page (roughly 10-15 seconds per page)
    estimated_time_per_page = 12
    total_estimated_time = max_pages * estimated_time_per_page
    
    start_time = time.time()
    while scraping_status['running'] and scraping_status['progress'] < 65:
        elapsed_time = time.time() - start_time
        
        # Calculate progress based on estimated time
        if total_estimated_time > 0:
            time_progress = min(elapsed_time / total_estimated_time, 0.8)  # Cap at 80%
            scraping_status['progress'] = int(20 + (time_progress * 45))  # 20% to 65%
        
        # Update message based on estimated page
        estimated_current_page = min(int(elapsed_time / estimated_time_per_page) + 1, max_pages)
        scraping_status['message'] = f'Scraping page {estimated_current_page} of {max_pages}...'
        
        time.sleep(2)  # Update every 2 seconds

def run_search(params):
    """Run the apartment search in a separate thread."""
    global scraping_status
    
    try:
        # Update Search_Agent configuration
        from Search_Agent import TARGET_URL, MAX_PRICE, BED_KEYWORDS, MAX_PAGES
        
        # Construct URL
        city = params['city'].lower().replace(' ', '-')
        state = params['state'].lower()
        target_url = f"https://www.apartments.com/{city}-{state}/"
        
        scraping_status['message'] = f'Searching apartments in {params["city"]}, {params["state"]}...'
        scraping_status['progress'] = 10
        
        # Update global variables (not ideal, but works with current structure)
        import Search_Agent
        Search_Agent.TARGET_URL = target_url
        Search_Agent.MAX_PRICE = params['max_price']
        Search_Agent.BED_KEYWORDS = params['bedroom_types']
        Search_Agent.MAX_PAGES = params['max_pages']
        
        scraping_status['progress'] = 20
        scraping_status['message'] = 'Scraping apartment listings...'
        
        # Start a progress updater thread
        progress_thread = threading.Thread(target=update_progress_during_scraping, args=(params['max_pages'],))
        progress_thread.daemon = True
        progress_thread.start()
        
        # Run the search - this may take several minutes
        apartments = get_apartment_data(target_url, params['max_pages'])
        
        scraping_status['progress'] = 70
        scraping_status['total_apartments'] = len(apartments)
        scraping_status['message'] = f'Found {len(apartments)} apartments. Saving results...'
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_filename = f"apartments_{timestamp}.xlsx"
        save_to_excel(apartments, results_filename)
        scraping_status['results_file'] = results_filename
        
        scraping_status['progress'] = 80
        
        # Run classification if requested
        if params['classify'] and params['openai_key']:
            scraping_status['message'] = 'Classifying apartments by neighborhood...'
            
            # Update Classify_Agent configuration
            import Classify_Agent
            Classify_Agent.API_KEY = params['openai_key']
            Classify_Agent.INPUT_FILE = results_filename
            classified_filename = f"apartments_classified_{timestamp}.xlsx"
            Classify_Agent.OUTPUT_FILE = classified_filename
            
            try:
                classify_excel_addresses()
                scraping_status['classified_file'] = classified_filename
                scraping_status['progress'] = 95
            except Exception as e:
                logger.error(f"Classification error: {str(e)}")
                scraping_status['message'] = f'Search completed, but classification failed: {str(e)}'
        
        scraping_status['progress'] = 100
        scraping_status['message'] = f'Search completed! Found {len(apartments)} apartments.'
        scraping_status['running'] = False
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        scraping_status['running'] = False
        scraping_status['error'] = str(e)
        scraping_status['message'] = f'Search failed: {str(e)}'

@app.route('/status')
def get_status():
    """Get the current search status."""
    return jsonify(scraping_status)

@app.route('/download/<filename>')
def download_file(filename):
    """Download a results file."""
    try:
        if not os.path.exists(filename):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/results')
def view_results():
    """View search results in the browser."""
    try:
        if not scraping_status['results_file'] or not os.path.exists(scraping_status['results_file']):
            return render_template('error.html', error='No results file found')
        
        # Read the Excel file
        df = pd.read_excel(scraping_status['results_file'])
        
        # Convert to HTML table
        table_html = df.to_html(classes='table table-striped table-hover', escape=False, index=False)
        
        return render_template('results.html', 
                             table=table_html, 
                             total_count=len(df),
                             filename=scraping_status['results_file'],
                             classified_file=scraping_status['classified_file'])
    except Exception as e:
        logger.error(f"Results view error: {str(e)}")
        return render_template('error.html', error=str(e))

@app.route('/stop')
def stop_search():
    """Stop the current search (note: this is a simple implementation)."""
    global scraping_status
    scraping_status['running'] = False
    scraping_status['message'] = 'Search stopped by user'
    return jsonify({'message': 'Search stopped'})

@app.route('/test')
def test():
    """Test route to verify the app is working."""
    return '<h1>✅ Apt-Hunter is working!</h1><p><a href="/">Go to main page</a></p>'

if __name__ == '__main__':
    print("=" * 50)
    print("🏠 APT-HUNTER WEB INTERFACE")
    print("=" * 50)
    print("Starting the web interface...")
    print("Open your browser to: http://localhost:5000")
    print("Test page: http://localhost:5000/test")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except Exception as e:
        print(f"Error starting app: {e}")
        print("Try running on a different port or check the troubleshooting guide.")
        input("Press Enter to exit...") 