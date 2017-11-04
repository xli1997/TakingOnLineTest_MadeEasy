import re, sys, os
from shutil import copyfile
import json

#define ocr program path
FOLDER_PATH = r"C:\download\1\Capture2Text_v3.9\Capture2Text"
EXE_PATH = FOLDER_PATH +r"\Capture2Text.exe"
OUTPUT_PATH = FOLDER_PATH + r"\Output"
TEXT_SOURCE = OUTPUT_PATH + "\ocr.txt"
IMAGE_SOURCE = OUTPUT_PATH + "\screen_capture.bmp"

#define workspace path
dir_path = os.path.dirname(os.path.realpath(__file__))
IMAGE_PATH = dir_path + "\\image"
if not os.path.exists(IMAGE_PATH):
    os.makedirs(IMAGE_PATH)
TEXT_PATH = dir_path + "\\text"
if not os.path.exists(TEXT_PATH):
    os.makedirs(TEXT_PATH)
JSON_PATH = dir_path + "\\json"
if not os.path.exists(JSON_PATH):
    os.makedirs(JSON_PATH)

#find the index of next filename	
names = os.listdir(IMAGE_PATH)
index = 0
if len(names) > 0:
	for name in names:
		item = name[:-4]
		i = int(item)
		if i > index:
			index = i
index += 1

def compare_dictionary(dict1, dict2):
	list1 = dict1.keys()
	list2 = dict2.keys()
	set1 = set(list1)
	set2 = set(list2)
	set3 = set1 & set2
	fraction = len(set3)*100/len(set1)
	return fraction

#main loop
while(1):
	#ocr scan command
	os.system(EXE_PATH + " 530 100 1650 880")
	
	#copy image file	
	filename = str(index) + ".bmp"	
	image_fullpath = IMAGE_PATH+"\\"+filename
	if os.path.isfile(IMAGE_SOURCE):
		copyfile(IMAGE_SOURCE, image_fullpath)
	else: 
		print "IMAGE_SOURCE not exist"
	
	#copy text file
	filename = str(index) + ".txt"
	text_fullpath = TEXT_PATH+"\\"+filename
	if os.path.isfile(TEXT_SOURCE):
		copyfile(TEXT_SOURCE, text_fullpath)
	else: 
		print "TEXT_SOURCE not exist"

	#generate dictionary
	dict1 = {}
	file1 =open(text_fullpath, 'r')
	lines = file1.readlines()
	for line in lines:
		items = line.split()
		for item in items:
			if dict1.has_key(item):
				dict1[item] += 1
			else:
				dict1[item] = 1
	file1.close()
	
	#read file json files to match
	names = os.listdir(JSON_PATH)
	for name in names:
		json_fullpath = JSON_PATH+"\\"+name
		dict2 = json.load(open(json_fullpath, 'r'))
		percent = compare_dictionary(dict1, dict2)

		if percent > 30:
			print "{0} is a match {1}%".format(name, percent)
		else:
			print name+ "\t {0}%".format(percent)
		
	#write dictionary to json file
	filename = str(index) + ".json"
	json_fullpath = JSON_PATH+"\\"+filename
	json.dump(dict1, open(json_fullpath,'w'))
	

	raw_input("Press Enter to continue...")
	index += 1
	

	
	



	
	