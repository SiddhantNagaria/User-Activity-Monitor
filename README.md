# User Activity Monitor

## Overview
The **User Activity Monitor** is a Python-based desktop application designed to monitor and log user activity in real-time on a Windows system. The application tracks key presses, mouse clicks, active window usage, and captures screenshots of the active window. It includes a login/signup system with password hashing for user authentication.

## Features
- **User Authentication:** Secure login and signup functionality with password hashing.
- **Activity Monitoring:** Tracks key presses, mouse clicks, active window usage time.
- **Screenshot Capture:** Captures and displays screenshots of the currently active window.
- **Graphical User Interface:** A user-friendly GUI for viewing activity logs in real-time.
- **Automatic Updates:** Activity logs and screenshots are refreshed every 5 seconds.

## Dependencies
The following libraries are required to run the project:

- **cx_Freeze:** Used for packaging the Python script into an executable.
- **hashlib:** For hashing user passwords.
- **json:** To handle storage and retrieval of user credentials.
- **platform:** For identifying the operating system.
- **time:** For managing time-related functions.
- **tkinter:** For creating the GUI components.
- **datetime:** For handling date and time.
- **threading:** For running background tasks concurrently.
- **psutil:** For fetching system and process information.
- **Pillow (PIL):** For handling image processing, specifically screenshot capture and display.
- **pynput:** For monitoring keyboard and mouse events.
- **pywin32:** For Windows-specific functions such as window title fetching and screenshot capturing.

## dependencies
pip install json5 psutil pillow pynput pywin32 cx_Freeze datetime

pip install -U pip

## run the project
python user_activity_monitor.py