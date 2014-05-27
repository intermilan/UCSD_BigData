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
            key=station_id[name]

        except Exception, e:
            stderr.write('Error in line:\n'+line)
            stderr.write(e)
            self.increment_counter('MrJob Counters','mapper-error',1)
            out=('error', 1)
        finally:
            #yield (int(key), data_list)
            yield (int(key)/2+1024, data_list)
            yield (int(key)/4+1024+512, data_list)
            yield (int(key)/8+1024+512+256, data_list)
            yield (int(key)/16+1024+512+256+128, data_list)
            yield (int(key)/32+1024+512+256+128+64, data_list)
            yield (int(key)/64+1024+512+256+128+64+32, data_list)
            yield (int(key)/128+1024+512+256+128+64+32+16, data_list)
            #yield (int(key)/256+1024+512+256+128+64+32+16+8, data_list)
            #yield (int(key)/512+1024+512+256+128+64+32+16+8+4, data_list)
            #yield (int(key)/1024+1024+512+256+128+64+32+16+8+4+2, data_list)
    
    def reducer(self, station, counts):
        self.increment_counter('MrJob Counters','reducer',1)
        id_data=list(counts)
        id_num=len(id_data)
        id_sum_x=np.zeros(730)
        
        for index in range(0, id_num):
            id_sum_x=id_sum_x+np.array(id_data[index])
        
        pca_mean=id_sum_x/id_num
        pca_cov=np.zeros((730, 730))
        
        for index in range(0, id_num):
            temp=np.array(id_data[index])-pca_mean
            pca_cov=pca_cov+np.outer(temp, temp)
        
        pca_cov=pca_cov/id_num
        U,D,V=np.linalg.svd(pca_cov)
        sum_temp=0
        sum_threshold=sum(D)*0.99
        for index in range(0,len(D)):
            sum_temp=sum_temp+D[index]
            if sum_temp >= sum_threshold:
                break

        yield (station, [id_num, index])
        #yield (station, [id_num, index+1, list(id_sum_x), [list(ee) for ee in id_sum_xx]])
                
if __name__ == '__main__':
    MRWeather.run()