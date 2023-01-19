#!/usr/bin/env python

import numpy as np
import os
from pathlib import Path
import pygrib


# directory with the initial grib files
initial_directory = '/mnt/e/ensembles_mean_PRED/PF_feed_gribs_2'

# directory with the calculated radiation grib files
ens_ready = '/mnt/e/ensembles_mean_PRED/PF_ens_ready'
os.chdir(initial_directory)

file_list = []

def list_files():
    os.chdir(initial_directory)

    for files in sorted(os.listdir(initial_directory), key=len):
        if os.path.isfile(os.path.join(initial_directory, files)):
            file_list.append(files)
            # print(files) 
    
def calc_rad():

    grbs = {}
    rad_values = []
    
    for i in range(0, (len(file_list))):
        grbs[i] = pygrib.open(file_list[i])
        grbout = open(ens_ready + '/' + file_list[i], 'wb')
        for grb in grbs[i]:
            grb
        print(file_list[i])
        print(grbs[i].tell())
        count = 0
        for j in range(1, (grbs[i].tell() + 1)):
            grb = grbs[i].message(j)
            
            # Calculate radiation
            if ('list_' + grb.name):
                ('list_' + grb.name).append(grb.values)
                ('count_' + grb.name) == ('count_' + grb.name)
            else:
                'list_' + grb.name = []

            if (grb.name == '2 metre temperature'):
                print(grb.name)
                count = count + 1
                rad_values.append(grb.values)
                if count == 50:
                    array = np.array(rad_values)
                    grb.values = np.mean(array, axis= 0)
                    msg = grb.tostring()
                # print(grb.values)
                # if len(rad_values) != 50: # message count in file
                #     rad_values.append(grb.values)
                # else:
                #     value = grb.values
                #     grb.values = abs(grb.values - rad_values[count-1])
                #     rad_values[count-1] = value
            # print(count)
            
            # Calculate total precipitation, multiply by 1000
            # so that the units of measurement are meters
            # if (grb.name == 'Total precipitation'):
            #     grb.values = grb.values*1000
                
            

        
        # grb.name = '2 metre temperature'
                    grbout.write(msg)
        
        grbout.close()
        grbs[i].close()
 

if __name__ == '__main__':
    list_files()
    calc_rad()