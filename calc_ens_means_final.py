#!/usr/bin/env python

import numpy as np
import os
from pathlib import Path
import pygrib


# directory with the initial grib files
initial_directory = '/mnt/e/ensembles_mean_PRED/PF_feed_gribs_MARS'

# directory with the calculated means of ensembles
ens_ready = '/mnt/e/ensembles_mean_PRED/PF_ens_ready_MARS'
os.chdir(initial_directory)

file_list = []

def list_files():
    os.chdir(initial_directory)

    for files in sorted(os.listdir(initial_directory), key=len):
        if os.path.isfile(os.path.join(initial_directory, files)):
            file_list.append(files)
    
def calc_means():

    grbs = {}
    rad_values = []
    name_list = []
    
    for i in range(0, (len(file_list))):

        # Yhe list of unique parameters in grib file
        unique_params = []

        # grib file to read
        grbs[i] = pygrib.open(file_list[i])

        # grib file to write
        grbout = open(ens_ready + '/' + file_list[i], 'wb')
        for grb in grbs[i]:
            if (grb.shortName not in unique_params):
                unique_params.append(grb.shortName)
        for param in unique_params:
            param_values = []
            grb = grbs[i].select(shortName=param)

            for g in grb:
                param_values.append(g.values)

            # Calculate mean values
            mean_values = np.mean(param_values, axis= 0)
            grb[0].values = mean_values

            # take only first element in the list which contain calculated mean values
            grb_mean = grb[0]

            msg = grb_mean.tostring()
            grbout.write(msg)           
            
        
        grbout.close()
        grbs[i].close()
 

if __name__ == '__main__':
    list_files()
    calc_means()