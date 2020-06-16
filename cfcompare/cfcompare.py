import csv
import requests
import xml.etree.ElementTree as ET

def getResponse(v): # v is an integer (version#) or "current"
		url = "http://cfconventions.org/Data/cf-standard-names/{}/src/cf-standard-name-table.xml".format(v)
		return requests.get(url)

def getRoot(r):
		return ET.fromstring(r.content)

def getTags(root): # Returns all child tags (at first nested position only, which is ideal)
		tags = []
		for child in root:
			tags.append(child.tag)
		return tags

def getStart(tags, value):
		for i,v in enumerate(tags):
			if v == value:
				return i

def getLast(tags, value):
		for i,v in enumerate(reversed(tags)):
			if v == value:
				return len(tags)-i

def getStandardNamePositions(tags): # First and last occurence of standard name entry
		return [getStart(tags, "entry"), getLast(tags, "entry")]

def getAliasNamesPositions(tags): # First and last occurence of alias entry
	return [getStart(tags, "alias"), getLast(tags, "alias")]

def makeSNDict(v):
	root = getRoot(getResponse(v))
	tags = getTags(root)
	standardNamePositions = getStandardNamePositions(tags)
	standardNames = getStandardNames(root, standardNamePositions)

####################################################################################

def version(v = "current"):
	root = getRoot(getResponse(v))
	return "Version: {},  updated on {}".format(root[0].text, root[1].text)

def standardnames(v = "current"):
	root = getRoot(getResponse(v))
	positions = getStandardNamePositions(getTags(root))
	standardNames = []
	for i in range(positions[0], positions[1]):
		standardNames.append(root[i].attrib['id'])
	return standardNames

def descriptions(v = "current"):
	root = getRoot(getResponse(v))
	positions = getStandardNamePositions(getTags(root))
	descriptions = []
	for i in range(positions[0], positions[1]):
		descriptions.append(root[i][3].text)
	return descriptions

def uom(v = "current"):
	root = getRoot(getResponse(v))
	positions = getStandardNamePositions(getTags(root))
	units = []
	for i in range(positions[0], positions[1]):
		units.append(root[i][0].text)
	return units

def aliases(v = "current"):
	root = getRoot(getResponse(v))
	positions = getAliasNamesPositions(getTags(root))
	aliasEntries = []
	for i in range(positions[0], positions[1]):
		aliasEntries.append(root[i][0].text)
	return aliasEntries

