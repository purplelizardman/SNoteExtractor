#!/usr/bin/env python3
"""Converts text in SNote files into .txt files. Currently does not handle images."""
# http://purplelizardman.com/
__author__ = "Finlam Elman"
__copyright__ = "Copyright 2018, Finlam Elman"
__credits__ = ["Finlam Elman"]
__license__ = "GPL3.0"
__version__ = "1.0.1"
__maintainer__ = "Not maintained"
__email__ = "finlam@purplelizardman.com"
__status__ = "Finished"
################################################
import os
import zipfile

notes = []
titles = []
target_dir = r"C:\Your\SNote\folder\path\here"
output_dir = "converted_snotes"
output_dir = target_dir + '\\..\\' + output_dir

def main(): 
	snote_files = [x for x in os.listdir(target_dir) if '.spd' in x]
	for snote_file in snote_files:
		print("Converting "+ snote_file) 
		convert_snote(snote_file,parse_spd(target_dir + "\\" +snote_file))

def parse_spd(spd_path):
	zip_ref = zipfile.ZipFile(spd_path, 'r')
	page_file = [x for x in zip_ref.namelist() if '.page' in x][0]
	with zip_ref.open(page_file) as myfile:
		t = myfile.read()
		return t

def convert_snote(title,raw_contents):
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	cleaned_contents = raw_contents#cleaning stage removed
	t= bytearray(cleaned_contents)
	midpoint = int(len(t)/2)
	start =0
	end = -1
	#find start
	header_terminals = [u"\u0002",u"\u0004",u"\u0005",u"\u0010"]
	for i,x in enumerate(reversed(t[:midpoint])):
		if chr(x) in header_terminals:
			 start = midpoint - i
			 break
	#find end
	for i,x in enumerate(t[midpoint:]):
		if chr(x)==u"\u0007":
			end = i + midpoint
			break

	with open(output_dir + '\\'+ title.split('.')[0] + '.txt','wb') as f:
		for byte in t[start:end-18]:
			if byte != 0:
				try: f.write(bytes([byte]))
				except: pass
	print("... Finished converting " + title)

if __name__ == '__main__':
	main()