from pymongo import *

client = MongoClient('localhost', 30000)
tw = client.twitter

uids = set()

f = file('features.txt')
for line in f:
	a = line.split('\t', 2)
	uid = int(a[0])
	uids.add(uid)

print 'read finished.'

cursor = tw.tweet.find({'location.country': 'USA'}, no_cursor_timeout=True)
output = file('edges.txt', 'w')

for obj in cursor:
	if obj['user_id'] not in uids:
		continue
	u = obj['user_id']
	for x in obj['entities']['user_mentions']:
		v = x['id']
		if v not in uids:
			continue
		output.write('%d %d\n' % (u, v))

cursor.close()
