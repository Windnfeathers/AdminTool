import win32security
import os
import datetime
import socket
import serial.tools.list_ports
import uuid
import tkinter as tk
import subprocess
import psutil

"""
Dependencies:
- Python 3.x
- pywin32: Provides access to the Windows API, including `win32security` (for the login function)
  Install using: pip install pywin32
- pyserial: Module encapsulating access for the serial port, including `serial.tools.list_ports`
  Install using: pip install pyserial
- psutil: Cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python
  Install using: pip install psutil
- tkinter: Standard Python interface to the Tk GUI toolkit (included with Python standard library)
- uuid: Included with Python standard library for generating unique identifiers
- datetime: Included with Python standard library for manipulating dates and times
- socket: Included with Python standard library for low-level networking interface
- subprocess: Included with Python standard library for spawning new processes, connecting to their input/output/error pipes, and obtaining their return codes
"""

# Define the colors
PURPLE = "#7e549f"  # Purple color
GREY = "#c0c0c0"    # Grey color

def calculate():
    # Get the current school year
    i = datetime.datetime.now()
    month = ("%s" % i.month)
    year = ("%s" % i.year)
    if int(month) > 6:
        date = (int(year) + 1)
    else:
        date = year
    current_school_year = date

    # Check which field is filled out and calculate the appropriate result
    if grade_entry.get():
        # Get the input grade and convert it to a graduation year
        input_grade = grade_entry.get()
        if input_grade.lower() == "pk":
            grade = "0"
        elif input_grade.lower() == "kg":
            grade = "1"
        else:
            grade = int(input_grade) + 1
        grad_year = int(current_school_year) + 13 - int(grade)

        # Update the GUI with the result
        result_label.config(text=f"Graduation Year: {grad_year}")

    elif year_entry.get():
        # Get the input graduation year and convert it to a grade level
        grad_year = year_entry.get()
        grade = int(current_school_year) + 12 - int(grad_year)
        if str(grade) == "-1":
            grade = "PK"
        if str(grade) == "0":
            grade = "KG"

        # Update the GUI with the result
        result_label.config(text=f"Students Grade Level: {grade}")

def login():
    # Get the user's domain, username, and password from the input fields
    domain = domain_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    try:
        # Attempt to log in using the entered credentials
        hUser = win32security.LogonUser(
            username,
            domain,
            password,
            win32security.LOGON32_LOGON_NETWORK,
            win32security.LOGON32_PROVIDER_DEFAULT
        )
    except win32security.error:
        # Display a message indicating that the login failed
        login_result.config(text="Login Failed", fg="red")
    else:
        # Display a message indicating that the login succeeded
        login_result.config(text="Login Succeeded", fg="green")

def clear():
    # Clear all input fields and result labels
    grade_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    domain_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    login_result.config(text="")
    result_label.config(text="")

def clear_ping_results():
    # Clear ping results and host entry field
    host_entry.delete(0, tk.END)
    ping_google_result_label.config(text="")
    ping_host_result_label.config(text="")

def list_com_ports_in_gui():
    com_ports = serial.tools.list_ports.comports()
    if com_ports:
        com_ports_text = "\n".join([f"{port}: {desc}" for port, desc, hwid in com_ports])
        com_ports_label.config(text="Available COM ports:\n" + com_ports_text)
    else:
        com_ports_label.config(text="No COM ports available.")

def refresh():
    # Refresh the COM port list and display in GUI
    list_com_ports_in_gui()

    # Refresh the IP address and display in GUI
    ip_label.config(text=f"IP address: {get_local_ip()}")

def parse_ping_output(output):
    loss = 0
    time_ms = None
    for line in output.splitlines():
        if 'Lost =' in line or 'loss' in line:
            loss = int(line.split('%')[0].split()[-1].replace('(', '').replace(')', ''))
        if 'time=' in line or 'time<' in line:
            time_ms = line.split('time=')[1].split('ms')[0].strip() if 'time=' in line else '<1'
    return loss, time_ms

