
# Task 4 Large-scale weakly supervised sound event detection for smart cars

### Update Log 
-----------------
* Dec 13: Added Groundtruth release folder - Contains groundtruth information for evaluation, testing set. 
* Nov 20: We've provided direct-download links for the audio of the development and evaluation sets in Section 1.
* August 16: Addition of script for SubTaskB computation for participant's convenience
* July 19: Update to params for Task 4 to maintain consistency with Task 3 parameters
* July 8: Corner case SubTaskA metrics - bug fix for compute metrics function. Additional files added to the prediction folder located in evaluation for sanity checks of metrics computation script. 
* July 4: Added development as well as challenge support after incorporating latest paramount changes from DCASE Framework repository made by Toni on July 3rd. Integration testing for challenge and development setup done.  
* June 26: Added script to compute duration of audio files. Added Training and testing set duration of audio files as a reference for participants to cross check with. Alternate Method to download audio for Development Set [Training and Testing Set] updated.  
* June 24: Modification to groundtruth_strong_label_testing_set.csv - Fixed annotations for redundant class
* June 21: Carriage return removal from groundtruth weak and strong labels csv files. 
* June 17: Evaluation Script Update for ClassWise Metrics Computation for Task4 SubTaskAMetrics
* May 1: Added baseline code (based on Task 3's system), performance and Subtask A metric code.
* April 2: Added strong labels.
* April 1: Added evaluation folder. 


## Coordinators

Benjamin Elizalde, Emmanuel Vincent, Bhiksha Raj

## Data Preparation, Annotations

Ankit Shah (ankit.tronix@gmail.com), Benjamin Elizalde (bmartin1@andrew.cmu.edu)

## Annotations, Baseline and Subtask A Metric

Rohan Badlani (rohan.badlani@gmail.com), Benjamin Elizalde (bmartin1@andrew.cmu.edu), Ankit Shah (ankit.tronix@gmail.com)

## Index
1. Direct-download for the audio of the development and evaluation sets

2. Script to download the development data for Task 4

3. Scripts to evaluate Task 4 - Subtask A (Audio tagging) and Subtask B

4. Strong Label's annotations for Testing


-------------------------------------------------


#### 1. Direct-download for the audio of the development and evaluation sets

The annotations for the evaluation set have not been released yet. The password can be shared via sending a request email to Ankit Shah (ankit.tronix@gmail.com) or Benjamin Elizalde (bmartin1@andrew.cmu.edu) 

[Development: Training](https://goo.gl/PJUVAd) 

[Development: Testing](https://goo.gl/ip8JXW)

[Evaluation](https://dl.dropboxusercontent.com/s/bbgqfd47cudwe9y/DCASE_2017_evaluation_set_audio_files.zip)

Quick download of large files via Google Drive. 

Thanks to Justin Salamon for sharing the trick - https://www.quora.com/How-do-I-download-a-very-large-file-from-Google-Drive/answer/Shane-F-Carr

-------------------------------------------------


#### 2. Script to download the development data for Task 4
-------------------------------------------------

#### Prerequisite installations
[Current version of our scripts require python 2.7 version installation - If user has other python revision installed, we encourage them to setup a virtualenvironment for the DCASE Challenge until the scripts support python 3 as well] 
1. youtube-dl - [sudo] pip install --upgrade youtube_dl
2. pafy -  [sudo] pip install pafy
3. tqdm (progress bar) -  [sudo] pip install tqdm
4. multiprocessing - [sudo] pip install multiprocessing
5. sox tool - sudo apt-get install sox
6. ffmpeg - sudo apt-get install ffmpeg 

#### Cloning this repository

Since this is a repository that references DCASE2017-baseline-system as a submodule, you should use the following command to clone this repository completely:

git clone --recurse <repo link>
git submodule foreach git pull origin master

#### Running Instructions for Task4 Baseline

Please follow the following steps to get the baseline results:

	1. git submodule foreach git pull origin master
	2. Go to DCASE2017-baseline-system (cd DCASE2017-baseline-system)
	3. Run pip install -r requirements.txt
	4. Go back to root (cd ..)
	5. Run python task4.py

The above will be using task.defaults.yaml for the baseline run.

If you would like to run your own modifications on top of DCASE baseline system, pls refer to the following links:
	1. Basic Usage: https://tut-arg.github.io/DCASE2017-baseline-system/usage_tutorial.html#basic-usage
	2. Extending the framework: https://tut-arg.github.io/DCASE2017-baseline-system/extending_framework.html
  
#### Features

1. Downloads the audio from the videos for the testing set first and then for the training set. - Multiprocessing - ensures three files are downloaded simultaneously to reduce the heavy download time to 40 percent as compared with single threaded performance.  
2. Formats the audio with consistent parameters - currently set as 1 channel, 16 bit precision, 44.1kHz sampling rate. 
3. Extracts the 10-sec clips from the formatted audio according to the start and end times.  
4. The script output includes the audio for 1,2 and 3, unless testing script is modified to remove audio from 2 and/or 3, that is the original audio and the formatted audio. 
5. To denote a unique identifier for every run/launch of downloading files - script stores the timestamp and assigns to each of the output files and folder names.  
6. Please, contact Ankit/Benjamin in case one or more videos are not properly downloaded or available, or with any other issue. Participants can create their own scripts to download the audio. Please ensure that you have all the 10-sec clip whose duration matches organizer's list. 

#### Lists

Download audio: testing_set.csv, training_set.csv

Groundtruth weak labels: groundtruth_weak_label_testing_set.csv groundtruth_weak_label_training_set.csv

Groundtruth strong labels: groundtruth_strong_label_testing_set.csv

Training Set Audio Duration: duration_of_files_in_training_set.csv

Testing Set Audio Duration: duration_of_files_in_testing_set.csv

#### Usage

$python download_audio.py  <CSV filename - relative path is also fine>
Sample Usage -  python download_audio.py training_set.csv 

#### Alternate Audio Download Method. 

* Development Set :- Training - https://goo.gl/PJUVAd. Testing - https://goo.gl/ip8JXW
* DCASE Forum [https://groups.google.com/forum/#!forum/dcase-discussions] contains password to the download files. 

#### User Modifiable Parameters and Options 

1. Audio formatting can be modified in the "format_audio" method defined in the script download_youtube_audio_from_csv_and_delete_original.py
2. Removal of original audio and/or formatted audio paths can be done by uncommenting and modifying <os.system(cmdstring2)> in "download_audio_method" function defined in download_audio.py

#### Output

1. First folder contains original best audio from youtube: 
<csv_name>_<testing/training>_<timestamp>_audio_downloaded 
2. Second folder contains the corresponding formatted audio:
<csv_name>_<testing/training>_<timestamp>_audio_formatted_downloaded
3. Third folder contains the extracted 10-sec clips:
<csv_name>_<testing/training>_<timestamp>_audio_formatted_downloaded_and_ssegmented_downloads

Note:- To each downloaded audio string "Y" is added as tools like sox and ffmpeg causes problem when filename starts with "--" or "-". 

#### Number of Audio id count files 

1. testing_set_num_files_per_class.csv - For each class - specifies number of audio segments present in the testing set

Total testing set downloaded files - 488

2. training_set_num_files_per_class.csv - For each class - specifies number of audio segments present in the training set

Total training set downloaded files - 51172

#### Script to compute duration of audio files. 

$bash bash_find_duration_of_audio_file.sh <training/testing/evaluation> \<Audio Path\> \<Output Path where duration list will be written\>

-------------------------------------------------


#### 3. Script to evaluate Task 4 - Subtask A (Audio tagging)
-------------------------------------------------

#### Usage Subtask A - refer to folder called "evaluation" and use the following command.

$python TaskAEvaluate.py groundtruth/groundtruth_weak_label_testing_set.csv prediction/perfect_prediction.csv output/perfect_prediction_output.csv

#### Usage Subtask B - refer to folder called "TaskB_evaluation" for instructions.

-------------------------------------------------


#### 4. Strong Label's annotations for Testing
-------------------------------------------------

1. Only one person was involved in the annotation of each 10-sec clip and all the clips were randomly divided and assigned to 5 people. 
2. The sound event annotations were based on the audio and not the video.
3. The strong labels correspond to the file: groundtruth_strong_label_testing_set.csv
4. The format of strong labels is the same as the DCASE format (Task 3 and Task 4: Audio tagging).
5. Less than 2% of the 10-sec clips had the presence of a sound according to AudioSet, but didn't seem to contain the sound event. Thus, start and end time were assigned 0.

#### Results for Task 4 DCASE 2017 challenge
-------------------------------------------------

DCASE 2017 Results - http://www.cs.tut.fi/sgn/arg/dcase2017/challenge/task-large-scale-sound-event-detection-results
