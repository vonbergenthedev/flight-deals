import os
import requests


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.SHEETY_AUTH_KEY = os.environ.get("SHEETY_AUTH_KEY")
        self.SHEETY_ENDPOINT = os.environ.get('SHEETY_ENDPOINT')
        self.sheety_header = {
            'Authorization': self.SHEETY_AUTH_KEY
        }

    def retrieve_sheet_data(self):
        retrieve_sheet_endpoint = self.SHEETY_ENDPOINT
        retrieve_sheet_response = requests.get(url=retrieve_sheet_endpoint, headers=self.sheety_header)
        json_data = retrieve_sheet_response.json()

        return json_data

    def edit_row_data(self, row_data_dict, object_id):
        edit_row_endpoint = f'{self.SHEETY_ENDPOINT}/{object_id}'
        requests.put(url=edit_row_endpoint, headers=self.sheety_header, json=row_data_dict)
