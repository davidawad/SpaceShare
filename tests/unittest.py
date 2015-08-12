#!/usr/bin/python

from app import *
from random import randint, choice
import unittest2 as unittest
import subprocess
import string
import os
# FIXME testcases.

##
# Turn these godawful testcases into something I can be proud of.
#
#

# append system path in order to import fleetdb as a module
sys.path.append(os.path.abspath('../'))

from spaceshare import *


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(choice(chars) for _ in range(size))

cmd = "rm -rf "
# no block, it starts as a sub process.
p = subprocess.Popen(cmd,
					 shell=True,
					 stdout=subprocess.PIPE,
					 stderr=subprocess.PIPE
					 )

# block until the cmd is done
p.wait()

spaceshare.app.get_db()

os.makedirs('upload/')

if not os.path.exists(spaceshare.config['UPLOAD_FOLDER']):
    raise Exception("SOMETHING WENT HORRIBLY WRONG. BREAKING.")


print id_generator()
with open("upload/example.txt", "w+") as f:
    f.write("This is some text I'm putting here.")


for x in range(0, 20):
	tNum = randint(0, 2000)
	# functions written in such a way that the upload folder is where the reads and writes will occur.
	insert_file('example.txt', tNum)
	search_file(tNum)
	insert_file('example.txt', tNum)
	temp = randint(0, 2000)
	extract_file('example.txt', temp)
	# should raise exception of some sort on second insert.
	extract_file('example.txt', temp)
	delete_file(randint(0, 2000))
	extract_file('example.txt', temp)
	search_file(temp)
	unfound = find_number()
	search_file(temp)
	search_file(temp)
	search_file(unfound)
	print find_number()
	insert_file('example.txt', temp)
	print find_number()
	insert_file('example.txt', unfound)
	print find_number()
	insert_file('example.txt', temp)
	delete_file(temp)
	delete_file(tNum)
    print 'ITERATION : ['+str(x) + ']'

print 'Success!!'
exit(0)


class FrontendTestCases(unittest.TestCase):

    def test_frontend(self):
        page = self.app.get('/')
        self.assertEqual(page.status_code, 200)
        self.assertTrue('<3' in page.data)



if __name__ == '__main__':
    unittest.main()
