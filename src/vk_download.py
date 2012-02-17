# -*- coding: utf8 -*-
__author__ = 'aleksaander@ya.ru'
import vk_api as vk
import cfg, os, urllib, re
folder = "Songs"
replace_list = [["&quot;",""], ["&#39;","'"], ["&amp;","&"], ["/",""],["|",""]]
GLOBAL_SEARCH_COUNT = 50

def get_access_token():
    import getpass
    login = raw_input("You email:\n")
    password = getpass.getpass("Your password:\n")
    print "wait..."
    cookies = vk.login(login, password, True)
    access_token = vk.api_login(cookies)
    return access_token

def get_user_songs_list(access_token) :
    user_id = raw_input("User id who provides songs for you (default it's yours):\n")
    response =  vk.method(access_token, "audio.get", {"uid": user_id})
    #print response.get("response")
    song_list = response.get("response")
    return song_list

def get_search_songs_list(access_token, search_str) :
    response =  vk.method(access_token, "audio.search", {"q": search_str, "count": GLOBAL_SEARCH_COUNT})
    #print response.get("response")
    song_list = response.get("response")[1:]
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

def get_song_duration(song) :
    drt = song.get("duration")
    drt = "%i:%02i" % (int(drt)/60, int(drt) % 60)
    return drt

def download(url, fs_song_name) :
    import urllib, time
    start_t = time.time()

    def progress(bl, blsize, size):
        dldsize = min(bl*blsize, size)
        if size != -1:
          p = float(dldsize) / size
          try:
            elapsed = time.time() - start_t
            est_t = elapsed / p - elapsed
          except:
            est_t = 0
          print "%6.2f %% %6.0f s %6.0f s %6i / %-6i bytes\r" % (
              p*100, elapsed, est_t, dldsize, size),
        else:
          print "%6i / %-6i bytes" % (dldsize, size)

    urllib.urlretrieve(url, fs_song_name, progress)

def download_song(song, i) :
    song_name = get_song_name(song)
    fs_song_name = folder + "/" + song_name
    try :
        print str(i+1) + ') "' + song_name + '"'
    except :
        print str(i+1) + ') ' + "Song name can't be shown!"
    if os.path.isfile(fs_song_name):
       url_size = urllib.urlopen(song.get("url")).info()['Content-Length']
       fs_size = os.stat(folder + "/" + song_name).st_size
       #print "url_size = " + str(url_size) + "; fs_size = " + str(fs_size)
       if str(url_size) > str(fs_size):
           print "need download..."
           download(song.get("url"), fs_song_name)
       else:
           print "already downloaded!"
           return
    else:
        pass
        print "downloading..."
        download(song.get("url"), fs_song_name)
        print " "*60 +"\r"

def download_songs_list(song_list) :
    print "Download " + str(len(song_list)) + " files..."
    for i in range(len(song_list)):
        song = song_list[i]
        download_song(song, i)
        progress = ((i+1)*1.0/len(song_list))*100
        print "Song downloaded! Total download rate", str(progress)[:4] + "%"
    print "\nThe work done!\nFind songs in path:\n" + os.getcwd() + "\\" + folder

def get_song_numbers_from_input (input) :
    numbers = input.split()
    if len(numbers) == 0 :
        return 0
    else :
        return numbers

def print_song_list(song_list) :
    for i, song in enumerate(song_list) :
        try :
            print "%i) %s %s" % (i+1, get_song_name(song), get_song_duration(song))
        except :
            print "%i) %s" % (i+1, "Song name can't be shown!")

def search_user_songs(song_list) :

    def get_search_result(song_list, search_str) :
        search_result = []
        for song in song_list:
            if search_str in get_song_name(song) :
                search_result.append(song)
        return search_result

    input = raw_input("Put search string:\n")
    search_result = get_search_result(song_list, input)
    print "Search result:"
    print_song_list(search_result)


    menu = """
Put number of what you want:
1. Download these songs
2. Put spaces separated songs numbers to download
3. New search
4. Exit
"""
    while True :
        input = raw_input(menu)
        if input == str(1) :
            download_songs_list(search_result)
        elif input == str(2) :
            input_numbers = raw_input("Put space separated songs numbers to download:\n")
            song_number_list = get_song_numbers_from_input (input_numbers)
            download_list = [search_result[int(str_num)-1] for str_num in song_number_list]
            download_songs_list(download_list)
            work_with_user_song_list(song_list)
        elif input == str(3) :
            search_user_songs(song_list)
        elif input == str(4) :
            exit("Bye")
        else :
            print ("Wrong input!")
            continue


def work_with_user_song_list(song_list) :
    menu = """
Put number of what you want:
1. Download all user's songs
2. Download by numbers
3. Search songs
4. View user's songs
5. Main menu
6. Exit
"""

    while True :
        input = raw_input(menu)
        if input == str(1) :
            download_songs_list(song_list)
        elif input == str(2) :
            input_numbers = raw_input("Put space separated songs numbers to download:\n")
            if re.match("^[\d ]+$", input_numbers):
                song_number_list = get_song_numbers_from_input (input_numbers)
            else:
                print ("Wrong input!")
                continue
            download_list = [song_list[int(str_num)-1] for str_num in song_number_list]
            download_songs_list(download_list)
        elif input == str(3) :
            search_user_songs(song_list)
        elif input == str(4) :
            print_song_list(song_list)
        elif input == str(5) :
            break
        elif input == str(6) :
            exit("Bye")
        else :
            print ("Wrong input!")
            continue

def work_with_global_search(access_token) :

    while True:

        search_str = raw_input("Put search string:\n")
        search_str = search_str.decode('cp1251',errors='ignore')
        search_str = search_str.encode('utf8', errors='ignore')
        song_list = get_search_songs_list(access_token, search_str)

        print "Global search result:"
        if len(song_list) == 0:
            print "Not found!"
            return
        else:
            print_song_list(song_list)

        menu = """
Put number of what you want:
1. Download by numbers
2. Main menu
3. New search
4. Exit
"""

        while True :
            input = raw_input(menu)
            if input == str(1) :
                input_numbers = raw_input("Put space separated songs numbers to download:\n")
                if re.match("^[\d ]+$", input_numbers):
                    song_number_list = get_song_numbers_from_input (input_numbers)
                else:
                    print ("Wrong input!")
                    continue
                download_list = [song_list[int(str_num)-1] for str_num in song_number_list]
                download_songs_list(download_list)
            elif input == str(2) :
                return
            elif input == str(3) :
                break
            elif input == str(4) :
                exit("Bye")
            else :
                print ("Wrong input!")
                continue


access_token = get_access_token()
create_dir()
while True:
    music_menu = """
Where would do like to search:
1. Everywhere
2. Certain user
3. Exit
"""
    input = raw_input(music_menu)
    if input == str(1):
        work_with_global_search(access_token)
    elif input == str(2):
        song_list = get_user_songs_list(access_token)
        work_with_user_song_list(song_list)
    elif input == str(3):
        exit("Bye")
    else :
        print ("Wrong input! Put the number:")
        continue
raw_input("Press Enter to Exit")