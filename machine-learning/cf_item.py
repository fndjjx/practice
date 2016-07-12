import numpy as np

seq = ['Lady in the Water', 'Snakes on a Plane','Just My Luck', 'Superman Returns', 'You, Me and Dupree','The Night Listener']
seq2 = ['Lisa Rose', 'Jack Matthews', 'Michael Phillips', 'Gene Seymour','Mick LaSalle','Claudia Puig','Toby']
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

def transform():
    d = {}
    for i in seq:
        dd = {}
        for j in critics:
            if i in critics[j].keys():
                dd[j] = critics[j][i]
        d[i] = dd

    return d
    

def simdistance(l1,l2):
    return 1/(1+np.sqrt(sum((np.array(l1)-np.array(l2))**2)))

def simpearson(l1,l2):
    return np.cov(l1,l2)[0][1]/(np.std(l1)*np.std(l2))


def get_movie_to_person(movie,c):
    l=[]
    for i in seq2:
        if i in c[movie].keys():
            l.append(c[movie][i])
        else:
            l.append(0)
    return l

def similar_movie_func(movie,measure,c,select):
    score = []
    movies = c.keys()
    movies.remove(movie)
    for i in range(len(movies)):
        score.append((movies[i],measure(get_movie_to_person(movie,c),get_movie_to_person(movies[i],c))))
    
    result = []
    for i in score:
        if i[0] in select:
            result.append(i)
    return result

def recommend_bymovie(person,measure,c):
    watched = [ (k,v) for k,v in critics[person].items()]
    watched_name = [i[0] for i in watched] 
    unwatched = [i for i in seq if i not in watched_name]

    watched_rank = [i[1] for i in watched] 

    unwatched_similar = []
    for i in watched_name:
        unwatched_similar.append(similar_movie_func(i,measure,c,unwatched))

    print unwatched_similar
    result1 = []
    result2 = []
    for i in range(len(watched)):
        tmp1 = 0
        tmp2 = 0
        for j in range(len(unwatched_similar[0])):
            tmp1 += watched_rank[i]*unwatched_similar[i][j][1] 
            tmp2 += unwatched_similar[i][j][1] 
        result1.append(tmp1)
        result2.append(tmp2)
    print result1
    print result2
    result1=np.array(result1)
    result2=np.array(result2)
    result = result1/result2
    print result
    return zip(unwatched,result)
    

            

if __name__=="__main__":
    c = transform()
    print recommend_bymovie("Toby",simpearson,c)
