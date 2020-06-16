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
	"""
	SUMMARY:
	Shows the version number and the release date of the version.

	PARAMETERS:
	v (int, default = "current"): 
		An integer representing the CF Standard Name version. eg. 66
		If left blank, it defaults to the latest (current) version.

	RETURNS:
	A string of the form: Version: ## released on YYYY-MM-DDTHH:MM:SSZ
	"""
	root = getRoot(getResponse(v))
	return "Version: {},  released on {}".format(root[0].text, root[1].text)

def standardnames(v = "current"): # Call
	"""
	SUMMARY:
	Shows the CF Standard Names in this version.

	PARAMETERS:
	v (int, default = "current"): 
		An integer representing the CF Standard Name version. eg. 66
		If left blank, it defaults to the latest (current) version.

	RETURNS:
	A list of strings representing the CF Standard Names.
	"""
	root = getRoot(getResponse(v))
	positions = getStandardNamePositions(getTags(root))
	standardNames = []
	for i in range(positions[0], positions[1]):
		standardNames.append(root[i].attrib['id'])
	return standardNames

def descriptions(v = "current"): # Call
	"""
	SUMMARY:
	Shows all descriptions in this version of the CF Standard Names.

	PARAMETERS:
	v (int, default = "current"): 
		An integer representing the CF Standard Name version. eg. 66
		If left blank, it defaults to the latest (current) version.

	RETURNS:
	A list of strings representing the descriptions for each CF Standard Name.
	"""
	root = getRoot(getResponse(v))
	positions = getStandardNamePositions(getTags(root))
	descriptions = []
	for i in range(positions[0], positions[1]):
		descriptions.append(root[i][3].text)
	return descriptions

def uom(v = "current"): # Call
	"""
	SUMMARY:
	Shows all Unit of Measures in this version of the CF Standard Names.

	PARAMETERS:
	v (int, default = "current"): 
		An integer representing the CF Standard Name version. eg. 66
		If left blank, it defaults to the latest (current) version.

	RETURNS:
	A list of strings representing the Unit of Measure for each CF Standard Name.
	"""
	root = getRoot(getResponse(v))
	positions = getStandardNamePositions(getTags(root))
	units = []
	for i in range(positions[0], positions[1]):
		units.append(root[i][0].text)
	return units

def aliases(v = "current"): # Call
	"""
	SUMMARY:
	Shows all alias terms in this version of the CF Standard Names.

	PARAMETERS:
	v (int, default = "current"): 
		An integer representing the CF Standard Name version. eg. 66
		If left blank, it defaults to the latest (current) version.

	RETURNS:
	dict object with CF Standard Name as the key and cooresponding alias(es) as values.
	"""
	root = getRoot(getResponse(v))
	positions = getAliasNamesPositions(getTags(root))
	aliasID = []
	aliasEntries = []
	for i in range(positions[0], positions[1]):
		aliasID.append(root[i].attrib['id'])
		aliasEntries.append(root[i][0].text)
	return {aliasID[i]: [aliasEntries[i]] for i in range(len(aliasID))}

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


def compare(ov, v = "current"): # Call
	"""
	SUMMARY:
	Compares two versions of CF Standard Names

	PARAMETERS:
	ov (int): 
		An integer representing the older version. eg: 65
	
	v (int, default = "current"): 
		An integer representing the newer version. eg. 66
		If left blank, it defaults to the latest (current) version.
	
	RETURNS:
	dict object with the following keys:
		numNewNames: The total number of new CF Standard Names added in the new version.
		newNames: The CF Standard Names added in the new version.
		numUpdatedDescriptions: The number of descriptions updated for existing CF Standard Names.
		updatedDescriptionFor: The CF Standard Names for which descriptions are updated in the new version.
		oldDescriptions: CF Standard Name descriptions from the older version.
		newDescriptions: CF Standard Name descriptions from the newer version.
		numUpdatedUnits: The number of units updated for existing CF Standard Names.
		updatedUnitsFor: The CF Standard Names for which units are updated in the new version.
		oldUnits: CF Standard Name units from the older version.
		newUnitsCF Standard Name units from the newer version.
	"""
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
		"numNewNames": len(newNames),
		"newNames": newNames,
		"numUpdatedDescriptions": len(udpatedDesc),
		"updatedDescriptionFor": udpatedDesc,
		"oldDescriptions": oldDesc,
		"newDescriptions": newDesc,
		"numUpdatedUnits": len(updatedUnits),
		"updatedUnitsFor": updatedUnits,
		"oldUnits": oldUnits,
		"newUnits": newUnits
	}

	return updateDict
	
