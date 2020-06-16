

	# Comparison functions
	def compareStandardNames(cfVersionNew, cfVersionOld):
		
		cfNewDict = makeSNDict(cfVersionNew)
		cfOldDict = makeSNDict(cfVersionOld)

		addedNames = {"standard_name": "units"}
		unitsMismatch = {"standard_name": ["old_units","new_units"]}
		for key in cfNewDict:
			if key in cfOldDict.keys():
				if cfNewDict[key] != cfOldDict[key]: # If units dont match
					unitsMismatch[key] = [cfNewDict[key], cfOldDict[key]]
			else:
				addedNames[key] = cfNewDict[key]

		with open('newStandardNames.csv', 'w') as csv_file:  
			writer = csv.writer(csv_file)
			for key, value in addedNames.items():
				writer.writerow([key, value])

		with open('unitsMismatch.csv', 'w') as csv_file:
			writer = csv.writer(csv_file)
			for key, value in unitsMismatch.items():
				writer.writerow([key, value])

		print("{} new standard names were added in the latest version. The terms have been written to newStandardNames.csv".format(len(addedNames)-1))
		print("A mismatch was found in {} existing standard names. These terms have been written to unitsMismatch.csv".format(len(unitsMismatch)-1))
		
		return

	compareStandardNames(cfVersionNew, cfVersionOld)
	return # parent wrapper return

cfCompare(71, cfVersionNew = "current", checkCurrent = True)