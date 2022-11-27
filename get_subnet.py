import re
with open("inet.txt", 'r') as f:
	l = f.readline()
	match = re.search(r"inet.[0-9\.\/]*.", l)
	if match:
		l = match.group().strip("inet ")
		print(l)
	else:
		print("I couldn't find your subnet..")
		raise IOError
	with open("subnet.txt","w") as out:
		out.write(l)
