buddy = {}
buddy['aku'] = '001'
buddy['kamu'] = '002'
def get_buddy(addr):
	for x in buddy:
		print x
		if buddy[x] == addr:
			return x
	return -1

print get_buddy('001')