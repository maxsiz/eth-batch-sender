f1 = open('wnew.csv')
lines = f1.readlines()
receivers_list=[s.rstrip('\n') for s in lines]
amounts = [int(x.split(';')[1]) for x in receivers_list]
receivers_list = [x.split(';')[0] for x in receivers_list]


amounts = [int(x.split(',')[1]) for x in receivers_list]
receivers_list = [x.split(',')[0] for x in receivers_list]