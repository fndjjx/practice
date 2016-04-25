
import numpy as np

def generate_data(n, k):
    sample = []   
    for i in range(n):
        x = np.random.randn(n)+5*i
        y = np.random.randn(n)+5*i
        sample.extend(zip(x,y))
    return np.array(sample)


def euclid_distance(v1,v2):
    diffv1v2 = np.array(v1)-np.array(v2)
    return np.sqrt(sum(diffv1v2**2))

def get_classify_result(point, core):
    r = []
    for i in range(len(core)):
        r.append((core[i], euclid_distance(point,core[i])))

    r.sort(key=lambda x:x[1])

    return r[0]

def train_k_means_classifier(sample, k, n_iter):

    def init_core(sample,k):
        max_list = []
        min_list = []
        for i in range(len(sample[0])):
            max_list.append(max(sample[:,i]))
            min_list.append(min(sample[:,i]))
        core = []
        for i in range(len(max_list)):
            core.append(np.random.uniform(min_list[i],max_list[i],k))
        core = np.array(core).T
        return core

    def update_core(sample, core):
        distance = []
        for i in range(len(sample)):
            distance.append([sample[i]])
            shortest = 100000000
            classify_core = 0
            for j in range(len(core)):
                current_distance = euclid_distance(core[j],sample[i])
                if current_distance<shortest:
                    shortest = current_distance
                    classify_core = j
            distance[-1].extend([classify_core])

        core_sample = []
        for i in range(len(core)):
            core_sample.append([i])
            for j in distance:
                if j[1] == i:
                    core_sample[-1].extend([j[0]])

        new_core = []
        for i in core_sample:
            each_core = []
            i.pop(0)
            if i!=[]:
                tmp = reduce(lambda x,y:np.vstack((x,y)),i)
                if len(tmp.shape) == 1:
                    each_core = tmp
                else:
                    for j in range(len(tmp[0])):
                        each_core.append(np.mean(tmp[:,j]))
                new_core.append(each_core)
        return new_core
                

    core = init_core(sample, k)
    for i in range(n_iter):
        core = update_core(sample,core)

    return core
    
    

if __name__=="__main__":
    data = generate_data(3,3)
    print data
    core = train_k_means_classifier(data, 2, 3)
    test = [1,1]
    print get_classify_result(test, core)
  
        
    
