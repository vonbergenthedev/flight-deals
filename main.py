# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.
import time

from data_manager import DataManager
from flight_data import FlightData
from notification_manager import NotificationManager

origin_city_code = 'WAS'
flight_data = FlightData(origin_city_code)
sheet_manager = DataManager()
notification_manager = NotificationManager()

google_sheet_data = sheet_manager.retrieve_sheet_data()


def check_city_code_replace():
    try:
        for city in google_sheet_data['prices']:
            iata_code = city['iataCode']

            if iata_code == '':
                iata_code = flight_data.iata_code_lookup(city['city'])
                new_row_data = {
                    'price': {
                        "iataCode": iata_code,
                    }
                }
                sheet_manager.edit_row_data(row_data_dict=new_row_data, object_id=city['id'])

    except KeyError:
        print('Sheet data not found!')
        print("")


def find_lowest_prices():
    for city in google_sheet_data['prices']:
        destination_code = city['iataCode']
        lowest_price = city['lowestPrice']
        print(f'Checking {origin_city_code} to {destination_code} == {city}')

        lowest_price_data_tuple = flight_data.get_lowest_prices(destination=destination_code,
                                                                starting_lowest_price=lowest_price,
                                                                is_direct=True)
        time.sleep(2)

        if lowest_price_data_tuple is not None:
            notification_manager.send_message(lowest_price_data_tuple, True)
        else:
            print('No direct flight found, checking for flights with stops!')
            lowest_price_data_tuple = flight_data.get_lowest_prices(destination=destination_code,
                                                                    starting_lowest_price=lowest_price,
                                                                    is_direct=False)
            time.sleep(2)

            if lowest_price_data_tuple is not None:
                notification_manager.send_message(lowest_price_data_tuple, False)


# check_city_code_replace()
find_lowest_prices()
