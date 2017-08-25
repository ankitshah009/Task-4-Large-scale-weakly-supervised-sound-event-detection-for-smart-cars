#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# DCASE 2017::Large-scale weakly supervised sound event detection for smart cars / Baseline System

from __future__ import print_function, absolute_import
import sys
import os
# Add one directory higher in case we are under examples folder
sys.path.append(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])

# Add DCASE baseline system if we are outside baseline system one directory
sys.path.append('DCASE2017-baseline-system')
sys.path.append('evaluation')
import numpy
import argparse
import textwrap
import platform
import sed_eval

from tqdm import tqdm

from dcase_framework.application_core import SoundEventAppCore
from dcase_framework.parameters import ParameterContainer
from dcase_framework.utils import *
from dcase_framework.learners import SceneClassifier
from dcase_framework.features import FeatureExtractor
from dcase_framework.datasets import SoundEventDataset
from dcase_framework.metadata import MetaDataContainer, MetaDataItem
from dcase_framework.decorators import before_and_after_function_wrapper
from dcase_framework.containers import DottedDict
from dcase_framework.files import ParameterFile

from Models import *
__version_info__ = ('1', '0', '0')
__version__ = '.'.join(__version_info__)


class CustomAppCore(SoundEventAppCore):
    def __init__(self, *args, **kwargs):
        super(CustomAppCore, self).__init__(*args, **kwargs)

    @before_and_after_function_wrapper
    def system_evaluation(self):
        """System evaluation stage.

        Testing outputs are collected and evaluated.

        Parameters
        ----------

        Returns
        -------
        None

        Raises
        -------
        IOError
            Result file not found

        """
        if not self.dataset.reference_data_present:
            return '  No reference data available for dataset.'
        else:
            output = ''
            if self.params.get_path('evaluator.scene_handling') == 'scene-dependent':
                #reset groundtruth and prediction files
		with open("groundtruth.txt", "w") as groundtruth_file:
			groundtruth_file.write("")
		groundtruth_file.close()
		
		with open("prediction.txt", "w") as prediction_file:
			prediction_file.write("")
		prediction_file.close()

		tagging_overall_metrics_per_scene = {}
                event_overall_metrics_per_scene = {}
                for scene_id, scene_label in enumerate(self.dataset.scene_labels):
                    if scene_label not in event_overall_metrics_per_scene:
                        event_overall_metrics_per_scene[scene_label] = {}

                    segment_based_metric = sed_eval.sound_event.SegmentBasedMetrics(
                        event_label_list=self.dataset.event_labels(scene_label=scene_label),
                        time_resolution=1.0,
                    )


                    event_based_metric = sed_eval.sound_event.EventBasedMetrics(
                        event_label_list=self.dataset.event_labels(scene_label=scene_label),
                        evaluate_onset=True,
                        evaluate_offset=False,
                        t_collar=0.5,
                        percentage_of_length=0.5
                    )

                    for fold in self._get_active_folds():
                        result_filename = self._get_result_filename(fold=fold,
                                                                    scene_label=scene_label,
                                                                    path=self.params.get_path('path.recognizer'))

                        results = MetaDataContainer().load(filename=result_filename)

                        for file_id, audio_filename in enumerate(self.dataset.test(fold, scene_label=scene_label).file_list):
                            # Subtask A (audio tagging)

                            # Subtask B (sound event detection)
                            # Select only row which are from current file and contains only detected event
                            current_file_results = []
                            for result_item in results.filter(
                                    filename=posix_path(self.dataset.absolute_to_relative(audio_filename))
                            ):
                                if 'event_label' in result_item and result_item.event_label:
                                    current_file_results.append(result_item)


                            meta = []
                            
                            for meta_item in self.dataset.file_meta(
                                    filename=posix_path(self.dataset.absolute_to_relative(audio_filename))
                            ):
                                if 'event_label' in meta_item and meta_item.event_label:
                                    meta.append(meta_item)


			    for item in meta:
			    	#Actual
				item = str(item)

				item1 = ""
				if self.setup_label=='Evaluation setup':
					item1 = item.split('|')[0].lstrip()
				else:
					item1 = item.split('|')[0].split('audio/')[1].lstrip()

				item2 = item.split('|')[2].lstrip()
				item3 = item.split('|')[3].lstrip()
				item4 = item.split('|')[4].lstrip()
			    	with open('groundtruth.txt','a') as file1:
					file1.write(str(item1) + str("\t") +str(item2) + str("\t") + str(item3) + str("\t") +  str(item4) + str('\n'))
				file1.close()

			    for item in current_file_results:
			   	#Predicted
				item = str(item)
				item1 = ""
				if self.setup_label=='Evaluation setup':
					item1 = item.split('|')[0].lstrip()
				else:
					item1 = item.split('|')[0].split('audio/')[1].lstrip()
				item2 = item.split('|')[2].lstrip()
				item3 = item.split('|')[3].lstrip()
				item4 = item.split('|')[4].lstrip()
				with open('prediction.txt','a') as file2:
					file2.write(str(item1) + str("\t") + str(item2) + str("\t") + str(item3) + str("\t") + str(item4) + str('\n'))
				file2.close()

                            segment_based_metric.evaluate(
                                reference_event_list=meta,
                                estimated_event_list=current_file_results
                            )

                            event_based_metric.evaluate(
                                reference_event_list=meta,
                                estimated_event_list=current_file_results
                            )

                    #from IPython import embed
                    #embed()

                    event_overall_metrics_per_scene[scene_label]['segment_based_metrics'] = segment_based_metric.results()
                    event_overall_metrics_per_scene[scene_label]['event_based_metrics'] = event_based_metric.results()
                    if self.params.get_path('evaluator.show_details', False):
                        output += "  Scene [{scene}], Evaluation over {folds:d} folds\n".format(
                            scene=scene_label,
                            folds=self.dataset.fold_count
                        )

                        output += " \n"
                        output += segment_based_metric.result_report_overall()
                        output += segment_based_metric.result_report_class_wise()
                event_overall_metrics_per_scene = DottedDict(event_overall_metrics_per_scene)
		
                output += " \n"
                output += "  Subtask B (event detection): Overall metrics \n"
                output += "  =============== \n"
                output += "    {event_label:<17s} | {segment_based_fscore:7s} | {segment_based_er:7s} | {event_based_fscore:7s} | {event_based_er:7s} | \n".format(
                    event_label='Event label',
                    segment_based_fscore='Seg. F1',
                    segment_based_er='Seg. ER',
                    event_based_fscore='Evt. F1',
                    event_based_er='Evt. ER',
                )
                output += "    {event_label:<17s} + {segment_based_fscore:7s} + {segment_based_er:7s} + {event_based_fscore:7s} + {event_based_er:7s} + \n".format(
                    event_label='-' * 17,
                    segment_based_fscore='-' * 7,
                    segment_based_er='-' * 7,
                    event_based_fscore='-' * 7,
                    event_based_er='-' * 7,
                )
                avg = {
                    'segment_based_fscore': [],
                    'segment_based_er': [],
                    'event_based_fscore': [],
                    'event_based_er': [],
                }
                for scene_id, scene_label in enumerate(self.dataset.scene_labels):
                    output += "    {scene_label:<17s} | {segment_based_fscore:<7s} | {segment_based_er:<7s} | {event_based_fscore:<7s} | {event_based_er:<7s} | \n".format(
                        scene_label=scene_label,
                        segment_based_fscore="{:4.2f}".format(event_overall_metrics_per_scene.get_path(scene_label + '.segment_based_metrics.overall.f_measure.f_measure') * 100),
                        segment_based_er="{:4.2f}".format(event_overall_metrics_per_scene.get_path(scene_label + '.segment_based_metrics.overall.error_rate.error_rate')),
                        event_based_fscore="{:4.2f}".format(event_overall_metrics_per_scene.get_path(scene_label + '.event_based_metrics.overall.f_measure.f_measure') * 100),
                        event_based_er="{:4.2f}".format(event_overall_metrics_per_scene.get_path(scene_label + '.event_based_metrics.overall.error_rate.error_rate')),
                    )

                    avg['segment_based_fscore'].append(event_overall_metrics_per_scene.get_path(scene_label + '.segment_based_metrics.overall.f_measure.f_measure') * 100)
                    avg['segment_based_er'].append(event_overall_metrics_per_scene.get_path(scene_label + '.segment_based_metrics.overall.error_rate.error_rate'))
                    avg['event_based_fscore'].append(event_overall_metrics_per_scene.get_path(scene_label + '.event_based_metrics.overall.f_measure.f_measure') * 100)
                    avg['event_based_er'].append(event_overall_metrics_per_scene.get_path(scene_label + '.event_based_metrics.overall.error_rate.error_rate'))

                output += "    {scene_label:<17s} + {segment_based_fscore:7s} + {segment_based_er:7s} + {event_based_fscore:7s} + {event_based_er:7s} + \n".format(
                    scene_label='-' * 17,
                    segment_based_fscore='-' * 7,
                    segment_based_er='-' * 7,
                    event_based_fscore='-' * 7,
                    event_based_er='-' * 7,
                )
                output += "    {scene_label:<17s} | {segment_based_fscore:<7s} | {segment_based_er:<7s} | {event_based_fscore:<7s} | {event_based_er:<7s} | \n".format(
                    scene_label='Average',
                    segment_based_fscore="{:4.2f}".format(numpy.mean(avg['segment_based_fscore'])),
                    segment_based_er="{:4.2f}".format(numpy.mean(avg['segment_based_er'])),
                    event_based_fscore="{:4.2f}".format(numpy.mean(avg['event_based_fscore'])),
                    event_based_er="{:4.2f}".format(numpy.mean(avg['event_based_er'])),
                )

                output += " \n"
                output += "  Subtask A (tagging): Overall metrics \n"
                output += "  =============== \n"
		
                # Insert audio tagging evaluation results here
		GroundTruthDS = FileFormat('groundtruth.txt')
		PredictedDS = FileFormat('prediction.txt')

		output += GroundTruthDS.computeMetricsString(PredictedDS)
		output += "\n"

            elif self.params.get_path('evaluator.scene_handling') == 'scene-independent':
                message = '{name}: Scene handling mode not implemented yet [{mode}]'.format(
                    name=self.__class__.__name__,
                    mode=self.params.get_path('evaluator.scene_handling')
                )

                self.logger.exception(message)
                raise ValueError(message)

            else:
                message = '{name}: Unknown scene handling mode [{mode}]'.format(
                    name=self.__class__.__name__,
                    mode=self.params.get_path('evaluator.scene_handling')
                )

                self.logger.exception(message)
                raise ValueError(message)

            if self.params.get_path('evaluator.saving.enable'):
                filename = self.params.get_path('evaluator.saving.filename').format(
                    dataset_name=self.dataset.storage_name,
                    parameter_set=self.params['active_set'],
                    parameter_hash=self.params['_hash']
                )

                output_file = os.path.join(self.params.get_path('path.evaluator'), filename)

                output_data = {
                    'overall_metrics_per_scene': event_overall_metrics_per_scene,
                    'average': {
                        'segment_based_fscore': numpy.mean(avg['segment_based_fscore']),
                        'segment_based_er': numpy.mean(avg['segment_based_er']),
                        'event_based_fscore': numpy.mean(avg['event_based_fscore']),
                        'event_based_er': numpy.mean(avg['event_based_er']),
                    },
                    'parameters': dict(self.params)
                }
                ParameterFile(output_data, filename=output_file).save()

	    with open("TaskB_metrics","w") as file1:
	    	file1.write(output)
	    file1.close()
            return output

