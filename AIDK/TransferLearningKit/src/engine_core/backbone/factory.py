#!/usr/bin/python
# -*- coding: utf-8 -*-
from .lenet import LeNet
from .resnet import resnet18
import logging

def createBackbone(backbone_name,**kwargs):
    ''' create backbone by name

    :param backbone_name: backbone name
    :param kwargs: kwargs to create backbone
    :return: a backbone model
    '''
    if backbone_name.lower() == 'lenet':
        model = LeNet(kwargs['num_classes'])#.cuda()
        return model
    elif backbone_name.lower() == 'resnet18':
        model = resnet18(num_classes=kwargs['num_classes'])
        return model
    else:
        logging.error("[%s] is not supported"%backbone_name)
        raise NotImplementedError("[%s] is not supported"%backbone_name)
