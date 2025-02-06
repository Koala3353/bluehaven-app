import os
import sys
import re
import tkinter as tk
from tkinter import ttk
from time import strftime
from arduino import get_temp, get_marine_life_density, runOpenAI, get_shake_detected, runArduino, getSummary
import pandas as pd
from tkinter import font, PhotoImage
import threading
from PIL import ImageGrab
import io
import base64
from ctypes import windll, byref, sizeof, c_int

def hex_to_colorref(hex_color: str):
    colorref = int(hex_color[1:], 16)  # remove the "#" character and convert to integer
    colorref = ((colorref & 0xFF) << 16) | (colorref & 0xFF00) | ((colorref >> 16) & 0xFF)
    return int(hex(colorref), 16)  # prints the converted colorref value in hex format


def change_caption_color(window, hex_code: str):
    HWND = windll.user32.GetParent(window.winfo_id())
    DWMWA_CAPTION_COLOR = 35

    caption_color = hex_to_colorref(hex_code)

    windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_CAPTION_COLOR, byref(c_int(caption_color)), sizeof(c_int))

frame = None

def shake_alert():
    global frame
    # show pop up for 10 seconds
    if not get_shake_detected():
        return
    else:
        print("Shake alert!")
        warning_image = PhotoImage(
            file=load_asset("warning.png")
        )   
        warning = tk.Label(
            frame,
            image=warning_image
        )
        warning.place(
            x=512.0,
            y=321.0,
            anchor="center"
        )

        # remove the loading image after 10 seconds
        frame.after(10000, lambda: warning.place_forget())

