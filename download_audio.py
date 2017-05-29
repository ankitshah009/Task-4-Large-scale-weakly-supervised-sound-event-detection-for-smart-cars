#Code Contributor - Ankit Shah - ankit.tronix@gmail.com
import pafy
import time
import datetime
import itertools
import os
import sys
import multiprocessing
from multiprocessing import Pool
from tqdm import tqdm

#Format audio - 16 bit Signed PCM audio sampled at 44.1kHz
def format_audio(input_audio_file,output_audio_file):
	temp_audio_file = output_audio_file.split('.wav')[0] + '_temp.wav'
	cmdstring = "ffmpeg -loglevel panic -i %s -ac 1 -ar 44100 %s" %(input_audio_file,temp_audio_file)
	os.system(cmdstring)
	cmdstring1 = "sox %s -G -b 16 -r 44100 %s" %(temp_audio_file,output_audio_file)
	os.system(cmdstring1)
	cmdstring2 = "del %s" % (temp_audio_file)
	os.system(cmdstring2)
	cmdstring3 = "del %s" % (input_audio_file)
	os.system(cmdstring3) # delete the original video

#Trim audio based on start time and duration of audio. 
def trim_audio(input_audio_file,output_audio_file,start_time,duration):
	#print input_audio_file
	#print output_audio_file
	cmdstring = "sox %s %s trim %s %s" %(input_audio_file,output_audio_file,start_time,duration)
	os.system(cmdstring)
	cmdstring1 = "del %s" % (input_audio_file) 
	os.system(cmdstring1) # delete the complete audio

def multi_run_wrapper(args):
	return download_audio_method(*args)

#Method to download audio - Downloads the best audio available for audio id, calls the formatting audio function and then segments the audio formatted based on start and end time. 
def download_audio_method(line,csv_file):
	query_id = line.split(",")[0];
	start_seconds = line.split(",")[1];
	end_seconds = line.split(",")[2];
	audio_duration = float(end_seconds) - float(start_seconds)
	#positive_labels = ','.join(line.split(",")[3:]);
	print "Query -> " + query_id
	#print "start_time -> " + start_seconds
	#print "end_time -> " + end_seconds
	#print "positive_labels -> " + positive_labels
	url = "https://www.youtube.com/watch?v=" + query_id
	try:
		video = pafy.new(url)
		bestaudio = video.getbestaudio()
		#.csv - split - to get the folder information. As path is also passed for the audio - creating the directory from the path where this audio script is present. THus using second split to get the folder name where output files shall be downloaded
		output_folder = sys.argv[1].split('.csv')[0].split("/")[-1] + "_" + csv_file.split('.csv')[0] +  "_" + "audio_downloaded"
		#print output_folder
		if not os.path.exists(output_folder):
			os.makedirs(output_folder)
		path_to_download = output_folder + "\\Y" + query_id + "." + bestaudio.extension
		#print path_to_download
		bestaudio.download(path_to_download)
		formatted_folder = sys.argv[1].split('.csv')[0].split("/")[-1] + "_" + csv_file.split('.csv')[0] + "_" + "audio_formatted_downloaded"
		if not os.path.exists(formatted_folder):
			os.makedirs(formatted_folder)
		path_to_formatted_audio = formatted_folder + "\\Y" + query_id + ".wav"
		format_audio(path_to_download,path_to_formatted_audio)
		#Trimming code
		segmented_folder = sys.argv[1].split('.csv')[0].split("/")[-1] + "_" + csv_file.split('.csv')[0] +  "_" + "audio_formatted_and_segmented_downloads"
		if not os.path.exists(segmented_folder):
			os.makedirs(segmented_folder)
		path_to_segmented_audio = segmented_folder + "\\Y" + query_id + '_' + start_seconds + '_' + end_seconds +  ".wav"
		trim_audio(path_to_formatted_audio,path_to_segmented_audio,start_seconds,audio_duration)

		#Remove the original audio and the formatted audio. Comment line to keep both. Delete "output_folder" or "formatted_folder" to keep one.  
		cmdstring2="rm -rf %s %s" %(output_folder,formatted_folder)
		#os.system(cmdstring2)
		#Remove formatted audio. Comment the line to keep the formatted files as well. Deleting as we have original - thus formatted_files could be generated easily
		cmdstring3="rm -rf %s" %(formatted_folder)
		#os.system(cmdstring3)

		ex1 = ""
	except Exception as ex:
		ex1 = str(ex) + ',' + str(query_id)
		print "Error is ---> " + str(ex)
	return ex1

#Download audio - Reads 3 lines of input csv file at a time and passes them to multi_run wrapper which calls download_audio_method to download the file based on id.
#Multiprocessing module spawns 3 process in parallel which runs download_audio_method. Multiprocessing, thus allows downloading process to happen in 40 percent of the time approximately to downloading sequentially - processing line by line of input csv file. 
def download_audio(csv_file,timestamp):	
	error_log = 'error' + timestamp + '.log'
	with open(csv_file, "r") as segments_info_file:	
		with open(error_log, "a") as fo:
			for line in tqdm(segments_info_file):
				line = (line,csv_file)
				lines_list = []
				lines_list.append(line)
				try:
					next_line = segments_info_file.next()
					next_line = (next_line,csv_file)
					lines_list.append(next_line)
				except:
					print "end of file"
				try:
					next_line = segments_info_file.next()
					next_line = (next_line,csv_file)
					lines_list.append(next_line)
				except:
					print "end of file"
				#print lines_list
				P = multiprocessing.Pool(3)

				exception = P.map(multi_run_wrapper,lines_list)
				for item in exception:
					if item:
						line = fo.writelines(str(item) +  '\n')
				P.close()
				P.join()
		fo.close()

if __name__ == "__main__":
	if len(sys.argv) !=2:
		print 'takes arg1 as csv file to downloaded'
	else:
		
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')			
		download_audio(sys.argv[1],timestamp)
	
