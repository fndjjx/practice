import numpy as np

seq = ['Lady in the Water', 'Snakes on a Plane','Just My Luck', 'Superman Returns', 'You, Me and Dupree','The Night Listener']
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


def simdistance(l1,l2):
    return 1/(1+np.sqrt(sum((np.array(l1)-np.array(l2))**2)))

def simpearson(l1,l2):
    return np.cov(l1,l2)[0][1]/(np.std(l1)*np.std(l2))


def get_person_to_movie(person):
    l=[]
    for i in seq:
        if i in critics[person].keys():
            l.append(critics[person][i])
        else:
            l.append(0)
    return l

def similar_people_func(person,measure,k):
    score = []
    people = critics.keys()
    people.remove(person)
    for i in range(len(people)):
        score.append((person,people[i],measure(get_person_to_movie(person),get_person_to_movie(people[i]))))
    score.sort(key=lambda x:x[2],reverse = True)
    similar_people=[]
    for i in score[:k]:
        similar_people.append((i[1],i[2]))
    return similar_people

def recommend_byperson(person,measure,k):
    similar_people = similar_people_func(person,measure,k)
    similarity = []
    movie_rank = []
    whether_critic = []
    for p in similar_people:
        similarity.append(p[1])
        movie_rank.append(np.array(get_person_to_movie(p[0])))
        whether_critic.append(movie_rank[-1]>0)

    movie_rank = np.array(movie_rank)
    similarity = np.array(similarity)
    whether_critic = np.array(whether_critic)
    

    result1 = movie_rank.T.dot(similarity.T)
    result2 = whether_critic.T.dot(similarity.T)
    return zip(result1/result2,seq)
            

if __name__=="__main__":
    print recommend_byperson("Toby",simdistance,5)
