-----------------------------------------------------------------
Paketsensor Dokumentation

*****************************************************************
Setup und Installation

*****************************************************************
API Dokumentation

Die API wird lokal gehostet ung läuft auf Port 5000
Die Basis für alle Adressen lautet daher 'http://127.0.0.1:5000'

Adresse  	 |Erlaubte Mthoden 
-------------|-----------------
/Control 	 |GET			   
/Data	 	 |GET			   
/Data/Update |POST


/Control
Gibt bei aktiver API "up and running" zurück.

/Data
Gibt bei Aufruf den zuletzt gespeicherten Wert als JSON zurück.
{"datenpunkt": wert als float}
Bei Fehlern wird -99999.9 als Wert übermittelt 

/Data/Update
Wird genutzt um den gespeicherten Gewichtswert zu aktualisieren.

Gibt bei Erfolg den hochgeladenen Wert als JSON zurück.
{"datenpunkt": wert als float}


*****************************************************************
Tara und Genauigkeit

Zur Tarierung der Wägeeinheit kann das Programm "tara.exe" 
(tara.py) verwendet werden.
Hierbei müssen Die Zinken vom boden gehoben sein
und sich im Stillstand befinden.
Dieser Vorgang muss nur zur Einrichtung eines Sensors im Fahrzeug
durchgeführt werden. 

Der verwendete serielle Port muss in der Datei "config.ini"
festgelegt werden. (z.B.: com_port= 6)

Die Wägeungenauigkeit beträgt
bei Stillstand <50kg
bei unsanfter Fahrt <150kg

*****************************************************************
Simulationsprogramm

Mithilfe des Programms "Paketsensor_Simulator.exe "
(Paketsensor_Simulator.py)
Dieses sendet im Abstand von einer Sekunde einen Wert an die API.
Der Wert wird Sinusförmig zwischen 0kg und 10000kg bewegt.

*****************************************************************
Im Auftrag der
Nord-ks GmbH & Co. KG

Geschrieben von
Jonas Schindzielorz
-----------------------------------------------------------------