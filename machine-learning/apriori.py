import numpy as np
import copy

def generate_data():
    d = [ [1,2,5],
         [2,4],
         [2,3],
         [1,2,4],
         [1,3],
         [2,3],
         [1,3],
         [1,2,3,5],
         [1,2,3]]

    return d

def removelist(l1,l2):
    for i in l2:
        l1.remove(i)
    return l1

class apriori():

    def __init__(self, sample):
        self.sample = sample


    def get_single_set(self, data):
        l = set([j for i in data for j in i])
        return [[i] for i in l]

    def prune(self,origin_data, c, min_support):
        def itemisin(sub,full):
            for i in sub:
                if i not in full:
                    return False
            return True
                 
        l = []
        support = [] 
        for i in c:
            count = 0
            for j in origin_data:
                if itemisin(i,j):
                    count += 1 
            if count>=min_support:
                support.append(count)
                l.append(i)
        return l,support

    def get_support(self, origin_data, item):
        def itemisin(sub,full):
            for i in sub:
                if i not in full:
                    return False
            return True

        count = 0
        for j in origin_data:
            if itemisin(item,j):
                count += 1
        return count

    def get_subset(self,data):
        true_subset = []
        if len(data)>1:
            for i in data:
                tmp=copy.deepcopy(data)
                tmp.remove(i)
                true_subset.append([i])
                true_subset.append(tmp)
                subset = self.get_subset(tmp)

        return true_subset
           
        
    def filter_subset(self, subset):
        l = []
        for i in subset:
            if i not in l:
                l.append(i)
        return l
        

    def link(self, l):
        ll = []
        for i in range(len(l)):
            for j in range(i+1,len(l)):
                if l[i][:-1] == l[j][:-1]:
                    tmp = copy.deepcopy(l[i])
                    tmp.extend(l[j])
                    ll.append(list(set(tmp)))

        return ll
        
    def generate_frequent_set(self, min_support):
        single_set = self.get_single_set(self.sample)
        c = single_set
        l_list = []
        support_list = []
        while True:
            l,support = self.prune(self.sample,c,min_support)
            if l == []:
                break
            l_list.append(l)
            support_list.append(support)
            c = self.link(l)
        return l_list[-1],support_list[-1]

    def get_rule(self, frequent_set, min_trust):
        fsl, fss = frequent_set
        rules = []
        for i in range(len(fsl)):
            subset = self.filter_subset(self.get_subset(fsl[i]))
            support = fss[i]
            for j in subset:
                s1 = copy.deepcopy(j)
                s2 = removelist(copy.deepcopy(fsl[i]),s1)
                s1support = self.get_support(self.sample, s1)
                trust = support/float(s1support)
                if trust>min_trust:
                    rules.append((s1,s2))
        return rules

if __name__=="__main__":
    data = generate_data()
    a = apriori(data)
    f = a.generate_frequent_set(1)
    print f
    print a.get_rule(f,0.3)
    



