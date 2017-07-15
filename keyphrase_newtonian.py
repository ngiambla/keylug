####+---------------------------------------------------------+#
### |Newtonian Keyphrase Extraction (keyphrase_newtonian.py)  |#
##  |-- Written By: Nicholas V. Giamblanco (2017)             |#
#   |-- Conceived in: Toronto, ON, Canada                     |#
####+---------------------------------------------------------+#
#   |   *** Last Edit: 01:30AM 05/01/2017 ***                 |#
#   +---------------------------------------------------------+#

#Imports

from __future__ import division
import os
import sys
import glob
import operator
import time
import math
import numpy.random as np

###################################################
# function listFiles(): lists file in dir.
###################################################
def listFiles():
	print(">> ")
	files=glob.glob("*.txt")
	for f in files:
		if "extract_" not in f:
			print("["+f+"]")

###################################################
# function help(): displays CLI menu
###################################################
def help():
	print("|##############################################|")
	print("+#- [MENU] -----------------------------------#+")
	print("|##############################################|")
	print("| [help] >> displays this                      |")
	print("| [run]  >> runs the keyword extraction system |")
	print("| [quit] >> quits this program.                |")
	print("| [ls]   >> lists files in directory for comp  |")
	print("+##############################################+\n")

####################################################
# function author(): displays author of this sys.
####################################################
def author():
	auth='''
        ####+---------------------------------------------------------+#
        ### |Newtonian Keyphrase Extraction (keyphrase_newtonian.py)  |#
        ##  |-- Written By: Nicholas V. Giamblanco (2017)             |#
        #   |-- Conceived in: Toronto, ON, Canada                     |#
        ####+---------------------------------------------------------+#
        #   |   *** Last Edit: 01:30AM 05/01/2017 ***                 |#
        #   +---------------------------------------------------------+#\n'''
	print(auth)

####################################################
# function hasNum(strng): determines if a string
# --- has a number inside
####################################################
def hasNum(strng):
	return any(char.isdigit() for char in strng)

####################################################
# function findAttraction(): assigns a mass to all
# --- words in a document, and calculates 
# --- newtonian gravity, and the force between words
# --- due to gravity and mass.
####################################################
def findAttraction():
	wWeight={}
	wPos={}
	attraction={}
	termfreq={}
	stpwds=[]
	keys=[]
	print("File to Analyze?")
	file=raw_input(">> ")
	doc=[]
	numOfWords=0
	with open("stopwords.txt",'r') as stops:
		for line in stops:
			stopwds=line.split()
			for wds in stopwds:
				stpwds.append(wds)			

	with open(file,'r') as f:
		for line in f:
			doc.append(line)
			words=line.split()
			for word in words:
				numOfWords=numOfWords+1
				word=''.join(e for e in word if e.isalnum())
				word=word.lower()
				if word not in stpwds:
					if word not in termfreq:
						if len(word) > 2:
							termfreq.update({word:1})
					if word in termfreq:
						if len(word) > 2:
							termfreq[word]=termfreq[word]+1

					if word not in wPos:
						if len(word) > 2:
							wPos.update({numOfWords:word})

					if word not in wWeight:
						if len(word) > 2:
							wWeight.update({word:0})

					if word in wWeight:
						if len(word) > 2:
							if not hasNum(word):
								wWeight[word]=len(word)+wWeight[word]

	print("Document Ready. Press any key to continue.")
	raw_input(">> ")
	print(">> Calculating...")

	start=time.time()
	tmpDict={}
	length=int(numOfWords/100)

	for j in range(1, numOfWords):
	
		# Looking for attraction within specified range. (1% of words)
		for i in range(j-length,j+length):
			if i in wPos and j in wPos and j!=i:
				sys.stdout.write("Progress: "+"{0:.2f}".format(100*j/numOfWords)+"%\r")
				if wPos[j] != wPos[i]:
					force=wWeight[wPos[j]]*wWeight[wPos[i]]
					force=force/(abs(j-i)**2)
					lst=[wPos[i],wPos[j]]
					lst.sort()
					label=lst[0]+" <--> "+lst[1]
					if label not in tmpDict:
						tmpDict.update({label:force})
					else:
						tmpDict[label]=tmpDict[label]+force


	

	outDict=sorted(tmpDict.items(),key=operator.itemgetter(1),reverse=True)
	predict=[]
	gp=True
	stop=time.time()
	with open("extract_"+file,'w+') as fout:
		cutoff=0
		size=len(outDict)
		print("Relationships: "+str(size))
		for item in outDict:
			if len(predict) <10:
				test=item[0].split("<-->")
				for thing in predict:
					if test[0].strip() in thing or test[1].strip()  in thing:
						gp=False
						break;
					else:
						gp=True
				if gp:
					predict.append(test[0].strip()+" "+test[1].strip())
					print("NP: "+test[0].strip()+" "+test[1].strip()+" Force[N]: "+str(item[1]))
					fout.write("NP: "+test[0].strip()+" "+test[1].strip()+" Force[N]: "+str(item[1])+"\n")
			else:
				break
		fout.write(">>> Elapsed Time: "+str(stop-start)+"\n")
		print("\n>> Completed @ "+str(stop-start))

def main():
	run=True
	os.system('clear')
	print(">> Starting Up.")
	author()
	help()
	while run:
		ans=raw_input("~$ ")
		ans.lower()
		if ans=="run":
			try:
				findAttraction()
			except IOError as er:
				print("Could Not Find this file.")
			except Exception as e:
				print("Unexpected result occured [<.<]\nWe Caught: "+str(e))
		if ans=="quit" or ans=="exit":
			run=False
		if ans=="ls":
			listFiles()
		if ans=="help":
			help()
	print("Bye.")
	
main()