def ping_google():
    google_ip = '8.8.8.8'
    try:
        response = subprocess.run(['ping', '-n', '4', google_ip], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        loss, time_ms = parse_ping_output(response.stdout)
        if loss <= 50:
            ping_google_result_label.config(text=f"Google Ping: Success ({time_ms} ms, {loss}% loss)")
        else:
            ping_google_result_label.config(text=f"Google Ping: Fail ({loss}% loss)")
    except Exception as e:
        ping_google_result_label.config(text=f"Google Ping: Error ({e})")

def ping_host():
    host = host_entry.get()
    if host:
        try:
            response = subprocess.run(['ping', '-n', '4', host], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            loss, time_ms = parse_ping_output(response.stdout)
            if loss <= 50:
                ping_host_result_label.config(text=f"Ping {host}: Success ({time_ms} ms, {loss}% loss)")
            else:
                ping_host_result_label.config(text=f"Ping {host}: Fail ({loss}% loss)")
        except Exception as e:
            ping_host_result_label.config(text=f"Ping {host}: Error ({e})")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unable to determine IP"
    

# Create the main window
root = tk.Tk()
root.title("AdminTool 2.1")
try:
    root.iconbitmap("admin-tools.ico")
except:
    pass
root.configure(bg=GREY)  # Set the background color to grey

padding_frame = tk.Frame(root, height=20, bg=GREY)
padding_frame.pack(fill=tk.X)

# Create a frame for the input fields
input_frame = tk.Frame(root)

# Create a label and entry for the grade
grade_label = tk.Label(input_frame, text="Grade:")
grade_entry = tk.Entry(input_frame)
grade_label.pack(side=tk.LEFT)
grade_entry.pack(side=tk.LEFT)

# Create a label and entry for the graduation year
year_label = tk.Label(input_frame, text="Graduation Year:")
year_entry = tk.Entry(input_frame)
year_label.pack(side=tk.LEFT)
year_entry.pack(side=tk.LEFT)

# Create a frame for the login fields
login_frame = tk.Frame(root, bg=GREY)

# Create a label and entry for the domain
domain_label = tk.Label(login_frame, text="Domain:", bg=GREY)
domain_entry = tk.Entry(login_frame)
domain_label.pack(side=tk.LEFT)
domain_entry.pack(side=tk.LEFT)

# Create a label and entry for the username
username_label = tk.Label(login_frame, text="Username:", bg=GREY)
username_entry = tk.Entry(login_frame)
username_label.pack(side=tk.LEFT)
username_entry.pack(side=tk.LEFT)

# Create a label and entry for the password
password_label = tk.Label(login_frame, text="Password:", bg=GREY)
password_entry = tk.Entry(login_frame, show="*")
password_label.pack(side=tk.LEFT)
password_entry.pack(side=tk.LEFT)

# Create a button for logging in
login_button = tk.Button(login_frame, text="Login", command=login)
login_button.pack(side=tk.LEFT)

# Create a label for the login result
login_result = tk.Label(root, text="", width=20)

# Create a frame for the buttons
button_frame = tk.Frame(root)

# Create a button for calculating the result
calc_button = tk.Button(button_frame, text="Calculate", command=calculate)
calc_button.pack(side=tk.LEFT)

# Create a label for the result
result_label = tk.Label(root, text="")

# Create a button for clearing the inputs
clear_button = tk.Button(button_frame, text="Clear", command=clear)
clear_button.pack(side=tk.LEFT)

# create a horizontal line separator
separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)

# Pack the frames and labels into the main window
input_frame.pack()
button_frame.pack()
result_label.pack()
login_frame.pack()
login_result.pack()
separator.pack(fill=tk.X, padx=5, pady=5)
com_ports_label = tk.Label(root, text="")
com_ports_label.pack()
refresh_frame = tk.Frame(root)
refresh_button = tk.Button(refresh_frame, text="Get COM Ports", command=refresh)
refresh_button.pack()
refresh_frame.pack()
separator.pack(fill=tk.X, padx=5, pady=5)

# Ping Google controls
ping_google_frame = tk.Frame(root)
ping_google_button = tk.Button(ping_google_frame, text="Ping Google", command=ping_google)
ping_google_button.pack(side=tk.LEFT)

ping_google_frame.pack()
ping_google_result_label = tk.Label(root, text="")
ping_google_result_label.pack()

# Separator between ping options
separator2 = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
separator2.pack(fill=tk.X, padx=5, pady=5)

# Ping Host controls
ping_host_frame = tk.Frame(root)
host_label = tk.Label(ping_host_frame, text="Host:")
host_entry = tk.Entry(ping_host_frame)
host_label.pack(side=tk.LEFT)
host_entry.pack(side=tk.LEFT)

ping_host_button = tk.Button(ping_host_frame, text="Ping Host", command=ping_host)
ping_host_button.pack(side=tk.LEFT)

ping_host_frame.pack()
ping_host_result_label = tk.Label(root, text="")
ping_host_result_label.pack()

# Create a button for clearing the ping results
clear_ping_button = tk.Button(root, text="Clear Ping Results", command=clear_ping_results)
clear_ping_button.pack(pady=5)

# Get the IP address
ip = get_local_ip()

# Get the MAC address
mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])

# Create labels to display the IP and MAC addresses
ip_label = tk.Label(root, text=f"IP address: {ip}", bg=GREY)
mac_label = tk.Label(root, text=f"MAC address: {mac}", bg=GREY)

# Pack the labels and separator onto the window
ip_label.pack()
mac_label.pack()
separator.pack(fill=tk.X, padx=5, pady=5)

# Apply color scheme to the elements
grade_label.configure(bg=GREY, fg=PURPLE)
year_label.configure(bg=GREY, fg=PURPLE)
login_button.configure(bg=PURPLE, fg="white")
calc_button.configure(bg=PURPLE, fg="white")
clear_button.configure(bg=PURPLE, fg="white")
refresh_button.configure(bg=PURPLE, fg="white")
ping_google_button.configure(bg=PURPLE, fg="white")
ping_host_button.configure(bg=PURPLE, fg="white")
clear_ping_button.configure(bg=PURPLE, fg="white")
result_label.configure(bg=GREY, fg=PURPLE)
login_result.configure(bg=GREY, fg=PURPLE)
com_ports_label.configure(bg=GREY, fg=PURPLE)
ping_google_result_label.configure(bg=GREY, fg=PURPLE)
ping_host_result_label.configure(bg=GREY, fg=PURPLE)
refresh_frame.configure(bg=GREY)

# Start the GUI main loop
root.mainloop()
