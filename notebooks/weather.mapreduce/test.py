#!/usr/bin/python
"""
count the number of measurement for each year
"""
import sys
sys.path.append('/usr/lib/python2.6/dist-packages')
from mrjob.job import MRJob
import re
from sys import stderr

class MRWeather(MRJob):

    def mapper(self, _, line):
        self.increment_counter('MrJob Counters','mapper-all',1)
        elements=line.split('\t')
        #word_1=elements[0].split[',']
        #word_11=word_1[0].replace('[', '')
        #word_11=word11.replace('\"', '')
        #word_11=word11.replace('"', '')
        #word_11=word11.replace('\\', '')
        out=(elements[0], 1)
        yield out
    
    def reducer(self, station, counts):
        self.increment_counter('MrJob Counters','reducer',1)
        yield(station, sum(counts))
                
if __name__ == '__main__':
    MRWeather.run()