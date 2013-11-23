#!/usr/bin/python

import numpy
import pandas


def returnNumpyData(file,delimiter=',',cols=None):
	''' 
	Read in a text file and return as a numpy array	
	cols = a list of column indices to retrieve, starting with 0
	'''
	data = numpy.genfromtxt(file,delimiter=delimiter,usecols=cols)	
	data = data[~numpy.isnan(data).any(1)]
	return data
	
def loadNumpyData(file,delimiter=','):
	return numpy.loadtxt(file,delimiter=delimiter)
	
def returnHeaders(file,kind='dict',delimiter=','):
	''' 
	Returns the header info as a dictionary of column indices or just an array 
	'''
	import linecache

	retrieved_line = linecache.getline(file, 1).strip()
	retrieved_line = retrieved_line.replace('# ','')
	headers = retrieved_line.split(',')
	
	if (kind=='dict'):
		index = range(0,len(headers))
		return dict(zip(headers,index))
	else:
		return headers

file = 'cell1-25.csv'
data = pandas.DataFrame(loadNumpyData(file),columns=returnHeaders(file,kind='arr'))
numCycle = max(data.cycle)

caps=[]
for i in range(0,int(numCycle)):
	dc = frame.dCap[frame.cycle==float(i)]
	dci = dc.index[len(dc)-1]
	cc = frame.cCap[frame.cycle==float(i)]
	cci = cc.index[len(cc)-1]
	caps.append([i,dc[dci],cc[cci]])

caps=pandas.DataFrame(caps,columns=['cycle','dCap','cCap'])
	
