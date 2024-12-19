import subprocess
import platform
import os
import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip  # For clipboard copying

def get_windows_wifi_passwords():
    data = (
        subprocess.check_output(["netsh", "wlan", "show", "profiles"])
        .decode("utf-8")
        .split("\n")
    )
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    wifi_data = []
    for i in profiles:
        results = (
            subprocess
            .check_output(["netsh", "wlan", "show", "profile", i, "key=clear"])
            .decode("utf-8")
            .split("\n")
        )
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        wifi_data.append((i, results[0] if results else ""))
    return wifi_data

def get_linux_wifi_passwords():
    networks_folder = "/etc/NetworkManager/system-connections/"
    if not os.path.exists(networks_folder):
        return "NetworkManager folder not found!"

    networks = os.listdir(networks_folder)
    wifi_data = []
    for network in networks:
        try:
            with open(f"{networks_folder}/{network}", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if "psk=" in line:
                        wifi_data.append((network, line.split('=')[1].strip()))
                        break
        except PermissionError:
            return "Permission denied! Try running as root."
    return wifi_data

def get_android_wifi_passwords():
    if os.geteuid() != 0:
        return "You need root access to retrieve Wi-Fi passwords on Android."
    try:
        with open("/data/misc/wifi/wpa_supplicant.conf", "r") as f:
            lines = f.readlines()
            wifi_data = []
            for line in lines:
                if "psk=" in line:
                    wifi_data.append((line.split('=')[0].strip(), line.split('=')[1].strip()))
            return wifi_data
    except FileNotFoundError:
        return "wpa_supplicant.conf not found!"
    except PermissionError:
        return "Permission denied! Try running as root."

def get_wifi_passwords(device_type):
    if device_type == "windows":
        return get_windows_wifi_passwords()
    elif device_type == "linux":
        return get_linux_wifi_passwords()
    elif device_type == "android":
        return get_android_wifi_passwords()

class WiFiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wi-Fi Password Retriever")
        self.root.geometry("700x500")
        self.root.config(bg="#f4f4f4")

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="Wi-Fi Password Retriever", font=("Arial", 16, "bold"), bg="#f4f4f4")
        title_label.pack(pady=10)

        # Device Type Selection
        self.device_type_label = tk.Label(self.root, text="Select Device Type:", font=("Arial", 12), bg="#f4f4f4")
        self.device_type_label.pack(pady=5)
        
        self.device_type_var = tk.StringVar(value="windows")
        self.device_type_menu = tk.OptionMenu(self.root, self.device_type_var, "windows", "linux", "android")
        self.device_type_menu.pack(pady=5)

        # Fetch Button
        self.fetch_button = tk.Button(self.root, text="Fetch Wi-Fi Passwords", font=("Arial", 12, "bold"), bg="#9CFF1E", command=self.fetch_data)
        self.fetch_button.pack(pady=20)

        # Table Frame
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack()

        # Define Table Styling
        self.style = ttk.Style()
        self.style.configure("Treeview",
                             background="#f4f4f4",
                             foreground="black",
                             fieldbackground="#f4f4f4",
                             font=("Arial", 10))
        self.style.configure("Treeview.Heading",
                             background="#9CFF1E",
                             font=("Arial", 12, "bold"),
                             foreground="black")
        self.style.map('Treeview', background=[('selected', '#006400')])  # Highlight row on selection

    def fetch_data(self):
        device_type = self.device_type_var.get()

        wifi_data = get_wifi_passwords(device_type)

        if isinstance(wifi_data, str):  # Error message
            messagebox.showerror("Error", wifi_data)
        else:
            self.display_table(wifi_data)

    def display_table(self, wifi_data):
        for widget in self.table_frame.winfo_children():
            widget.destroy()  # Clear any previous table content

        # Create Table Header
        headers = ["Network Name", "Password"]
        table = ttk.Treeview(self.table_frame, columns=headers, show="headings", height=15)
        table.pack(pady=10)

        for header in headers:
            table.heading(header, text=header)

        # Populate Table with data
        for network, password in wifi_data:
            table.insert("", "end", values=(network, password))

        # Bind the copy function to double-clicking a password
        table.bind("<Double-1>", self.copy_to_clipboard)

    def copy_to_clipboard(self, event):
        item = event.widget.selection()  # Get selected item
        if not item:
            return
        # Get the password value (second column)
        password = event.widget.item(item)["values"][1]
        pyperclip.copy(password)  # Copy to clipboard
        messagebox.showinfo("Copied", f"Password '{password}' copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = WiFiApp(root)
    root.mainloop()
