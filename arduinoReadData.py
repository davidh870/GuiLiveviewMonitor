import serial.tools.list_ports
import PySimpleGUI as sg
import pandas as pd
import time 
import xlsxwriter

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

# Graph design and data
GRAPH_SIZE_X = 400
GRAPH_SIZE_Y = 1000
X_VALUE = 0
Y_VALUE = 0
PREV_X_VALUE = 0
PREV_Y_VALUE = 0




# Create layout
layout = [
    [sg.Text(portListStrings, key='-PORTLIST-')],
    [sg.Text('Select Com Port Number', key='-SCPN-'), sg.Combo(portNumList, key='-COMLIST-')],  
    [sg.Button('Ok', key='-OK-', bind_return_key=True)],
    [sg.Text("Live Photoresistor Value", key='-PV-', visible=False)],
    [sg.Graph(canvas_size=(GRAPH_SIZE_X, GRAPH_SIZE_Y), graph_bottom_left=(0,0), graph_top_right=(GRAPH_SIZE_X, GRAPH_SIZE_Y), background_color='white', key='-GRAPH-')],
    [sg.Button('Record', key='-RECORD-', visible=False), sg.Button('Stop', key='-STOP-', visible=False, disabled=True)]
]

# Create the window
window = sg.Window("Live View Monitor", layout)
""""""""""""""""""""""""""""""""""""""""""




"""""""""""""""""""""""""""""""""""""""""
EXCEL FILE FOR DATA LOG
"""""""""""""""""""""""""""""""""""""""""
# Function to create and return a new excel file everytime Record button is pressed
def createExcelFile(filename):
    # Create excel file
    excel_file = xlsxwriter.Workbook(str(filename))
    
    # Create the worksheet
    worksheet = excel_file.add_worksheet()

    # Create the header columns
    worksheet.write('A1', 'Time')
    worksheet.write('B1', 'Photoresistor Value')

    excel_file.close()
    
    # convert workbok into dataframe excel
    xls = pd.ExcelFile(file_name)

    # Returns excel file as dataframe
    return pd.read_excel(xls)

# Boolean to check Record button is pressed
record = False

""""""""""""""""""""""""""""""""""""""""""
 

# Flag to check if connection with ardiuno has been made
portCreated = False 

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
            window['-SCPN-'].update(visible=False)
            window['-COMLIST-'].update(disabled=True, visible=False)
            window['-OK-'].update(disabled=True, visible=False)
            window['-PV-'].update(visible=True)
            window['-RECORD-'].update(visible=True)
            window['-STOP-'].update(visible=True)


    # Read serial once connection has been made
    else:
        # Read serial from arduino
        if serialInst.in_waiting:
            # Read any event (e.g. End program if user closes window)
            event, values = window.read(timeout=1) # Add a time out of 1 millisecond to exit of window.read()
            if event == sg.WIN_CLOSED:
                break

            # If record button is pressed a new excel file is created
            if event == '-RECORD-':
                record = True

                # Create dataframe to edit excel once file was created
                file_name = time.strftime("%Y%m%d-%H%M%S") + '-LOG.xlsx'
                datalogDF = createExcelFile(file_name)

                # Update GUI buttons
                window['-RECORD-'].update(disabled=True)
                window['-STOP-'].update(disabled=False)

            # If stop button is pressed log stops recording
            if event == '-STOP-':
                record = False

                # Update GUI buttons
                window['-RECORD-'].update(disabled=False)
                window['-STOP-'].update(disabled=True)

                # Writes excel sheet with new data when recording stops
                datalogDF.to_excel(file_name, index=False)

            # Retrieve serial packet from arduino and update gui
            packet = serialInst.readline()
            PhotoResistorValue = packet.decode('utf')
            window['-PV-']("Photoresistor Value " + PhotoResistorValue)
            #print(PhotoResistorValue.rstrip('\n')) # Print to terminal

            # Update Y Value 
            # Tries to get a int from photo resistor. If unique character can't converter give it default value of 0
            try:
                Y_VALUE = int(float(PhotoResistorValue))
            except:
                Y_VALUE = 0

            # If X values is greater than the graph size then reset graph
            if X_VALUE > GRAPH_SIZE_X:
                # Shift X Value to the left by 1 pixel
                #window['-GRAPH-'].Move(-1,0)
                X_VALUE, PREV_X_VALUE, PREV_Y_VALUE = (0,0,0)

                # Reset Graph 
                window['-GRAPH-'].erase()

            # Draw Updated Graph
            window['-GRAPH-'].DrawLine((PREV_X_VALUE, PREV_Y_VALUE), (X_VALUE, Y_VALUE), width=1)

            # Add values to excel if record button is True
            if record == True: 
                new_row = {'Time': time.strftime("%Y%m%d-%H%M%S"), 'Photoresistor Value': Y_VALUE}
                datalogDF.loc[len(datalogDF)] = new_row # Adds new row to excel sheet
            

            # Update PREV Value for X, and Y
            PREV_X_VALUE, PREV_Y_VALUE = (X_VALUE, Y_VALUE)

            # Increment X value one pixel to the right
            X_VALUE += 1

 

window.close() # Close window once user closes window and exit program

