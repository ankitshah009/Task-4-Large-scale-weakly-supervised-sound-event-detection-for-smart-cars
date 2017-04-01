#Code Contributor: Rohan Badlani, Email: rohan.badlani@gmail.com
import os
import sys

class FileFormat(object):
	def readLabels(self):
		try:
			#Filename will act as key and labels list will be the value 
			labelsDict = {}
			with open(self.filepath) as filename:
				for line in filename:
					

	def __init__(self, filepath):
		self.filepath = filepath
		self.labelDict = self.readLabels()

	

def evaluateMetrics(groundtruth_filepath, predicted_filepath, output_filepath):
	#Load GroundTruth to memory, indexed by 
	with open 

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Running Instruction: python TaskAEvaluate.py <groundtruth_filepath> <predicted_filepath> <output_filepath>"
	else:
		evaluateMetrics(sys.argv[1], sys.argv[2], sys.agv[3])