.. ulyxes_user_documentation

######
ULYXES
######
User's Guide
------------


.. topic:: Overview

    This documentation stands as an User Manual of `Ulyxes <http://www.agt.bme.hu/ulyxes/>`_ system. The main aim of it is to represent the Ulyxes system and describe the usage of it with given examples and tutorials.



    :Date: 2022-01-04
    :Authors: **Daniel Moka** <mokabme@gmail.com>, **Zoltan Siki** <siki.zoltan@emk.bme.hu>
    :Version: 1.0


.. contents:: 
    :depth: 5

.. sectnum::

.. raw:: LaTeX

   \newpage


Introduction
############

Ulyxes is an open source project to drive Robotic Total Stations (RTS) and
other location aware sensors and publish observation results on web based maps 
(GPL 2). The name of Ulyxes come from the Greek Odysseus who was a legendary
Greek king of Ithaca island. Or it can be resolved as Ultimate Y X Estimation
System.

The first aim of the project is to create a framework to drive different 
location aware sensors from a computer, furthermore publish the data on the
Internet. The project is based on several open source projects and programming
languages. The overview of the system can been seen on the following figure:

.. figure:: img/ulyxes_overview.png
    :align: center
    :scale: 74
    :alt: Overview Ulyxes

    Ulyxes system overview

System Divisions
################

Publisher Interface
*******************

The first part of the system is the publishing interface where the measurement
results and the related analysis are published in the form of maps, tables and 
graphs with the associated Geo-spatial visualization. The interface works within
an Internet browser (e.g. Mozzila Firefox or Google Chrome) which supports to
run Javascript. As for operation system, the interface is cross-platform so it
can be used on any operation system.

Servers
*******

There are number of open source server projects contribute the back-end
operation of the system. In order to store the observation data in databases,
Ulyxes uses PostgreSQL/PostGIS object relational database. The data flow from 
the database to the web-server is solved by using PHP scriptins or MapServer. 
The webserver is driven and supported by the Apache Web Server. In addition, 
other possibilities and alternatives can be used to solve the server side works,
for example a Map Server (Web Map Service - WMS) can be also an effective 
solution.


Sensor Managers
***************

The system contains two different API independent from each other: the 
**TclAPI** and the **PyAPI**. The TclAPI is the old and its development is 
finished (depricated). Tha PyAPI is the new and actively developed.

PyAPI
=====

