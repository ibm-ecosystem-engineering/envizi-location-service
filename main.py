import pandas as pd

from datetime import datetime, timedelta
import pandas as pd
import logging
import os
import re
import numpy as np
import shutil

import sys

from src.LocationService import LocationService
from dotenv import load_dotenv

#### Logging Configuration
logging.basicConfig(
    format='%(asctime)s - %(levelname)s:%(message)s',
    handlers=[
        logging.StreamHandler(), #print to console
    ],
    level=logging.INFO
)


def execute_main() :
    print (" Processing Started " )
    load_dotenv()

    file_name = ""
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        print(f"File name : {file_name} ")

        locationService = LocationService()
        locationService.process_main(file_name)
    else:
        print("File name not given.....")

    print (" Processing Completed " )

if __name__ == "__main__":
    execute_main()


