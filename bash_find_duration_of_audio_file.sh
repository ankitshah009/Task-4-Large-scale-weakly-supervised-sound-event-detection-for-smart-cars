#!/bin/bash

#Script to compute the duration of the audio clips into a list.

###Sample usage
#$bash bash_find_duration_of_audio_file.sh <testing/training/evaluation> <Audio Root Path> <Output Path>

#Define set
#$1 - testing/training/evaluation

#NOTE: Audio root path should only contain the .wav files
AUDIO_ROOT_PATH=$2

#Path where the list containing the duration of the clips will be written>
OUTPUT_PATH=$3

#Remove duration list if it exists
rm -rf $OUTPUT_PATH/duration_of_files_in_${1}_set.csv

cd $AUDIO_ROOT_PATH
wav_file=(*)
for i in "${wav_file[@]}"
do
	a=`soxi -D $i`
	if [ $1 == "testing" ]; then
	echo -e $i ' \t '$a >> $OUTPUT_PATH/duration_of_files_in_testing_set.csv
	elif [ $1 == "training" ]; then
	echo -e $i ' \t '$a >> $OUTPUT_PATH/duration_of_files_in_training_set.csv
	elif [ $1 == "evaluation" ]; then
	echo -e $i ' \t '$a >> $OUTPUT_PATH/duration_of_files_in_evaluation_set.csv
	else
	echo "Duration File not created - Check your input - Argument 1 should be either testing, training or evaluation"
	fi
done
