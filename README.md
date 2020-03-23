# Distributed Systems coursework:

## Basic info
- This program was written and tested in Python 3.8.2
- The program uses Pyro4 to run this distributed system
- The Pyro name-server will listen on Localhost port number 9090 by default.
- This program supports use by multiple clients at the same time
- It also continue to run even when primary servers quit unexpectedly
- Servers that down suddenly need to be manually restarted

## Requirments to run:
  - python 3.8.2
  - Pyro4 installed
  - port 9090 to be free on localhost
  - an internet connection
  - have installed postcodes.io api. Can install with command **pip install postcodes-io-api**
  
## How to run:
  - First open a terminal in this program's folder. Then run the command **python -m Pyro4.naming** to start the Pyro4 name server.
  - Then open four more terminals in this program's folder and run each of the following commands in a seperate terminal:
    - **python primary_one.py**
    - **python primary_two.py**
    - **python primary_three.py**
    - **python front_end.py**
  - Then open one more terminal that will be used as the interface for the program with the command **python client.py**. 
  - Follow the instructions on this termianl to use the program and see the other terminals for updates on whats happening in each component.
    
