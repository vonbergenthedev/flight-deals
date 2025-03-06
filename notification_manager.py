class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def send_message(self, data_tuple, is_direct_flight):
        # (destination, lowest_price_record['price']['total'], lowest_price_record['departureDate'], lowest_price_record['returnDate'])
        ## TODO Hook to twillio to test
        if is_direct_flight:
            print(
                f'Low price flight alert! Only ${data_tuple[2]} to fly from {data_tuple[0]} to {data_tuple[1]}, on {data_tuple[3]} until {data_tuple[4]}.')
        else:
            print(
                f'Low price NON-DIRECT flight alert! Only ${data_tuple[2]} to fly from {data_tuple[0]} to {data_tuple[1]}, on {data_tuple[3]} until {data_tuple[4]}.')
