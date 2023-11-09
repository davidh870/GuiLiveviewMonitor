import serial.tools.list_ports

ports = serial.tools.list_ports.comports() # Reads ports in computer
serialInst = serial.Serial() # Arduino

portList = [] # List of ports

# Iterate through the ports and append to list
print("List of Ports:")
for port in ports:
    portList.append(str(port)) 
    print(str(port))

# Ask for port selection
portSelected = input("Select Port: COM")

for x in range(0, len(portList)):
        if portList[x].startswith("COM" + str(portSelected)):
              portSelected = "COM" + str(portSelected) # Update to correct port
              print("Port Selected: " + portList[x])


# Setup up serial connection of arduino
serialInst.baudrate = 9600
serialInst.port = portSelected
serialInst.open()


# Read serial from arduino
while True:
    if serialInst.in_waiting:
          packet = serialInst.readline()
          print(packet.decode('utf').rstrip('\n'))


# Create GUI for live view data