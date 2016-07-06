
class search():
    def __init__(self):
 
        self.result = False
    def binarysearch(self, sorted_l,item):
        if len(sorted_l)>1:
            median = sorted_l[len(sorted_l)/2]
            if median>item:
                self.binarysearch(sorted_l[:len(sorted_l)/2],item)
            elif median<item:
                self.binarysearch(sorted_l[len(sorted_l)/2:],item)
            else:
                self.result = True
    def binarysearch2(self,sorted_l,item):
        low = 0
        high = len(sorted_l)
        l = sorted_l[low:high]
        median = len(l)/2
        while len(l)>1:
            if l[median] == item:
                return True
            elif l[median]>item:
                high = median
            else:
                low = median
            l = l[low:high]
            median = len(l)/2
        return False 


if __name__ == "__main__":
    l = [2,3,4,7,23,6,6746,7867,8]
    l.sort()
    s = search()
    print s.binarysearch2(l,4)
    print s.binarysearch2(l,77)

    

