
import numpy as np
data = [3,4,1,5.7,3,6,10,23]

def create_array():
    arr = np.array(data)
    print arr
    
    data2 = [data,[i*2 for i in data]]
    arr2 = np.array(data2)
    print arr2
    print arr2.ndim
    print arr2.shape
    print arr2.dtype
    
    
    data3 = np.zeros(arr.shape)
    data4 = np.ones_like(arr)
    data5 = np.empty(arr2.shape)
    print data3
    print data4
    print data5
    
    
    data6 = np.arange(10)
    print data6

    data7 = np.eye(5)
    print data7

def array_scalar_cal():
    data = np.array([[1,2,3],[4,5,6]])
    print data*2
    print data+2
    print data*data


def array_index():
    data = np.array([[1,2,3],[4,5,6]])
    print data
    print data[:,2]
    print data[1]
    data_slice = data[1,1:2]
    print data_slice
    data_slice = 77
    print data_slice
    print data

def array_bool_index():
    data = np.array(['a','b','c','d'])
    randnum = np.random.randn(4,5)
    print data
    print randnum
    print data=='a'
    print randnum[data=='a']
    print randnum[data!='a']
    mask = (data != 'a') & (data != 'b' )
    print randnum[mask]
    mask2 = (data == 'a') | (data != 'b' )
    print randnum[mask2]
    randnum[randnum>0]=0
    print randnum

def array_fancy_index():
    data = np.empty((8,4))
    for i in range(8):
        data[i] = i
    print data
    arr = np.array([3,2,5])
    print data[arr]
    arr2 = np.array([[3,2,5],[2,3,1]])
    print data[arr2]
    print data[[3,2,5],[2,3,1]]
    data2 = np.arange(32).reshape((8,4))
    index = np.ix_([3,2,5],[2,3,1])
    print data2
    print data2[index]



def calc():
    data = np.arange(5)
    print data*2+data/5.0
    data2 = np.arange(-5,0)
    cond = np.array([True,False,True,False,False])
    print cond
    print np.where(cond,data,data2)
    print np.where(data>2,2,-2)
    print np.where(data>2,2,data)
    print np.cumsum(data)
    data3 = np.arange(10).reshape(2,5)
    print data3
    print data3.cumsum()
    print data3.cumsum(0)
    print data3.cumsum(1)
    data4 = np.random.randn(10).reshape(2,5)
    print data4
    data4.sort(1)
    print data4


def linalg_calc():
    x = np.array([[1,2],[2,3],[3,4]])
    y = np.array([[1,2,3],[2,3,4]])
    m = x.dot(y)
    print m
    print np.linalg.inv(m) 
    

def random_walk(n):
    position = 0
    walk = [position]
    for i in range(n):
        position = position + np.random.randn()
        walk.append(position)

    print walk


    step = np.random.randn(n)
    walk = step.cumsum()
    print walk


    step = np.random.randn(3,n)
    walk = step.cumsum(1)
    print walk



if __name__ == "__main__":
    calc()
