## This script is a wrapper of sed_eval to compute metrics for Task 4 - Subtask B

#### Instruction to run the script: 
1. Get the task4_subtaskB_evaluation.py file from this directory. 
2. Git clone of sed_eval [https://github.com/TUT-ARG/sed_eval]
3. We will call sed_eval path as $SED_EVAL_ROOT
4. Place the reference (ground truth) and estimated (system's prediction) files in the path $SED_EVAL_ROOT/tests/data/sound_event
5. Copy task4_subtaskB_evaluation.py file to $SED_EVAL_ROOT/tests
6. cd $SED_EVAL_ROOT/tests
7. Command to run: "python task4_subtaskB_evaluation.py <reference filename> <estimated filename>"

Reference file should be in the following format (Sed_eval expects a scene label, which was assigned to be YouTube for every row):
[filename (string)][tab][event onset time in seconds (float)][tab] YouTube [tab] [event offset time in seconds (float)][tab][event label (string)]

Estimated file should be in the following format (It is not necessary to include scene label):
[filename (string)][tab][event onset time in seconds (float)][tab][event offset time in seconds (float)][tab][event label (string)]

Note: Remember the filename convention must match for both reference file and estimated file. 
