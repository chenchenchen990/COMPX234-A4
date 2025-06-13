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
