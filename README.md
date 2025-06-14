# COMPX234-A4: UDP File Transfer System
By Liu Jiachen 20233006445 Assignment 4

## 1. Project Overview
This project implements a **reliable file transfer system** using UDP sockets and multi-threading in Python 3. The system enables clients to download files from a server through an unreliable channel using a stop-and-wait protocol for reliability.

The server handles multiple concurrent clients by creating dedicated threads, while clients download files synchronously with automatic retry mechanisms for network failures.

## 2. Project Structure
```
COMPX234-A4/
├── UDPserver.py          # Multi-threaded UDP file server
├── UDPclient.py          # UDP client with reliable transmission
├── files.txt             # Download file list
├── Server/               # Files to serve
│   ├── 07.pdf           # Test PDF file 1
│   ├── 08.pdf           # Test PDF file 2
│   └── IM-NZ.mov        # Test video file
├── Client/               # Download destination
└── README.md
```

## 3. Requirements
1. Python 3.6 or higher
2. UDP ports 50000-51000 available for data transfer
3. Test files placed in Server directory

## 4. How to Run

### 4.1 Start the Server
```bash
cd Server
python ../UDPserver.py 51234
```
The server will start on port 51234 and wait for download requests.

### 4.2 Run the Client
```bash
cd Client
python ../UDPclient.py localhost 51234 ../files.txt
```
This will connect to the server and download all files listed in files.txt.

### 4.3 Multi-Client Testing
```bash
# Terminal 1
mkdir Client1 && cd Client1
python ../UDPclient.py localhost 51234 ../files.txt

# Terminal 2
mkdir Client2 && cd Client2
python ../UDPclient.py localhost 51234 ../files.txt
```

## 5. Implementation Details

### 5.1 Protocol Format
The system uses a text-based protocol over UDP:

**Download Request:**
```
DOWNLOAD filename
```

**Server Response:**
```
OK filename SIZE size_bytes PORT port_number
ERR filename NOT_FOUND
```

**Data Transfer:**
```
FILE filename GET START start_byte END end_byte
FILE filename OK START start_byte END end_byte DATA base64_data
```

**Connection Termination:**
```
FILE filename CLOSE
FILE filename CLOSE_OK
```

### 5.2 Server Implementation
1. **Multi-threading Architecture**
   - Welcome socket listens for DOWNLOAD requests
   - Each client gets dedicated thread with random port (50000-51000)
   - Thread-safe operations without shared data

2. **File Handling**
   - Binary file reading with seek/read operations
   - Base64 encoding for reliable transmission
   - Chunk size: 1000 bytes maximum

3. **Error Management**
   - File existence validation
   - Invalid request handling
   - Resource cleanup and thread termination

### 5.3 Client Implementation
1. **Reliable Transmission**
   - Stop-and-wait protocol with acknowledgments
   - Exponential backoff retry (5 attempts, 1s initial timeout)
   - Automatic timeout doubling on failures

2. **File Operations**
   - Sequential file downloads from file list
   - Random access writing with seek operations
   - Progress tracking with visual indicators

3. **Error Recovery**
   - Network timeout handling
   - Server error response processing
   - Graceful failure recovery

## 6. Development Process

### 6.1 Understanding Requirements
1. Analyzed UDP unreliability challenges and stop-and-wait solutions
2. Studied multi-threading requirements for concurrent clients
3. Identified Base64 encoding necessity for binary data
4. Understood chunk-based transmission approach

### 6.2 Server Development
1. Implemented welcome socket for initial requests
2. Created thread spawning mechanism for client handling
3. Added random port allocation and data socket creation
4. Implemented file reading and Base64 encoding
5. Added proper error handling and resource cleanup

### 6.3 Client Development
1. Created command-line argument parsing and validation
2. Implemented file list reading and processing
3. Added reliable send-and-receive function with timeouts
4. Created chunked file download with progress tracking
5. Implemented connection termination protocol

### 6.4 Testing and Validation
1. Single file download verification
2. Multiple file sequential download testing
3. Concurrent multi-client testing
4. Network failure simulation and recovery
5. File integrity verification using MD5 checksums

## 7. Sample Output

### 7.1 Server Output
```
Server started on port 51234
Waiting for download requests...
Received: 'DOWNLOAD 07.pdf' from ('127.0.0.1', 54321)
Creating thread for '07.pdf' to ('127.0.0.1', 54321)
Sent OK response: OK 07.pdf SIZE 2847 PORT 50234
File '07.pdf' opened for transmission
Thread: Received 'FILE 07.pdf GET START 0 END 999'
Thread: Sent data block 0-999
Thread: Received 'FILE 07.pdf GET START 1000 END 1999'
Thread: Sent data block 1000-1999
Thread: Received 'FILE 07.pdf CLOSE'
Thread: Sent close confirmation, terminating
```

### 7.2 Client Output
```
Downloading file: 07.pdf
File size: 2847 bytes, Data port: 50234
Progress: ***
File '07.pdf' downloaded successfully (2847 bytes)
File '07.pdf' transfer completed

Downloading file: 08.pdf
File size: 3921 bytes, Data port: 50567
Progress: ****
File '08.pdf' downloaded successfully (3921 bytes)
File '08.pdf' transfer completed

All files downloaded successfully!
```

## 8. Implementation Challenges

### 8.1 Reliable Transmission over UDP
1. Implemented timeout and retry mechanisms for packet loss
2. Used stop-and-wait protocol to ensure data integrity
3. Added exponential backoff to handle network congestion
4. Ensured proper sequence control with byte ranges

### 8.2 Multi-threading and Concurrency
1. Created thread-safe server architecture without shared data
2. Implemented proper resource cleanup for thread termination
3. Used random port allocation to avoid conflicts
4. Handled concurrent client connections efficiently

### 8.3 Binary Data Transmission
1. Used Base64 encoding to transmit binary files over text protocol
2. Implemented chunked transmission for large files
3. Added proper file positioning with seek operations
4. Ensured data integrity through encoding/decoding process

## 9. Verification and Validation

### 9.1 Testing Results
The implementation successfully passes all requirements:
1. Multiple file downloads complete successfully
2. Concurrent clients operate without interference
3. Network failures are handled gracefully with automatic recovery
4. File integrity verified through MD5 checksum comparison
5. Progress indicators provide real-time feedback

### 9.2 Performance Metrics
- **Code Size**: Server ~105 LoC, Client ~130 LoC
- **Chunk Size**: 1000 bytes (optimal for UDP)
- **Encoding Overhead**: ~33% due to Base64
- **Concurrent Capacity**: Up to 1000 clients (port range limit)
- **Recovery Time**: 1-32 seconds depending on network conditions

### 9.3 Protocol Compliance
1. All message formats follow specification exactly
2. Stop-and-wait acknowledgment implemented correctly
3. Error handling aligns with protocol requirements
4. Thread creation and port allocation work as specified

## 10. Conclusion
This implementation successfully demonstrates reliable file transfer over an unreliable UDP channel using stop-and-wait protocol. The multi-threaded server architecture enables scalable concurrent client handling, while the client's retry mechanisms ensure robust operation despite network unreliability. The system meets all assignment requirements and handles real-world network conditions effectively.
