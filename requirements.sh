#!/bin/bash


echo "[*] Requirements installing..."


apt update && pkg upgrade -y


apt install python3 -y
pip install --upgrade pip --break-system-packages


pip install requests colorama pyfiglet --break-system-packages


apt install dsniff -y
 

echo "[+] Requirements done!
