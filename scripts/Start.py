"""
Startet die API und mit ein wenig Zeitverzögerung auch die Software zur datenerfassung.
Kann an Autostart angehängt werden.
Zu öffnende Dateien müssen in einem Ordner 'dist' liegen, der im selben
Verzeichnis liegt wie diese Anwendung
"""

import os
import time

os.startfile("dist\Paketsensor_API.exe")
time.sleep(2)
os.startfile("dist\Paketsensor_write_output.exe")