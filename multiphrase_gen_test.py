import mysql.connector
import json
import yake
import threading
import multiprocessing
from stoptopic import stopwords
import math

dir_name = 'res/keywords/'

mydb = mysql.connector.connect(
	host='',
	user='',
	passwd=''
)

language = "en"
max_ngram_size = 3
deduplication_thresold = 0.5
deduplication_algo = 'seqm'
windowSize = 1
numOfKeywords = 10

mycursor = mydb.cursor()


def cal(chunck,filename):
	res = []
	count = 1
	print('started')
	kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold,dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
	for x in chunck:
		if count%10000 == 0:
			print(count,filename)
		appln_id = x[0]
		str = ''
		if x[1] is not None:
			str=str+x[1]
		if x[2] is not None:
			str=str+x[2]
		if len(str) == 0:
			continue
		keywords = kw_extractor.extract_keywords(str)
		topics = []
		for topic,score in keywords:
			if topic not in stopwords and len(topic.split(' '))>1:
				topics.append(topic)
		dict = {
		  "id": id,
		  "topics": ','.join(topics)
		}
		res.append(dict)
		count=count+1

	with open(dir_name+filename,'w') as f:
		json.dump(res,f,ensure_ascii=False)


def start_process():
	for uid in range(4):
		statement = "select text from phrasetest where uid between {} and {}".format(uid*1000000+1,(uid+1)*1000000)
		mycursor.execute(statement)
		myresult = mycursor.fetchall()
		total_process = math.ceil(len(myresult)/100000)
		procs = []
		for p in range(total_process):
			filename = "uid-{}-{}".format((uid+1)*100000*(p+1),(uid+1)*100000*(p+1))
			proc = multiprocessing.Process(target=cal,args=(myresult[(p*100000+1):(p+1)*100000],filename,))
			procs.append(proc)
			proc.start()

		for proc in procs:
			proc.join()

start_process()


# if __name__ == "__main__":
# 	print('fldkjf')
	 process1 = multiprocessing.Process(target=cal,args=(myresult[0:10000],'2018-1.json',))
	 process1.start()
	 process2 = multiprocessing.Process(target=cal,args=(myresult[10000:20000],'2018-2.json',))
	 process2.start()
	 process3 = multiprocessing.Process(target=cal,args=(myresult[20001:30000],'2018-3.json',))
	 process3.start()
	 process4 = multiprocessing.Process(target=cal,args=(myresult[30001:40000],'2018-4.json',))
	 process4.start()
	 process5 = multiprocessing.Process(target=cal,args=(myresult[40001:50000],'2018-5.json',))
	# process5.start()
	# process6 = multiprocessing.Process(target=cal,args=(myresult[50001:60000],'2018-6.json',))
	# process6.start()
	# process7 = multiprocessing.Process(target=cal,args=(myresult[60001:70000],'2018-7.json',))
	# process7.start()
	# process8 = multiprocessing.Process(target=cal,args=(myresult[70001:80000],'2018-8.json',))
	# process8.start()
	# process9 = multiprocessing.Process(target=cal,args=(myresult[80001:90000],'2018-9.json',))
	# process9.start()
	# process10 = multiprocessing.Process(target=cal,args=(myresult[90001:100000],'2018-10.json',))
	# process10.start()
	 process1.join()
	 process2.join()
	 process3.join()
	 process4.join()
	 process5.join()
	# process6.join()
	# process7.join()
	# process8.join()
	# process9.join()
	# process10.join()

