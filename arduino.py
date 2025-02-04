from tkinter import *
from tkinter.simpledialog import askinteger
from serial.tools.list_ports import comports
import time
import csv
from telemetrix import telemetrix
from threading import Thread
import random
import sys
from openai import OpenAI
import threading
from PIL import ImageGrab
from pathlib import Path
import io
import base64

# Define the pins for the sensors
TRIGGER_PIN = 8
ECHO_PIN = 9
BUTTON = 10
TEMP_PIN = 0
VIBRATION_SENSOR_PIN = 1

# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3

temp_value = None
marine_life_density = None
shake_detected = False
marine_life_density_output = None
button_pressed = False  # Variable to store button state

board = None
client = None

def ultrasonic(data):
    global marine_life_density
    print(f"Ultrasonic Sensor Data: {data}")
    distance = data[2]
    print(f"Distance: {distance} cm")
    if distance < 15:
        print(f"Marine life detected! Count is now {marine_life_density}. Latest density is {marine_life_density_output}")
        if marine_life_density is None:
            marine_life_density = 1
        else:
            marine_life_density += 1
            
def temp(data):
    global temp_value
    reading = data[CB_VALUE]
    voltage = reading * (5.0 / 1024.0)
    temp_value = round(voltage * 100, 2)
    print(f"Temperature: {temp_value}°C")
    

def shake_alert():
    # show pop up for 10 seconds
    global shake_detected
    shake_detected = True
    print("Shake alert!")

def vibration_callback(data):   
    value = data[CB_VALUE]
    print(f"Vibration Intensity (Analog Value): {value}")
    if value > 100:
        global shake_detected
        shake_detected = True
        print("Shake detected!")
        shake_alert()

def temp_in(my_board, pin):
    """
    This function establishes the pin as an
    analog input. Any changes on this pin will
    be reported through the call back function.

    :param my_board: a telemetrix instance
    :param pin: Arduino pin number
    """

    # set the pin mode
    my_board.set_pin_mode_analog_input(pin, differential=0, callback=temp)

    # time.sleep(5)s
    # my_board.disable_analog_reporting()
    # time.sleep(5)
    # my_board.enable_analog_reporting()

    print('Temperature sensor initiated')
    try:
        while True:
            continue
    except KeyboardInterrupt:
        my_board.shutdown()
        sys.exit(0)

def getSummary(window, type):
    # Take a screenshot of the current Tkinter window
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    width = x + window.winfo_width() + 300
    height = y + window.winfo_height() + 300
    screenshot = ImageGrab.grab(bbox=(x, y, width, height))

    # Save the screenshot to a bytes buffer
    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG")
    buffer.seek(0)

    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    img_type = "image/png"

    # save the screenshot to a file for debugging purposes
    with open("screenshot.png", "wb") as f:
        f.write(buffer.getbuffer())

    prompt = ""
    if type == 1:
        prompt = "Summarize the content of this image. Focus primarily on the weather statistics and not the design of the app.. Mention the salinity, temperature, wind current, oxygen level, sesimic event, water pressure, ph level, and marine lift density that is displayed in the app, but if not provided then dont mention it-- the layout in the picture is the value then below it is the label. Finally, give recommendations targetted for divers or for marine researchers."
    elif type == 2:
        prompt = "Summarize the content of this image in 2-3 sentences. Focus primarily on the weather prediction statistics and not the design of the app.. Finally, give recommendations targetted for divers or for marine researchers."
    elif type == 3:
        prompt = "Summarize the content of this image in 3-4 sentences. Focus primarily on the weather history statistics and not the design of the app.. Finally, give recommendations targetted for divers or for marine researchers."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{img_type};base64,{img_str}"},
                    },
                ],
            }
        ],
    )

    print(response)
    summary = response.choices[0].message.content
    print(summary)
    return summary    
    
def shock_in(my_board):
    # set the pin mode
    my_board.set_pin_mode_analog_input(VIBRATION_SENSOR_PIN, callback=vibration_callback)

    # time.sleep(5)
    # my_board.disable_analog_reporting()
    # time.sleep(5)
    # my_board.enable_analog_reporting()

    print('Shock sensor initiated')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        my_board.shutdown()
        sys.exit(0)
        
def sonar(my_board, trigger_pin, echo_pin, callback):
    my_board.set_pin_mode_sonar(trigger_pin, echo_pin, callback)
    print('Ultrasonic Sensor initiated')
    while True:
        try:
            my_board.sonar_enable()
        except KeyboardInterrupt:
            my_board.shutdown()
            sys.exit(0)

def button_callback(data):
    global button_pressed, shake_detected
    button_pressed = data[CB_VALUE] == 1  # Update button state
    if button_pressed:
        shake_alert()
    elif not button_pressed:
        print("Button released")
        shake_detected = False

def update_data():
    global temp_value, marine_life_density, marine_life_density_output
    
    if marine_life_density is None:
        marine_life_density = random.randint(1, 3)
        if marine_life_density == 1:
            marine_life_density_output = "Low"
        elif marine_life_density == 2:
            marine_life_density_output = "Medium"
        else:
            marine_life_density_output = "High"         
    elif marine_life_density <= 10:
        marine_life_density_output = "Low"
    elif marine_life_density <= 15:
        marine_life_density_output = "Medium"
    elif marine_life_density > 15:
        marine_life_density_output = "High"
    
    with open("data.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([marine_life_density_output, temp_value, shake_detected])
    
    marine_life_density = None
    threading.Timer(3, update_data).start()

def button_in(my_board, pin):
    my_board.set_pin_mode_digital_input(pin, callback=button_callback)
    try:
        while True:
            continue
    except KeyboardInterrupt:
        board.shutdown()
        sys.exit(0)
        
def run_sonar():
    try:
        sonar(board, TRIGGER_PIN, ECHO_PIN, ultrasonic)
    except (KeyboardInterrupt, RuntimeError):
        board.shutdown()
        sys.exit(0)

def run_temp():
    try:
        temp_in(board, TEMP_PIN)
    except (KeyboardInterrupt, RuntimeError):
        board.shutdown()
        sys.exit(0)

def run_vibration():
    try:
        shock_in(board)
    except (KeyboardInterrupt, RuntimeError):
        board.shutdown()
        sys.exit(0)

def run_button():
    try:
        button_in(board, BUTTON)
    except (KeyboardInterrupt, RuntimeError):
        board.shutdown()
        sys.exit(0)

def get_temp():
    return temp_value

def get_marine_life_density():
    return marine_life_density_output

def get_shake_detected():
    return shake_detected
    
def runArduino():
    global board
    board = telemetrix.Telemetrix()
    
    Thread(target=run_sonar, daemon=True).start()
    Thread(target=run_temp, daemon=True).start()
    Thread(target=run_vibration, daemon=True).start()
    Thread(target=run_button, daemon=True).start()
    Thread(target=update_data, daemon=True).start()

def runOpenAI():
    global client
    client = OpenAI(
        api_key=""
    )