# wifi-password-dumper

This script allows you to dump saved Wi-Fi passwords from Windows, Linux, and Android devices. It automatically retrieve all saved Wi-Fi passwords.

## Features

- **Windows**: Uses `netsh` to retrieve saved Wi-Fi passwords.
- **Linux**: Reads Wi-Fi passwords from the `NetworkManager` system connections files.
- **Android**: Reads Wi-Fi passwords from the `wpa_supplicant.conf` file (root access required).

## Requirements

- **Windows**: No additional dependencies. The script uses `netsh`, which is available by default.
- **Linux**: Requires `sudo` or root access to read the system network configurations.
- **Android**: Requires root access to access the `wpa_supplicant.conf` file.

## Installation

1. Clone this repository or download the script to your device.
   ```
   git clone https://github.com/saltX5/silver-eureka.git
   ```
2. Navigate to the Project Folder
   ```
   cd silver-eureka
   ```
3. Run the Script
   ```
   python main.py
   ```
3. Select your device
   ```
   Which device are you on?
    1. Windows
    2. Linux
    3. Android

    Enter your choice (1, 2, or 3): 1
     Network1                    |  password1
     Network2                    |  password2
   ```
