"""
MIT License

Copyright (c) 2023 ArtCHeV

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import subprocess
import re
import tkinter as tk
from tkinter import messagebox

def get_wifi_profiles() -> list:
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode('cp866')
    wifi_profiles = re.findall(r"(?:All User Profile|Все профили пользователей)\s*: (.*)(\r)?", command_output)
    wifi_profiles = [profile_name[:-1:] for profile_name, _ in wifi_profiles]
    return wifi_profiles

def get_wifi_password(profile_name: str) -> str:
    password_command_output = subprocess.run(["netsh", "wlan", "show", "profile", "name=" + profile_name, "key=clear"], capture_output = True).stdout.decode('cp866')
    password_line = re.search(r"(?:Содержимое ключа|Key Content)\s*: (.*)\r?", password_command_output)
    password = password_line[1] if password_line else None
    return password

def display_password():
    profile_name = wifi_profiles_listbox.get(wifi_profiles_listbox.curselection())
    password = get_wifi_password(profile_name)
    messagebox.showinfo("Wi-Fi Password", f"Password for {profile_name}: {password}")

# Create main window
root = tk.Tk()
root.title("Wi-Fi Password Viewer")

# Create listbox for wifi profiles
wifi_profiles_listbox = tk.Listbox(root)
wifi_profiles_listbox.pack()

# Load wifi profiles into listbox
wifi_profiles = get_wifi_profiles()
for profile in wifi_profiles:
    wifi_profiles_listbox.insert(tk.END, profile)

# Create button to display selected password
display_password_button = tk.Button(root, text="Display Password", command=display_password)
display_password_button.pack()

root.mainloop()
