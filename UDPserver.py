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