First of all the TclAPI is only able to control total stations and GPSs. The
usage of such instruments does not raise controversies, however other sensors
(i.e. web-cameras or Miro-Electro-Mechanical (MEMS) Sensors) can be also 
effectively used for certain motion monitoring tasks. Furthermore, as for the 
long term tasks the changes of the atmosphere influence our measurements, 
therefore meteorological sensors should be used to determine the meteorological 
elements which with the total stations can be maintained. To easily integrate 
such a different kind of instruments to the system, we decided to rethink our 
system so the PyAPI was created which is based on Python object oriental
language (OOP). Python is a general purpose high-level programming language
that provides a very fast development and testing tools for the user. It has 
countless additional library which can significantly contribute and help the 
programmers' work. Last but not least the biggest commercial and open source 
applications (QGIS, ArcGIS) have selected Python for development tool. (For 
more info, visit https://www.python.org/)

PyAPI is an Application Programming Interface (API) provides several classes to
handle different sensors e.g. Totalstations, NMEA GNSS receivers, MEMS sensors,
web-cameras. The API still only has a beta version.

It has been already tested with the following type of instruments:

    * Leica TS 15i
    * Leica TCA1800 
    * Leica TPS120x
    * Leica TPS110x 
    * STEC Axis 10
    * Trimble 550x
    * Leica DNA03
    * TopCon HiperPro II
    * U-blox F9P
    * Garmin GPS18 
    * Leica GPS 500 
    * USB WebCam
    * RasPi camera

Specification
^^^^^^^^^^^^^

*Supported OS (Operating System):*

    * Linux (probably any distro, tested on Fedora, Ubuntu, Raspbian) 
    * Windows XP/Vista/7/8/10 (32 and 64 bit) (tested on XP/7/10) 
    * any other OS with Python 2.7.x/3.x installed (not tested)

*Requirements:*

    * Python 2.7.x/3.x
    * at least one serial port or USB to serial converter (tested with Prolific)
    * serial cabel to connect the instrument to the computer 
    * I2C interface for MEMS (Raspberry PI)

How to install Python 3.x
^^^^^^^^^^^^^^^^^^^^^^^^^

See: https://realpython.com/installing-python/

Required Python modules
^^^^^^^^^^^^^^^^^^^^^^^

*Standard modules*:

    * datetime
    * json
    * logging
    * math
    * os
    * re
    * socket
    * sys
    * tempfile
    * time
    * urllib
    * xml.etree.ElementTree
    
*Extra modules*:

    * pyserial
	* pybluez
    * smbus
    * sqlite3
    * wifi 
    * numpy
    * opencv

*External dependencies*:
    * GNU Gama
	* sqlite3, spatialite-bin
    * PostgreSQL

How to install PyAPI
^^^^^^^^^^^^^^^^^^^^

The PyAPI is a part of Ulyxes system. In order to install the API, the whole Ulyxes project folder has to be installed.

*Linux*

    1. Open a terminal
    2. Go to or make the desired “MyFolder” you want to install Ulyxes/PyAPI
    3. Clone the Ulyxes Git directory, so type: git clone https://github.com/zsiki/ulyxes.git
    4. The PyAPI can be found at: “MyFolder/Ulyxes/PyAPI”

*Windows*

    1. Go to https://github.com/zsiki/ulyxes.git Ulyxes Git website 
    2. On the website, you can find a “Download ZIP” button at the bottom right part
    3. The downloaded Ulyxes directory will contain the PyAPI



PyAPI Modules
#############

(For more detailed information and sources codes about modules of PyAPI, please visit the `official developer documentation <http://www.agt.bme.hu/ulyxes/pyapi_doc/>`_ of PyAPI  )

.. figure:: img/abstraction.png
    :align: center
    :alt: Overview Ulyxes

    Sensor Abstraction

|

*There are three groups of modules used by PyAPI:*

PyAPI Object-Model modules
**************************

The first group consist of modules which build up the logical model between sensors, interfaces and the writer.

Independent modules
*******************

angle.py
========

This module stands for storing angle value of numbers in radian internally. Using this class the angle conversions and sum/difference can be easily done. 

|

Supported angle units:

    * RAD  radians (e.g. 1.54678432)
    * DMS sexagesimal (Degree-Minit-Second, e.g. 123-54-24)
    * DEG decimal degree (e.g. 25.87659)
    * GON gradian whole circle is 400g (e.g. 387.7857)
    * NMEA ddmm.mmmm used in NMEA sentences (e.g. 47.338765)
    * PDEG pseudo sexagesimal (e.g. 156.2745 = 156-27-45)
    * SEC sexagesimal seconds
    * MIL mills the whole circle is 6400 mills

|

.. code:: python

    #Create Angle object with the given value and unit
    a1 = Angle("152-23-45", "DMS")
    #Convert a1 "angle" object to supported units
    for u in ['RAD', 'DMS', 'GON', 'NMEA', 'DEG', 'PDEG', 'MIL']:
        print (a1.GetAngle(u))


Readers
=======

reader.py is the base class for all readers (virtual).

confreader.py
^^^^^^^^^^^^^^^

ConfReader class can be used to read simple JSON configurations. It can load 
and validate JSON files based on a definition. It is used by applications
as a alternative solution to the command line switches.

csvreader.py
^^^^^^^^^^^^

Class to read csv file, first line may contain field names.
Default separator is semicolon (;).

.. code:: python

    # create a csvreader object
    cr = CsvReader('test', 'test.csv')
    # load the whole file into a list
    lines = cr.Load()

dbreader.py
^^^^^^^^^^^

DbReader reads observations and/or coordinates fron SQLite or PostgreSQL
database. Table names are fixed in the code.

filereader.py
^^^^^^^^^^^^^

Class to read file. It is mostly used as a base class for other readers
loading information from file.

.. code:: python
    
    # create a filereader object
    fr = FileReader('test', 'test.txt')
    # read and print the next line
    print (fr.GetNext())

georeader.py
^^^^^^^^^^^^

Class to read GeoEasy geo or coo files. Data are loaded into a list of
dictionaries. Possible keys in dictionaries:

* station - station ID
* ih - instrument height
* code - additional textual information to point
* id - target ID
* th - target height
* hz - horizontal direction
* v - zenith angle
* distance - slope distance
* hd - horizontal distance
* pc - prism constant
* north - north coordinate
* east - east coordinate
* elev - elevation
* datetime - date and time of observation
* faces - number of faces

Creating a new GeoReader instance a file name and a filter can be specified.
The filter is a list of the keys above. Only those lines are kept where all
filter keys are present. One can use a filter to load only 3D points from
the coordinate list.

.. code:: python
    
	# load 3D points from a GeoEasy coo file
	g = GeoReader(fname='your_file.coo', filt=['east', 'north', 'elev'])
	m = g.Load()	# load 3D points
	print(m)

httpreader.py
^^^^^^^^^^^^^

Read data from a remote web server using HTTP protocol and server side service
for POST/GET requests.

On the server side scripts have to be created. For example the query.php in 
the server folder fetches coodinates from a server side database and sends
them to the client httpreader.

imagereader.py
^^^^^^^^^^^^^^

ImageReader reads images from folder(s) or video file or web camera or
Raspberry Pi camera.

jsonreader.py
^^^^^^^^^^^^^

Simple JSON reader class used by confreader.py.

queuereader.py
^^^^^^^^^^^^^^

QueueReader reads data from memory queue.

sqlitereader.py
^^^^^^^^^^^^^^^

Load coordinates or observations from a spatialite database.
This class is OBSOLATE, use dbreader.py.

Writers
=======

All writer class inheriter from Writer virtual base class.

csvwriter.py
^^^^^^^^^^^^

dbwriter.py
^^^^^^^^^^^

echowriter.py
^^^^^^^^^^^^^

filewriter.py
^^^^^^^^^^^^^

geowriter.py
^^^^^^^^^^^^

httpwriter.py
^^^^^^^^^^^^^

imagewriter.py
^^^^^^^^^^^^^^

queuewriter.py
^^^^^^^^^^^^^^

sqlitewriter.py
^^^^^^^^^^^^^^^

Measure units
=============

gsiunit.py
^^^^^^^^^^

leicadnaunit.py
^^^^^^^^^^^^^^^

leicameasureunit.py
^^^^^^^^^^^^^^^^^^^

lsm9ds0unit.py
^^^^^^^^^^^^^^

nmeagnssunit.py
^^^^^^^^^^^^^^^

picameraunit.py
^^^^^^^^^^^^^^^

webmetmeasureunit.py
^^^^^^^^^^^^^^^^^^^^

wifiunit.py
^^^^^^^^^^^

External Python modules
***********************

Logging
=======
This module defines functions and classes which implement a flexible event
logging system for applications and libraries.

For more information, please visit the `official Logging documentation <https://docs.python.org/2/library/logging.html>`_.

Pyusb
=====
The PyUSB module provides for Python easy access to the host machine's Universal Serial Bus (USB) system.

For more information, please visit the `official PyUSB Github page <https://github.com/walac/pyusb>`_.

Pyserial
========
This module encapsulates the access for the serial port. It provides backends
for Python running on Windows, Linux, BSD (possibly any POSIX compliant system),
Jython and IronPython (.NET and Mono).

For more information, please visit the `official PySerial documentation <http://pyserial.sourceforge.net/pyserial.html#overview>`_.

Smbus
=====

TODO

Cv2/cv (OpenCV)
===============

OpenCV (Open Source Computer Vision Library: http://opencv.org) is an
open-source BSD-licensed library that includes several hundreds of computer
vision algorithms.

For more information, please visit the `official OpenCV documentation <http://docs.opencv.org/modules/core/doc/intro.html>`_.


PyAPI Tutorials
###############

Most of the Python modules contain a unit test part at the end (after
the if __name__ == "__main__":). These are also usage examples.

Use of the SerialInterface
**************************

The SearialIface class can be used alone to drive an instrument through the
serial chanel or as a building block of an Instrument instance.

.. code:: python

    from serialiface import SerialIface
    si = SerialIface('test', 'COM1')
    si.Send('%R1Q,9028:0,0,0')
    %R1P,0,0:

Sensor Creation
***************

All the sensors (instruments) are inherited from the Instrument virtual base 
class. A sensor consists of three building blocks:

* measure unit
* interface (communication)
* writer (saving observed data), optional

.. code:: python

    import logging
	from leicatps1200 import LeicaTPS1200
	from serialiface import SerialIface
    from echowriter import EchoWriter
    logging.getLogger().setLevel(logging.DEBUG)
    mu = LeicaTPS1200()
    iface = SerialIface("rs-232", "/dev/ttyUSB0")
    wrt = EchoWriter()
    ts = TotalStation("Leica", mu, iface, wrt)
    ts.SetEDMMode(ts.measureUnit.edmModes['RLSTANDARD'])
    ts.Move(Angle(90, 'DEG'), Angle(85, 'DEG'))
    ts.Measure()
    print (ts.GetMeasure())

PyAPPS Applications Tutorials
#############################

MeasureToPrism
**************

Repeated robotic totalstation observations to a single (slowly moving) point. 
It has several modes:

* 0 - determine horizontal movement of a point using reflectorless (RL) EDM
* 1 - determine movement ofa slowly moving prism
* 2 - determine vertical movement of a prims (supposing horizontal distance not changed
* 3 - determine vertical movement of a moving prism on a car/machine, we suppose horizontal distance is not changed
* 4 - determine 3D movement of a moving prism
* 5 - measure if prism stop moving for few seconds (stop and go) obsevations

Command line parameters:

* Sensor type 1100/1800/1200
* Mode 0-5
* EDM mode FAST/STANDARD
* serial port
* output file

Measurematrix
*************

An application to scan a region with given angle steps. Parameters are given in
the command line, the corners of the region are given by targeting manually on 
the points.
Commands line parameters are positional:

# number of horizontal intervals in the region
# number of vertical intervals in the region
# sensor (total station) type
# serial port
# output file

After starting the program the user have to target on the lower left corner of 
the region and the upper right corner of the region. The automatic observations
are started then. If no output file given the observations are written to the 
standard output.

NMEA_demo
*********

A simple demo application to read NMEA GGA sentences from GNSS receiver in an
infinite loop.

Horizsection
************

Scan horizontally around the total station with a given angle step in one or
more horizontal sections.

.. code:: text

    usage: horizsection.py [-h] [-l LOG] [--log_level LOG_LEVEL]
                           [--log_format LOG_FORMAT]
                           [--angle_step ANGLE_STEP]
                           [--station_type STATION_TYPE]
                           [--station_east STATION_EAST]
                           [--station_north STATION_NORTH]
                           [--station_elev STATION_ELEV]
                           [--station_ih STATION_IH] [-p PORT]
                           [--hz_start HZ_START] [--hz_top HZ_TOP]
                           [--max_angle MAX_ANGLE] [--max_top MAX_TOP]
                           [--tolerance TOLERANCE] [--iteration ITERATION]
                           [--height_list HEIGHT_LIST] [--wrt WRT]
                           [--coords COORDS] [--pid PID]
                           [--center_east CENTER_EAST]
                           [--center_north CENTER_NORTH] [--radius RADIUS]
                           [--radius_top RADIUS_TOP] [--gama GAMA]

    options:
      -h, --help            show this help message and exit
      -l LOG, --log LOG     Logfile name, default: stdout, "stdout" for
                            screen output
      --log_level LOG_LEVEL
                            Log level, default: 40
      --log_format LOG_FORMAT
                            Log format, default: time, level, message
      --angle_step ANGLE_STEP
                            Angle step in section [DEG], default: 5.0
      --station_type STATION_TYPE
                            Total station type, default: 1200
      --station_east STATION_EAST
                            Station east, default: None
      --station_north STATION_NORTH
                            Station north, default: None
      --station_elev STATION_ELEV
                            Station elevation, default: None
      --station_ih STATION_IH
                            Instrument height, default: 0.0
      -p PORT, --port PORT  Communication port, default: /dev/ttyUSB0
      --hz_start HZ_START   Horizontal start direction, default: actual
                            telescope direction
      --hz_top HZ_TOP       Horizontal start direction at top, default: same
                            as start
      --max_angle MAX_ANGLE
                            Max angle, default: whole circle
      --max_top MAX_TOP     Max angle at top, default: same as max
      --tolerance TOLERANCE
                            Height tolerance, default: 0.01
      --iteration ITERATION
                            Max iteration to find section, default: 10
      --height_list HEIGHT_LIST
                            list of elevations for more sections between
                            double quotes, default: single section at the
                            telescope direction
      --wrt WRT             Name of output file, default: stdout
      --coords COORDS       Name of coordinate file, default: None
      --pid PID             Starting point ID, default: 0
      --center_east CENTER_EAST
                            Center point east of section, default: None
      --center_north CENTER_NORTH
                            Center point north of section, default: None
      --radius RADIUS       Radius of section at bottom section, default:
                            None
      --radius_top RADIUS_TOP
                            Radius of section at top section, default: None
      --gama GAMA           Path to gama-local, default: gama-local

Parameters can be passed in a JSON file.

There are three possible application situations

# Station coordinates are given but no fixed points are given (*--coords*), it is supposed the station is orineted
# Station coordinates and fixed points (marked by prisms)  are given, orientation is calculated
# No station coordinates but fixed points (marked by prism) are given, station coordinates and orientation are calculated

After heights parameter more values can be given.

The range of the sections can be given by angles or a target. The two methos are mutual exclusive.
*--hz_start* defines the horizontal direction of first (bottom) section, *--max_angle* is the angle range of section to the rigth from the START. *--hz_top* and *--max_top* are the same for the last (top) section. Horozsection will interpolate between these values for other sections.
The other solution to set the *--center_east* and *--center_north* and *--radius*. Center point is the center of the sections, the radius defines the range to left and right. 

*--center_...* and *--radius** parameters have precedence to *--hz_stat*, *max_angle*, etc.

Section
*******

Scan in an arbitrary plain aroun the total station with a given angle step.

Monitoring
**********

This block consist of several apps to solve simple tasks for monitoring.

- *filemaker* creates an input file for monitoring using manual targeting (obsolate use coomaker instead)
- *filegen* creates an input file for monitoring from coordinates automaticly
- *coomaker* creates a GeoEasy format input file for monitoring using manual targeting
- *blindorientation* searches for a prism from a known station and calculates orientation angle
- *freestation* calculates station coordinates and orientation using GNU gama, approximate station coordinates must be given
- *anystation* calculates station coordinates and orientation using GNU gama, no approximate coordinates are necessary, the total station must have power search function
- *robot* makes automatic observation using a file from FileMaker or FileGen (obsolate use robotplus instead)
- *robotplus* complex monitoring application using FileGen, Blindorientation, FreeStation, AnyStation and Robot

FileMaker
=========

*This application is obsolate, use coomaker.*
It is a simple interactive app to create input file for monitoring observations.
First set up the total station on a known point and set the orientation.

Usage: filemaker.py output_file [sensor] [serial_port]

Start the application. Two types of output files can be generated, CSV dump 
(.dmp) or GeoEasy (.geo) file.
First it will prompt for the id of the station and the station coordinates.

For each target points the id and mode must be entered.

Target modes:

- ATR*n* use automatic targeting, n is prism type id (1/2/3/...)
- PR*n* prism with manual targeting
- RL reflectorless distance with manual targeting
- RLA automatic reflectorless ditance measurement to given direction
- OR orientation direction, manual targeting, no distance

.. NOTE::
   Generated output file cannot be used for Blindorientation because
   distance missing!

FileGen
=======

A simple application to create input observations file for robot.py or robotplus.py. 
The input is a coordinate list in GeoEasy coo or CSV format. The output is a 
GeoEasy geo or DMP file with bearings, zenith angles and distances from
the station to the points in the coordinate list.

Usage: filegen.py input_coo_file output_obs_file station_id instrument_height

Tha station_id is optional, if not given the first point in the coordinate list
is considered as the station. Instrument height is also optional, the default
value is 0.

CooMaker
========

A simple application to create coordinate and observation data for robot.py
or robotplus.py. User have to set up and orient the total station on the 
station and observe targets.

Usage: coomaker.py output_file sensor port

- output file: two files are created with the same name extensions .geo/.coo
- sensor: total station type 1100/1800/1200/5500
- port: serial port e.g. COM1 or /dev/ttyUSB0

Further data are given at the prompt of the program.

FreeStation
===========

An application to calculate free station from observations and coordinates.
A least squares estimation is used based on GNU gama.
It is used by robotplus application but can be used as a standalone application using CLI.

Usage: freestation.py input_file gama-local_path

- input_file: this parameter defines a pair of files observations and coordinates, two types are accepted dmp + cvs or geo + coo. See GeoEasy documentation for dmp, geo, coo formats. Csv file must have four columns: point_id, easting, northing, elevation.
- gama-local_path: path to gama-local program

AnyStation
==========

Solves the free station task if there are no approximate station coordinates are given.
The total station searches for prisms using power search and matches them with the given
coordinate list.

Blindorientation
================

This apllication tries to solve orientation. It searches for prisms.
First tries if a prism is in the view of telescope using Automatic Target Recognition (ATR).
If a target found it checks the distance and the zenith angle to find the 
target in the coordinate list and set the orientation angle on the 
instrument.

If no target found in the actual view it rotates the instrument to the first 
target supposing oriented instrument and set the orientation angle.

Finally it starts search using Power Search if it is available on the total 
station or starts a long searching algorithm.

Robot
=====

*This application is obsolate, please use robotplus.*
Sample application of Ulyxes PyAPI to measure a serie of points.

Usage: robot.py input_file output_file sensor port retry delay met met_addr met_par

Positional command line parameters:

- input_file: input file with directions .geo or .dmp
- output_file: output file with observations default stdout
- sensor: tcra1103/1100/tca1800/1800/tps1201/1200, default 1200
- port: serial port, default COM1
- retry: number of retry if target not found, default 3
- delay: delay between retries default 0
- met: name of met sensor BMP180/webmet, default None
- met_addr address of met sensor, i2c addres for BMP180 or internet address of webmet service
- met_par: parameters for webmet sensor

Input file is a GeoEasy geo file or a dmp (can be created by filemaker.py
or filegen.py).
Sample geo file::

    {2 S2} {3 0.0}                                   # station id & istrumnt h.
    {5 2} {7 6.283145} {8 1.120836} {4 PR0} {112 2}  # target id, hz, v, code,
    {5 T1} {7 2.022707} {8 1.542995} {4 RL} {112 2}  # number of faces
    {5 3} {7 3.001701} {8 1.611722} {4 OR} {112 2}
    {5 T2} {7 3.006678} {8 1.550763} {4 ATR1} {112 2}
    {5 4} {7 3.145645} {8 1.610680} {4 PR2} {112 2}
    {5 1} {7 6.002123} {8 1.172376} {4 PR} {112 2}
    {5 9} {7 6.235123} {8 1.178538} {4 RLA} {112 2}

    instead of code=4 you can define prism constant using code=20
    prism constant units are meter

Sample dmp file::

    station; id; hz; v; code;faces
    S2;2;6.283145;1.120836;PR0;2
    S2;T1;2.022707;1.542995;RL;2
    S2;3;3.001701;1.611722;OR;2
    S2;T2;3.006678;1.550763;ATR1;2
    S2;4;3.145645;1.610680;PR2;2
    S2;1;6.002123;1.172376;PR;2

Codes describe target type:

- ATRn: prism and automatic targeting, n referes to prism type 0/1/2/3/4/5/6/7 round/mini/tape/360/user1/user2/user3/360 mini
- ATR-n: prims and automatictargeting but wait for a keypress to measure
- PRn: prism, n referes to prism type 0/1/2/3/4/5/6/7 round/mini/tape/360/user1/user2/user3/360 mini, manual targeting
- RL: refrectorless observation, manual targeting
- RLA: reflectorless observation (automatic)
- OR: do not measure distance (orientation), manual targeting

In case of PR/RL/OR the program stops and the user have to aim at the target

Robotplus
=========

RobotPlus is the most comprehensive application. It is based on FileGen, 
BlindOrientation, FreeStation and Robot applications.
Besides the total station metheorological sensors are also supported.

There are so many parameters to this aplication that a JSON configuration 
file is applied to describe parameters.

The whole process consists of the following steps:

# Load JSON configuration file
# Generate the observations from the input coordinate list (using FileGen)
# Orientate total station (usinf BlindOrientation)
# Make observations to the reference/fix points (using Robot)
# Calculate station coordinates and precise orientation (using FreeStation)
# Make observations to the monitoring points and store data

During the process a log file is written, the log level DEBUG/INFO/WARNING/ERROR/FATAL can be set in the JSON config.

Usage: robotplus.py config.json

- config.json: JSON file describing parameters

There are several parameters in a config file, most parameters are optional.
Parameters:

- log_file: path to log file, file must exist!
- log_level: 10/20/30/40/50 for DEBUG/INFO/WARNING/ERROR/FATAL
- log_format: format string for log (default: "%(asctime)s %(levelname)s:%(message)s"), optional
- station_type: 1100/1200/1800
- station_id: pont id for the station
- station_height: instrument height above point, optional (default: 0)
- station_coo_limit: limitation for station coordinate change from free station (default 0.01 m), optional
- orientation_limit: distance limit for orientation to identify a target (default 0.1 m)
- faces: number of faces to measure (first face left for all pointt then face right) (default 1)
- face_coo_limit: maximum difference for face left and face right coords (m) (default: 0.01 m)
- face_dir_limit: maximum difference for face left and face right angle (rad) (default 0.0029 60")
- face_dist_limit: maximum difference for face left and face right dist (m) (default 0.01 m)
- directfaces: number of faces to measure (face left and right are measured directly) (default 1)
- avg_faces: 1/0 calculate average for faces of monitoring points and store only average/do not calculate average store individual faces, default: 1
- fix_list: list of fix points to calculate station coordinates, optional (default: empty)
- mon_list: list of monitoring points to measure, optional (default: empty)
- max_try: maximum trying to measure a point, optional (default: 3)
- delay_try: delay between tries, optional (default: 0)
- dir_limit: angle limit for false direction in radians (default 0.015. 5')
- dist_limit: distance limit for false direction in meters (default 0.1 m)
- port: serial port to use (e.g. COM1 or /dev/ttyS0 or /dev/ttyUSB0)
- coo_rd: source to get coordinates from
- coo_wr: target to send coordinates to
- obs_wr: target to send observations to
- met_wr: target to send meteorological observations to, optional (default: no output)
- inf_wr: target to send general information to
- decimals: number of decimals in output (coords and distances), optional (default: 4)
- gama_path: path to GNU Gama executable, optional (default: empty, no adjustment)
- stdev_angle: standard deviation of angle measurement (arc seconds), optional (default: 1)
- stdev_dist: additive tag for standard deviation of distance measurement (mm), optional (default: 1)
- stdev_dist1: multiplicative tag for standard deviation of distance measurement (mm), optional (default: 1.5)
- dimension: dimension of stored points (1D/2D/3D), optional (default: 3)
- probability: probability for data snooping, optional (default: 0.95)
- blunders: data snooping on/off 1/0, optional (default: 1)
- met: met sensor name WEBMET/BMP180/SENSEHAT, optional default None
- met_addr: URL to webmet data, optional (default: empty)
- met_par: parameters to webmet service, optional (default: empty)

Sample config file::

	{ "log_file": "/home/siki/ulyxes/data/rp103.log",
	  "log_level": 10,
	  "station_type": "1200",
	  "station_id": "103",
	  "station_height": 0.369,
	  "station_coo_limit": 0.1,
	  "orientation_limit": 0.05,
	  "faces": 1,
	  "directfaces": 1,
	  "fix_list": ["601", "603", "605", "607"],
	  "mon_list": ["602", "604", "606", "608", "601", "603", "605", "607"],
	  "max_try": 3,
	  "delay_try": 0,
	  "dir_limit": 0.015,
	  "port": "/dev/ttyUSB0",
	  "coo_rd": "/home/siki/ulyxes/data/labor.coo",
	  "coo_wr": "/home/siki/ulyxes/data/labor_out.coo",
	  "obs_wr": "/home/siki/ulyxes/data/labor_obs.geo",
	  "met_wr": "",
	  "inf_wr": "/home/siki/ulyxes/data/labor_inf.csv",
	  "decimals": 4,
	  "gama_path": "/home/siki/gama-2.07/bin/gama-local",
	  "stdev_angle": 1,
	  "stdev_dist": 1,
	  "stdev_dist1": 1.5,
	  "dimension": 3,
	  "probability": 0.95,
	  "blunders": 0
	}

To start robotplus from cron a simple shell script should be created::

    cd /home/your_name/ulyxes/pyapps
    python3 robotplus.py path_to_your_json_config


Camera Applications Tutorials
#############################

Video ArUco
***********

Find ArUco markers in recorded video or in webcam video stream.

.. code::

    usage: video_aruco.py [-h] [-f FPS] [-d DICT] [-c CODE] [--debug DEBUG]
                          [--delay DELAY] [-m CALIBRATION] [-s SIZE] [--hist]
                          [--lchanel] [--clip CLIP] [--tile TILE] [-o OUTPUT]
                          [-i IMG_PATH] [-t IMG_TYPE]
                          file_name

    positional arguments:
      file_name             video file to process or camera ID (e.g. 0)

    options:
      -h, --help            show this help message and exit
      -f FPS, --fps FPS     frame per sec
      -d DICT, --dict DICT  marker dictionary id, default=1 (DICT_4X4_100)
      -c CODE, --code CODE  marker id to search, if not given all found markers
                            are detected
      --debug DEBUG         display every nth frame with marked marker position,
                            default 0 (off)
      --delay DELAY         delay in seconds between frames in debug
      -m CALIBRATION, --calibration CALIBRATION
                            use camera calibration from file for undistort image
                            and pose estimation
      -s SIZE, --size SIZE  marker size for pose extimation, default: 0.28 m
      --hist                Increase image constrast using histogram
      --lchanel             Increase image constrast using histogram on lchanel
                            only
      --clip CLIP           Clip limit for adaptive histogram, use with --hist,
                            default: 3
      --tile TILE           Tile size for adaptive histogram, use with --hist,
                            default: 8
      -o OUTPUT, --output OUTPUT
                            name of output file
      -i IMG_PATH, --img_path IMG_PATH
                            path to save images to
      -t IMG_TYPE, --img_type IMG_TYPE
                            image type to save to, use with --img_path, default
                            png

Use the --fps switch to set the frame per seconds parameter of a recorded video.If you select debug mode, the delay between frames can be set in seconds.
It is highly recommended to calibrate camera (use charuco.py for calibration),
a yaml file should be given after --calibration switch. If the ArUco marker is 
near pependicular to the axis of the camera using --size the change of 
position is converted to metric value in the output file.

--hist, --lchanel, --clip and --tile are used to enhance image quality before
marker detection.

The output file contains the positions of detected ArUco markers with a
time stamp and id of markers. If marker code is given only that marker is 
printed into the output, otherwise all markers are detected and sent to 
output.

The images of the video stream can be saved to jpg or png files using 
--img_path and --img_type.

Sample commands:

.. code::

    python3 video_aruco.py 0

Use first camera, find all 4x4 markers and send the output to standard output.

.. code::

    python3 video_aruco.py --code 5 --dict 99 -m camera_calibration.yaml --fps 30 --hist 1_20220803_100445.h264

Pocess 30 fps recorded video, recornding started at 2022-08-03 10:04:45,
search for 3x3 ArUco marker with id = 5, consider the calibration data from the
camera_calibration.yaml file. Enhance image quality by increasing contrast.

Image ArUco
***********

Find ArUco markers in an image serie.

.. code::

    usage: imgs_aruco.py [-h] [-d DICT] [-c CODE] [--fast] [--debug DEBUG]
                         [--delay DELAY] [-m CALIBRATION] [-s SIZE] [--hist]
                         [--lchanel] [--clip CLIP] [--tile TILE] [-o OUTPUT]
                         file_names [file_names ...]

    positional arguments:
      file_names            image files to process

    options:
      -h, --help            show this help message and exit
      -d DICT, --dict DICT  marker dictionary id, default=1 (DICT_4X4_100)
      -c CODE, --code CODE  marker id to search, if not given first found marker
                            is used
      --debug DEBUG         display every nth frame with marked template position,
                            default 0 (off)
      --delay DELAY         delay in seconds between frames use with debug>0,
                            default 1
      -m CALIBRATION, --calibration CALIBRATION
                            use camera calibration from file
      -s SIZE, --size SIZE  marker size for pose extimation, default: 0.28 m
      --hist                Increase image constrast using histogram
      --lchanel             Increase image constrast using histogram on lchanel
                            only
      --clip CLIP           Clip limit for adaptive histogram, use with --hist,
                            default: 3
      --tile TILE           Tile size for adaptive histogram, use with --hist,
                            default: 8
      -o OUTPUT, --output OUTPUT
                            name of output file

It is very similar to video_aruco, but the images are read from the hard disk.

Video nth
*********

Read video file and write frames to image files.

.. code::

usage: video_nth.py [-h] [-s START] [-f FRAMES] [--steps STEPS] [-t] file_name

positional arguments:
  file_name             video file or input video chanel to process

options:
  -h, --help            show this help message and exit
  -s START, --start START
                        start frame to save from, default 0
  -f FRAMES, --frames FRAMES
                        number of frames to save, default 1
  --steps STEPS         save only every steps-th frame, default 1
  -t, --total           report total frame number, it ignores --start and

Video correlation
*****************

Get positions of a pattern in a video stream.

.. code::

    usage: video_correlation.py [-h] -t TEMPLATE [-f FPS] [-m METHOD] [-r]
                                [--fast] [-d DEBUG] [--delay DELAY]
                                [--calibration CALIBRATION] [-o OUTPUT]
                                [-i IMG_PATH] [--img_type IMG_TYPE]
                                file_name

    positional arguments:
      file_name             video file to process

    options:
      -h, --help            show this help message and exit
      -t TEMPLATE, --template TEMPLATE
                            template image to find in video frames
      -f FPS, --fps FPS     frame per sec
      -m METHOD, --method METHOD
                            method to compare video frame and template,
                            0/1/2/3/4/5 TM_SQDIFF/TM_SQDIFF_NORMED/TM_CCORR/TM_CCO
                            RR_NORMED/CV_TM_CCOEFF/CV_TM_CCOEFF_NORMED, default 5
      -r, --refresh_template
                            refresh template after each frames
      --fast                reduce input image size to double the template
      -d DEBUG, --debug DEBUG
                            display every nth frame with marked template position,
                            default 0 (off)
      --delay DELAY         delay in seconds between frames in debug
      --calibration CALIBRATION
                            use camera calibration from file for undistort image
                            and pose estimation
      -o OUTPUT, --output OUTPUT
                            name of output file
      -i IMG_PATH, --img_path IMG_PATH
                            path to save images to
      --img_type IMG_TYPE   image type to save to, use with --img_path, default
                            png

Image correlation
*****************

Get positions of a pattern in a serie of images.

.. code::

    usage: imgs_correlation.py [-h] -t TEMPLATE [-m METHOD] [-r] [--fast]
                               [-d DEBUG] [--delay DELAY]
                               [--calibration CALIBRATION] [-o OUTPUT]
                               file_names [file_names ...]

    positional arguments:
      file_names            image files to process

    options:
      -h, --help            show this help message and exit
      -t TEMPLATE, --template TEMPLATE
                            template image to find in video frames
      -m METHOD, --method METHOD
                            method to compare video frame and template,
                            0/1/2/3/4/5 TM_SQDIFF/TM_SQDIFF_NORMED/TM_CCORR/TM_CCO
                            RR_NORMED/CV_TM_CCOEFF/CV_TM_CCOEFF_NORMED, default 5
      -r, --refresh_template
                            refresh template after each frames
      --fast                reduce input image size to double the template
      -d DEBUG, --debug DEBUG
                            display every nth frame with marked template position,
                            default 0 (off)
      --delay DELAY         delay in seconds between frames use with debug>0,
                            default 1
      --calibration CALIBRATION
                            use camera calibration from file for undistort image
                            and pose estimation
      -o OUTPUT, --output OUTPUT
                            name of output file

Undistort images
****************

Using camera calibration data make an undistorted copy of images.

.. code::

    Usage: undist.py calibration_yaml image [image] [...]

Charuco calibration
*******************

Find camara calibration parameters from 15-20 images taken from different
direction of a charuco board.

.. code::

    usage: charuco.py [-h] [-b] [-w WIDTH] [-e HEIGHT] [-c] [-s] [-o OUTPUT]
                      [file_names ...]

    positional arguments:
      file_names            board images from different directions to process or a
                            video file

    options:
      -h, --help            show this help message and exit
      -b, --board           save only board image to charuco.png file
      -w WIDTH, --width WIDTH
                            Width of board, default 5, max 10
      -e HEIGHT, --height HEIGHT
                            Height of board, default 7, max 10
      -c, --camera          use first camera or video file to take photos until
                            enter pressed
      -s, --save            save camera images to file cal0.png, cal1.png if
                            camera is used
      -o OUTPUT, --output OUTPUT
                            output yaml camera calibration data file, default:
                            calibration_matrix.yaml

TclAPI (depricated)
===================

The TclAPI consist of a couple of Tcl (Tool Command Language) files/procs which
give a higher level interface to drive RTSs and GPSs from computer. The TclAPI 
is released under GNU GPL V2.0. This API is obsolate and no new functionality
will be added.

Specification
^^^^^^^^^^^^^

*Supported OS (Operating System):*

    * Linux (probably any distro, tested on Fedora and Ubuntu) 
    * Windows XP/Vista/7 (32 and 64 bit) (tested on XP/7) 
    * any other OS with Tcl 8.3 or newer installed (not tested)

|

*Requirements:*

    * Tcl (Tool Command Language) 8.3 or newer must be installed 
    * at least one serial port or USB to serial converter (tested with Prolific)
    * serial cabel to connect the instrument to the computer 

How to install Tcl/Tk
^^^^^^^^^^^^^^^^^^^^^

*Linux (Ubuntu/Debian):*

    1. Open a terminal
    2. Type: *sudo apt-get install tk8.5 tcl8.5* 

.. note::  The apt-get command is a powerful command-line tool, performing such functions as installation of new software packages, upgrade of existing, so on. For more info, visit: https://help.ubuntu.com/lts/serverguide/apt-get.html

*Windows:*

These steps can be also found at http://trac.osgeo.org/osgeo4w/

    1. Download the 32bit (http://www.activestate.com/activetcl/downloads) or 
       the 64bit installer
    2. Run the installer

..Note:
    * OSGeo4W installer also install Tcl/Tk, you can use it also

How to install TclAPI
^^^^^^^^^^^^^^^^^^^^^

The TclAPI is a part of Ulyxes system. In order to install the API, the whole Ulyxes project folder has to be installed.

*If you have git client installed on your machine:*

    1. Open a terminal
    2. Go to or make the desired “MyFolder” you want to install Ulyxes/TclAPI
    3. Clone the Ulyxes Git directory, so type: git clone https://github.com/zsiki/ulyxes.git
    4. The TclAPI can be found at: “MyFolder/Ulyxes/TclAPI”


*If you have no git client on your machine:*

    #. Open your browser
    #. Navigate to `Ulyxes Github page <https://github.com/zsiki/ulyxes>`_ 
    #. Press the **Download ZIP** button (right side, down)
    #. Uncompress the downloaded file to a suitable directory

.. figure:: img/uly_git.png
    :align: right
    :width: 195px
    :height: 140px
    :scale: 330
    :alt: Overview Ulyxes

    Download Ulyxes ZIP folder
