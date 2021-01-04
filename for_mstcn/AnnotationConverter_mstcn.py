# -*- coding: utf-8 -*-

import numpy as np
import sys
args = sys.argv

dir_in = str(args[1])
file = str(args[2])
extension = '.txt'
dir_out = str(args[3])
path_out = dir_out + file + '_mstcn' + extension
frame_rate = int(args[4])
num_of_frame = int(args[5])
hierarchy1 = str(args[6])
hierarchy2 = str(args[7])

path_in = dir_in + file + extension
fh = open(path_in,'r',encoding="utf-8_sig")
#fh = open(path_in,'r')
line = fh.readline()

start_time1_hierarchy1 = []
start_time2_hierarchy1 = []
end_time_hierarchy1 = []
duration_hierarchy1 = []
label_hierarchy1 = []
size_hierarchy1 = 0
start_time1_hierarchy2 = []
start_time2_hierarchy2 = []
end_time_hierarchy2 = []
duration_hierarchy2 = []
label_hierarchy2 = []
size_hierarchy2 = 0

i = 1
while line:
    tab_pos = []
    target = '\t'
    index = -1
    while True:
        index = line.find(target, index + 1)
        if index == -1:
            break
        tab_pos.append(index)
        #print('start=%d' % index)
    newline_pos = line.find('\n')

    #print(line)
    #print(tab_pos)
    #print(newline_pos)
    
    hierarchy_tmp = line[0 : tab_pos[0]]
    start_time1_tmp = line[tab_pos[1]+1 : tab_pos[2]]
    start_time2_tmp = line[tab_pos[2]+1 : tab_pos[3]]
    end_time1_tmp = line[tab_pos[3]+1 : tab_pos[4]]
    end_time2_tmp = line[tab_pos[4]+1 : tab_pos[5]]
    duration1_tmp = line[tab_pos[5]+1 : tab_pos[6]]
    duration2_tmp = line[tab_pos[6]+1 : tab_pos[7]]
    label_tmp = line[tab_pos[7]+1 : newline_pos]
    
    if hierarchy_tmp == hierarchy1:
        start_time1_hierarchy1.append(start_time1_tmp)
        start_time2_hierarchy1.append(start_time2_tmp)
        end_time_hierarchy1.append(end_time2_tmp)
        duration_hierarchy1.append(duration2_tmp)
        label_hierarchy1.append(label_tmp)
        size_hierarchy1 += 1
    
    if hierarchy_tmp == hierarchy2:
        start_time1_hierarchy2.append(start_time1_tmp)
        start_time2_hierarchy2.append(start_time2_tmp)
        end_time_hierarchy2.append(end_time2_tmp)
        duration_hierarchy2.append(duration2_tmp)
        label_hierarchy2.append(label_tmp)
        size_hierarchy2 += 1
    
    
    line = fh.readline()
    i += 1

cnt1 = 0
cnt2 = 0
cnt_line = 0
f = open(path_out, 'w')
while True:
    
    if (cnt1 < size_hierarchy1) & (cnt2 < size_hierarchy2):
        #if (start_time1_hierarchy1[cnt1][0:11] == start_time1_hierarchy2[cnt2][0:11]):
        if (round(float(start_time2_hierarchy1[cnt1]), 1)) == (round(float(start_time2_hierarchy2[cnt2]), 1)):
            loop = round(float(duration_hierarchy2[cnt2]) * float(frame_rate))
            for pn in range(0, loop, 1):
                f.write(label_hierarchy2[cnt2])
                f.write('\n')
                cnt_line += 1
                if cnt_line == num_of_frame:
                    break
            latest_label = label_hierarchy2[cnt2]
            cnt1 += 1
            cnt2 += 1
        elif (float(start_time2_hierarchy1[cnt1]) < float(start_time2_hierarchy2[cnt2])):
            loop = round(float(duration_hierarchy1[cnt1]) * float(frame_rate))
            for pn in range(0, loop, 1):
                f.write(label_hierarchy1[cnt1])
                f.write('\n')
                cnt_line += 1
                if cnt_line == num_of_frame:
                    break
            latest_label = label_hierarchy1[cnt1]
            cnt1 += 1
        elif (float(start_time2_hierarchy1[cnt1]) > float(start_time2_hierarchy2[cnt2])):
            print('annotation error 1')
            break
    elif (cnt1 < size_hierarchy1) & (cnt2 == size_hierarchy2):
        loop = round(float(duration_hierarchy1[cnt1]) * float(frame_rate))
        for pn in range(0, loop, 1):
            f.write(label_hierarchy1[cnt1])
            f.write('\n')
            cnt_line += 1
            if cnt_line == num_of_frame:
                break
        latest_label = label_hierarchy1[cnt1]
        cnt1 += 1
    elif (cnt1 == size_hierarchy1) & (cnt2 < size_hierarchy2):
        print('annotation error 2')
        break
    elif (cnt1 == size_hierarchy1) & (cnt2 == size_hierarchy2):
        if (cnt_line < num_of_frame):
            while cnt_line < num_of_frame:
                f.write(latest_label)
                f.write('\n')
                cnt_line += 1
        print('end converting')
        break

f.close()
