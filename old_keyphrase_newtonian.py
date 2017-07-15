####+---------------------------------------------------------+#
### |Newtonian Keyphrase Extraction (keyphrase_newtonian.py)  |#
##  |-- Written By: Nicholas V. Giamblanco (2017)             |#
#   |-- Conceived at: OPR Labs, Toronto, ON, Canada           |#
####+---------------------------------------------------------+#
#   |   *** Last Edit: 10:39PM 02/18/2017 ***                 |#
#   +---------------------------------------------------------+#

#Imports

from __future__ import division
import sys
import operator
import time
import math




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
	stpwds=[]
	print("File to Analyze?")
	file=raw_input(">> ")
	doc=[]
	numOfWords=0
	
	with open("stopwords.txt",'r') as stops:
		for line in stops:
			stopwds=line.split()
			for wds in stopwds:
				stpwds.append(wds)			

	#stpwds=[]
	with open(file,'r') as f:
		for line in f:
			doc.append(line)
			words=line.split()
			for word in words:
				numOfWords=numOfWords+1
				word=''.join(e for e in word if e.isalnum())
				word=word.lower()
				if word not in stpwds:
					if word not in wPos:
						if len(word) > 2:
							wPos.update({numOfWords:word})

					if word not in wWeight:
						if len(word) > 2:
							#wWeight.update({word:len(word)})
							wWeight.update({word:0})

					if word in wWeight:
						if len(word) > 2:
							if not hasNum(word):
								#wWeight[word]=wWeight[word]+(wWeight[word]/len(word))*len(word)
								wWeight[word]=len(word)+wWeight[word]


	print("Document Ready. Press any key to continue.")
	raw_input(">> ")
	print(">> Calculating...")

	# TEMP WORKS.
	if 1 == 1:
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
							#tmpDict[label]=tmpDict[label]+1
							tmpDict[label]=tmpDict[label]+force

	outDict=sorted(tmpDict.items(),key=operator.itemgetter(1),reverse=True)
	t1=[]
	t2=[]
	t3=[]
	stop=time.time()
	with open("topics_"+file,'w+') as fout:
		cutoff=0
		size=len(outDict)
		print("Relationships: "+str(size))
		for item in outDict:
			cutoff=cutoff+1
			if cutoff < 11:
				print("["+str(cutoff)+"] "+str(item[0])+"\n     -- Force [N]: "+str(item[1]))
				fout.write("["+str(cutoff)+"] "+str(item[0])+"\n     -- Force [N]: "+str(item[1])+"\n")
				test=item[0].split("<-->")
				t1.append(test[0])
				t2.append(test[1])
			else:
				break;

		fout.write(">>> Elapsed Time: "+str(stop-start)+"\n")
		print(">> Completed @ "+str(stop-start))
	


def main():
	run=True
	print(">> Starting Up.")
	
	while run:
		try:
			findAttraction()
                	print("Continue Analysis? [Y or y] to continue. Any other key exits.")
                	if raw_input(">> ").upper() == 'Y':
                        	run=True
                	else:
                        	run=False
		except IOError as e:
			print("Could Not Find this file. Try Again?")
	print("Bye.")
	
main()
