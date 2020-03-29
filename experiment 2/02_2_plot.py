#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creating plots for experiment 2
"""
import numpy as np
import bbi
import matplotlib.pyplot as plt
import pickle


# my main method (iterative map estimation)
content = np.load('output/03_main.npz')
n_eval = content['n_eval']
#ll_m = content['ll_m']
errors_m = content['errors_m']
t_m = content['t_m']

e_m = np.exp(np.mean( np.log(errors_m), axis=0))
plt.semilogy(n_eval, e_m)

# the miracle solution
content = np.load('output/03_miracle.npz')
errors_mir = content['errors_mir']

e_mir = np.exp(np.mean( np.log(errors_mir), axis=0))
plt.semilogy(n_eval, e_mir, color = 'red')


# random guessing
content = np.load('output/03_21_random_se.npz')
errors_gpe = content['errors_gpe']
error_5 = np.percentile(errors_gpe, 5, axis = 0)
error_95 = np.percentile(errors_gpe, 95, axis = 0)
error_average = np.exp(np.mean( np.log(errors_gpe), axis=0))

plt.fill_between(n_eval, error_5, error_95, color = 'lightgray')
plt.semilogy(n_eval, error_average, color = 'black')

# with exploratory phase

n_eval_pre = pickle.load(open('output/03_pre20_n_eval.pkl', 'rb'))
errors_f = pickle.load(open('output/03_pre_errors_f.pkl', 'rb'))
errors_r = pickle.load(open('output/03_pre_errors_r.pkl', 'rb'))


for e,n in zip(errors_r, n_eval_pre):
    e_r = np.exp(np.mean( np.log(e), axis=0))
    plt.semilogy(n, e_r, color = 'lightgray')


for e,n in zip(errors_f, n_eval_pre):
    e_f = np.exp(np.mean( np.log(e), axis=0))
    plt.semilogy(n,e_f, color = 'black')
    
plt.show()

plotdata = np.zeros((len(n_eval), 6))
plotdata[:,0] = n_eval
plotdata[:,1] = e_m
plotdata[:,2] = e_mir
plotdata[:,3] = error_average
plotdata[:,4] = error_5
plotdata[:,5] = error_95

np.savetxt('output/exp3.data', plotdata, '%3i %1.3e %1.3e %1.3e %1.3e %1.3e')


for e_r, e_f, n in zip(errors_r, errors_f, n_eval_pre):
        n_init = n[0]
        filename = 'output/exp3_{}.data'.format(n_init)
        plotdata = np.zeros((len(n), 3))
        plotdata[:,0] = n
        plotdata[:,1] = np.exp(np.mean( np.log(e_f), axis=0))
        plotdata[:,2] = np.exp(np.mean( np.log(e_r), axis=0))
        np.savetxt(filename, plotdata, '%3i %1.3e %1.3e')
