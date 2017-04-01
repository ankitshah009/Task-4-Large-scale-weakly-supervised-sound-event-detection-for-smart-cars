import os
import sys

class FileFormat(object):
	def __init__(self, filepath):
		self.filepath = filepath
		self.labelDict = self.readLabels()

	def readLabels(self):
		try:
			#Filename will act as key and labels list will be the value 
			self.labelsDict = {}
			with open(self.filepath) as filename:
				for line in filename:
					audioFile = line.split("\t")[0]
					startTime = line.split("\t")[1]
					endTime = line.split("\t")[2]
					label = line.split("\t")[3].split("\r\n")[0]

					if audioFile not in self.labelsDict.keys():
						#does not exist
						self.labelsDict[audioFile] = [label]
					else:
						#exists
						self.labelsDict[audioFile].append(label)

			filename.close()
			for key in self.labelsDict.keys():
				print str(key) + ":" + str(self.labelsDict[key])

		except Exception as ex:
			print "Fileformat of the file " + str(self.filepath) + " is invalid."
			raise ex