#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 14:54:03 2020

@author: msakr
"""
import sys
import os
import shutil

bddMapTime = dict()
dnfMapTime = dict()
bddMapSize = dict()
dnfMapSize = dict()
bddMapABC = dict()
dnfMapABC = dict()
labelsMap = dict()

filename = "results.txt"
if len(sys.argv) > 1:
    filename = sys.argv[1]
plotsFileName = "exp-plots.tex"
writeToFile = "plots.tex"
if len(sys.argv) > 2:
    writeToFile = sys.argv[2]

myFolder =""
latexDir = ""
if not os.path.isfile('exp-plots.tex'):
    myFolder = "AIGEN-AE-Submission/"
    latexDir = "-output-directory=AIGEN-AE-Submission"
    
    
with open(filename) as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
for line in content:
    if line.startswith('#'):
        continue
    lineData = line.split()
    if len(lineData) > 0:
        fileNameData = lineData[1].split('_')
        label = fileNameData[3]+'-' + fileNameData[4] + '-' + fileNameData[5]
        if(label not in labelsMap):
            labelsMap[label] = int(fileNameData[3])+ int(fileNameData[4]) + int(fileNameData[5])
        if lineData[0] == "bdd":
            genTime = float(lineData[2][0:-2])
            if(label not in bddMapTime):
                bddMapTime[label] = (1,genTime)
            else:
                bddMapTime[label] = (bddMapTime[label][0]+1,bddMapTime[label][1] + genTime);
            agSize = float(lineData[4])
            if(label not in bddMapSize):
                bddMapSize[label] = (1,agSize)
            else:
                bddMapSize[label] = (bddMapSize[label][0]+1,bddMapSize[label][1] + agSize);
            if(len(lineData) > 6):
                abcTime = float(lineData[6][0:-2])
                if(label not in bddMapABC):
                    bddMapABC[label] = (1,abcTime)
                else:
                    bddMapABC[label] = (bddMapABC[label][0]+1,bddMapABC[label][1] + abcTime);
        if lineData[0] == "dnf":
            genTime = float(lineData[2][0:-2])
            if(label not in dnfMapTime):
                dnfMapTime[label] = (1,genTime)
            else:
                dnfMapTime[label] = (dnfMapTime[label][0]+1,dnfMapTime[label][1] + genTime);
            agSize = float(lineData[4])
            if(label not in dnfMapSize):
                dnfMapSize[label] = (1,agSize)
            else:
                dnfMapSize[label] = (dnfMapSize[label][0]+1,dnfMapSize[label][1] + agSize);
            if(len(lineData) > 6):
                abcTime = float(lineData[6][0:-2])
                if(label not in dnfMapABC):
                    dnfMapABC[label] = (1,abcTime)
                else:
                    dnfMapABC[label] = (dnfMapABC[label][0]+1,dnfMapABC[label][1] + abcTime);

labelsString = ""
for w in sorted(labelsMap, key=labelsMap.get, reverse=True):
    labelsString = w +"," + labelsString
labelsString = labelsString[0:-1]
bddTimeString = ""
for mapKey in bddMapTime:
    bddTimeString += "(" + mapKey + "," + str(bddMapTime[mapKey][1]/float(bddMapTime[mapKey][0] * 1000)) + ")"
dnfTimeString = ""
for mapKey in dnfMapTime:
    dnfTimeString += "(" + mapKey + "," + str(dnfMapTime[mapKey][1]/float(dnfMapTime[mapKey][0] * 1000)) + ")"
bddSizeString = ""
for mapKey in bddMapSize:
    bddSizeString += "(" + mapKey + "," + str(int(bddMapSize[mapKey][1]/bddMapSize[mapKey][0])) + ")"
dnfSizeString = ""
for mapKey in dnfMapSize:
    dnfSizeString += "(" + mapKey + "," + str(int(dnfMapSize[mapKey][1]/dnfMapSize[mapKey][0])) + ")"
bddABCString = ""
for mapKey in bddMapABC:
    bddABCString += "(" + mapKey + "," + str(bddMapABC[mapKey][1]/float(bddMapABC[mapKey][0] * 1000)) + ")"
dnfABCString = ""
for mapKey in dnfMapABC:
    dnfABCString += "(" + mapKey + "," + str(dnfMapABC[mapKey][1]/float(dnfMapABC[mapKey][0] * 1000)) + ")"


with open(myFolder + plotsFileName, 'r') as file :
  filedata = file.read()

#"""
filedata = filedata.replace("labelsString", labelsString)
filedata = filedata.replace("bddTimeString", bddTimeString)
filedata = filedata.replace("dnfTimeString", dnfTimeString)
filedata = filedata.replace("bddSizeString", bddSizeString)
filedata = filedata.replace("dnfSizeString", dnfSizeString)
filedata = filedata.replace("bddABCString", bddABCString)
filedata = filedata.replace("dnfABCString", dnfABCString)




beginComment = ""
endComment = ""
if len(bddMapABC) == 0:
    beginComment = "\\begin{comment}"
    endComment = "\end{comment}"
filedata = filedata.replace("beginComment", beginComment)
filedata = filedata.replace("endComment", endComment)
# Write the file out again
with open(writeToFile, 'w') as file:
  file.write(filedata)
  
os.system('pdflatex ' + latexDir + ' ' + myFolder + 'plots.tex')

#move and empty files:


src = os.getcwd()
if myFolder == "":
    parent = os.path.join(src, os.pardir)
else:
    parent = src
    src = src + "/" + myFolder

if os.path.isfile(os.path.join(src, 'plots.aux')):
    os.remove(os.path.join(src, 'plots.aux'))
if os.path.isfile(os.path.join(src, 'plots.log')):
    os.remove(os.path.join(src, 'plots.log'))
if myFolder != "":
    if os.path.isfile(os.path.join(src, 'plots.pdf')):
        shutil.move(os.path.join(src, 'plots.pdf'), os.path.join(parent, 'plots.pdf'))
    if os.path.isfile(os.path.join(src, 'results.txt')):
        shutil.copy(os.path.join(src, 'results.txt'), os.path.join(parent, 'results.txt'))
    open(filename, 'w').close()
open(writeToFile, 'w').close()
  

