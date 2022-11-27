name = ""
with open("physface.txt","r") as f:
	name = f.read()
with open("physface.txt","w") as f:
	f.write(name[:-2])
