#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author : Hua XiaoZhuan          
# @Time   : 7/27/2022 3:13 PM

import torch.nn as nn
import torch
import logging
import datetime
import os
import numpy as np

def initWeights(layer):
    ''' Initialize layer parameters

    :param layer: the layer to be initialized
    :return:
    '''
    classname = layer.__class__.__name__
    if classname.find('Conv2d') != -1 or classname.find('ConvTranspose2d') != -1:
        nn.init.kaiming_uniform_(layer.weight)
        if layer.bias is not None:
            nn.init.zeros_(layer.bias)
        logging.info("init layer [%s] with kaiming_uniform"% classname)
    elif classname.find('BatchNorm') != -1:
        nn.init.normal_(layer.weight, 1.0, 0.02)
        if layer.bias is not None:
            nn.init.zeros_(layer.bias)
        logging.info("init layer [%s] with normal" % classname)
    elif classname.find('Linear') != -1:
        nn.init.xavier_normal_(layer.weight)
        if layer.bias is not None:
            nn.init.zeros_(layer.bias)
        logging.info("init layer [%s] with xavier_normal" % classname)
    else:
        logging.info("no init layer[%s]"%classname)
        print("no init layer[%s]"%classname)

class EarlyStopping():
    ''' Early Stopping

    '''
    def __init__(self, tolerance_epoch = 5, delta=0, is_max = False):
        ''' Init method

        :param tolerance_epoch: tolarance epoch
        :param delta: delta for difference
        :param is_max: max or min
        '''

        self._tolerance_epoch = tolerance_epoch
        self._delta = delta
        self._is_max = is_max

        self._counter = 0
        self.early_stop = False
        self.optimal_model = None
        self.optimal_metric = None

    def __call__(self, validation_metric,model_state_dict):
        if self.optimal_metric is not None:
            if (self._is_max and (validation_metric < self.optimal_metric - self._delta)) or\
                ((not self._is_max) and (validation_metric > self.optimal_metric + self._delta)): # less optimal
                self._counter += 1
            else: # more optimal
                logging.info("Reset earlystop counter")
                self._counter = 0
                self.optimal_metric = validation_metric
        else:
            self.optimal_model = model_state_dict
            self.optimal_metric = validation_metric

        if self._counter >= self._tolerance_epoch:
            self.early_stop = True

    def __str__(self):
        _str = 'EarlyStopping:%s\n'%self._tolerance_epoch
        _str += '\tdelta:%s\n'%self._delta
        _str += '\tis_max:%s\n' % self._is_max
        return _str

def adjust_learning_rate(epoch, optimizer, cfg):
    steps = np.sum(epoch > np.asarray(cfg.SOLVER.LR_DECAY_STAGES))
    if steps > 0:
        new_lr = cfg.SOLVER.LR * (cfg.SOLVER.LR_DECAY_RATE**steps)
        for param_group in optimizer.param_groups:
            param_group["lr"] = new_lr
        print(f"At epoch {epoch}, learning rate change to {new_lr}")
        return new_lr
    return cfg.SOLVER.LR

class Timer:
    ''' Timer to stat elapsed time

    '''
    def __enter__(self):
        self.start = datetime.datetime.now()
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = datetime.datetime.now()
        total_seconds = (self.end - self.start).total_seconds()
        _str = "Total seconds:%s" % (total_seconds)
        print(_str)
        logging.info(_str)