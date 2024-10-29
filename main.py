
from flask import Flask, request, jsonify, render_template, send_file
import logging
import os
from src.LocationService import LocationService
from dotenv import load_dotenv
import pandas as pd

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# Load environment variables
load_dotenv()

#### Logging Configuration
logging.basicConfig(
    format='%(asctime)s - %(levelname)s:%(message)s',
    handlers=[
        logging.StreamHandler(),  # print to console
    ],
    level=logging.INFO
)

@app.route('/')
def index():
    print("main home page")
    return render_template('index.html')


@app.route('/index', methods=['POST'])
def execute_main():
    print("Processing Started")
    
    # Check if a file was uploaded
    if 'uploadFile' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    # Get the uploaded file
    file = request.files['uploadFile']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file to the 'data' folder
    file_path = os.path.join('data', file.filename)
    file.save(file_path)

    print(f"File saved to: {file_path}")

    # Process the file (using LocationService)
    locationService = LocationService()
    output_file = locationService.process_main(file_path)
    print("returned from location service process_main function = ",output_file)

    print("Processing Completed")

    df = pd.read_excel(output_file)
    table_data = df.to_html(index=False, na_rep='')
    
    return {    "message": "Processing completed successfully",
                "file_name":output_file,
                "table_data":table_data}


@app.route('/download', methods=['GET'])
def download_file():
    # Get the file path from query parameters
    file_path = request.args.get('file_path')
    
    if file_path:
        # Serve the file for download
        return send_file(file_path, as_attachment=True)
    else:
        return "No file specified", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
