



def bubble(l):
    for i in range(len(l)):
        for j in range(0,len(l)-i-1):
            if l[j]>l[j+1]:
                l[j],l[j+1] = l[j+1],l[j]

    return l


def selection(l):
    for i in range(len(l)-1,0,-1):
        tmpmax = l[0]
        tmpmaxindex = 0
        for j in range(0,i+1):
            if l[j]>tmpmax:
                tmpmax = l[j]
                tmpmaxindex = j
        l[i],l[tmpmaxindex] = l[tmpmaxindex],l[i]
    return l


def insert(l):
    for i in range(1,len(l)):
        j = i
        while l[j]<l[j-1] and j>0:
            l[j],l[j-1] = l[j-1],l[j]
            j -= 1

    return l
            
            
def qs(l,low,high):
    i = low
    j = high
    k = l[low]
    if i>=j:
        return l
    while i<j:
        while l[j]>k and j>i:
            j -= 1
        while l[i]<k and j>i:
            i += 1
        if i<j:
            l[i],l[j] = l[j],l[i]
    l[i] = k
    qs(l,low,i)
    qs(l,i+1,high)
    return l

        
def merge(l1,l2):
    tmp = []
    i = 0
    j = 0
    while i<len(l1) and j<len(l2):
        if l1[i]<l2[j]:
            tmp.append(l1[i])
            i += 1
        else:
            tmp.append(l2[j])
            j += 1
    while i<len(l1):
        tmp.append(l1[i])
        i += 1
    while j<len(l2):
        tmp.append(l2[j])
        j += 1
    return tmp
            
def mergesort(l,low,high):
    if len(l[low:high+1])>1:
        mid = (low+high)/2
        left = mergesort(l,low,mid)
        right = mergesort(l,mid+1,high)
        result = merge(left,right)
        return result
    else:  
        return l[low:high+1]
        
        
    




if __name__=="__main__":
    a = [3, 4, 5, 2, 1, 6, 34]
    t1 = [1,2]
    t2 = [3]
    print mergesort(a,0,len(a)-1)
    
