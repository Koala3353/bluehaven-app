# BlueHaven

BlueHaven is a weather monitoring and marine life density tracking application that interfaces with Arduino sensors and provides real-time data visualization using a Tkinter-based GUI. The application also integrates with OpenAI to generate summaries of the displayed data.

## Project Structure
BlueHaven/ ├── pycache/ ├── arduino.py ├── assets/ │ ├── frame_1/ │ ├── frame_2/ │ ├── frame_3/ ├── data.csv ├── Gui_Final.py

### Files

- [`arduino.py`](arduino.py): Contains the code for interfacing with Arduino sensors and handling sensor data.
- [`Gui_Final.py`](Gui_Final.py): Contains the code for the Tkinter-based GUI and integrates with the Arduino and OpenAI functionalities.
- [`data.csv`](data.csv): Stores the logged sensor data.
- [`assets`](assets): Contains image assets used in the GUI.

## Requirements

- Python 3.x
- Tkinter
- Telemetrix
- OpenAI API
- PIL (Pillow)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/BlueHaven.git
    cd BlueHaven
    ```

2. Install the required Python packages:
    ```sh
    pip install tkinter telemetrix openai pillow
    ```

3. Set up your OpenAI API key in [arduino.py](http://_vscodecontentref_/3):
    ```python
    client = OpenAI(
        api_key="your_openai_api_key"
    )
    ```

## Usage

1. Run the application:
    ```sh
    python Gui_Final.py
    ```

2. The main window will display real-time weather data and marine life density information.

3. Use the buttons to navigate between different views:
    - **Weather Details**: Displays current weather and marine life density data.
    - **History**: Shows historical data graphs.
    - **Forecasts**: Displays weather forecasts.

4. The application will automatically update the displayed data every 2 seconds.

## Functions

### [arduino.py](http://_vscodecontentref_/4)

- `runArduino()`: Initializes the Arduino board and starts sensor data collection threads.
- `runOpenAI()`: Initializes the OpenAI client.
- `get_temp()`: Returns the current temperature value.
- `get_marine_life_density()`: Returns the current marine life density.
- `get_shake_detected()`: Returns whether a shake event was detected.

### [Gui_Final.py](http://_vscodecontentref_/5)

- [show_weather(window)](http://_vscodecontentref_/6): Displays the main weather details view.
- [show_history(window)](http://_vscodecontentref_/7): Displays the historical data view.
- [show_forecasts(window)](http://_vscodecontentref_/8): Displays the weather forecasts view.
- [ai_summary(window, type)](http://_vscodecontentref_/9): Generates a summary of the displayed data using OpenAI.

## Troubleshooting

- Ensure that the Arduino board is properly connected and the correct pins are used.
- Verify that the OpenAI API key is correctly set up.
- Check for any missing image assets in the [assets](http://_vscodecontentref_/10) directory.

## Pictures
![image](https://github.com/user-attachments/assets/ec6209db-6f3e-4f59-879c-5d3a3b2474fb)
![image](https://github.com/user-attachments/assets/a2f77078-c29d-458d-91b4-6e307de87379)
![image](https://github.com/user-attachments/assets/dbf8d4a6-89d4-4267-aa6f-9258026f08e4)
![image](https://github.com/user-attachments/assets/5bb91426-40d3-4f61-b901-f3f38a6c5a8c)
![image](https://github.com/user-attachments/assets/df2908ef-52f2-4013-8e50-5321d0644402)
![image](https://github.com/user-attachments/assets/f28d93e0-b149-4d5d-a4d2-258b0ed224e5)
![image](https://github.com/user-attachments/assets/5820c364-f813-4c86-a951-14efb5e3b317)

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [Telemetrix](https://github.com/MrYsLab/telemetrix) for Arduino communication.
- [OpenAI](https://openai.com/) for the AI summarization functionality.
- [Pillow](https://python-pillow.org/) for image handling in Tkinter.
