#!/usr/bin/env python3
"""
UDP File Transfer Client - COMPX234 Assignment 4
Client for reliable file download using UDP with stop-and-wait protocol
"""

import socket
import sys
import os
import base64

INITIAL_TIMEOUT = 1000  # milliseconds
MAX_RETRIES = 5
CHUNK_SIZE = 1000


def main():
    if len(sys.argv) != 4:
        print("Usage: python UDPclient.py <hostname> <port> <files_list>")
        sys.exit(1)

    hostname = sys.argv[1]
    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print("Error: Port number must be an integer")
        sys.exit(1)

    files_list = sys.argv[3]

    try:
        with open(files_list, 'r') as f:
            filenames = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Cannot open file list '{files_list}'")
        sys.exit(1)

    if not filenames:
        print("Error: No files to download")
        sys.exit(1)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
