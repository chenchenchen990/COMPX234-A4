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

    try:
        for filename in filenames:
            print(f"\nDownloading file: {filename}")
            download_file(client_socket, hostname, server_port, filename)
        print("\nAll files downloaded successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def download_file(sock, hostname, server_port, filename):
    download_message = f"DOWNLOAD {filename}"

    try:
        response = send_and_receive(sock, hostname, server_port, download_message)
        parts = response.split(" ")

        if len(parts) >= 3 and parts[0] == "ERR" and parts[2] == "NOT_FOUND":
            print(f"Error: File '{filename}' not found on server")
            return

        if (len(parts) == 6 and parts[0] == "OK" and
                parts[2] == "SIZE" and parts[4] == "PORT"):
            file_size = int(parts[3])
            data_port = int(parts[5])
            print(f"File size: {file_size} bytes, Data port: {data_port}")
            download_file_content(sock, hostname, data_port, filename, file_size)
        else:
            print(f"Unexpected response format: {response}")
    except Exception as e:
        print(f"Error downloading file '{filename}': {e}")


def download_file_content(sock, hostname, data_port, filename, file_size):
    try:
        with open(filename, 'wb') as file:
            bytes_downloaded = 0
            print(f"Progress: ", end='', flush=True)

            while bytes_downloaded < file_size:
                start_byte = bytes_downloaded
                end_byte = min(start_byte + CHUNK_SIZE - 1, file_size - 1)
                file_request = f"FILE {filename} GET START {start_byte} END {end_byte}"

                try:
                    response = send_and_receive(sock, hostname, data_port, file_request)

                    if response.startswith(f"FILE {filename} OK START {start_byte} END {end_byte} DATA "):
                        data_start_index = response.find("DATA ") + 5
                        base64_data = response[data_start_index:].strip()
                        file_data = base64.b64decode(base64_data)

                        file.seek(start_byte)
                        file.write(file_data)
                        bytes_downloaded = end_byte + 1
                        print("*", end='', flush=True)
                    else:
                        print(f"\nUnexpected data response: {response[:100]}...")
                        break
                except Exception as e:
                    print(f"\nError receiving data chunk {start_byte}-{end_byte}: {e}")
                    break

            print(f"\nFile '{filename}' downloaded successfully ({bytes_downloaded} bytes)")

            # Send closing request
            close_request = f"FILE {filename} CLOSE"
            try:
                close_response = send_and_receive(sock, hostname, data_port, close_request)
                if close_response == f"FILE {filename} CLOSE_OK":
                    print(f"File '{filename}' transfer completed")
                else:
                    print(f"Unexpected close response: {close_response}")
            except Exception as e:
                print(f"Error sending close request: {e}")

    except Exception as e:
        print(f"Error creating/writing file '{filename}': {e}")


def send_and_receive(sock, hostname, port, message):
    current_timeout = INITIAL_TIMEOUT

    for attempt in range(MAX_RETRIES):
        try:
            sock.settimeout(current_timeout / 1000.0)
            sock.sendto(message.encode(), (hostname, port))

            response_buffer = bytearray(4096)
            bytes_received, server_address = sock.recvfrom_into(response_buffer)
            return response_buffer[:bytes_received].decode().strip()

        except socket.timeout:
            print(f"Timeout on attempt {attempt + 1}, retrying...")
            current_timeout *= 2
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")
            if attempt < MAX_RETRIES - 1:
                current_timeout *= 2

    raise Exception(f"Failed to send/receive after {MAX_RETRIES} attempts")


if __name__ == "__main__":
    main()