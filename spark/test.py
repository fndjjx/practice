from pyspark import SparkConf,SparkContext

conf = SparkConf().setMaster("local").setAppName("myapp")
sc = SparkContext(conf=conf)

lines = sc.textFile("data")
select_lines = lines.filter(lambda x:"good" in x)
print select_lines.first()
print select_lines.collect()


lines2 = sc.parallelize(["pandas","like pandas","hate pandas"])
select_lines1 = lines2.filter(lambda x:"like" in x)
select_lines2 = lines2.filter(lambda x:"hate" in x)
ul = select_lines1.union(select_lines2)
print ul.collect()
print ul.count()



lines3 = sc.parallelize([3,2,1,-1,-2,-3])
sq = lines3.map(lambda x:x**2)
print sq.collect()
su = lines3.reduce(lambda x,y:x+y)
print su



