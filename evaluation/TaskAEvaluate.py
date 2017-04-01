#Code Contributor: Rohan Badlani, Email: rohan.badlani@gmail.com
import os
import sys
from Models import *

def evaluateMetrics(groundtruth_filepath, predicted_filepath, output_filepath):
	#Load GroundTruth to memory, indexed by 
	groundTruthDS = FileFormat(groundtruth_filepath)
	preditedDS = FileFormat(predicted_filepath)

	#simple audioFileCheck
	if len(groundTruthDS.labelsDict.keys()) != len(preditedDS.labelsDict.keys()):
		print "The prediction file submitted does not have prediction for all the audio files"
		sys.exit(1)

	#complex check for audioFile
	if not groundTruthDS.validatePredictedDS(preditedDS):
		print "The prediction file submitted does not have prediction for all the audio files"
		sys.exit(1)

	#the submission is valid. Compute Metrics and Push to File
	groundTruthDS.computeMetrics(preditedDS, output_filepath)

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "Running Instruction: python TaskAEvaluate.py <groundtruth_filepath> <predicted_filepath> <output_filepath>"
	else:
		evaluateMetrics(sys.argv[1], sys.argv[2], sys.argv[3])