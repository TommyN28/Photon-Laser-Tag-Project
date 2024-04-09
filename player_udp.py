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
    def __init__(self):
        # Initialize the UDP socket for broadcasting
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Initialize the UDP socket for receiving
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.bind(("", RECEIVE_PORT))  # Bind to RECEIVE_PORT for receiving

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
        while True:
            try:
                data, _ = self.receive_socket.recvfrom(RECEIVE_PORT)
                if data.decode("utf-8") == str(START_GAME_CODE):
                    print("Start code received. Generating traffic...")
                    break
            except Exception as e:
                print(f"Error while waiting for start: {e}")

    def start_traffic_generator(self, red_players, green_players):
        traffic_thread = threading.Thread(target=self.generate_traffic, args=(red_players, green_players))
        traffic_thread.start()

    def generate_traffic(self, red_players, green_players):
        counter = 0

        while True:
            try:
                if random.randint(1, 2) == 1:
                    redplayer = random.choice(red_players)
                else:
                    redplayer = random.choice(red_players)

                if random.randint(1, 2) == 1:
                    greenplayer = random.choice(green_players)
                else:
                    greenplayer = random.choice(green_players)

                if random.randint(1, 2) == 1:
                    message = f"{redplayer}:{greenplayer}"
                else:
                    message = f"{greenplayer}:{redplayer}"

                # After 10 iterations, send base hit
                if counter == 10:
                    message = f"{redplayer}:43"
                if counter == 20:
                    message = f"{greenplayer}:53"

                print("Transmitting to game: " + message)

                # Transmit message to game software
                self.broadcast_socket.sendto(message.encode(), CLIENT_ADDRESS_PORT)

                # Receive answer from game software
                data, _ = self.receive_socket.recvfrom(BUFFER_SIZE)
                received_data = data.decode('utf-8')
                print ("Received from game software: " + received_data)
                print ('')

                counter += 1
                if received_data == str(END_GAME_CODE) or counter >= 30:  # End game condition or maximum iterations
                    break
                time.sleep(random.randint(1, 3))

            except Exception as e:
                print("An error occurred:", e)
                break

        print("Traffic generation complete")
    def send_end_code(self):
        end_code = str(END_GAME_CODE).encode()  # Convert integer to bytes
        try:
            for _ in range(3):
                self.broadcast_socket.sendto(end_code, ('<broadcast>', RECEIVE_PORT))
                logging.info("End code 221 sent.")
        except Exception as e:
            logging.error("Failed to send end code 221:", e)
