import os
import sys
import sed_eval
import numpy

def test_dcase_style2(argument1,argument2):
    reference = os.path.join('data', 'sound_event', argument1)
    estimated = os.path.join('data', 'sound_event', argument2)
    print reference
    print estimated

    reference_event_list = sed_eval.io.load_event_list(reference)
    estimated_event_list = sed_eval.io.load_event_list(estimated)

    evaluated_event_labels = reference_event_list.unique_event_labels
    files={}
    for event in reference_event_list:
        files[event['file']] = event['file']

    evaluated_files = sorted(list(files.keys()))

    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(
        event_label_list=evaluated_event_labels,
        time_resolution=1.0
    )

    for file in evaluated_files:
        reference_event_list_for_current_file = []
        for event in reference_event_list:
            if event['file'] == file:
                reference_event_list_for_current_file.append(event)
                estimated_event_list_for_current_file = []
        for event in estimated_event_list:
            if event['file'] == file:
                estimated_event_list_for_current_file.append(event)

        segment_based_metrics.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file
        )
    results = segment_based_metrics.results()
    output = " \n"
    output += segment_based_metrics.result_report_overall()
    output += segment_based_metrics.result_report_class_wise()
    output += " \n"
    print output

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "usage - python test_DCASE.py <first file name - reference file> <second file name - estimated file> - Make sure that the files are placed in the correct path - $PWD/data/sound_event/<file is here>"	
	else:
		test_dcase_style2(sys.argv[1],sys.argv[2])	
