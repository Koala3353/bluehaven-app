from tkinter import *
import csv
from telemetrix import telemetrix
from threading import Thread
import threading
import random
import sys
from openai import OpenAI

# Define sensor pins
TRIGGER_PIN = 8
ECHO_PIN = 9
BUTTON = 10
TEMP_PIN = 0
VIBRATION_SENSOR_PIN = 1

# Global variables
temp_value = None
marine_life_density = 0
shake_detected = False
marine_life_density_output = "Low"
button_pressed = False  
board = None
client = None


def ultrasonic(data):
    """ Callback function for the ultrasonic sensor """
    global marine_life_density
    distance = data[2]
    if distance < 15:
        marine_life_density += 1


def temp(data):
    """ Callback function for the temperature sensor """
    global temp_value
    reading = data[2]
    voltage = reading * (5.0 / 1024.0)
    temp_value = round(voltage * 100, 1)


def vibration_callback(data):  
    """ Callback function for the vibration sensor """
    global shake_detected
    shake_detected = data[2] > 100  


def button_callback(data):
    """ Callback function for the button press """
    global button_pressed, shake_detected
    button_pressed = data[2] == 1
    if not button_pressed:
        shake_detected = False  


def update_data():
    """ Updates sensor data and writes it to a CSV file every 3 seconds """
    global marine_life_density, marine_life_density_output

    # Assign density category
    if marine_life_density <= 10:
        marine_life_density_output = "Low"
    elif marine_life_density <= 15:
        marine_life_density_output = "Medium"
    else:
        marine_life_density_output = "High"

    # Save data to CSV
    with open("data.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([marine_life_density_output, temp_value, shake_detected])

    marine_life_density = 0  # Reset counter
    threading.Timer(3, update_data).start()  # Use non-blocking scheduling


def runArduino():
    """ Initializes Arduino board and sets up sensors without blocking the main thread. """
    global board
    board = telemetrix.Telemetrix()

    # Use callbacks instead of separate threads
    board.set_pin_mode_sonar(TRIGGER_PIN, ECHO_PIN, ultrasonic)
    board.set_pin_mode_analog_input(TEMP_PIN, callback=temp)
    board.set_pin_mode_analog_input(VIBRATION_SENSOR_PIN, callback=vibration_callback)
    board.set_pin_mode_digital_input(BUTTON, callback=button_callback)

    # Start scheduled data updates without blocking
    update_data()


def runOpenAI():
    """ Initialize OpenAI API """
    global client
    client = OpenAI(api_key="API-KEY")


def getSummary(img_str, type):
    img_type = "image/png"
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

    # print(response)
    return response.choices[0].message.content


def get_temp():
    return temp_value


def get_marine_life_density():
    return marine_life_density_output


def get_shake_detected():
    return shake_detected
