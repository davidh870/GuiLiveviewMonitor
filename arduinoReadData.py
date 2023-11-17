import serial.tools.list_ports
import PySimpleGUI as sg

ports = serial.tools.list_ports.comports() # Reads ports in computer
serialInst = serial.Serial() # Arduino



"""""""""""""""""""""""""""""""""""""""""
Create COM PORT LIST AND STRINGS 
"""""""""""""""""""""""""""""""""""""""""
# Iterate through the ports and append to string
portListStrings = "List of Ports:\n"
portNumList = []

for port in ports:
    portNumList.append(str(port)[3])
    portListStrings += str(port) + '\n'
""""""""""""""""""""""""""""""""""""""""""


"""""""""""""""""""""""""""""""""""""""""
Create GUI for live view data
"""""""""""""""""""""""""""""""""""""""""
# Create layout
layout = [
    [sg.Text(portListStrings, key='-PORTLIST-')],
    [sg.Text('Enter Com Port Number', key='-ECPN-'), sg.Combo(portNumList, key='-COMLIST-')],  
    [sg.Button('Ok', key='-OK-', bind_return_key=True)],
    [sg.Text("Photoresistor Value", key='-PV-', visible=False)]
]


# Create the window
window = sg.Window("Live View Monitor", layout)
""""""""""""""""""""""""""""""""""""""""""




# Flag to check if connection with ardiuno has been made
portCreated = False # 

while True:
    # Setup up serial connection of arduino if haven't
    if portCreated == False:
        event, values = window.read(timeout=1)

        if event == sg.WIN_CLOSED:
            break

        # Get user input of com port and setup connection if there is a item selected in com port list
        if event == '-OK-' and len(str(window['-COMLIST-'].get())):
            serialInst.port = 'COM' + str(window['-COMLIST-'].get())
            serialInst.baudrate = 9600
            serialInst.open()
            portCreated = True

            # Clear out gui to only display live data from arduino
            window['-ECPN-'].update(visible=False)
            window['-COMLIST-'].update(disabled=True, visible=False)
            window['-OK-'].update(disabled=True, visible=False)
            window['-PV-'].update(visible=True)


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

