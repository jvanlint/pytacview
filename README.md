# pytacview
A Python script that will process a TacView XML log file and create a SQLite3 relational database of objects from the file .


How to use:

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
