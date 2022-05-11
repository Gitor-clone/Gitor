# -*- coding: utf-8 -*-
from ast import arg
import numpy as np
import pandas as pd
import re
import os
import math
import time
import random
from tqdm import tqdm

import torch
import torch.nn as nn
import gensim
import argparse


class source_func_info:
    def __init__(self, path=None):
        self.source_path = path
        self.word2index = {}
        self.index2word = {}
        self.func_num = 0

        self.weights = None
    
    def read_source_func(self):
        file_list = os.listdir(self.source_path)
        print(f'INFO: Loading {len(file_list)} source code.')
        for file in file_list:
            tmp_file = int(file.split('.')[0])

            if tmp_file not in self.word2index:
                self.word2index[tmp_file] = self.func_num + 1
                self.index2word[self.func_num + 1] = tmp_file
                self.func_num += 1
            else:
                raise ValueError
    def get_weights(self, weights):
        self.weights = weights

def get_funcs(args):  

    funcs_info = source_func_info(args.source_func_path)
    funcs_info.read_source_func()


    word2vec_model = gensim.models.KeyedVectors.load_word2vec_format(args.embed_model_path, binary=False)

    weights = torch.randn(funcs_info.func_num + 1, args.embed_dim)
    weights[0] = torch.zeros(args.embed_dim)

    funcs_cnt = 0
    for word, func_idx in funcs_info.word2index.items():
        # TODO
        word = f'{word}.java'
        if word in word2vec_model:
            funcs_cnt += 1
            weights[func_idx] = torch.FloatTensor(word2vec_model.get_vector(word))
        else:
            pass

    print(f'INFO: Loading {funcs_cnt} funcs to weights.')
    funcs_info.get_weights(weights)

    del word2vec_model

    # tmp_func = 5647
    # print(f'{tmp_func} weight is {funcs_info.weights[funcs_info.word2index[tmp_func]]}')

    return funcs_info


def get_csv(path):

    eval_dataset = []

    df = pd.read_csv(path, sep=',', engine='python')
    # for _, row in tqdm(df.iterrows(), desc='Read_csv', mininterval=10):
    for _, row in df.iterrows():
        f1 = int(row['f1'])
        f2 = int(row['f2'])
        eval_dataset.append([f1, f2])
    
    return eval_dataset

def cal_sim(args, funcs_info, f1, f2, manhattan_dis=None):
    f1, f2 = funcs_info.word2index[f1], funcs_info.word2index[f2]
    wf1, wf2 = funcs_info.weights[f1], funcs_info.weights[f2]
    if args.sim_metric == 'cos':
        return torch.cosine_similarity(wf1, wf2, dim=0)
    elif args.sim_metric == 'manhattan':
        return manhattan_dis(wf1.unsqueeze(0), wf2.unsqueeze(0))
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--sim_metric', type=str, default='cos', 
                            choices=['cos', 'manhattan'])
    parser.add_argument('--cos_sim_threshold', type=float, default=0.85)
    parser.add_argument('--Manhattan_threshold', type=float, default=1)

    parser.add_argument('--embed_dim', type=int, default=16)
    parser.add_argument('--embed_model_path', default='./embedding.txt')
    parser.add_argument('--source_func_path', default='./data/id2sourcecode/')
    parser.add_argument('--pair_csv_path', default='./data/BCB/')

    args = parser.parse_args()
    
    print('INFO: --------args----------')
    for k in list(vars(args).keys()):
        print('INFO: %s: %s' % (k, vars(args)[k]))
    print('INFO: --------args----------\n')


    funcs_info = get_funcs(args)

    if 'csv' in args.pair_csv_path:
        csv_list = [args.pair_csv_path]
    else:
        csv_list = [os.path.join(args.pair_csv_path, i) for i in os.listdir(args.pair_csv_path)]


    # cal cosine similarity for each csv file
    manhattan_dis = nn.PairwiseDistance(p=1)


    tp = tn = fp = fn = 0

    # f_out = open('output_code2vec.txt', 'a+')

    csv_list.sort()

    begin_time = time.time()
    read_time = 0
    pd_time = 0

    for csv_file in csv_list:
        print(f'\n\nINFO: Loading {csv_file}...')

        read_begin_time = time.time()
        eval_dataset = get_csv(csv_file)
        read_time += (time.time() - read_begin_time)

        print(f'INFO: The length of {csv_file} is {len(eval_dataset)}')

        tmp_tp = tmp_fn = 0

        pd_begin_time = time.time()
        # for i in tqdm(eval_dataset, desc=args.sim_metric, mininterval=10):
        for i in eval_dataset:
            f1, f2 = i[0], i[1]
            tmp_sim = cal_sim(args, funcs_info, f1, f2, manhattan_dis=manhattan_dis)
            # f_out.write(f'{tmp_sim.item()}\n')

            # clone csv
            if 'NoClone' not in csv_file:
                if tmp_sim >= args.cos_sim_threshold:
                    tp += 1
                    tmp_tp += 1
                else:
                    fn += 1
                    tmp_fn += 1
            # non clone csv
            elif 'NoClone' in csv_file:
                if tmp_sim < args.cos_sim_threshold:
                    tn += 1
                else:
                    fp += 1
        
        pd_time += (time.time() - pd_begin_time)

        if 'NoClone' not in csv_file:
            print(f'INFO: *csv: {csv_file}, tp: {tmp_tp}, fn: {tmp_fn}, R: {float(tmp_tp/(tmp_tp+tmp_fn))} ')
        
        del eval_dataset

    
    print(f'\n\nINFO: all time is {time.time() - begin_time}')
    print(f'\n\nINFO: read time is {read_time}')
    print(f'\n\nINFO: pred time is {pd_time}')


    print(f'\n\nINFO: #####################final result#####################')
    print('INFO: --------args----------')
    for k in list(vars(args).keys()):
        print('INFO: %s: %s' % (k, vars(args)[k]))
    print('INFO: --------args----------\n')
    print(f'*INFO: tp: {tp}, tn: {tn}, fp: {fp}, fn: {fn}')
    P = float(tp/(tp+fp))
    R = float(tp/(tp+fn))
    f1 = float(2.0*P*R/(P+R))
    print(f'*INFO: P: {P}, R: {R}, f1: {f1}')
    

