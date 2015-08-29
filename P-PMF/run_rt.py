########################################################
# run_rt.py 
# Author: Jamie Zhu <jimzhu@GitHub>
# Created: 2014/2/6
# Last updated: 2015/02/11
# Implemented approach: P-PMF (Privacy-Preserving MF)
# Evaluation metrics: MAE, NMAE, RMSE
########################################################

import numpy as np
import os, sys, time
import multiprocessing
sys.path.append('src')
# Build external model
if not os.path.isfile('src/core.so'):
	print 'Lack of core.so (built from the C++ module).' 
	print 'Please first build the C++ code into core.so by using: '
	print '>> python setup.py build_ext --inplace'
	sys.exit()
from utilities import *
import evaluator
import dataloader
 

#########################################################
# config area
#
para = {'dataType': 'rt', # set the dataType as 'rt' or 'tp'
		'dataPath': '../data/dataset#1/',
		'outPath': 'result/',
		'metrics': ['MAE', 'NMAE', 'RMSE'], # delete where appropriate		
		'density': np.arange(0.05, 0.31, 0.05), # matrix density
		'rounds': 20, # how many runs are performed at each matrix density
		'dimension': 10, # dimenisionality of the latent factors
		'etaInit': 0.01, # inital learning rate. We use line search
						 # to find the best eta at each iteration
		'lambda': 12, # regularization parameter
		'maxIter': 300, # the max iterations
		'noiseType': 'uniform', # the type of noises: 'guassian' or 'uniform'
		'noiseRange': 0.5, # the range of the noises
		'saveTimeInfo': False, # whether to keep track of the running time
		'saveLog': True, # whether to save log into file
		'debugMode': False, # whether to record the debug info
        'parallelMode': False # whether to leverage multiprocessing for speedup
		}

initConfig(para)
#########################################################


startTime = time.clock() # start timing
logger.info('==============================================')
logger.info('Approach: P-PMF (Privacy-Preserving MF)')

# load the dataset
dataMatrix = dataloader.load(para)
logger.info('Loading data done.')

# run for each density
if para['parallelMode']: # run on multiple processes
    pool = multiprocessing.Pool()
    for density in para['density']:
		pool.apply_async(evaluator.execute, (dataMatrix, density, para))
    pool.close()
    pool.join()
else: # run on single processes
	for density in para['density']:
		evaluator.execute(dataMatrix, density, para)

logger.info(time.strftime('All done. Total running time: %d-th day - %Hhour - %Mmin - %Ssec.',
         time.gmtime(time.clock() - startTime)))
logger.info('==============================================')
sys.path.remove('src')