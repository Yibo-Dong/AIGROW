#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This function minimizes an AIGER file by first converting it 
to AIG format using the aigtoaig tool, then it uses the abc tool to minimize 
the AIG file, then uses again aigtoaig tool to convert the resized AIG to AIGER
@author: msakr
"""
import os

def minimize(filePath):
    
    filePath = os.path.splitext(filePath)[0]
    #https://bitbucket.org/alanmi/abc/downloads
    abcCommand = """abc -c \"read {0}.aig; strash; refactor -zl; rewrite -zl;
    strash; refactor -zl; rewrite -zl; strash; refactor -zl; rewrite -zl;
      dfraig; rewrite -zl; dfraig; write {1}.aig\" ./run > /dev/null"""    
    
    #AIGER Toolset (http://fmv.jku.at/aiger/aiger-1.9.4.tar.gz)
    aagToaig = 'aigtoaig {0}.aag {1}.aig'
    aigToaag = 'aigtoaig {0}.aig {1}.aag'
    os.system(aagToaig.format(filePath, filePath))
    os.system(abcCommand.format(filePath, filePath))
    os.system(aigToaag.format(filePath, filePath))
    os.remove(filePath + '.aig')
