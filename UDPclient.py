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
