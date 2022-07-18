#!/usr/bin/env python3

import requests
import json
import os.path
import logging
import time

dirpath = os.getcwd()
output_path = os.path.join(dirpath,'result.csv')
path = os.path.dirname(os.path.abspath(__file__))  # path where the script is located

url = "https://developer.koodous.com/apks/"
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)      # configuration for logging
required_values = ["sha256","md5","sha1","app","package_name","company","version","size","is_trusted","rating","is_detected","is_corrupted","is_static_analyzed","is_dynamic_analyzed","last_yara_analysis_at"]


def api_request():
    """Send api request and save body of response (= information about 50 mobile applications)"""

    headers = {"Authorization": f"Token {kodoous_api_token}"}
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            break
        else:
            time.sleep(300)
            
    logging.info("Data from koodous has been downloaded")
    list_of_apks_from_koodous = response.json()
    return list_of_apks_from_koodous


def choose_only_malicious_apk(list_of_apks_from_koodous):
    """Choose only apks with a negative raiting or labeled as detected"""

    for apk in list_of_apks_from_koodous["results"]:
        if apk["is_detected"] == True or apk["rating"] < 0:
            save_to_file(apk)
    logging.info(f"Data has been saved to a {output_path} file")

 
def save_to_file(apk):
    """Save information about mobile applications to file"""

    with open(output_path, "a") as f:
        for value in required_values:
            f.write(str(apk[value])+ ',')
        f.write('\n') 


def main():
    logging.info("Script started to run")
    list_of_apks_from_koodous = api_request()
    choose_only_malicious_apk(list_of_apks_from_koodous)
    logging.info("script ended")


if __name__ == "__main__":
    main()