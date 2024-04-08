import socket
import random
import time
import logging

class PlayerUDP:
    def __init__(self):
        # Initialize the UDP socket for broadcasting
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Initialize the UDP socket for receiving
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.bind(("", 7501))  # Bind to port 7501 for receiving

    def broadcast_equipment_id(self, equipment_id):
        # Broadcast the equipment ID over UDP
        message = str(equipment_id).encode()
        try:
            self.broadcast_socket.sendto(message, ('<broadcast>', 7500))
            logging.info(f"Equipment ID {equipment_id} successfully registered.")
        except Exception as e:
            logging.error(f"Failed to broadcast equipment ID {equipment_id}: {e}")

    def wait_for_start(self):
        print("Waiting for start from game software")
        while True:
            data, _ = self.receive_socket.recvfrom(1024)
            if data.decode("utf-8") == "202":
                print("Start code received. Generating traffic...")
                break

    def generate_traffic(self):
        while True:
            data, _ = self.receive_socket.recvfrom(1024)
            data = data.decode("utf-8")
            transmitter_id, _, receiver_id = data.partition(":")
            if receiver_id == self.equipment_id:
                self.broadcast_socket.sendto(self.equipment_id.encode(), ("<broadcast>", 7500))
            else:
                self.broadcast_socket.sendto(receiver_id.encode(), ("<broadcast>", 7500))
            if transmitter_id == self.equipment_id:
                if self.team_color == "red" and data.endswith(":43"):
                    print("Red base scored!")
                elif self.team_color == "green" and data.endswith(":53"):
                    print("Green base scored!")
            time.sleep(random.randint(1, 3))

# Usage
player = PlayerUDP()

# Get equipment IDs from player entries and broadcast them
red1 = input("Enter equipment ID for red player 1: ")
player.broadcast_equipment_id(red1)

green1 = input("Enter equipment ID for green player 1: ")
player.broadcast_equipment_id(green1)

# Wait for start code and generate traffic
player.wait_for_start()
player.generate_traffic()
