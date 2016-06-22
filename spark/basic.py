from pyspark import SparkConf,SparkContext

conf = SparkConf().setMaster("local").setAppName("myapp")
sc = SparkContext(conf=conf)

#lines = sc.textFile("data")
#select_lines = lines.filter(lambda x:"good" in x)
#print select_lines.first()
#print select_lines.collect()
#
#
#lines2 = sc.parallelize(["pandas","like pandas","hate pandas"])
#select_lines1 = lines2.filter(lambda x:"like" in x)
#select_lines2 = lines2.filter(lambda x:"hate" in x)
#ul = select_lines1.union(select_lines2)
#print ul.collect()
#print ul.count()
#
#
#
#lines3 = sc.parallelize([3,2,1,-1,-2,-3])
#sq = lines3.map(lambda x:x**2)
#print sq.collect()
#su = lines3.reduce(lambda x,y:x+y)
#print su


#lines4 = sc.parallelize(["a 10","b 3","c 4","d 3","e 1","a 3","d 6"])
#pairs = lines4.map(lambda x:(x.split(" ")[0], float(x.split(" ")[1])))
#pairs = pairs.mapValues(lambda x:(x,1)).reduceByKey(lambda x,y:(x[0]+y[0],x[1]+y[1]))
#print pairs.collect()


#lines5 = sc.parallelize("good bad good wrong happy no")
#rdd = lines5.flatMap(lambda x:x.split(" "))
#rdd = rdd.map(lambda x:(x,1)).reduceByKey(lambda x,y:x+y)
#print rdd.collect()

lines6 = sc.parallelize(["a 10","b 3","c 4","d 3","e 1","a 3","d 6"])
lines7 = sc.parallelize(["a 10","c 4","d 3","e 1","a 3","d 6"])
lines8 = sc.parallelize(["a 10","c 4"])
lines6 = lines6.map(lambda x:(x.split(" ")[0],float(x.split(" ")[1])))
lines7 = lines7.map(lambda x:(x.split(" ")[0],float(x.split(" ")[1])))
lines8 = lines8.map(lambda x:(x.split(" ")[0],float(x.split(" ")[1])))

print lines6.collect()
count = lines6.combineByKey((lambda x:(x,1)),(lambda x,y:(x[0]+y,x[1]+1)),(lambda x,y:(x[0]+y[0],x[1]+y[1])))

count = count.map(lambda x:(x[0],x[1][0]/x[1][1]))
count = count.map(lambda x:(x[1],x[0]))
print count.sortByKey().collect()

print lines7.join(lines8).collect()

