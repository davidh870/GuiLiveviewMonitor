import serial.tools.list_ports
import PySimpleGUI as sg

ports = serial.tools.list_ports.comports() # Reads ports in computer
serialInst = serial.Serial() # Arduino

portList = [] # List of ports



"""
Setup serial connection with Arduino
"""

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



"""
Create GUI for live view data
"""
# Create layout
layout = [
      [sg.Text("Photoresistor Value", key = 'pv')]
]

# Create the window
window = sg.Window("Live View Monitor", layout)


while True:
    # Read serial from arduino
    if serialInst.in_waiting:
        # Read any event (e.g. End program if user closes window)
        event, values = window.read(timeout=1) 
        if event == sg.WIN_CLOSED:
            break

        packet = serialInst.readline()
        window['pv']("Photoresistor Value " + packet.decode('utf'))
        print(packet.decode('utf').rstrip('\n'))

window.close()


