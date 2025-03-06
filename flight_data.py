from flight_search import FlightSearch
import datetime
import pandas


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, origin_point):
        self.origin = origin_point
        self.search = FlightSearch()
        self.today_date = datetime.date.today()

    def iata_code_lookup(self, city):

        lookup_parameters = {
            'subType': 'CITY',
            'keyword': f'{city}',
            'view': 'LIGHT',
        }

        city_json_data = self.search.location_response(lookup_parameters)

        try:
            iataCode = city_json_data['data'][0]['iataCode']
        except IndexError:
            iataCode = 'Not Found in FlightSearch API DATA'

        return iataCode

    def get_lowest_prices(self, destination, starting_lowest_price, is_direct=True):

        if destination != 'Not Found in FlightSearch API DATA':

            lowest_price_parameters = {
                'origin': self.origin,
                'destination': destination,
                'departureDate': f'{self.today_date + datetime.timedelta(days=1)},{self.today_date + datetime.timedelta(days=180)}',
                'nonStop': is_direct,
                'viewBy': 'WEEK'
            }

            lowest_prices_json = self.search.lowest_price_response(lowest_price_parameters)

            if 'errors' in lowest_prices_json.keys():
                # print(f'{lowest_prices_json['errors'][0]['detail']}')
                pass

            else:
                df = pandas.DataFrame(lowest_prices_json['data'])
                # with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
                #     print(df)

                lowest_price_index = 0
                current_index = 0
                lowest_price = starting_lowest_price
                lowest_price_found = False

                for item in df['price']:
                    current_flight_price = float(item['total'])

                    if lowest_price > current_flight_price:
                        lowest_price = current_flight_price
                        lowest_price_index = current_index
                        lowest_price_found = True

                    current_index += 1

                if lowest_price_found:
                    lowest_price_record = df.iloc[lowest_price_index]

                    return lowest_price_record['origin'], lowest_price_record['destination'], \
                    lowest_price_record['price']['total'], lowest_price_record[
                        'departureDate'], \
                        lowest_price_record['returnDate']

                else:
                    return None

        else:
            print("Skipping due to unsearchable value.")
