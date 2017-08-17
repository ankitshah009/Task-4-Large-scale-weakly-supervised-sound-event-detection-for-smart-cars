#Task 4 - SubTask B metrics evaluation script. 
#This script was created referencing an example of sed_eval and calls the sed_eval to perform metrics computation
#Purpose of adding this script is to make evaluation convenient for participants

Instruction to run the script:- 
1. Get the task4_subtaskB_evaluation.py file from this directory. 
2. Git clone of sed_eval [https://github.com/TUT-ARG/sed_eval]
3. We will call sed_eval path as $SED_EVAL_ROOT
4. Place the reference (groundtruth_file) and estimated (classifier prediction file) in the path $SED_EVAL_ROOT/data/sound_event
5. Copy task4_subtaskB_evaluation.py file to $SED_EVAL_ROOT/tests
6. cd $SED_EVAL_ROOT/tests
7. Command to run " python task4_subtaskB_evaluation.py <reference file name> <predicted file name>

Reference file should be in the following format
Filename \t Scene(youtube for task 4) \t Start_time \t End_time \t Class name

Estimated file should be in the following format
Filename \t Start_time \t End_time \t Class name

Note: - The filename must match for both reference file and estimated file. 
