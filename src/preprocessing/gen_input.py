import sys

output = file('input_fgm.txt', 'w')

cnt = 0
train = 0
valid = 0
test = 0
uid2line = {}

f = file('features.txt')
for line in f:
	a = line.strip().split('\t', 6)
	uid = int(a[0])
	tw_cnt = int(a[4].split(':')[1])
	if tw_cnt < 10:
		continue
	# if len(a) <= 5:
	#	print line
	uid2line[uid] = cnt
	cnt += 1
	del a[4]
	out_line = '\t'.join(a[1:]) + '\t#%d\n' % uid
	if uid % 2 == 0:
		out_line = '+' + out_line
		train += 1
	else:
		if uid % 10 == 1:
			out_line = '*' + out_line
			valid += 1
		else:
			out_line = '?' + out_line
			test += 1
	output.write(out_line)
f.close()

f = file('edges.txt')
for line in f:
	a = line.split(' ')
	u = int(a[0])
	v = int(a[1])
	if u not in uid2line or v not in uid2line:
		continue
	output.write('#edge %d %d mt\n' % (uid2line[u], uid2line[v]))

f.close()

output.close()
print cnt, train, valid, test