def main(argv):
    numpy.random.seed(123456)  # let's make randomization predictable

    parser = argparse.ArgumentParser(
        prefix_chars='-+',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            DCASE 2017
            Task 4: Large-scale weakly supervised sound event detection for smart cars
            ---------------------------------------------
                Carnegie Mellon University
                Author:  Rohan Badlani/Ankit Shah ( rohan.badlani@gmail.com/aps1@andrew.cmu.edu )

            System description
            The baseline system for task 4 in DCASE 2017 Challenge.
                Features: log mel-band energies
                Classifier: MLP
        '''))

    # Setup argument handling
    parser.add_argument('-m', '--mode',
                        choices=('dev', 'challenge'),
                        default=None,
                        help="Selector for system mode",
                        required=False,
                        dest='mode',
                        type=str)

    parser.add_argument('-p', '--parameters',
                        help='parameter file override',
                        dest='parameter_override',
                        required=False,
                        metavar='FILE',
                        type=argument_file_exists)

    parser.add_argument('-s', '--parameter_set',
                        help='Parameter set id',
                        dest='parameter_set',
                        required=False,
                        type=str)

    parser.add_argument("-n", "--node",
                        help="Node mode",
                        dest="node_mode",
                        action='store_true',
                        required=False)

    parser.add_argument("-show_sets",
                        help="List of available parameter sets",
                        dest="show_set_list",
                        action='store_true',
                        required=False)

    parser.add_argument("-show_datasets",
                        help="List of available datasets",
                        dest="show_dataset_list",
                        action='store_true',
                        required=False)

    parser.add_argument("-show_parameters",
                        help="Show parameters",
                        dest="show_parameters",
                        action='store_true',
                        required=False)

    parser.add_argument("-show_eval",
                        help="Show evaluated setups",
                        dest="show_eval",
                        action='store_true',
                        required=False)

    parser.add_argument("-o", "--overwrite",
                        help="Overwrite mode",
                        dest="overwrite",
                        action='store_true',
                        required=False)

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    # Parse arguments
    args = parser.parse_args()

    # Load default parameters from a file
    default_parameters_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                               os.path.splitext(os.path.basename(__file__))[0]+'.defaults.yaml')
    if args.parameter_set:
        parameters_sets = args.parameter_set.split(',')
    else:
        parameters_sets = [None]

    for parameter_set in parameters_sets:
        # Initialize ParameterContainer
        params = ParameterContainer(project_base=os.path.dirname(os.path.realpath(__file__)))

        # Load default parameters from a file
        params.load(filename=default_parameters_filename)

        if args.parameter_override:
            # Override parameters from a file
            params.override(override=args.parameter_override)

        if parameter_set:
            # Override active_set
            params['active_set'] = parameter_set

        # Process parameters
        params.process()

        # Force overwrite
        if args.overwrite:
            params['general']['overwrite'] = True

        # Override dataset mode from arguments
        if args.mode == 'dev':
            # Set dataset to development
            params['dataset']['method'] = 'development'

            # Process dataset again, move correct parameters from dataset_parameters
            params.process_method_parameters(section='dataset')

        elif args.mode == 'challenge':
            # Set dataset to training set for challenge
            params['dataset']['method'] = 'challenge_train'
            params['general']['challenge_submission_mode'] = True
            # Process dataset again, move correct parameters from dataset_parameters
            params.process_method_parameters(section='dataset')

        if args.node_mode:
            params['general']['log_system_progress'] = True
            params['general']['print_system_progress'] = False

        # Force ascii progress bar under Windows console
        if platform.system() == 'Windows':
            params['general']['use_ascii_progress_bar'] = True

        # Setup logging
        setup_logging(parameter_container=params['logging'])

        app = CustomAppCore(name='DCASE 2017::Acoustic Scene Classification / Baseline System',
                            params=params,
                            system_desc=params.get('description'),
                            system_parameter_set_id=params.get('active_set'),
                            setup_label='Development setup',
                            log_system_progress=params.get_path('general.log_system_progress'),
                            show_progress_in_console=params.get_path('general.print_system_progress'),
                            use_ascii_progress_bar=params.get_path('general.use_ascii_progress_bar')
                            )

        # Show parameter set list and exit
        if args.show_set_list:
            params_ = ParameterContainer(
                project_base=os.path.dirname(os.path.realpath(__file__))
            ).load(filename=default_parameters_filename)

            if args.parameter_override:
                # Override parameters from a file
                params_.override(override=args.parameter_override)
            if 'sets' in params_:
                app.show_parameter_set_list(set_list=params_['sets'])

            return

        # Show dataset list and exit
        if args.show_dataset_list:
            app.show_dataset_list()
            return

        # Show system parameters
        if params.get_path('general.log_system_parameters') or args.show_parameters:
            app.show_parameters()

        # Show evaluated systems
        if args.show_eval:
            app.show_eval()
            return

        # Initialize application
        # ==================================================
        if params['flow']['initialize']:
            app.initialize()

        # Extract features for all audio files in the dataset
        # ==================================================
        if params['flow']['extract_features']:
            app.feature_extraction()

        # Prepare feature normalizers
        # ==================================================
        if params['flow']['feature_normalizer']:
            app.feature_normalization()

        # System training
        # ==================================================
        if params['flow']['train_system']:
            app.system_training()

        # System evaluation
        if not args.mode or args.mode == 'dev':

            # System testing
            # ==================================================
            if params['flow']['test_system']:
                app.system_testing()

            # System evaluation
            # ==================================================
            if params['flow']['evaluate_system']:
                app.system_evaluation()

        # System evaluation in challenge mode
        elif args.mode == 'challenge':
            # Set dataset to testing set for challenge
            params['dataset']['method'] = 'challenge_test'

            # Process dataset again, move correct parameters from dataset_parameters
            params.process_method_parameters('dataset')

            if params['general']['challenge_submission_mode']:
                # If in submission mode, save results in separate folder for easier access
                params['path']['recognizer'] = params.get_path('path.recognizer_challenge_output')

            challenge_app = CustomAppCore(name='DCASE 2017::Acoustic Scene Classification / Baseline System',
                                          params=params,
                                          system_desc=params.get('description'),
                                          system_parameter_set_id=params.get('active_set'),
                                          setup_label='Evaluation setup',
                                          log_system_progress=params.get_path('general.log_system_progress'),
                                          show_progress_in_console=params.get_path('general.print_system_progress'),
                                          use_ascii_progress_bar=params.get_path('general.use_ascii_progress_bar')
                                          )
            # Initialize application
            if params['flow']['initialize']:
                challenge_app.initialize()

            # Extract features for all audio files in the dataset
            if params['flow']['extract_features']:
                challenge_app.feature_extraction()

            # System testing
            if params['flow']['test_system']:
                if params['general']['challenge_submission_mode']:
                    params['general']['overwrite'] = True

                challenge_app.system_testing()

                if params['general']['challenge_submission_mode']:
                    challenge_app.ui.line(" ")
                    challenge_app.ui.line("Results for the challenge are stored at ["+params.get_path('path.recognizer_challenge_output')+"]")
                    challenge_app.ui.line(" ")

            # System evaluation if not in challenge submission mode
            if params['flow']['evaluate_system']:
                challenge_app.system_evaluation()

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except (ValueError, IOError) as e:
        sys.exit(e)
