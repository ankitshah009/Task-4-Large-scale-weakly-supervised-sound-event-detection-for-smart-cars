# Task 4 Large-scale weakly supervised sound event detection for smart cars

Coming soon: Baseline performance. Baseline system will be based on Task 3's system.
Last update Apr2: Updated Readme.md and added strong labels.
Update Apr1: Updated Readme.md and added evaluation folder. 

## Coordinators

Benjamin Elizalde, Emmanuel Vincent, Bhiksha Raj

## Data Preparation, Annotations

Ankit Shah (ankit.tronix@gmail.com), Benjamin Elizalde (bmartin1@andrew.cmu.edu)

## Annotations, Baseline and Subtask A Metric

Rohan Badlani (rohan.badlani@gmail.com), Benjamin Elizalde (bmartin1@andrew.cmu.edu)

## Index
1. Script to download the development data for Task 4

2. Script to evaluate Task 4 - Subtask A (Audio tagging)

3. Strong Label's annotations for Testing


-------------------------------------------------


1. Script to download the development data for Task 4
-------------------------------------------------

Prerequisite installations

1. youtube-dl - [sudo] pip install --upgrade youtube_dl
2. pafy -  [sudo] pip install pafy
3. tqdm (progress bar) -  [sudo] pip install tqdm
4. multiprocessing - [sudo] pip install multiprocessing
5. sox tool - sudo apt-get install sox

Features

1. Downloads the audio from the videos for the testing set first and then for the training set. - Multiprocessing - ensures three files are downloaded simultaneously to reduce the heavy download time to 40 percent as compared with single threaded performance.  
2. Formats the audio with consistent parameters - currently set as 1 channel, 16 bit precision, 44.1kHz sampling rate. 
3. Extracts the 10-sec segments from the formatted audio according to the start and end times.  
4. The script output includes the audio for 1,2 and 3, unless testing script is modified to remove audio from 2 and/or 3, that is the original audio and the formatted audio. 
5. To denote a unique identifier for every run/launch of downloading files - script stores the timestamp and assigns to each of the output files and folder names.  
6. Please, contact Ankit/Benjamin in case one or more videos are not properly downloaded or available, or with any other issue. Participants can create their own scripts to download the audio. Please ensure that you have all the 10-sec clip in the lists.

Lists

Download audio: testing_set.csv, training_set.csv
Groundtruth weak labels: groundtruth_weak_label_testing_set.csv groundtruth_weak_label_training_set.csv
Groundtruth strong labels: groundtruth_strong_label_testing_set.csv groundtruth_strong_label_training_set.csv

Usage

$python download_audio.py  <CSV filename - relative path is also fine>
Sample Usage -  python download_audio.py training_set.csv 

User Modifiable Parameters and Options 

1. Audio formatting can be modified in the "format_audio" method defined in the script download_youtube_audio_from_csv_and_delete_original.py
2. Removal of original audio and/or formatted audio paths can be done by uncommenting and modifying <os.system(cmdstring2)> in "download_audio_method" function defined in download_audio.py

Output

1. First folder contains original best audio from youtube: 
<csv_name>_<testing/training>_<timestamp>_audio_downloaded 
2. Second folder contains the corresponding formatted audio:
<csv_name>_<testing/training>_<timestamp>_audio_formatted_downloaded
3. Third folder contains the extracted 10-sec segments:
<csv_name>_<testing/training>_<timestamp>_audio_formatted_downloaded_and_ssegmented_downloads

Note:- To each downloaded audio string "Y" is added as tools like sox and ffmpeg causes problem when filename starts with "--" or "-". 

Number of Audio id count files 

1. testing_set_num_files_per_class.csv - For each class - specifies number of audio segments present in the testing set
2. training_set_num_files_per_class.csv - For each class - specifies number of audio segments present in the training set

-------------------------------------------------


2. Script to evaluate Task 4 - Subtask A (Audio tagging)
-------------------------------------------------

Usage

$python TaskAEvaluate.py groundtruth/groundtruth_weak_label_testing_set.csv prediction/perfect_prediction.csv output/perfect_prediction_output.csv


-------------------------------------------------


3. Strong Label's annotations for Testing
-------------------------------------------------

1. Only one person was involved in the annotation of each 10-sec clip. 
2. The sound event annotations were based on the audio and not the video.
3. The strong labels correspond to the file: groundtruth_strong_label_testing_set.csv
4. The format of strong labels is the same as the DCASE format (Task 3 and Task 4: Audio tagging).
5. Less than 2% of the 10-sec clips had the presence of a sound according to AudioSet, but didn't seem to contain the sound event. Thus, start and end time were assigned 0.
