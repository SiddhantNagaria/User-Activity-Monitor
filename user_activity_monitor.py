import hashlib
import json
import platform
import time
import tkinter as tk
from datetime import datetime
from threading import Thread
from tkinter import messagebox, ttk

import psutil
from PIL import Image, ImageTk
from pynput import keyboard, mouse

if platform.system() == 'Windows':
    import win32api
    import win32con
    import win32gui
    from PIL import ImageGrab

# Path to store user credentials
CREDENTIALS_FILE = 'credentials.json'

# Load credentials from file or create an empty file
def load_credentials():
    try:
        with open(CREDENTIALS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_credentials(credentials):
    with open(CREDENTIALS_FILE, 'w') as file:
        json.dump(credentials, file)

# Hashing passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Activity log to store application usage data
activity_log = {}

# Variables to track user interactions
key_presses = 0
mouse_clicks = 0

def fetch_active_window():
    if platform.system() == 'Windows':
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    return "Unknown"

def capture_screenshot():
    if platform.system() == 'Windows':
        bbox = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
        return ImageGrab.grab(bbox)
    return None

def monitor_activity():
    global key_presses, mouse_clicks

    while True:
        current_time = datetime.now()
        active_window = fetch_active_window()

        if active_window not in activity_log:
            activity_log[active_window] = {
                'start_time': current_time,
                'key_presses': 0,
                'mouse_clicks': 0,
                'usage_time': 0
            }

        activity = activity_log[active_window]
        activity['usage_time'] = (current_time - activity['start_time']).total_seconds()
        activity['key_presses'] += key_presses
        activity['mouse_clicks'] += mouse_clicks

        key_presses = 0
        mouse_clicks = 0

        screenshot = capture_screenshot()
        update_screenshot(screenshot)

        refresh_gui()

        time.sleep(5)

def refresh_gui():
    global tree
    for item in tree.get_children():
        tree.delete(item)
        
    for app, info in activity_log.items():
        tree.insert("", "end", values=(app, info['start_time'].strftime("%Y-%m-%d %H:%M:%S"), 
                                       f"{info['usage_time']:.2f}", info['key_presses'], info['mouse_clicks']))

def update_screenshot(img):
    global screenshot_label
    if img:
        img = ImageTk.PhotoImage(img.resize((300, 200)))
        screenshot_label.config(image=img)
        screenshot_label.image = img

def key_event_handler(key):
    global key_presses
    key_presses += 1

def mouse_event_handler(x, y, button, pressed):
    global mouse_clicks
    if pressed:
        mouse_clicks += 1

def signup_window():
    def create_account():
        username = entry_username.get()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        credentials = load_credentials()

        if username in credentials:
            messagebox.showerror("Error", "Username already exists")
        else:
            credentials[username] = hash_password(password)
            save_credentials(credentials)
            messagebox.showinfo("Success", "Account created successfully")
            signup_win.destroy()

    def open_login():
        signup_win.destroy()
        login_window()

    def on_enter(e):
        e.widget.config(style="Hover.TButton")

    def on_leave(e):
        e.widget.config(style="TButton")

    signup_win = tk.Tk()
    signup_win.title("Signup")
    signup_win.geometry("400x300")  # Increased window height for better visibility
    signup_win.configure(bg="#2E3440")  # Set background color

    style = ttk.Style(signup_win)
    style.theme_use("clam")

    # Customize styles
    style.configure("TLabel", background="#2E3440", foreground="#ECEFF4", font=("Arial", 12))
    style.configure("TButton", background="#4C566A", foreground="#ECEFF4", font=("Arial", 10, "bold"))
    style.map("TButton", background=[("active", "#5E81AC")])
    style.configure("Hover.TButton", background="#5E81AC", foreground="#ECEFF4", font=("Arial", 10, "bold"))

    ttk.Label(signup_win, text="Username:").pack(pady=5)
    entry_username = ttk.Entry(signup_win, font=("Arial", 12))
    entry_username.pack(pady=5)

    ttk.Label(signup_win, text="Password:").pack(pady=5)
    entry_password = ttk.Entry(signup_win, show="*", font=("Arial", 12))
    entry_password.pack(pady=5)

    ttk.Label(signup_win, text="Confirm Password:").pack(pady=5)
    entry_confirm_password = ttk.Entry(signup_win, show="*", font=("Arial", 12))
    entry_confirm_password.pack(pady=5)

    signup_button = ttk.Button(signup_win, text="Signup", command=create_account)
    signup_button.pack(pady=10)
    signup_button.bind("<Enter>", on_enter)
    signup_button.bind("<Leave>", on_leave)

    login_button = ttk.Button(signup_win, text="Login", command=open_login)
    login_button.pack(pady=5)
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

    signup_win.mainloop()

def login_window():
    def authenticate():
        username = entry_username.get()
        password = entry_password.get()
        credentials = load_credentials()

        if username in credentials and credentials[username] == hash_password(password):
            login_win.destroy()
            initialize_gui(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_signup():
        login_win.destroy()
        signup_window()

    def on_enter(e):
        e.widget.config(style="Hover.TButton")

    def on_leave(e):
        e.widget.config(style="TButton")

    login_win = tk.Tk()
    login_win.title("Login")
    login_win.geometry("400x250")
    login_win.configure(bg="#2E3440")  # Set background color

    style = ttk.Style(login_win)
    style.theme_use("clam")

    # Customize styles
    style.configure("TLabel", background="#2E3440", foreground="#ECEFF4", font=("Arial", 12))
    style.configure("TButton", background="#4C566A", foreground="#ECEFF4", font=("Arial", 10, "bold"))
    style.map("TButton", background=[("active", "#5E81AC")])
    style.configure("Hover.TButton", background="#5E81AC", foreground="#ECEFF4", font=("Arial", 10, "bold"))

    ttk.Label(login_win, text="Username:").pack(pady=5)
    entry_username = ttk.Entry(login_win, font=("Arial", 12))
    entry_username.pack(pady=5)

    ttk.Label(login_win, text="Password:").pack(pady=5)
    entry_password = ttk.Entry(login_win, show="*", font=("Arial", 12))
    entry_password.pack(pady=5)

    login_button = ttk.Button(login_win, text="Login", command=authenticate)
    login_button.pack(pady=10)
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

    signup_button = ttk.Button(login_win, text="Signup", command=open_signup)
    signup_button.pack(pady=5)
    signup_button.bind("<Enter>", on_enter)
    signup_button.bind("<Leave>", on_leave)

    login_win.mainloop()
    
def initialize_gui(username):
    global tree, screenshot_label, root

    root = tk.Tk()
    root.title(f"User Activity Monitor - Logged in as {username}")
    root.geometry("1000x600")
    root.configure(bg="#2E3440")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#3B4252", foreground="#ECEFF4", rowheight=25, fieldbackground="#3B4252")
    style.configure("Treeview.Heading", background="#4C566A", foreground="#ECEFF4", font=("Helvetica", 10, "bold"))
    style.map("Treeview", background=[("selected", "#5E81AC")])

    columns = ("Application", "Start Time", "Usage Time (s)", "Key Presses", "Mouse Clicks")
    
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.heading("Application", text="Application")
    tree.heading("Start Time", text="Start Time")
    tree.heading("Usage Time (s)", text="Usage Time (s)")
    tree.heading("Key Presses", text="Key Presses")
    tree.heading("Mouse Clicks", text="Mouse Clicks")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscroll=scrollbar.set)

    screenshot_label = tk.Label(root, bg="#2E3440")
    screenshot_label.pack(pady=10)

    logout_button = tk.Button(root, text="Logout", command=logout)
    logout_button.pack(pady=10)

    Thread(target=monitor_activity, daemon=True).start()

    keyboard_listener = keyboard.Listener(on_press=key_event_handler)
    mouse_listener = mouse.Listener(on_click=mouse_event_handler)
    keyboard_listener.start()
    mouse_listener.start()

    root.mainloop()

def logout():
    root.destroy()
    login_window()

if __name__ == "__main__":
    login_window()
