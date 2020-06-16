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


def version(v = "current"): # Call
	root = getRoot(getResponse(v))
	return "Version: {},  updated on {}".format(root[0].text, root[1].text)

def standardnames(v = "current"): # Call
	root = getRoot(getResponse(v))
	positions = getStandardNamePositions(getTags(root))
	standardNames = []
	for i in range(positions[0], positions[1]):
		standardNames.append(root[i].attrib['id'])
	return standardNames

def descriptions(v = "current"): # Call
	root = getRoot(getResponse(v))
	positions = getStandardNamePositions(getTags(root))
	descriptions = []
	for i in range(positions[0], positions[1]):
		descriptions.append(root[i][3].text)
	return descriptions

def uom(v = "current"): # Call
	root = getRoot(getResponse(v))
	positions = getStandardNamePositions(getTags(root))
	units = []
	for i in range(positions[0], positions[1]):
		units.append(root[i][0].text)
	return units

def aliases(v = "current"): # Call
	root = getRoot(getResponse(v))
	positions = getAliasNamesPositions(getTags(root))
	aliasEntries = []
	for i in range(positions[0], positions[1]):
		aliasEntries.append(root[i][0].text)
	return aliasEntries

def makeDict(v):
	root = getRoot(getResponse(v))
	positions = getStandardNamePositions(getTags(root))
	standardNames = []
	descriptions = []
	units = []
	for i in range(positions[0], positions[1]):
		standardNames.append(root[i].attrib['id'])
		descriptions.append(root[i][3].text)
		units.append(root[i][0].text)
	
	return  {standardNames[i]: [descriptions[i], units[i]] for i in range(len(standardNames))} 


def compare(v = "current", ov): # Call
	vDict = makeDict(v)
	ovDict = makeDict(ov)

	newNames = []
	udpatedDesc = []
	oldDesc = []
	newDesc = []
	updatedUnits = []
	oldUnits = []
	newUnits = []
	for key in vDict:
		if key not in ovDict:
			newNames.append(key)
		elif key in ovDict:
			if vDict[key][0] != ovDict[key][0]:
				udpatedDesc.append(key) # The key for which description got updated
				oldDesc.append(ovDict[key][0])
				newDesc.append(vDict[key][0])
			if vDict[key][1] != ovDict[key][1]:
				updatedUnits.append(key) # The key for which units got updated
				oldUnits.append(ovDict[key][1])
				newUnits.append(vDict[key][1])
	
	updateDict = {
		"numNewTerms": len(newNames),
		"newTerms": newNames,
		"numUpdatedDescriptions": len(udpatedDesc),
		"oldDescriptions": oldDesc,
		"newDescriptions": newDesc,
		"numUpdatedUnits": len(updatedUnits),
		"oldUnits": oldUnits,
		"newUnits": newUnits
	}

	return updateDict
	
