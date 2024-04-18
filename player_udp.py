import socket
import random
import time
import logging
from typing import Tuple
import threading

# Defining constants for transmitting and receiving codes
START_GAME_CODE: int = 202
END_GAME_CODE: int = 221
RED_BASE_SCORED_CODE: int = 53
GREEN_BASE_SCORED_CODE: int = 43
BUFFER_SIZE: int = 1024
GAME_TIME_SECONDS: int = 360  # Seconds
SERVER_ADDRESS_PORT: Tuple[str, int] = ("127.0.0.1", 7501)
CLIENT_ADDRESS_PORT: Tuple[str, int] = ("127.0.0.1", 7500)
TRANSMIT_PORT: int = 7501
RECEIVE_PORT: int = 7500

class PlayerUDP:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_done = False
        return cls._instance

    def __init__(self):
        if not self._instance._init_done:
            # Initialize the UDP socket for broadcasting
            self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # Initialize the UDP socket for receiving
            self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.receive_socket.bind(("", RECEIVE_PORT))  # Bind to RECEIVE_PORT for receiving
            self._instance._init_done = True

    def broadcast_equipment_id(self, equipment_id):
        # Broadcast the equipment ID over UDP
        message = str(equipment_id).encode()
        try:
            self.broadcast_socket.sendto(message, ('<broadcast>', RECEIVE_PORT))
            logging.info(f"Equipment ID {equipment_id} successfully registered.")
        except Exception as e:
            logging.error(f"Failed to broadcast equipment ID {equipment_id}: {e}")

    def send_start_code(self):
        # Send code START_GAME_CODE to signal the start of the game
        start_code = str(START_GAME_CODE).encode()  # Convert integer to bytes
        try:
            self.broadcast_socket.sendto(start_code, ('<broadcast>', RECEIVE_PORT))
            logging.info("Start code 202 sent.")
        except Exception as e:
            logging.error("Failed to send start code 202:", e)

    def wait_for_start(self):
        print("Waiting for start from game software")
        self.send_start_code()
        while True:
            try:
                data, _ = self.receive_socket.recvfrom(RECEIVE_PORT)
                if data.decode("utf-8") == str(START_GAME_CODE):
                    print("Start code received. Generating traffic...")
                    break
            except Exception as e:
                print(f"Error while waiting for start: {e}")

    def start_traffic_generator(self, red_players, green_players, callback):
        traffic_thread = threading.Thread(target=self.generate_traffic, args=(red_players, green_players, callback))
        self.wait_for_start()
        traffic_thread.start()

    def generate_traffic(self, red_players, green_players, callback):
        print("Starting traffic generation")
        counter = 0
        while True:
            try:
                # Select random players
                red_player = random.choice(list(red_players.values()))
                green_player = random.choice(list(green_players.values()))

                # Get player names and equipment IDs
                red_player_name = red_player['name']
                green_player_name = green_player['name']
                red_equipment_id = red_player['equipment_id']
                green_equipment_id = green_player['equipment_id']

                # Extract equipment IDs from nested dictionaries
                if isinstance(red_equipment_id, dict):
                    red_equipment_id = red_equipment_id['equipment_id']
                if isinstance(green_equipment_id, dict):
                    green_equipment_id = green_equipment_id['equipment_id']

                # Construct message
                if random.randint(1, 2) == 1:
                    message = f"E ID: {red_equipment_id} Tag E ID: {green_equipment_id}"
                else:
                    message = f"E ID: {green_equipment_id} Tag E ID: {red_equipment_id}"

                # After 10 iterations, broadcast green base scored code with player info
                if counter == 3:
                    message = f"Base scored code: {GREEN_BASE_SCORED_CODE} and player E ID: {red_equipment_id}"

                if counter == 6:
                    message = f"Base scored code: {RED_BASE_SCORED_CODE} and player E ID: {green_equipment_id}"

                # Transmit message to game software
                self.broadcast_socket.sendto(message.encode(), CLIENT_ADDRESS_PORT)

                # Receive answer from game software
                data, _ = self.receive_socket.recvfrom(BUFFER_SIZE)
                received_data = data.decode('utf-8')
                logging.info("Received response from game software: %s", received_data)
                callback(received_data)

                counter += 1
                if received_data == str(END_GAME_CODE):
                    break
                time.sleep(random.randint(1, 3))

            except Exception as e:
                logging.error("An error occurred: %s", e)
                break
        logging.info("Traffic generation complete")

    def send_end_code(self):
        end_code = str(END_GAME_CODE).encode()  # Convert integer to bytes
        try:
            for _ in range(3):
                self.broadcast_socket.sendto(end_code, ('<broadcast>', RECEIVE_PORT))
                logging.info("End code 221 sent.")
        except Exception as e:
            logging.error("Failed to send end code 221:", e)

