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
            out = (elements[0], number_defined)
        except Exception, e:
            stderr.write('Error in line:\n'+line)
            stderr.write(e)
            self.increment_counter('MrJob Counters','mapper-error',1)
            out=('error',(1,1))
        finally:
            yield out
                
    def combiner(self, station, counts):
        self.increment_counter('MrJob Counters','combiner',1)
        yield (word, sum(counts))
    
    def reducer(self, station, counts):
        self.increment_counter('MrJob Counters','combiner',1)
        yield (word, sum(counts))

if __name__ == '__main__':
    MRWeather.run()