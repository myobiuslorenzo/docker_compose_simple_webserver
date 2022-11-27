import re
with open("route.txt", 'r') as f:
	l = f.readline()
	match = re.search(r"via.[0-9\.\/]*.dev", l)
	if match:
		l = match.group().strip("viadev: ")
		print(l)
	else:
		print("I couldn't find your gateway..")
		raise IOError
	with open("gateway.txt","w") as out:
		out.write(l)
