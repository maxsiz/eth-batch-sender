# -*- coding: utf-8 -*-
import sys

if  len(sys.argv)==2:
        file1 = sys.argv[1] #file with receivers list
else:
    print (
        'wrong params number - {}'
        ' , usage: python3 {} full_file'.format(
            len(sys.argv), sys.argv[0]
        )
    )
    sys.exit('use file as script param')

with open(file1) as r_file:
    lines = r_file.readlines()
    receivers_list=[s.rstrip('\n') for s in lines]
    print('Full Receivers list len={}, are {}'.format(len(receivers_list) ,receivers_list))

i=0
while len(receivers_list) >= 250:
    batch = receivers_list[i:i+250]
    batch_file = open(file1.split('.')[0]+'250_'+str(i)+'.csv', 'w')
    batch_file.writelines([s+'\n' for s in batch])
    batch_file.close()
    receivers_list = receivers_list[i+250:]
    i += 1
    print('File: {}, len()={}, len(receivers_list)={}'.format(batch_file, len(batch), len(receivers_list)))
    if len(receivers_list) < 250:
        batch = receivers_list
        batch_file = open(file1.split('.')[0]+'b_last'+'.csv', 'w')
        batch_file.writelines([s+'\n' for s in batch])
        batch_file.close()
