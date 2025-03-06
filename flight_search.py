import requests
import os


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.API_KEY = os.environ.get('FLIGHT_SEARCH_API_KEY')
        self.API_SECRET = os.environ.get('FLIGHT_SEARCH_API_SECRET')
        self.LOCATIONS_ENDPOINT = os.environ.get('FLIGHT_SEARCH_LOCATION_ENDPOINT')
        self.LOWEST_PRICE_ENDPOINT = os.environ.get('FLIGHT_SEARCH_LOWEST_PRICE_ENDPOINT')
        self.token = self._get_access_token()
        self.header = {
            'Authorization': f'Bearer {self.token}'
        }

    def _get_access_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        parameters = {
            'grant_type': 'client_credentials',
            'client_id': self.API_KEY,
            'client_secret': self.API_SECRET
        }

        token_response = requests.post(url='https://test.api.amadeus.com/v1/security/oauth2/token', headers=header,
                                       data=parameters)
        token_response.raise_for_status()

        return token_response.json()['access_token']

    def location_response(self, location_lookup_parameters):
        lookup_response = requests.get(url=self.LOCATIONS_ENDPOINT, headers=self.header,
                                       params=location_lookup_parameters)

        return lookup_response.json()

    def lowest_price_response(self, lowest_price_parameters):
        lowest_price_response = requests.get(url=self.LOWEST_PRICE_ENDPOINT, headers=self.header,
                                             params=lowest_price_parameters)

        return lowest_price_response.json()
