#!/usr/bin/python

import sqlite3
from sqlite3 import Error
import xml.etree.ElementTree as ET
import argparse
import time
import sys


def create_connection(db_file):
    """ create a database connection to the SQLite database
                    specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_mission(conn, mission):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO Mission(name,date,duration, source, recorder, recording_time, author)
							VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, mission)
    conn.commit()
    return cur.lastrowid


def create_event(conn, event):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO Event(mission_id,time,action)
							VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, event)
    conn.commit()
    return cur.lastrowid


def create_primary(conn, primary):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO PrimaryObject(event_id, tacview_id, type, name, pilot, coalition, country, obj_group, parent_id)
							VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, primary)
    conn.commit()
    return cur.lastrowid


def create_secondary(conn, secondary):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO SecondaryObject(event_id, tacview_id, type, name, pilot, coalition, country, obj_group, parent_id)
						VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, secondary)
    conn.commit()
    return cur.lastrowid


def create_parent(conn, parent):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO ParentObject(event_id, tacview_id, type, name, pilot, coalition, country, obj_group)
						VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, parent)
    conn.commit()
    return cur.lastrowid


def process_tacview_file(filename):

	tree = ET.parse(filename)		#'mission1_server.xml'
	root = tree.getroot()

	pilots = []
	statistics = []
	enemyLosses = []

	missionName = root[1][0].text
	missionTime = root[1][1].text
	missionDuration = root[1][2].text
	missionSource = root[0][0].text
	missionRecorder = root[0][1].text
	missionRecordingTime = root[0][2].text
	missionAuthor = root[0][3].text

	mission_id = 0

	database = 'pytacview.db'

	# create a database connection
	conn = create_connection(database)
	print("Creating Mission Record...")
	with conn:
		# create a new project
		mission = (missionName, missionTime, missionDuration, missionSource,
				missionRecorder, missionRecordingTime, missionAuthor)
		mission_id = create_mission(conn, mission)

	print("Creating Event Records...")
	for event in root[2].findall('Event'):
		# Each Event will have a Time, Action and a Primary Object
		action = event.find('Action').text
		time = event.find('Time').text
		event_id = 0

		with conn:
			event_1 = (mission_id, time, action)
			event_id = create_event(conn, event_1)

		# Get the primary object
		# Every Event has at least a Primary Object
		primaryObject = event.find('PrimaryObject')
		primaryID = primaryObject.get('ID')
		primaryName = primaryObject.find('Name').text
		primaryType = getattr(primaryObject.find('Type'), 'text', 'n/a')
		primaryPilot = getattr(primaryObject.find('Pilot'), 'text',  'n/a')
		primaryCoalition = getattr(primaryObject.find('Coalition'), 'text',  'n/a')
		primaryCountry = getattr(primaryObject.find('Country'), 'text',  'n/a')
		primaryGroup = getattr(primaryObject.find('Group'), 'text',  'n/a')
		primaryParent = getattr(primaryObject.find('Parent'), 'text',  'n/a')

		with conn:
			primary = (event_id, primaryID, primaryType, primaryName, primaryPilot,
					primaryCoalition, primaryCountry, primaryGroup, primaryParent)
			primary_id = create_primary(conn, primary)

		# Get the Secondary Object. This object tells us what the action ws performed on.
		secondaryObject = event.find('SecondaryObject')

		if secondaryObject is not None:
			secondaryID = secondaryObject.get('ID')
			secondaryType = secondaryObject.find('Type').text
			secondaryName = secondaryObject.find('Name').text
			secondaryPilot = getattr(secondaryObject.find('Pilot'), 'text', 'n/a')
			secondaryCoalition = secondaryObject.find('Coalition').text
			secondaryCountry = secondaryObject.find('Country').text
			secondaryParent = getattr(
				secondaryObject.find('Parent'), 'text', 'n/a')
			secondaryGroup = getattr(secondaryObject.find('Group'), 'text', 'n/a')
			secondaryParent = getattr(
				secondaryObject.find('Parent'), 'text', 'n/a')

			with conn:
				secondary = (event_id, secondaryID, secondaryType, secondaryName, secondaryPilot,
							secondaryCoalition, secondaryCountry, secondaryGroup, secondaryParent)
				secondary_id = create_secondary(conn, secondary)

		# Get the Parent Object. This object tells who performed the action.
		parentObject = event.find('ParentObject')

		if parentObject is not None:
			parentID = secondaryObject.get('ID')
			parentType = parentObject.find('Type').text
			parentName = parentObject.find('Name').text
			parentPilot = getattr(parentObject.find('Pilot'), 'text', None)
			parentCoalition = parentObject.find('Coalition').text
			parentCountry = parentObject.find('Country').text
			parentGroup = parentObject.find('Group').text

			with conn:
				parent = (event_id, parentID, parentType, parentName,
						parentPilot, parentCoalition, parentCountry, parentGroup)
				parent_id = create_parent(conn, parent)


def main(argv):
	parser = argparse.ArgumentParser(description='Process TacView XML into a SQLite3 database.')
	parser.add_argument('filename', action='store', help='the XML filename to process')
	args = parser.parse_args()
	
	filename = args.filename

	start = time.time()

	process_tacview_file(filename)

	print('-' * 80)
	print('*** Export to database complete! ***')
	print('The script took %.3f seconds to finish.' % (time.time() - start))


if __name__ == '__main__':
    main(sys.argv[1:])
