from datetime import datetime, timedelta
import logging
import os, json
import requests

### Static methods
class ApiUtil:
    
    logger = logging.getLogger('ApiUtil')
    logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    @staticmethod
    def _processApiResponse( response):
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            resp = response.json()
        else:
            # Print an error message if the request was not successful
            ApiUtil.logger.error(f"API  : request failed with status code {response.status_code} : {response.text}")
            resp = {}
        return resp


    @staticmethod
    def callAPI(api_url):
        ApiUtil.logger.info(f"----------------------------callAPI : ---------------------------- ")
        ApiUtil.logger.debug(f" url : {api_url}")

        myheaders = {   
            "accept" : "application/json",
            "Content-Type" : "application/json" 
        }

        response = requests.get(api_url, headers=myheaders, verify=False, stream=True)
        resp = ApiUtil._processApiResponse( response)

        ApiUtil.logger.debug(f"---------------------------- Response : " +  json.dumps(resp))
        ApiUtil.logger.debug(f"----------------------------  ---------------------------- ")
        return resp
