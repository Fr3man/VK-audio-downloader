# -*- coding: utf-8 -*-
'''
LICENSE GNU
made by vk.com/myafk
email: mikeking568@gmail.com

http://python.su/forum/viewtopic.php?id=13059
'''

import os, json

def parse(filead = '.\config.ini') :
	fileis = os.path.exists(filead)
	if fileis == True :
		file = open(filead, 'r')
		string = file.readlines()
		file.close()
		
		string = string[0]
		string = json.loads(string)
		return string
	else :
		update()
		return {}

def update(wif = {}, filead = '.\config.ini') :
	string = json.dumps(wif)
	
	file = open(filead, 'w')
	file.write(str(string))
	file.close()