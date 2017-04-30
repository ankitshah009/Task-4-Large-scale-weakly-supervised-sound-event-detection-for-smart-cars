#Code Contributor: Rohan Badlani, Email: rohan.badlani@gmail.com
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
			#Debug Print
			#for key in self.labelsDict.keys():
			#	print str(key) + ":" + str(self.labelsDict[key])

		except Exception as ex:
			print "Fileformat of the file " + str(self.filepath) + " is invalid."
			raise ex

	def validatePredictedDS(self, predictedDS):
		#iterate over predicted list

		#check bothways
		for audioFile in predictedDS.labelsDict.keys():
			if(audioFile not in self.labelsDict.keys()):
				return False


		for audioFile in self.labelsDict.keys():
			if(audioFile not in predictedDS.labelsDict.keys()):
				return False
		
		#check complete. One-One mapping
		return True

	def computeMetrics(self, predictedDS, output_filepath):
		TP = 0
		FP = 0
		FN = 0

		#iterate over predicted list
		for audioFile in predictedDS.labelsDict.keys():
			markerList = [0]*len(self.labelsDict[audioFile])
			for predicted_label in predictedDS.labelsDict[audioFile]:
				#for a predicted label
				
				#1. Check if it is present inside groundTruth, if yes push to TP, mark the existance of that groundtruth label
				index = 0 
				for groundtruth_label in self.labelsDict[audioFile]:
					if(predicted_label == groundtruth_label):
						TP += 1
						markerList[index] = 1
						break
					index+=1

				if(index == len(self.labelsDict[audioFile])):
					#not found. Add as FP
					FP += 1
			
			#check markerList, add all FN
			for marker in markerList:
				if marker == 0:
					FN += 1

		if(TP + FP != 0):
			Precision = float(TP) / float(TP + FP)
		else:
			Precision = 0.0
		if(TP + FN != 0):
			Recall = float(TP) / float(TP + FN)
		else:
			Recall = 0.0
		if(Precision + Recall != 0.0):
			F1 = 2 * Precision * Recall / float(Precision + Recall)
		else:
			F1 = 0.0

		#push to file
		with open(output_filepath, "w") as Metric_File:
			Metric_File.write("Precision = " + str(Precision*100.0) + "\n")
			Metric_File.write("Recall = " + str(Recall*100.0) + "\n")
			Metric_File.write("F1 Score = " + str(F1*100.0) + "\n")
			Metric_File.write("Number of Audio Files = " + str(len(self.labelsDict.keys())))
		Metric_File.close()

	def computeMetricsString(self, predictedDS):
		TP = 0
		FP = 0
		FN = 0
		#iterate over predicted list
		for audioFile in predictedDS.labelsDict.keys():
			markerList = [0]*len(self.labelsDict[audioFile])
			for predicted_label in predictedDS.labelsDict[audioFile]:
				index = 0 
				for groundtruth_label in self.labelsDict[audioFile]:
					TP += 1
					markerList[index] = 1
					break
				index += 1
			if(index == len(self.labelsDict[audioFile])):
				FP+=1
		for marker in markerList:
			if marker == 0:
				FN+=1

		if(TP + FP != 0):
			Precision = float(TP) / float(TP + FP)
		else:
			Precision - 0.0
		if(TP + FN != 0):
			Recall = float(TP) / float(TP + FN)
		else:
			Recall = 0.0
		if(Precision + Recall != 0.0):
			F1 = 2*Precision*Recall / float(Precision + Recall)
		else:
			F1 = 0.0

		output = ""
		output += "\t\t\tPrecision = " + str(Precision*100.0) + "\n"
		output += "\t\t\tRecall = " + str(Recall * 100.0) + "\n"
		output += "\t\t\tF1 Score = " + str(F1*100.0) + "\n"
		return output

