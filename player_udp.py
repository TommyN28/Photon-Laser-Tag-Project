import socket
import logging

class player_udp:
    def __init__(self):
        # Initialize the UDP socket for broadcasting
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Initialize the UDP socket for receiving
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.bind(("", 7501))  # Bind to port 7501 for receiving
        logging.basicConfig(level=logging.INFO)



    def broadcast_equipment_id(self, equipment_id):
        # Broadcast the equipment ID over UDP
        message = str(equipment_id).encode()
        try:
            self.broadcast_socket.sendto(message, ('<broadcast>', 7500))
            logging.info(f"Equipment ID {equipment_id} successfully register.")
        except Exception as e:
            logging.error(f"Failed to broadcast equipment ID {equipment_id}: {e}")
