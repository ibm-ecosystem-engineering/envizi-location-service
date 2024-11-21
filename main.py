
from flask import Flask, request, jsonify, render_template, send_file
import logging
import os
from src.LocationService import LocationService
from src.LoginService import LoginService

from dotenv import load_dotenv
import pandas as pd

from flask_httpauth import HTTPBasicAuth

# Initialize Flask app
app = Flask(__name__, static_folder='static')
auth = HTTPBasicAuth()

# Load environment variables
load_dotenv()

#### Logging Configuration
logging.basicConfig(
    format='%(asctime)s - %(levelname)s:%(message)s',
    handlers=[
        logging.StreamHandler(),  # print to console
    ],
)

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

@auth.verify_password
def verify_password(username, password):
    loginService = LoginService()
    result = loginService.verifyLogin(username, password)        
    return result


@app.route('/')
@auth.login_required
def index():
    logger.info("main home page")
    return render_template('index.html')

@app.route('/hello')
@auth.login_required
def hello():
    return "hello", 200

@app.route('/index', methods=['POST'])
def execute_main():
    logger.info("Processing Started")

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

    logger.info(f"File saved to: {file_path}")

    # Process the file (using LocationService)
    locationService = LocationService()
    output_file = locationService.process_main(file_path)
    logger.info(f"Output file = {output_file} ")

    logger.info("Processing Completed")

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
    app.run(host='0.0.0.0', port=3001, debug=False)
