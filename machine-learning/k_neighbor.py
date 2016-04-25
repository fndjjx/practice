import numpy as np

def euclid_distance(v1,v2):
    diffv1v2 = np.array(v1)-np.array(v2)
    return np.sqrt(sum(diffv1v2**2))


def generate_data():
    x = np.linspace(0,10,100)
    y = np.linspace(0,10,100)
    feature = zip(x,y)
    target1 = 10*np.random.randn(50)+30
    target2 = 10*np.random.randn(50)+80
    target = np.hstack((target1,target2))

    return feature,target


def predict(feature,target,testdata,k):
    def calc_distance(v,l,k,target):
        r = []
        for i in range(len(l)):
            r.append((euclid_distance(v,i),target[i]))

        r.sort(key=lambda x:x[0])
        return np.array(r[:k])

    k_neighbors = calc_distance(testdata,feature,k,target) 
    print k_neighbors
    return np.mean(k_neighbors[:,1])
    
        



if __name__ == "__main__":
    feature,target = generate_data()
    print predict(feature,target,[3,3],3)
  
