import __init__
import os
from random import randint, choice
import subprocess
import string

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(choice(chars) for _ in range(size))

cmd = "rm -rf upload/"
# no block, it starts as a sub process.
p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# block until the cmd is done
p.wait()

if os.path.exists('upload/'):
    raise Exception("SOMETHING WENT HORRIBLY WRONG. BREAKING.")

os.makedirs('upload/')

print id_generator()

with open("upload/example.txt", "w+") as f:
	f.write("this is some text I'm putting here.")

for x in range(0,200):
	tName = id_generator()
	tNum = randint(0,2000)
	# functions written in such a way that the upload folder is where the reads and writes will occur.
	__init__.insert_file(tName,tNum)
	__init__.insert_file('example.txt',tNum)
	__init__.search_file(tNum)
	__init__.insert_file('example.txt',tNum)
	temp = randint(0,2000)
	__init__.extract_file('example.txt', temp)
	# should raise exception of some sort on second insert.
	__init__.extract_file('example.txt', temp)
	__init__.extract_file('example.txt', temp)
	__init__.search_file(temp)
	unfound = __init__.find_number()
	__init__.search_file(temp)
	__init__.search_file(temp)
	__init__.search_file(unfound)
	__init__.insert_file('example.txt', temp)
	__init__.insert_file('example.txt', unfound)
	__init__.insert_file('example.txt', temp)
	__init__.delete_file(temp)
	__init__.delete_file(tNum)
	print 'ITERATION : '+str(x)

__init__.insert_file('example.txt',37)
time.sleep(11*60) ##wait at least 10 minutes for file to expire.

if __init__.extract_file('example.txt', temp):
	raise Exception("extraction passed?!")
	
__init__.delete_file(37)


print 'Success!!'
exit(0)
