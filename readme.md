# Envizi Location Service

Helps to fill in the `LATITUDE Y` and `LONGITUDE X` columns of the Envizi Setup Config template.

## How to run the application

To run the application follow the below steps. 

### Prerequisite

Python should be available.

### 1 Download the repo

1. Download this repo 

2. Goto to the root folder of the repo.

3. Do the following steps. 

### 2 Create .env file

1. Create `.env` file with the below entries. 

2. Update all the properties accordingly.

```
# Environment variables
LOGLEVEL = INFO

LOCATION_API_URL = "https://api.weather.com/v3/location/search"
LOCATION_API_KEY = ""

OUTPUT_FOLDER = "output"
WRITE_INTERIM_FILES=TRUE
```

### 3  Install python modules

1. Run the below command to create virutal environment and instal the required python modules.
```
python -m venv myvenv
source myvenv/bin/activate

python -m pip install -r requirements.txt
```

### 4  Run the app

1. Runs the below command to start the app. (using the given sample file)

```
python main.py ./data/Envizi_SetupConfig_1_INBank.xlsx
```

### 5  Result

The generated file should be available under the `output` folder with the timesamp.

Ex:
```
/output/results-2024-06-13-213435-730476/Envizi_SetupConfig_1_INBank_result.xlsx
```
