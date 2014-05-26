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
            if elements[1] == 'TMAX' or elements[1] == 'TMIN':
                number_defined=sum([e!='' for e in elements[3:]])
                out = ((elements[1], number_defined), 1)
                yield out
        except Exception, e:
            stderr.write('Error in line:\n'+line)
            stderr.write(e)
            self.increment_counter('MrJob Counters','mapper-error',1)
            out=('error',(1,1))
        #finally:
        #    yield out
                
    def combiner(self, station, counts):
        self.increment_counter('MrJob Counters','combiner',1)
        yield (station, sum(counts))
    
    def reducer(self, station, counts):
        self.increment_counter('MrJob Counters','combiner',1)
        yield (station, sum(counts))

if __name__ == '__main__':
    MRWeather.run()