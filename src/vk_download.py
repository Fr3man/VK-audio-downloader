# -*- coding: utf8 -*-
__author__ = 'akonovalov'
import vk_api as vk
import cfg, os, urllib
folder = "Songs"
replace_list = [["&quot;",""], ["&#39;","'"], ["&amp;","&"], ["/",""]]

def get_access_token():
    login = raw_input("You email:\n")
    password = raw_input("Your password:\n")
    cookies = vk.login(login, password, True)
    access_token = vk.api_login(cookies)
    return access_token

def get_songs_list(access_token) :
    user_id = raw_input("User id who provides songs for you (default it's yours):\n")
    response =  vk.method(access_token, "audio.get", {"uid": user_id})
    #print response.get("response")
    song_list = response.get("response")
    return song_list

def create_dir() :
    if not os.path.exists(folder):
        os.mkdir(folder)

def get_song_name(song) :
    artist = song.get("artist")[:61].strip()
    song_title = song.get("title")[:61].strip()
    suffix = ".mp3"
    song_name = song_title + " - " + artist + suffix
    for pair in replace_list:
        song_name = song_name.replace(pair[0],pair[1])
    return song_name

def download_song(song) :
    song_name = get_song_name(song)
    fs_song_name = folder + "/" + song_name
    try :
        print str(i+1) + ') "' + song_name + '"'
    except :
        print str(i+1) + ') "' + "Song name can't be shown!"
    if os.path.isfile(fs_song_name):
       url_size = urllib.urlopen(song.get("url")).info()['Content-Length']
       fs_size = os.stat(folder + "/" + song_name).st_size
       #print "url_size = " + str(url_size) + "; fs_size = " + str(fs_size)
       if str(url_size) > str(fs_size):
           print "need download..."
           urllib.urlretrieve(song.get("url"), fs_song_name)
       else:
           print "already downloaded!"
           return
    else:
        pass
        print "downloading..."
        urllib.urlretrieve(song.get("url"), fs_song_name)
    progress = ((i+1)*1.0/len(song_list))*100
    print "Song downloaded! Total", str(progress)[:4] + "%"

access_token = get_access_token()
create_dir()
song_list = get_songs_list(access_token)
print "Download " + str(len(song_list)) + " files..."
for i in range(len(song_list)):
    song = song_list[i]
    download_song(song)
#print os.listdir(".")
print "\nThe work done!\nFind songs in path:\n" + os.getcwd() + "\\" + folder
raw_input()