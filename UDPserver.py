#!/usr/bin/env python3
"""
UDP File Transfer Server - COMPX234 Assignment 4
Multi-threaded server for reliable file transmission over UDP
"""

import socket
import threading
import sys
import os
import base64
import random


def main():
    if len(sys.argv) != 2:
        print("Usage: python UDPserver.py <port_number>")
        sys.exit(1)

    try:
        server_port = int(sys.argv[1])
    except ValueError:
        print("Error: Port number must be an integer")
        sys.exit(1)

    welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        welcome_socket.bind(('', server_port))
        print(f"Server started on port {server_port}")
        print("Waiting for download requests...")

    while True:
        request_buffer = bytearray(1024)
        bytes_received, client_address = welcome_socket.recvfrom_into(request_buffer)
        client_request = request_buffer[:bytes_received].decode().strip()
        print(f"Received: '{client_request}' from {client_address}")

        parts = client_request.split(" ")
        if len(parts) != 2 or parts[0] != "DOWNLOAD":
            print(f"Invalid request from {client_address}, ignoring...")
            continue

        filename = parts[1]
        if not os.path.exists(filename):
            error_message = f"ERR {filename} NOT_FOUND"
            welcome_socket.sendto(error_message.encode(), client_address)
            print(f"File '{filename}' not found, sent error")
            continue

        file_size = os.path.getsize(filename)
        print(f"Creating thread for '{filename}' to {client_address}")
        threading.Thread(target=handle_file_transmission,
                         args=(filename, client_address, file_size)).start()

    except Exception as e:
        print(f"Server error: {e}")
    finally:
        welcome_socket.close()


def handle_file_transmission(filename, client_address, file_size):
    data_port = random.randint(50000, 51000)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        client_socket.bind(('', data_port))
        ok_message = f"OK {filename} SIZE {file_size} PORT {data_port}"
        client_socket.sendto(ok_message.encode(), client_address)
        print(f"Sent OK response: {ok_message}")

    with open(filename, 'rb') as file:
        print(f"File '{filename}' opened for transmission")

        while True:
            request_buffer = bytearray(1024)
            bytes_received, sender_address = client_socket.recvfrom_into(request_buffer)
            client_request = request_buffer[:bytes_received].decode().strip()
            print(f"Thread: Received '{client_request}'")

            parts = client_request.split(" ")

            # Handle close request
            if len(parts) == 3 and parts[0] == "FILE" and parts[2] == "CLOSE":
                close_response = f"FILE {filename} CLOSE_OK"
                client_socket.sendto(close_response.encode(), sender_address)
                print(f"Thread: Sent close confirmation, terminating")
                break

            # Handle data request
            elif (len(parts) == 7 and parts[0] == "FILE" and
                  parts[2] == "GET" and parts[3] == "START" and parts[5] == "END"):
                try:
                    start_byte = int(parts[4])
                    end_byte = int(parts[6])

                if start_byte < 0 or end_byte >= file_size or start_byte > end_byte:
                    print(f"Thread: Invalid byte range {start_byte}-{end_byte}")
                    continue

                bytes_to_read = end_byte - start_byte + 1
                file.seek(start_byte)
                file_data = file.read(bytes_to_read)

                if file_data:
                    base64_data = base64.b64encode(file_data).decode()
                    data_response = f"FILE {filename} OK START {start_byte} END {end_byte} DATA {base64_data}"
                    client_socket.sendto(data_response.encode(), sender_address)
                    print(f"Thread: Sent data block {start_byte}-{end_byte}")

            except (ValueError, IndexError) as e:
                print(f"Thread: Error processing request: {e}")
                continue
        else:
            print(f"Thread: Unknown request format, ignoring")

except Exception as e:
    print(f"Error in file transmission thread: {e}")











