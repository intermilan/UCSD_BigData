#!/usr/bin/python
"""
count the number of measurement for each year
"""
import sys
sys.path.append('/usr/lib/python2.6/dist-packages')
from mrjob.job import MRJob
import re
from sys import stderr
import numpy as np

station_id={}

class MRWeather(MRJob):

    def configure_options(self):
        super(MRWeather,self).configure_options()
        self.add_file_option('--station_partition')
        
    def mapper_init(self):        
        data_in=open(self.options.station_partition, 'r')
        for line in data_in.readlines():
            words=line.split(',')
            words[1]=words[1].replace('\n', '')
            station_id[words[0]]=words[1]
        data_in.close()

    def mapper(self, _, line):
        try:
            self.increment_counter('MrJob Counters','mapper-all',1)
            elements_1=line.split('\t')
            elements_2=elements_1[0].split(',')
            name=elements_2[0].replace('"','')
            name=name.replace('[','')
            name=name.replace(']','')
            data=elements_1[1].replace('""','"0"')
            data=data.replace('" "','"0"')
            data=data.replace('[','')
            data=data.replace(']','')
            data=data.replace('"','')
            data_temp=data.split(', ')
            data_list=[int(e) for e in data_temp]
            if station_id[name]%2 ==0:
                out = (station_id[name], data_list)
            else:
                out = (station_id[name]-1, data_list)
            yield out

        except Exception, e:
            stderr.write('Error in line:\n'+line)
            stderr.write(e)
            self.increment_counter('MrJob Counters','mapper-error',1)
            out=('error', 1)
    
    def reducer(self, station, counts):
        self.increment_counter('MrJob Counters','reducer',1)
        id_data=list(counts)
        id_num=len(id_data)
        id_sum_x=np.zeros(730)
        id_sum_xx=np.zeros((730, 730))
        
        for index in range(0, id_num):
            id_sum_x=id_sum_x+np.array(id_data[index])
            id_sum_xx=id_sum_xx+np.outer(id_data[index],id_data[index])
        
        pca_mean=id_sum_x/id_num
        pca_cov=np.zeros((730, 730))
        
        for index in range(0, id_num):
            temp=np.array(id_data[index])-pca_mean
            pca_cov=pca_cov+np.outer(temp, temp)
        
        pca_cov=pca_cov/id_num
        U,D,V=np.linalg.svd(pca_cov)
        sum_temp=0
        sum_threshold=sum(D)*0.99
        #print len(D)
        for index in range(0,len(D)):
            sum_temp=sum_temp+D[index]
            if sum_temp >= sum_threshold:
                break

        yield (station, [id_num, index])
        #yield (station, [id_num, index+1, list(id_sum_x), [list(ee) for ee in id_sum_xx]])
                
if __name__ == '__main__':
    MRWeather.run()