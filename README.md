# pytacview
A Python script that will process a TacView XML log file and create a SQLite3 relational database of objects from the file .


## How To Use It

1. Use TacView to export an XML log from a Tacview file (preferably from the server)
2. Place the XML file in the same directory as tacview2db.py and the pytacview.db files.
3. Run the Python script passing it the name of your xml file. (eg. ```python tacview2db.py mymission.xml```)

Typing ```python tacview2db.py -h``` will give you some help.
```
usage: tacview2db.py [-h] filename

Process TacView XML into a SQLite3 database.

positional arguments:
  filename    the XML filename to process

optional arguments:
  -h, --help  show this help message and exit
  ```
## How It Works
The TacView XML is basically a list of events. An event consists of an action and several objects. Each event will have an action and a Primary Object as a minimum. Depending on the type of action, the event may also contain a Secondary Object and a Parent Object.

This Python script processes these events and builds out a relational data model in the pytacview.db SQLite database. The database contains the following tables:
- Mission (data pertaining to the mission you are importing)
- Events (the events contained in the XML). This is related to the Mission table.
- PrimaryObjects (a list of primary objects related to an event)
- SecondaryObjects (a list of secondary objects related to an event)
- ParentObjects (a list of parent objects related to an event)

The database also contains some sample views that will give you ideas for how to structure SQL queries to get some value out of the data.
