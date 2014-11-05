#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: f314labs@gmail.com

# Purpose: 
#	Display temperature & humidity measurements:
#	 - done using a DHT-11 sensor connected to a Raspberry Pi computer
#	 - collected in CSV format
#	 - parsed using Papa parse
#	 - displayed using Highcharts
	 
# Project under Attribution, Non-Commercial (CC BY-NC 4.0) Creative Commons License
# http://creativecommons.org/licenses/by-nc/4.0/

# Derived from:
#
# Google Spreadsheet DHT Sensor Data-logging Example
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import time
import datetime

import Adafruit_DHT

# Type of sensor, can be Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT_TYPE = Adafruit_DHT.DHT11

# Sensor connected to Raspberry Pi pin 4
DHT_PIN  = 4




def open_file (filename):
	try:
		f = open(filename, "w")
		return f
	except:
		print 'Erreur d\'ouverture du fichier {}'.format(filename)
		sys.exit(1)


FREQUENCY_SECONDS      = int(sys.argv[1])

# Au moins 10 secondes entre 2 mesures

if FREQUENCY_SECONDS < 10 : 
	FREQUENCY_SECONDS = 10
        print 'Fréquence des mesures forcée à 10 secondes'

FICHIER 	       = sys.argv[2]

print 'Mesure toutes les {0} secondes et stockage au format CSV format dans {1}'.format(FREQUENCY_SECONDS , FICHIER)

NBMES = 0
if len(sys.argv) == 4:
	NBMES = int(sys.argv[3])
        print 'Le programme s\'arrêtera après {} mesures'.format(NBMES)
else:
	print 'Tapez Ctrl-C pour sortir.'

print ''

f = None
nbmes = 0
go_on = True

while go_on:

        if f is None:
		f = open_file(FICHIER)
                f.write("Date;Temp;Humid\n"); 

	# Attempt to get sensor reading.
        humid, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)

	# Skip to the next reading if a valid measurement couldn't be taken.
	# This might happen if the CPU is under a lot of load and the sensor
	# can't be reliably read (timing is critical to read the sensor).
	if humid is None or temp is None:
		time.sleep(2)
		continue
    # ATTENTION:
	# Le DHT-11 a une résolution de 8 bits: mesures en entier
    # Pour un DHT-22 (résolution 16 bits) prévoir un traitement des decimales --> type float    
	i_humid = int(humid) 
	i_temp = int(temp)

	now = datetime.datetime.now()
	fnow = now.strftime("%Y-%m-%d %H:%M:%S")
	print fnow
	print 'Temperature: {:d} °C'.format(i_temp)
	print 'Humidité:    {:d} %'.format(i_humid)

	data_record = '{}; {:d}; {:d}\n'.format(fnow, i_temp, i_humid)
	
	# Append the data in the spreadsheet, including a timestamp
	try:
		f.write(data_record)
		f.flush() # So that the file with up-to-date data can be used by other apps
	except:
		print 'Erreur ecriture fichier'
		sys.exit(1)

	# Wait 30 seconds before continuing
        nbmes += 1
	if (NBMES):
		go_on = (nbmes < NBMES)
		print 'Enregistrement {:d} sur {:d}'.format(nbmes, NBMES)
	
	print 'Enregistrement inscrit\n'
	time.sleep(FREQUENCY_SECONDS)

f.close()

