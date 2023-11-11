import serial.tools.list_ports
import PySimpleGUI as sg

ports = serial.tools.list_ports.comports() # Reads ports in computer
serialInst = serial.Serial() # Arduino


# Iterate through the ports and append to string
portListStrings = "List of Ports:\n"

for port in ports:
    portListStrings += str(port) + '\n'




"""
Create GUI for live view data
"""
# Create layout
portListL = sg.Text(portListStrings)
inputTitleL = sg.Text('Enter Com Port Number', key='-ECPN-')
inputValueL = sg.Input('', enable_events=True, key ='-COMIN-')
comOkButL = sg.Button('Ok', key='-OK-', bind_return_key=True)
pvL = sg.Text("Photoresistor Value", key='-PV-')

layout = [
    [portListL],
    [inputTitleL],
    [inputValueL],  
    [comOkButL],
    [pvL]
]

# Create the window
window = sg.Window("Live View Monitor", layout)


portCreated = False # 

while True:
    # Setup up serial connection of arduino if haven't
    if portCreated == False:
        

        # Ask for port selection
        event, values = window.read(timeout=1)

        if event == sg.WIN_CLOSED:
            break

        # Get user input of com port and setup connection if there is a value in input box
        if event == '-OK-' and len(values['-COMIN-']):
            serialInst.port = 'COM' + str(window['-COMIN-'].get())
            serialInst.baudrate = 9600
            serialInst.open()
            portCreated = True

    # Read serial once connection has been made
    else:
        # Read serial from arduino
        if serialInst.in_waiting:
            # Read any event (e.g. End program if user closes window)
            event, values = window.read(timeout=1) # Add a time out of 1 millisecond to exit of window.read()
            if event == sg.WIN_CLOSED:
                break

            # Retrieve serial packet from arduino and update gui
            packet = serialInst.readline()
            window['-PV-']("Photoresistor Value " + packet.decode('utf'))
            print(packet.decode('utf').rstrip('\n')) # Print to terminal

window.close() # Close window once user closes window and exit program

