from __init__ import *
import subprocess, string, os
from random import randint, choice

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

for x in range(0,20):
	tNum = randint(0,2000)
	# functions written in such a way that the upload folder is where the reads and writes will occur.
	insert_file('example.txt',tNum)
	search_file(tNum)
	insert_file('example.txt',tNum)
	temp = randint(0,2000)
	extract_file('example.txt', temp)
	# should raise exception of some sort on second insert.
	extract_file('example.txt', temp)
	delete_file( randint(0,2000) )
	extract_file('example.txt', temp)
	search_file(temp)
	unfound = find_number()
	search_file(temp)
	search_file(temp)
	search_file(unfound)
	insert_file('example.txt', temp)
	insert_file('example.txt', unfound)
	insert_file('example.txt', temp)
	delete_file(temp)
	delete_file(tNum)
	print 'ITERATION : '+str(x)

'''
insert_file('example.txt',37)
time.sleep(11*60) ##wait at least 10 minutes for file to expire.

if extract_file('example.txt', temp):
	raise Exception("extraction passed?!")

delete_file(37)

'''

print 'Success!!'
exit(0)
