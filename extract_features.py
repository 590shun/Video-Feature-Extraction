#-*- coding:utf-8 -*-

import os
os.environment["CUDA_VISIBLE_DEVICES"]='0,1,2,3'
#os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-mode', type=str, help='rgb or flow')
parser.add_argument('-load_model', type=str)
parser.add_argument('-root', type=str)
#parser.add_argument('-gpu', type=str)
parser.add_argument('-save_dir', type=str)
parser.add_argument('-file', type=str)

args = parser.parse_args()
#os.environ["CUDA_VISIBLE_DEVICES"]=args.gpu

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim import lr_scheduler
from torch.autograd import Variable

import torchvision
from torchvision import datasets, transforms
import videotransforms


import numpy as np

from pytorch_i3d import InceptionI3d

from charades_dataset_full import Charades as Dataset


def run(max_steps=64e3, mode='rgb', root='../MMdata/', split='../tmp.json', batch_size=1, load_model='', save_dir='', file=''):
    # setup dataset
    test_transforms = transforms.Compose([videotransforms.CenterCrop(224)])

    dataset = Dataset(split, 'training', root, mode, file, test_transforms, num=-1, save_dir=save_dir)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=0, pin_memory=True)

    #val_dataset = Dataset(split, 'testing', root, mode, test_transforms, num=-1, save_dir=save_dir)
    #val_dataloader = torch.utils.data.DataLoader(val_dataset, batch_size=batch_size, shuffle=True, num_workers=8, pin_memory=True)    

    #dataloaders = {'train': dataloader, 'val': val_dataloader}
    #datasets = {'train': dataset, 'val': val_dataset}
    dataloaders = {'train': dataloader}
    datasets = {'train': dataset}

    
    # setup the model
    if mode == 'flow':
        i3d = InceptionI3d(400, in_channels=2)
    else:
        i3d = InceptionI3d(400, in_channels=3)
    i3d.replace_logits(157)
    i3d.load_state_dict(torch.load(load_model))
    i3d.cuda()

    #for phase in ['train', 'val']:
    for phase in ['train']:
        i3d.train(False)  # Set model to evaluate mode
                
        tot_loss = 0.0
        tot_loc_loss = 0.0
        tot_cls_loss = 0.0
                    
        # Iterate over data.
        for data in dataloaders[phase]:
            # get the inputs
            inputs, labels, name = data
            if os.path.exists(os.path.join(save_dir, name[0]+'.npy')):
                continue

            b,c,t,h,w = inputs.shape
            print('input size: ', inputs.shape)
            size = 100
            #if t > size:
            #    features = []
            #    for start in range(1, t-56, size):
            #        end = min(t-1, start+size+56)
            #        start = max(1, start-48)
            #        ip = Variable(torch.from_numpy(inputs.numpy()[:,:,start:end]).cuda(), volatile=True)
            #        features.append(i3d.extract_features(ip).squeeze(0).permute(1,2,3,0).data.cpu().numpy())
            #    #print(np.concatenate(features, axis=0).shape)
            #    np.save(os.path.join(save_dir, name[0]), np.concatenate(features, axis=0))
            #else:
            #    # wrap them in Variable
            #    inputs = Variable(inputs.cuda(), volatile=True)
            #    print(inputs.shape)
            #    features = i3d.extract_features(inputs)
            #    print(features.squeeze(0).permute(1,2,3,0).data.cpu().numpy().shape)
            #    np.save(os.path.join(save_dir, name[0]), features.squeeze(0).permute(1,2,3,0).data.cpu().numpy())
            stride = 16
            features = []
            print('test')
            for start in range(0, t, 1):
                start = max(0, start - (stride//2 - 1))
                end = start + (stride - 1) + 1
                if end > t:
                    end = t
                    start = end - stride
                #print('start: ', start)
                #print('end: ', end)
                #print('inputs: ', inputs.numpy()[:, :, start:end, :, :].shape)
                #print('ip: ', ip.shape)
                with torch.no_grad():
                    ip = Variable(torch.from_numpy(inputs.numpy()[:, :, start:end, :, :]).cuda(), volatile=True)
                    features.append(i3d.extract_features(ip).squeeze(0).permute(1,2,3,0).data.cpu().numpy())
            if mode == 'rgb' or mode == 'flow':
                np.save(os.path.join(save_dir, name[0]), np.concatenate(features, axis=0))
                print('output size: ', np.concatenate(features, axis=0).shape)
            elif mode == 'temp':
                #print(np.concatenate(features, axis=0).shape)
                np.save(os.path.join(save_dir, name[0] + '_i3d'), np.concatenate(np.squeeze(np.squeeze(features, axis = 1), axis = 1), axis=0))
                print('output size: ', np.concatenate(np.squeeze(np.squeeze(features, axis = 1), axis = 1), axis=0).shape)


if __name__ == '__main__':
    # need to add argparse
    run(mode=args.mode, root=args.root, load_model=args.load_model, save_dir=args.save_dir, file=args.file)
