import subprocess
import platform
import os

def get_windows_wifi_passwords():
    data = (
        subprocess.check_output(["netsh", "wlan", "show", "profiles"])
        .decode("utf-8")
        .split("\n")
    )
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    for i in profiles:
        results = (
            subprocess
            .check_output(["netsh", "wlan", "show", "profile", i, "key=clear"])
            .decode("utf-8")
            .split("\n")
        )
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        try:
            print("{:<30}|  {:<}".format(i, results[0]))
        except IndexError:
            print("{:<30}|  {:<}".format(i, ""))

def get_linux_wifi_passwords():
    # Linux stores Wi-Fi passwords in the NetworkManager folder or wpa_supplicant.conf
    networks_folder = "/etc/NetworkManager/system-connections/"
    if not os.path.exists(networks_folder):
        print("NetworkManager folder not found!")
        return

    networks = os.listdir(networks_folder)
    for network in networks:
        try:
            with open(f"{networks_folder}/{network}", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if "psk=" in line:
                        print(f"{network:<30}|  {line.split('=')[1].strip()}")
                        break
        except PermissionError:
            print("Permission denied! Try running as root.")

def get_android_wifi_passwords():
    # Android: This requires root access and the script will access the wpa_supplicant.conf file
    if os.geteuid() != 0:
        print("You need root access to retrieve Wi-Fi passwords on Android.")
        return
    try:
        with open("/data/misc/wifi/wpa_supplicant.conf", "r") as f:
            lines = f.readlines()
            for line in lines:
                if "psk=" in line:
                    print(f"{line.split('=')[0].strip():<30}|  {line.split('=')[1].strip()}")
    except FileNotFoundError:
        print("wpa_supplicant.conf not found!")
    except PermissionError:
        print("Permission denied! Try running as root.")

def get_wifi_passwords(device_type):
    if device_type == "windows":
        get_windows_wifi_passwords()
    elif device_type == "linux":
        get_linux_wifi_passwords()
    elif device_type == "android":
        get_android_wifi_passwords()

def main():
    print("Which device are you on?")
    print("1. Windows")
    print("2. Linux")
    print("3. Android")
    device_type = input("Enter your choice (1, 2, or 3): ").lower()

    if device_type == "1":
        get_wifi_passwords("windows")
    elif device_type == "2":
        get_wifi_passwords("linux")
    elif device_type == "3":
        get_wifi_passwords("android")
    else:
        print("Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    main()
