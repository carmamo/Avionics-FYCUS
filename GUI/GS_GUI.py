#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 17:23:35 2023
Todos estos códigos requieren comentarios y una limpieza
Limpio=NO
Comentarios=50%
@author: carlos
"""
import PySimpleGUI as sg
import serial
import serial.tools.list_ports
import threading
import struct
import vedo
from vedo import settings
import tkinter as tk
import tkintermapview

# Constants
BAUDRATE = 9600

# Create serial object
serialPort = None

# Define struct format
struct_fmt = "<f3B3B"


# Define function to receive telemetry packet from serial port
def receive_struct(port, window):
    while run_thread:
        # Check if serial port is open
        if not port.is_open:
            return

        # Read telemetry packet from serial port
        # Read until the start of the header is detected
        serialPort.read_until(b'\xde\xad\xbe\xef')
        raw_data = port.read(struct.calcsize(struct_fmt))

        # Unpack telemetry packet
        telemetry = struct.unpack(struct_fmt, raw_data)

        # Update GUI
        if window['-TEMP-'] is not None:
            window['-TEMP-'].update(f"{telemetry[0]:.2f}")
        accel_values = telemetry[1:4]
        accel_string = ", ".join(str(x) for x in accel_values)
        if window['-ACCEL-'] is not None:
            window['-ACCEL-'].update(accel_string)
        if window['-PRESS-'] is not None:
            window['-PRESS-'].update(telemetry[4])
        if window['-BATT-'] is not None:
            window['-BATT-'].update(telemetry[5]/10)
        if window['-COUNT-'] is not None:
            window['-COUNT-'].update(telemetry[6])

        # Update 3D object
        obj.rotateY(telemetry[5]/4)  # rotate object around Y-axis

        # Render the updated object in the viewer
        plt.render()


# Define function to show the plotter window
def show_plotter():
    global plt
    # Create non-blocking 3D viewer window
    plt = vedo.Plotter(axes=1, size=(800, 600), offscreen=False)
    plt += [obj]

    plt.show(interactive=False)


# Define map viewer widget
def show_map():
    global root

    # Define map widget
    root = tk.Tk()
    root.title("MapView Tracker")
    root.geometry("900x700")

    my_label = tk.LabelFrame(root)
    my_label.pack(pady=20)

    map_widget = tkintermapview.TkinterMapView(
        my_label, width=800, height=600, corner_radius=0)
    map_widget.pack()

    # Set coordinates
    map_widget.set_position(37.41099172851576, -6.000683100212201)      # ETSI

    # Set a zoom
    map_widget.set_zoom(20)

    # root.mainloop()


# Define GUI layout
layout = [[sg.Text("Select serial port:"), sg.Combo(serial.tools.list_ports.comports(), size=(40, 1), key="-COM-")],
          [sg.Button('Connect'), sg.Button('Disconnect')],
          [sg.Text('Temperature:'), sg.Text(
              '0.00', key='-TEMP-'), sg.Text('C')],
          [sg.Text('Accelerometer:'), sg.Text('(0, 0, 0)', key='-ACCEL-')],
          [sg.Text('Pressure:'), sg.Text('0', key='-PRESS-')],
          [sg.Text('Battery:'), sg.Text('0', key='-BATT-'), sg.Text('V')],
          [sg.Text('Counter:'), sg.Text('0', key='-COUNT-')],
          [sg.Button('Exit', size=(10, 1))]]


# Create GUI window
window = sg.Window("Ground Station GUI", layout)

# Load 3D object
obj = vedo.load("SXC-F3U-02.obj")

# Set initial camera position
obj.pos(0, 0, 0)
obj.scale(20)
obj.rotateX(0)

# Configure vedo settings
settings.useDepthPeeling = True

# Create non-blocking 3D viewer window
show_plotter()

# Create non-blocking Map Viewer window
show_map()

# Get initial list of available ports
prev_port_list = serial.tools.list_ports.comports()

# Main loop
while True:
    event, values = window.read(timeout=500)

    # Handle events
    if event in (sg.WIN_CLOSED, 'Exit'):
        # Signal the thread loops to stop running
        run_thread = False
        plt.close()

        break
    elif event == 'Connect':
        if serialPort is None:
            com_port = values['-COM-']
            if com_port:
                try:
                    serialPort = serial.Serial(
                        port=com_port.device, baudrate=BAUDRATE)

                    # Start a new thread to receive image data
                    run_thread = True
                    thread = threading.Thread(
                        target=receive_struct, args=(serialPort, window))
                    thread.start()

                    # sg.PopupNonBlocking('Connected to serial port!')

                except serial.SerialException as e:
                    sg.popup_error(f"Error opening serial port: {e}")
                    continue
            else:
                sg.popup_error("COM port is not selected!")

    elif event == 'Disconnect':
        # Disconnect from serial port
        if serialPort:
            # Signal the receive image thread to stop running
            run_thread = False
            serialPort.close()
        serialPort = None

    elif event == sg.TIMEOUT_EVENT:
        # Check for changes in available serial ports
        port_list = serial.tools.list_ports.comports()
        if port_list != prev_port_list:
            # Update the combo box with the new list of ports
            window['-COM-'].update(values=port_list)
            prev_port_list = port_list

# Clean up resources
if serialPort:
    serialPort.close()
window.close()
