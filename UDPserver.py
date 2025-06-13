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