# Placeholder functions from PlaceHolder.py
def show_weather(window):
    
    canvas = tk.Canvas(
        window,
        bg = "#000e3c",
        width = 1024,
        height = 643,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x=0, y=0)

    image_7 = tk.PhotoImage(file=load_asset("frame_1/Weather Details.png"))

    canvas.create_image(550, 502, image=image_7)

    canvas.create_text(
        710,
        573,
        anchor="nw",
        text="Marine Life Density",
        fill="#ffffff",
        font=("Poppins", 12 * -1)
    )

    marine_life_label = canvas.create_text(
        745,
        550,
        anchor="nw",
        text="High",
        fill="#ffffff",
        font=("Poppins", 18 * -1)
    )

    canvas.create_text(
        777,
        475,
        anchor="nw",
        text="Seismic Event",
        fill="#ffffff",
        font=("Poppins", 14 * -1)
    )

    shake_label = canvas.create_text(
        812,
        449,
        anchor="nw",
        text="Yes",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    canvas.create_text(
        650,
        475,
        anchor="nw",
        text="Oxygen Level",
        fill="#ffffff",
        font=("Poppins", 14 * -1)
    )

    canvas.create_text(
        673,
        449,
        anchor="nw",
        text="5mg/L",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    image_8 = tk.PhotoImage(file=load_asset("frame_1/1.png"))

    canvas.create_image(692, 429, image=image_8)

    image_9 = tk.PhotoImage(file=load_asset("frame_1/2.png"))

    canvas.create_image(759, 533, image=image_9)

    image_10 = tk.PhotoImage(file=load_asset("frame_1/3.png"))

    canvas.create_image(827, 429, image=image_10)

    canvas.create_text(
        600,
        575,
        anchor="nw",
        text="pH Level",
        fill="#ffffff",
        font=("Poppins", 14 * -1)
    )

    canvas.create_text(
        620,
        553,
        anchor="nw",
        text="8.1",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    canvas.create_text(
        450,
        577,
        anchor="nw",
        text="Water Pressure",
        fill="#ffffff",
        font=("Poppins", 14 * -1)
    )

    canvas.create_text(
        450,
        553,
        anchor="nw",
        text="11,013hPa",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    image_11 = tk.PhotoImage(file=load_asset("frame_1/4.png"))

    canvas.create_image(502, 533, image=image_11)

    canvas.create_text(
        531,
        475,
        anchor="nw",
        text="Wind Current",
        fill="#ffffff",
        font=("Poppins", 14 * -1)
    )

    canvas.create_text(
        546,
        449,
        anchor="nw",
        text="28 km/h",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    canvas.create_text(
        439,
        474,
        anchor="nw",
        text="Salinity ",
        fill="#ffffff",
        font=("Poppins", 14 * -1)
    )

    canvas.create_text(
        444,
        448,
        anchor="nw",
        text="3.5%",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    image_12 = tk.PhotoImage(file=load_asset("frame_1/5.png"))

    canvas.create_image(461, 428, image=image_12)

    image_13 = tk.PhotoImage(file=load_asset("frame_1/6.png"))

    canvas.create_image(575, 427, image=image_13)

    image_14 = tk.PhotoImage(file=load_asset("frame_1/7.png"))

    canvas.create_image(630, 533, image=image_14)

    temp_label = canvas.create_text(
        183,
        473,
        anchor="nw",
        text="24°C",
        fill="#ffffff",
        font=("Poppins", 60 * -1, 'bold')
    )

    canvas.create_text( 
        183,
        445,
        anchor="nw",
        text="Temperature",
        fill="#ffffff",
        font=("Poppins", 30 * -1, 'bold')
    )

    image_15 = tk.PhotoImage(file=load_asset("frame_1/Date and Time Info.png"))

    canvas.create_image(544, 250, image=image_15)

    canvas.create_text(
        445,
        149,
        anchor="nw",
        text="Manila Bay",
        fill="#ffffff",
        font=("Poppins", 36 * -1, 'bold')
    )

    time_label = canvas.create_text(
        410,
        195,
        anchor="nw",
        text="09:03",
        fill="#ffffff",
        font=("Poppins", 96 * -1, 'bold')
    )

    date_label = canvas.create_text(
        435,
        310,
        anchor="nw",
        text="Thursday, 31 Aug",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    image_16 = tk.PhotoImage(file=load_asset("frame_1/Clothing trans 1.png"))

    canvas.create_image(135, 71, image=image_16)

    image_17 = tk.PhotoImage(file=load_asset("frame_1/8.png"))

    canvas.create_image(51, 526, image=image_17)

    button_5_image = tk.PhotoImage(file=load_asset("frame_1/9.png"))

    button_5 = tk.Button(
        image=button_5_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0, activebackground="#161D6F", bg="#161D6F",
        command=lambda: print("button_5 has been pressed!")
    )

    button_5.place(x=24, y=435, width=57, height=52)

    button_6_image = tk.PhotoImage(file=load_asset("frame_1/10.png"))

    button_6 = tk.Button(
        image=button_6_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0, activebackground="#161D6F",
        command=lambda: show_forecasts(window)
    )

    button_6.place(x=24, y=498, width=62, height=58)

    button_7_image = tk.PhotoImage(file=load_asset("frame_1/11.png"))

    button_7 = tk.Button(
        image=button_7_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0, activebackground="#161D6F",
        command=lambda: show_history(window)
    )

    button_7.place(x=22, y=563, width=57, height=48)

    button_8_image = tk.PhotoImage(file=load_asset("frame_1/12.png"))

    button_8 = tk.Button(
        image=button_8_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0, bg="#000F3C", activebackground="#000F3C",
        command=lambda: {
            ai_summary(window, 1)
        }
    )

    button_8.place(x=731, y=34, width=261, height=54)
    global frame
    frame = window

    def update_time():
        current_time = strftime('%I:%M')  # Get current time in 12-hour format with AM/PM
        current_date = strftime('%A, %B %d')  # Get current date in Weekday, Month Day format (e.g., Thursday, March 30)
        try:
            canvas.itemconfig(time_label, text=current_time)  # Update the time label with the current time
            canvas.itemconfig(date_label, text=current_date)  # Update the date label with the current date
        except Exception as e:
            print("Error updating GUI:")

        window.after(1000, update_time)  # Call the update_time function every 1000 ms (1 second)

    def update_gui():
        # Update temperature
        temp_value = get_temp()
        marine_life_density = get_marine_life_density()
        shake_detected = get_shake_detected()
        
        try:
            # Update the GUI elements with the sensor data
            canvas.itemconfig(temp_label, text=f"{temp_value}°C" if temp_value is not None else "N/A")
            canvas.itemconfig(marine_life_label, text=marine_life_density if marine_life_density is not None else "N/A")
            canvas.itemconfig(shake_label, text="Yes" if shake_detected else "No")
        except Exception as e:
            print("Error updating GUI:")

        # Schedule the function to run again after 1000 ms (1 second)
        window.after(2000, update_gui)

    update_time()  # Initial call to start updating time
    update_gui()  # Initial call to start updating GUI
    window.resizable(False, False)
    window.update()
    change_caption_color(window, "#000F3C")
    window.mainloop()

def show_history(window):
    canvas = tk.Canvas(
        window,
        bg = "#000e3c",
        width = 1024,
        height = 643,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x=0, y=0)

    image_1 = tk.PhotoImage(file=load_asset("frame_2/1.png"))

    canvas.create_image(335, 508, image=image_1)

    image_2 = tk.PhotoImage(file=load_asset("frame_2/2.png"))

    canvas.create_image(335, 260, image=image_2)

    image_3 = tk.PhotoImage(file=load_asset("frame_2/3.png"))

    canvas.create_image(787, 260, image=image_3)


    temp_graph = tk.PhotoImage(file=load_asset("frame_2/tempGraph.png"))

    canvas.create_image(335, 275, image=temp_graph)

    oxyLvl = tk.PhotoImage(file=load_asset("frame_2/oxyLvl.png"))

    canvas.create_image(335, 513, image=oxyLvl)

    windCurrentGraph = tk.PhotoImage(file=load_asset("frame_2/windCurrentGraph.png"))

    canvas.create_image(787, 275, image=windCurrentGraph)

    canvas.create_text(
        129,
        157,
        anchor="nw",
        text="",
        fill="#ffffff",
        font=("Default Font", 12 * -1)
    )

    canvas.create_text(
        160,
        157,
        anchor="nw",
        text="Temperature (Celcius)",
        fill="#ffffff",
        font=("Inter", 14 * -1)
    )

    canvas.create_text(
        614,
        157,
        anchor="nw",
        text="Wind Current (km/h)",
        fill="#ffffff",
        font=("Inter", 14 * -1)
    )

    image_4 = tk.PhotoImage(file=load_asset("frame_2/4.png"))

    canvas.create_image(787, 508, image=image_4)

    waterPressure = tk.PhotoImage(file=load_asset("frame_2/waterPressure.png"))

    canvas.create_image(787, 518, image=waterPressure)

    canvas.create_text(
        160,
        405,
        anchor="nw",
        text="Oxygen Level (mg/L)",
        fill="#ffffff",
        font=("Inter", 14 * -1)
    )

    canvas.create_text(
        614,
        405,
        anchor="nw",
        text="Water Pressure (hPa)",
        fill="#ffffff",
        font=("Inter", 14 * -1)
    )

    image_5 = tk.PhotoImage(file=load_asset("frame_2/Clothing trans 1.png"))

    canvas.create_image(135, 71, image=image_5)

    image_6 = tk.PhotoImage(file=load_asset("frame_2/5.png"))

    canvas.create_image(51, 526, image=image_6)

    button_1_image = tk.PhotoImage(file=load_asset("frame_2/6.png"))

    button_1 = tk.Button(
        image=button_1_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0, activebackground="#161D6F",
        command=lambda: show_weather(window)
    )

    button_1.place(x=23, y=435, width=57, height=52)

    button_2_image = tk.PhotoImage(file=load_asset("frame_2/7.png"))

    button_2 = tk.Button(
        image=button_2_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0, activebackground="#161D6F",
        command=lambda: show_forecasts(window)
    )

    button_2.place(x=23, y=498, width=62, height=58)

    button_3_image = tk.PhotoImage(file=load_asset("frame_2/8.png"))

    button_3 = tk.Button(
        image=button_3_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0, activebackground="#161D6F",
        command=lambda: print("button_2 has been pressed!")
    )

    button_3.place(x=22, y=563, width=57, height=48)

    button_4_image = tk.PhotoImage(file=load_asset("frame_2/9.png"))

    button_4 = tk.Button(
        image=button_4_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0, bg="#000F3C", activebackground="#000F3C",
        command=lambda: ai_summary(window, 3)
    )

    button_4.place(x=741, y=34, width=261, height=54)
    global frame
    frame = window
    window.resizable(False, False)
    window.update()
    change_caption_color(window, "#000F3C")
    window.mainloop()

def show_forecasts(window):
    canvas = tk.Canvas(
        window,
        bg = "#000e3c",
        width = 1024,
        height = 643,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x=0, y=0)

    image_18 = tk.PhotoImage(file=load_asset("frame_3/1.png"))

    canvas.create_image(746, 251, image=image_18)

    image_19 = tk.PhotoImage(file=load_asset("frame_3/2.png"))

    canvas.create_image(746, 504, image=image_19)

    image_20 = tk.PhotoImage(file=load_asset("frame_3/Clothing trans 1.png"))

    canvas.create_image(135, 71, image=image_20)

    image_21 = tk.PhotoImage(file=load_asset("frame_3/3.png"))

    canvas.create_image(929, 533, image=image_21)

    canvas.create_text(
        901,
        518,
        anchor="nw",
        text="21,311\n kPa",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    canvas.create_text(
        921,
        482,
        anchor="nw",
        text="F",
        fill="#ffffff",
        font=("Poppins", 24 * -1)
    )

    image_22 = tk.PhotoImage(file=load_asset("frame_3/4.png"))

    canvas.create_image(839, 533, image=image_22)

    canvas.create_text(
        825,
        482,
        anchor="nw",
        text="Th",
        fill="#ffffff",
        font=("Poppins", 24 * -1)
    )

    canvas.create_text(
        812,
        518,
        anchor="nw",
        text="19,413\n kPa",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    image_23 = tk.PhotoImage(file=load_asset("frame_3/5.png"))

    canvas.create_image(748, 533, image=image_23)

    canvas.create_text(
        735,
        483,
        anchor="nw",
        text="W",
        fill="#ffffff",
        font=("Poppins", 24 * -1)
    )

    canvas.create_text(
        718,
        518,
        anchor="nw",
        text="18,312\n kPa",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    image_24 = tk.PhotoImage(file=load_asset("frame_3/6.png"))

    canvas.create_image(657, 533, image=image_24)

    canvas.create_text(
        650,
        483,
        anchor="nw",
        text="T",
        fill="#ffffff",
        font=("Poppins", 24 * -1)
    )

    canvas.create_text(
        629,
        518,
        anchor="nw",
        text="17,312\n kPa",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    image_25 = tk.PhotoImage(file=load_asset("frame_3/7.png"))

    canvas.create_image(565, 533, image=image_25)

    canvas.create_text(
        536,
        518,
        anchor="nw",
        text="16,114\n kPa",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    canvas.create_text(
        555,
        483,
        anchor="nw",
        text="M",
        fill="#ffffff",
        font=("Poppins", 24 * -1)
    )

    canvas.create_text(
        645,
        400,
        anchor="nw",
        text="Water Pressure",
        fill="#ffffff",
        font=("Poppins", 27 * -1, 'bold')
    )

    image_26 = tk.PhotoImage(file=load_asset("frame_3/8.png"))

    canvas.create_image(295, 504, image=image_26)

    canvas.create_text(
        286,
        593,
        anchor="nw",
        text="Tuesday, 5 Sep",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        147,
        593,
        anchor="nw",
        text="16km/h",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        286,
        554,
        anchor="nw",
        text="Monday, 4 Sep",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        147,
        554,
        anchor="nw",
        text="18km/h",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        286,
        516,
        anchor="nw",
        text="Sunday, 3 Sep",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        147,
        516,
        anchor="nw",
        text="27km/h",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        286,
        476,
        anchor="nw",
        text="Saturday, 2 Sep",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        147,
        476,
        anchor="nw",
        text="29km/h",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        286,
        438,
        anchor="nw",
        text="Friday, 1 Sep",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        147,
        440,
        anchor="nw",
        text="30km/h",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        195,
        395,
        anchor="nw",
        text="Wind Current",
        fill="#ffffff",
        font=("Poppins", 27 * -1, 'bold')
    )

    # image_27 = tk.PhotoImage(file=load_asset("None"))

    # canvas.create_image(155, 481, image=image_27)

    image_28 = tk.PhotoImage(file=load_asset("frame_3/Rectangle 4.png"))

    canvas.create_image(612, 247, image=image_28)

    canvas.create_text(
        590,
        247,
        anchor="nw",
        text="High",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    canvas.create_text(
        599,
        217,
        anchor="nw",
        text="M",
        fill="#ffffff",
        font=("Poppins", 24 * -1)
    )

    image_29 = tk.PhotoImage(file=load_asset("frame_3/Rectangle 5.png"))

    canvas.create_image(755, 249, image=image_29)

    canvas.create_text(
        716,
        249,
        anchor="nw",
        text="Medium",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    canvas.create_text(
        742,
        219,
        anchor="nw",
        text="T",
        fill="#ffffff",
        font=("Poppins", 24 * -1)
    )

    image_30 = tk.PhotoImage(file=load_asset("frame_3/Rectangle 6.png"))

    canvas.create_image(898, 249, image=image_30)

    canvas.create_text(
        860,
        249,
        anchor="nw",
        text="Medium",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    canvas.create_text(
        885,
        219,
        anchor="nw",
        text="W",
        fill="#ffffff",
        font=("Poppins", 24 * -1)
    )

    image_31 = tk.PhotoImage(file=load_asset("frame_3/Rectangle 7.png"))

    canvas.create_image(688, 326, image=image_31)

    canvas.create_text(
        665,
        326,
        anchor="nw",
        text="High",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    canvas.create_text(
        669,
        296,
        anchor="nw",
        text="Th",
        fill="#ffffff",
        font=("Poppins", 24 * -1)
    )

    image_32 = tk.PhotoImage(file=load_asset("frame_3/Rectangle 8.png"))

    canvas.create_image(831, 328, image=image_32)

    canvas.create_text(
        790,
        328,
        anchor="nw",
        text="Medium",
        fill="#ffffff",
        font=("Poppins", 20 * -1)
    )

    canvas.create_text(
        818,
        298,
        anchor="nw",
        text="F",
        fill="#ffffff",
        font=("Poppins", 24 * -1)
    )

    canvas.create_text(
        624,
        144,
        anchor="nw",
        text="Marine Life Density",
        fill="#ffffff",
        font=("Poppins", 27 * -1, 'bold')
    )

    canvas.create_text(
        682,
        178,
        anchor="nw",
        text="5-Day Forcast",
        fill="#ffffff",
        font=("Inter", 20 * -1, 'bold')
    )

    canvas.create_text(
        682,
        438,
        anchor="nw",
        text="5-Day Forcast",
        fill="#ffffff",
        font=("Inter", 20 * -1, 'bold')
    )

    image_33 = tk.PhotoImage(file=load_asset("frame_3/9.png"))

    canvas.create_image(295, 251, image=image_33)

    canvas.create_text(
        282,
        333,
        anchor="nw",
        text="Tuesday, 5 Sep",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        147,
        333,
        anchor="nw",
        text="27°C",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        282,
        296,
        anchor="nw",
        text="Monday, 4 Sep",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        147,
        296,
        anchor="nw",
        text="28°C",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        282,
        260,
        anchor="nw",
        text="Sunday, 3 Sep",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        147,
        258,
        anchor="nw",
        text="27°C",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        282,
        223,
        anchor="nw",
        text="Saturday, 2 Sep",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        147,
        223,
        anchor="nw",
        text="22°C",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        282,
        187,
        anchor="nw",
        text="Friday, 1 Sep",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        147,
        187,
        anchor="nw",
        text="26°C",
        fill="#ffffff",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        195,
        145,
        anchor="nw",
        text="Temperature",
        fill="#ffffff",
        font=("Poppins", 27 * -1, 'bold')
    )

    image_34 = tk.PhotoImage(file=load_asset("frame_3/10.png"))

    canvas.create_image(51, 526, image=image_34)

    button_9_image = tk.PhotoImage(file=load_asset("frame_3/11.png"))

    button_9 = tk.Button(
        image=button_9_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0, activebackground="#161D6F",
        command=lambda: show_weather(window)
    )

    button_9.place(x=23, y=435, width=57, height=52)

    button_10_image = tk.PhotoImage(file=load_asset("frame_3/12.png"))

    button_10 = tk.Button(
        image=button_10_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0, activebackground="#161D6F",
        command=lambda: print("button_10 has been pressed!")
    )

    button_10.place(x=23, y=498, width=62, height=58)

    button_11_image = tk.PhotoImage(file=load_asset("frame_3/13.png"))

    button_11 = tk.Button(
        image=button_11_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0, activebackground="#161D6F",
        command=lambda: show_history(window)
    )

    button_11.place(x=22, y=563, width=57, height=48)

    button_12_image = tk.PhotoImage(file=load_asset("frame_3/14.png"))

    button_12 = tk.Button(
        image=button_12_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0, bg="#000F3C", activebackground="#000F3C",
        command=lambda: ai_summary(window, 2)
    )

    button_12.place(x=730, y=34, width=260, height=54)
    global frame
    frame = window
    
    window.resizable(False, False)
    window.update()
    change_caption_color(window, "#000F3C")
    window.mainloop()

def ai_summary(window, type):
    """ Takes a screenshot and provides an AI summary with improved UI and correctly formatted bold text """

    # Take a screenshot of the current Tkinter window
    x, y = window.winfo_rootx(), window.winfo_rooty()
    width, height = x + window.winfo_width() + 300, y + window.winfo_height() + 300
    screenshot = ImageGrab.grab(bbox=(x, y, width, height))

    # Convert screenshot to base64 string
    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG")
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Create a modern AI summary window
    toplevel = tk.Toplevel(window)
    toplevel.configure(bg="#121212")  # Dark theme
    toplevel.geometry("700x500")  
    toplevel.title("AI Summary")
    
    # Disable the main window while loading
    window.attributes("-disabled", True)

    toplevel.update()
    change_caption_color(toplevel, "#121212")

    def on_close():
        """ Re-enable the main window when the summary window is closed """
        window.attributes("-disabled", False)
        toplevel.destroy()

    toplevel.protocol("WM_DELETE_WINDOW", on_close)

    # Create a frame for the UI
    frame = tk.Frame(toplevel, bg="#121212")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Add loading image at the center
    loading_image = PhotoImage(file=load_asset("loading.png"))  
    loading_label = tk.Label(frame, image=loading_image, bg="#121212")
    loading_label.image = loading_image  # Prevent garbage collection
    loading_label.pack(expand=True)

    # Create a styled Text widget with a custom scrollbar
    text_frame = tk.Frame(frame, bg="#121212")

    text_widget = tk.Text(
        text_frame, wrap="word", bg="#1E1E1E", fg="#ffffff",
        font=("Poppins", 16), relief="flat", padx=10, pady=10,
        insertbackground="white",  # White cursor for better visibility
        spacing1=5, spacing2=5, spacing3=5  # Improved spacing between lines
    )

    # Custom scrollbar styling
    scrollbar_style = ttk.Style()
    scrollbar_style.theme_use("clam")
    scrollbar_style.configure("Custom.Vertical.TScrollbar",
                              gripcount=0,
                              background="#3E3E3E", 
                              darkcolor="#3E3E3E", 
                              lightcolor="#3E3E3E",
                              troughcolor="#1E1E1E",
                              bordercolor="#1E1E1E",
                              arrowcolor="white")
    scrollbar_style.map("Custom.Vertical.TScrollbar",
                        background=[("active", "#505050"), ("!active", "#3E3E3E")])  # Fixes inactive white color

    custom_scrollbar = ttk.Scrollbar(
        text_frame, orient="vertical", style="Custom.Vertical.TScrollbar", command=text_widget.yview
    )
    text_widget.config(yscrollcommand=custom_scrollbar.set)

    # Packing the text widget and scrollbar (initially hidden)
    custom_scrollbar.pack(side="right", fill="y")
    text_widget.pack(side="left", fill="both", expand=True)

    # Define text styles
    text_widget.tag_configure("bold", font=("Poppins", 16, "bold"), foreground="#FFD700")  # Gold-colored bold
    text_widget.tag_configure("heading", font=("Poppins", 20, "bold", "underline"), foreground="#FFA500")  # Orange headings
    text_widget.tag_configure("list", lmargin1=20, lmargin2=40)  # Indent bullet points
    text_widget.tag_configure("numbered_list", lmargin1=20, lmargin2=40)  # Indent numbered lists

    def format_summary_text(summary_text):
        """ 
        Formats text by applying bold styling and properly structuring headings and lists.
        Handles Markdown-style formatting like **bold**, ### headings, and lists.
        """
        text_widget.configure(state="normal")  # Make it editable for insertion
        text_widget.delete("1.0", "end")  # Clear any previous content

        lines = summary_text.split("\n")
        for line in lines:
            if line.startswith("###"):  # Headings
                text_widget.insert("end", line.replace("###", "").strip() + "\n", "heading")
            elif line.startswith("- "):  # Bulleted lists
                text_widget.insert("end", line + "\n", "list")
            elif line[:2].isdigit() and line[2] == ".":  # Numbered lists
                text_widget.insert("end", line + "\n", "numbered_list")
            else:
                # Process bold text by removing ** but keeping formatting
                while "**" in line:
                    parts = re.split(r"\*\*(.*?)\*\*", line, maxsplit=1)
                    if len(parts) == 3:  # Ensure the split worked correctly
                        before, bold_text, after = parts
                        text_widget.insert("end", before)  # Insert normal text
                        text_widget.insert("end", bold_text, "bold")  # Insert bold text
                        line = after  # Continue processing the rest of the line
                    else:
                        break  # Exit if no more ** are found
                text_widget.insert("end", line + "\n")  # Insert remaining text

        text_widget.configure(state="disabled")  # Make text read-only
        text_widget.yview_moveto(1)  # Auto-scroll to bottom

    def fetch_summary():
        """ Fetch AI-generated summary in a separate thread """
        summary_text = getSummary(img_str, type)
        toplevel.after(100, lambda: display_summary(summary_text))  # Update UI safely

    def display_summary(summary_text):
        """ Inserts formatted summary into the text widget and removes the loading image """
        loading_label.pack_forget()  # Hide loading animation
        text_frame.pack(expand=True, fill="both")  # Show text area
        format_summary_text(summary_text)  # Apply formatting
    
    def show_context_menu(event):
        """ Displays a dark-themed right-click menu with 'Select All' and 'Copy' options. """
        context_menu.tk_popup(event.x_root, event.y_root)

    def select_all():
        """ Selects all text in the widget. """
        text_widget.tag_add("sel", "1.0", "end")
        text_widget.mark_set("insert", "1.0")
        text_widget.see("insert")

    def copy_text():
        """ Copies selected text, or everything if nothing is selected. """
        try:
            selected_text = text_widget.get("sel.first", "sel.last")
        except tk.TclError:  # If no text is selected, copy everything
            selected_text = text_widget.get("1.0", "end-1c")
        
        window.clipboard_clear()
        window.clipboard_append(selected_text)
        window.update()

    # Create the right-click menu
    context_menu = tk.Menu(text_widget, tearoff=0, bg="#2E2E2E", fg="white", activebackground="#505050", activeforeground="white", borderwidth=0)
    context_menu.add_command(label="Select All", command=select_all)
    context_menu.add_command(label="Copy", command=copy_text)

    # Bind right-click event to show the menu
    text_widget.bind("<Button-3>", show_context_menu)


    # Run AI summary generation in a separate thread
    threading.Thread(target=fetch_summary, daemon=True).start()

    # Center the AI summary window
    toplevel.update_idletasks()
    main_x, main_y = window.winfo_x(), window.winfo_y()
    main_w, main_h = window.winfo_width(), window.winfo_height()
    top_w, top_h = toplevel.winfo_width(), toplevel.winfo_height()
    pos_x, pos_y = main_x + (main_w // 2) - (top_w // 2), main_y + (main_h // 2) - (top_h // 2)
    toplevel.geometry(f"+{pos_x}+{pos_y}")

    toplevel.focus_set()
    toplevel.grab_set()
    window.wait_window(toplevel)


def load_asset(path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(base, "assets")
    return os.path.join(assets, path)

window = tk.Tk()
window.geometry("1024x643")
window.configure(bg="#000f3c")
window.title("BlueHaven")

runOpenAI()  # Start the OpenAI communication thread

# Start the Arduino communication thread in the background
arduino_thread = threading.Thread(target=runArduino)
arduino_thread.start()

app_thread = threading.Thread(target=show_weather(window))
app_thread.start()