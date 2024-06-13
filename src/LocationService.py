import pandas as pd

from datetime import datetime, timedelta
import pandas as pd
import logging
import os
import json
from src.ApiUtil import ApiUtil
from src.FileUtil import FileUtil
from src.DictionaryUtil import DictionaryUtil
from dotenv import load_dotenv

from src.CommonConstants import *

class LocationService :

    def __init__(self):
        load_dotenv()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

        self.LOCATION_API_URL = os.getenv("LOCATION_API_URL", None)
        self.LOCATION_API_KEY = os.getenv("LOCATION_API_KEY", None)

        self.fileUtil = FileUtil()
        self.fileUtil.start()

    def process_main(self, input_file):
        self.logger.info(f"==================================================================================================================================")
        self.logger.info(f"process_main  stated ... ")

        ### Copy the source file
        self.fileUtil.copy_file(input_file)

        ### file name and extension split
        file_name_with_extension = self.fileUtil.extractFilename(input_file)
        file_name_only, file_entension = self.fileUtil.split_filename_and_extension(file_name_with_extension)

        ### Identify the template type from file name.
        template_type = TEMPLATE_1_SETUP_CONFIG
        sheet_name = TEMPLATE_1_SETUP_CONFIG_SHEET_NAME
        if file_name_only.startswith(TEMPLATE_1_SETUP_CONFIG_FILE_PREFIX) :
            template_type = TEMPLATE_1_SETUP_CONFIG
            sheet_name = TEMPLATE_1_SETUP_CONFIG_SHEET_NAME
        elif file_name_only.startswith(TEMPLATE_2_SETUP_LOCATION_FILE_PREFIX) :
            template_type = TEMPLATE_2_SETUP_LOCATION
            sheet_name = TEMPLATE_2_SETUP_LOCATION_SHEET_NAME

        ### frame output file name
        ouput_file = self.fileUtil.getFileNameWithoutCounter(file_name_only + "_result" + file_entension)

        ### Logs
        self.logger.info(f"process_main  input_file : {input_file} ")
        self.logger.info(f"process_main  ouput_file : {ouput_file} ")
        self.logger.debug(f"process_main  file_name_with_extension : {file_name_with_extension} ")
        self.logger.debug(f"process_main  file_name_only : {file_name_only} ")
        self.logger.debug(f"process_main  file_entension : {file_entension} ")
        self.logger.debug(f"process_main  template_type : {template_type} ")

        ### Process the excel
        self.process_excel(input_file, ouput_file, template_type, sheet_name)

        self.logger.info(f"process_main  completed ... ")
        self.logger.info(f"==================================================================================================================================")
        return 0

    def process_excel(self, input_file, ouput_file, template_type, sheet_name):
        self.logger.info(f"process_excel  stated ... ")
        try:
            # Read the Excel file
            df = pd.read_excel(input_file)

            # Iterate over each row in the DataFrame
            processed_data = []
            for index, row in df.iterrows():
                self.process_row (row, template_type)
                processed_data.append(row)

            # Write the processed data to a new Excel file
            self.generateExcel(ouput_file, processed_data, sheet_name)

        except FileNotFoundError:
            print(f"process_excel : Error: The file '{input_file}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

        self.logger.info(f"process_excel  Completed ... ")

    ### Process each row of the excel
    def process_row(self, row, template_type):
        self.logger.debug(f"process_row  stated ... ")
        self.logger.debug(f"process_row  row : {row}")

        ### combine the address fields.
        address_text = ""
        try :
            if template_type == TEMPLATE_1_SETUP_CONFIG :
                address_text = self.check_and_append("", row['STREET ADDRESS'])
                address_text = self.check_and_append(address_text, row['CITY'])
                address_text = self.check_and_append(address_text, row['STATE PROVINCE'])
                address_text = self.check_and_append(address_text, row['POSTAL CODE'])
                address_text = self.check_and_append(address_text, row['COUNTRY'])
            elif template_type == TEMPLATE_2_SETUP_LOCATION :
                address_text = self.check_and_append("", row['STREET ADDRESS'])
                address_text = self.check_and_append(address_text, row['ADDRESS'])
                address_text = self.check_and_append(address_text, row['STATE PROVINCE'])
                address_text = self.check_and_append(address_text, row['POSTAL CODE'])
                address_text = self.check_and_append(address_text, row['COUNTRY'])
        except Exception as e:
            self.logger.info(f"process_row  error occured... ", e)

        ### frame the URL
        url = f"{self.LOCATION_API_URL}?query={address_text}&locationType=address&language=en-US&format=json&apiKey={self.LOCATION_API_KEY}"
        self.logger.info(f"----------------------------------------------------")
        self.logger.info(f"process_row  URL : {url}")
        self.logger.info(f"process_row  address_text : {address_text}")

        ### Call the API
        response = ApiUtil.callAPI(url)
        self.fileUtil.writeInFileWithCounter("api_response.json", json.dumps(response))

        ### extract the longitude and latitude from API Response
        latitude = DictionaryUtil.findValue(response, "location.latitude[1]")
        longitude = DictionaryUtil.findValue(response, "location.longitude[1]")

        self.logger.info(f"process_row  latitude : {latitude}")
        self.logger.info(f"process_row  longitude : {longitude}")
        self.logger.debug(f"----------------------------------------------------")

        ### Update the excel row with the retrieved LATITUDE and LONGITUDE
        if template_type == TEMPLATE_1_SETUP_CONFIG :
            row['LATITUDE Y'] = latitude
            row['LONGITUDE X'] = longitude
        elif template_type == TEMPLATE_2_SETUP_LOCATION :
            row['LATITUDE Y'] = latitude
            row['LONGITUDE X'] = longitude

        self.logger.debug(f"process_row  completed ... ")
        return row

    ### Save Excel file
    def generateExcel(self, file_name, myData, sheet_name):
        df = pd.DataFrame(myData)
        try:
            excel_writer = pd.ExcelWriter(file_name, engine='openpyxl')
            df.to_excel(excel_writer, sheet_name=sheet_name, index=False)
            excel_writer.save()
            self.logger.info(f"The output file is created and available as : {file_name} ")
        except FileNotFoundError:
            print(f"Error: The file '{file_name}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    ### Make a comma separated text for combining the address fields
    def check_and_append(self, input_string, append_string):
        result = input_string
        if (not pd.isna(append_string)) :
            if input_string is None or input_string == "":
                result = str(append_string)
            else:
                result = input_string + "," + str(append_string)
        return result