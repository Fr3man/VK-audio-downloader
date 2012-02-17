# -*- coding: utf-8 -*-
'''
LICENSE GNU
made by vk.com/myafk
email: mikeking568@gmail.com

http://python.su/forum/viewtopic.php?id=13059
'''
import urllib, urllib2, cookielib, re, json, cfg

app_id = 2681884 # Desktop приложение
useragent = 'Opera/9.80 (Windows NT 6.1; U; ru) Presto/2.10.229 Version/11.60'
settings = cfg.parse()

def login(login, password, use_ini = True) : # Получение Cookies remixsid
	url_login = 'https://login.vk.com/'
	login_ini = 1
	
	if use_ini == True :
		account_settings = {}
		
		if settings.has_key(login) == True :
			account_settings = settings[login]
			
			if account_settings.has_key('sid') == True :
				login_ini = 0
				sid = account_settings['sid']
	
	try:
		if login_ini == 0 and use_ini == True:
			if check_sid(sid) == True:
				#print 'VK: sid in config'
				print 'please wait...'
				return sid
			else :
				print 'VK: relogin'
				login_ini = 1
				
		if login_ini == 1 :
		
			values = {
				'act' : 'login',
				'email' : login,
				'pass' : password
				}

			headers = {
				'User-Agent' : useragent
				}
				
			cookie = cookielib.CookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
			urllib2.install_opener(opener)

			data = urllib.urlencode(values)
			req = urllib2.Request(url_login, data, headers)
			response = urllib2.urlopen(req)
			res = response.read()

			reg = 'remixsid=(.*) for'
			rg = re.compile(reg,re.IGNORECASE|re.DOTALL)
			m = rg.findall(str(cookie))
			
			if m :
				sid = m[0]

				if sid != None and check_sid(sid) == True :
					if use_ini == True :
						account_settings.update({'sid' : sid})
						settings.update({login : account_settings})
						cfg.update(settings)

					print 'VK: login'
					return sid
				else :
					print 'VK: login error'
					return False
	
	except Exception, detail: 
		print "def login:", detail
		e = raw_input('Error')

def api_login(sid, login = None, use_ini = True) : # Получение токена (Desktop приложение)
	url = 'https://oauth.vk.com/authorize'
	login_ini = 1
	
	if use_ini == True :
		account_settings = {}
		
		if settings.has_key(login) == True :
			account_settings = settings[login]
			
			if account_settings.has_key('token') == True :
				login_ini = 0
				token = account_settings['token']

	try:
		if login_ini == 0 and use_ini == True:
			if check_token(token) == True:
				print 'API: token in config'
				return token
			else :
				login_ini = 1
		
		if login_ini == 1 :
			if check_sid(sid) == False :
				print 'API: login error - bad sid'
				return False
			
			values = {
				'client_id' : app_id,
				'scope' : 524287,
				'response_type' : 'token'
				}
			
			headers = {
				'User-Agent' : useragent,
				'Cookie' : 'remixsid=%s' % (sid)
				}
			
			data = urllib.urlencode(values)
			req = urllib2.Request(url, data, headers)
			response = urllib2.urlopen(req)
			res = response.read()
			geturl = response.geturl()
			
			if geturl != url :
				reg = 'access_token=(.*?)&'
			
				rg = re.compile(reg,re.IGNORECASE|re.DOTALL)
				m = rg.findall(geturl)
			
				if m:
					token=m[0]
					
					if token != None and check_token(token) == True :
						if use_ini == True :
							account_settings.update({'token' : token})
							settings.update({login : account_settings})
							cfg.update(settings)

						#print 'API: login'
						print 'login success'
						return token
			else :
				reg='\?hash=(.*?)&'
				rg = re.compile(reg,re.IGNORECASE|re.DOTALL)
				m = rg.findall(res)
				
				if m:
					hash = m[0]
					values = {
						'hash' : hash,
						'client_id' : app_id,
						'settings' : 524287,
						'redirect_uri' : 'blank.html',
						'response_type' : 'token'
						}
					url = 'https://api.vk.com/oauth/grant_access'
					
					data = urllib.urlencode(values)
					req = urllib2.Request(url + '?' + data, '', headers)
					response = urllib2.urlopen(req)
					res = response.read()
					geturl = response.geturl()
					
					reg = 'access_token=(.*?)&'
					rg = re.compile(reg,re.IGNORECASE|re.DOTALL)
					m = rg.findall(geturl)
					
					if m:
						token=m[0]
						
						if token != None and check_token(token) == True :
							if use_ini == True :
								account_settings.update({'token' : token})
								settings.update({login : account_settings})
								cfg.update(settings)

							#print 'API: login'
							print 'login success'
							return token
	except Exception, detail:
		print "def api_login:", detail
		e = raw_input('Error')

def method(token, method, values = {}) : # Использование методов API
	url = 'https://api.vk.com/method/%s.json' % (method)
	
	values.update({'access_token' : token})

	try:
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		res = response.read()
		res = json.loads(res)

		if 'error' in res : # Вывод информации об ошибке
			error = res['error']
			error = error['error_code']
			error_text = 'API: '
			
			if error == 1 :
				error_text += 'Unknown error occurred'
			elif error == 2 :
				error_text += 'Application is disabled'
			elif error == 4 :
				error_text += 'Incorrect signature'
			elif error == 5 :
				error_text += 'User authorization failed'
			elif error == 6 :
				error_text += 'Too many requests per second'
			elif error == 14 :
				error_text += 'Captcha is needed'
			else :
				error_text += 'error'
				print str(res)
				
			print error_text
			
		return res
	except Exception, detail:
		print "def method:", detail
		e = raw_input('Error')

def check_sid(sid) : # Прверка Cookies remixsid на валидность
	url_check = 'https://vk.com/feed2.php'
	
	headers = {
		'User-Agent' : useragent,
		'Cookie' : 'remixsid=%s' % (sid)
	}
	
	req = urllib2.Request(url_check, '', headers)
	response = urllib2.urlopen(req)
	res = response.read()
	unlogin = '{"user": {"id": -1}}'
	
	if unlogin in res :
		return False
	else :
		return True
		
def check_token(token) : # Прверка access_token на валидность
	res = method(token, 'isAppUser')
	if 'response' in res :
		return True
	elif 'error' in res :
		return False