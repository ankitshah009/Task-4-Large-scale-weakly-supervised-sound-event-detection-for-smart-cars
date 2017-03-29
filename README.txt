# Task-4-Large-scale-weakly-supervised-sound-event-detection-for-smart-cars
Task 4 Large-scale weakly supervised sound event detection for smart cars

Note: Ground truth with strong labels for testing are coming soon.

---
Coordinators:
Benjamin Elizalde, Emmanuel Vincent, Bhiksha Raj
Data Preparation,Annotations and Baseline:
Ankit Shah, Anurag Kumar, Rohan Badlani
---


---
Script to download the development data for Task 4: Large-scale weakly supervised sound event detection for smart cars.
Author: Ankit P Shah (and Benjamin Elizalde)
Please send questions to email: ankit.tronix@gmail.com and bmartin1@andrew.cmu.edu
---

---
Prerequisite installations
---
1. youtube-dl - [sudo] pip install --upgrade youtube_dl
2. pafy -  [sudo] pip install pafy
3. tqdm (progress bar) -  [sudo] pip install tqdm
4. multiprocessing - [sudo] pip install multiprocessing
5. sox tool - sudo apt-get install sox
---

---
Features
---
1. Downloads the audio from the videos for the testing set first and then for the training set. - Multiprocessing - ensures three files are downloaded simultaneously to reduce the heavy download time to 40 percent as compared with single threaded performance.  
2. Formats the audio with consistent parameters - currently set as 1 channel, 16 bit precision, 44.1kHz sampling rate. 
3. Extracts the 10-sec segments from the formatted audio according to the start and end times.  
4. The script output includes the audio for 1,2 and 3, unless testing script is modified to remove audio from 2 and/or 3, that is the original audio and the formatted audio. 
5. To denote a unique identifier for every run/launch of downloading files - script stores the timestamp and assigns to each of the output files and folder names.  
6. Please, contact the Author in case one or more videos are not properly downloaded/available, or with any other issue.
---

---
Lists
---
Download audio: testing_set.csv, training_set.csv
Groundtruth weak labels: groundtruth_weak_label_testing_set.csv groundtruth_weak_label_training_set.csv
Groundtruth strong labels: groundtruth_strong_label_testing_set.csv groundtruth_strong_label_training_set.csv

---
Usage
---
$python download_youtube_audio_from_csv_and_delete_original_standalone.py  <CSV filename - relative path is also fine>
Sample Usage -  python download_youtube_audio_from_csv_and_delete_original_standalone.py training_set.csv 
---

---
User Modifiable Parameters and Options 
---
1. Audio formatting can be modified in the "format_audio" method defined in the script download_youtube_audio_from_csv_and_delete_original.py
2. Removal of original audio and/or formatted audio paths can be done by uncommenting and modifying <os.system(cmdstring2)> in "download_audio_method" function defined in download_youtube_audio_from_csv_and_delete_original_standalone.py

---
Output
---
Output Audio paths 
-First folder contains original best audio from youtube: 
<csv_name>_<testing/training>_<timestamp>_audio_downloaded 
-Second folder contains the corresponding formatted audio:
<csv_name>_<testing/training>_<timestamp>_audio_formatted_downloaded
-Third folder contains the extracted 10-sec segments:
<csv_name>_<testing/training>_<timestamp>_audio_formatted_downloaded_and_ssegmented_downloads

---
Note:- To each downloaded audio string "Y" is added as tools like sox and ffmpeg causes problem when filename starts with "--" or "-". 
