from mpi4py import MPI
import re
from collections import Counter
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm_size = comm.Get_size()
reducer = comm_size-1
def array_packer(arr,size):
    arr_size = len(arr)
    
    mod = arr_size % (size-1)
    
    ele_size = int(arr_size/(size-1))
    
    packed_arr = []
    count = 0
    
    for i in range(0,size):
        if i == 0:
            packed_arr.append(None)
            continue
        temp = []
        for j in range(0,ele_size):
            data = arr[count]
            temp.append(data)
            count = count +1
        if mod > 0 :
            data = arr[count]
            temp.append(data)
            count = count + 1
            mod = mod -1
            
        packed_arr.append(temp)
    
    return packed_arr


map_list = [i for i in range(0,comm_size-1)]
real_map_list =  [i for i in range(1,comm_size-1)]
reduce_list = [i for i in range (1,comm_size)]
if rank in map_list:
    color = 1
else: 
    color = 0
map_comm = comm.Split(color,rank)
if rank in reduce_list:
    color2 = 2
else:
    color2 = 0
reduce_comm = comm.Split(color2,rank)
map_size = len(map_list) 
data = None
word_fre = Counter()
if rank == 0:
    data = []
    with open("test.txt","r") as file:
        for line in file:
            data.append(line)
    data = array_packer(data,map_size)
if rank in map_list:
    root = 0
    data = map_comm.scatter(data,root)

if rank in real_map_list :
    #print(f"{rank}: {data}")
    
    word_fre = Counter()
    for sent in data:
        text = re.sub(r'[^A-Za-z ]+', '', sent.replace('-', ' '))
        text = text.split()
        word_fre = word_fre + Counter(text)
    #print(word_fre)

if rank in reduce_list:
    word_fre = reduce_comm.gather(word_fre,reducer-1)
if rank == reducer :
    temp = Counter()
    
    for item in word_fre:
        
        temp = temp + item
    for key,value in temp.items():
        print(key,value)

    

#print(f"i have rank {rank} and my data is {data}")

