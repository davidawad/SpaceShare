#!/usr/bin/python

from app import *
import subprocess, string, os
from random import randint, choice
import unittest2 as unittest

# FIXME all testcases.

# append system path in order to import fleetdb as a module
sys.path.append(os.path.abspath('../'))

import spaceshare


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(choice(chars) for _ in range(size))

cmd = "rm -rf upload/"
# no block, it starts as a sub process.
p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# block until the cmd is done
p.wait()

get_db()

if os.path.exists('upload/'):
    raise Exception("SOMETHING WENT HORRIBLY WRONG. BREAKING.")

os.makedirs('upload/')

print id_generator()
with open("upload/example.txt", "w+") as f:
	f.write("This is some text I'm putting here.")

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


class FrontendTestCase(unittest.TestCase):

    def test_frontend(self):
        page = self.app.get('frontend/')
        self.assertEqual(page.status_code, 200)
        # self.assertTrue("Are you winkin at me?" in page.data) FIXME
        self.assertTrue('table id="machines"' in page.data)
