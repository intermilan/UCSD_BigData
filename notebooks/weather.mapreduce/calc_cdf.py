#!/usr/bin/python
"""
count the number of measurement for each year
"""
import sys
sys.path.append('/usr/lib/python2.6/dist-packages')
from mrjob.job import MRJob
import re
from sys import stderr
import re,pickle,base64,zlib

class MRWeather(MRJob):

    def mapper(self, _, line):
        try:
            self.increment_counter('MrJob Counters','mapper-all',1)
            elements=line.split(',')
            if elements[1] == 'TMAX':
                number_defined=sum([e!='' for e in elements[3:]])
                out=((elements[0], elements[2]), (elements[1], number_defined))
                yield out
            if elements[1] == 'TMIN':
                number_defined=sum([e!='' for e in elements[3:]])
                out=((elements[0], elements[2]), (elements[1], number_defined))
                yield out
        except Exception, e:
            stderr.write('Error in line:\n'+line)
            stderr.write(e)
            self.increment_counter('MrJob Counters','mapper-error',1)
            out=('error',(1,1))

    def reducer(self, station, counts):
        self.increment_counter('MrJob Counters','reducer',1)
        count = list(counts)
        if len(count) == 2:
            if count[0][0] == 'TMAX':
                yield(station, (count[0][1], count[1][1]))
            else:
                yield(station, (count[1][1], count[0][1]))
                
                
if __name__ == '__main__':
    MRWeather.run()