__author__ = 'patrickjameswhite'
import os
import pyautogui
import time
import cv2
import numpy as np
import pytesseract
from PIL import Image,ImageGrab
import datetime
import logging

debug_time = 8
cache_image_analysis = {}
cur_dir = os.path.dirname(os.path.abspath(__file__))
cur_dir_imgs = "{}/Images".format(cur_dir)
cur_dir_screen_caps = "{}/Bot Screen Captures".format(cur_dir)

def app_running(name):
    import psutil
    for x in psutil.pids():
        try:

            if name in psutil.Process(x).name():
                return True
        except BaseException:
            pass
    return False

def enter_soundcloud_search_bar(song):
    #searching soundcloud search bar and entering the song name
    pass

def search_soundcloud_song(song):
    time.sleep(0.3)
    pyautogui.moveTo(421, 123)
    pyautogui.click()
    pyautogui.hotkey('command', 'a','delete')
    pyautogui.typewrite(song)
    pyautogui.hotkey('enter')
    time.sleep(1.0)
#print("entry searched in soundcloud")

def click_track_from_search():
    #clicking the track button on the left to get only songs
    pyautogui.moveTo(183, 312)
    pyautogui.click()
    pyautogui.click()


    time.sleep(1.5)
#taking a screenshot

def click_play_from_click_track():
    #(click_x,click_y) = get_middle_point("code screen.png","sc play.png")
    (click_x,click_y) = (554, 304)
    pyautogui.moveTo(click_x,click_y)
    pyautogui.click()
    #print("playing %s",song)

    time.sleep(0.25)

def fetch_song_length_soundcloud():
    screenshot = ImageGrab.grab()
    screenshot.save(cur_dir_screen_caps+"/current soundcloud code screen.png","PNG")

    puzzle = cv2.imread(cur_dir_screen_caps+"/current soundcloud code screen.png")
    newXY1 = macToPicXY((855, 800))
    newXY2 = macToPicXY((891, 825))
    img = puzzle[int(newXY1[1]):int(newXY2[1]),int(newXY1[0]):int(newXY2[0])]
    cv2.imwrite("debug song length soundcloud.png",img)
    cv2_im = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im)
    base_split_string = pytesseract.image_to_string(pil_im).split(":")
    try:
        seconds = int(base_split_string[0])*60 + int(base_split_string[1])
    except BaseException:
        raise Exception("BlahBlahBlah")

    return seconds

def fetch_song_length_spotify(tup):
    screenshot = ImageGrab.grab()
    screenshot.save(cur_dir_screen_caps+"/current spotify code screen.png","PNG")


    puzzle = cv2.imread(cur_dir_screen_caps+"/current spotify code screen.png")
    pixTup = macToPicXY(tup)

    #(x,y) = get_middle_point1("current spotify code screen.png","new song length match spotify.png")

    img = puzzle[int(pixTup[1]-15):int(pixTup[1]+50),int(pixTup[0]-50):int(pixTup[0]+30)]

    cv2.imwrite("debug song length spotify.png",img)

    cv2_im = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im)
    base_split_string = pytesseract.image_to_string(pil_im).split(":")
    try:
        seconds = int(base_split_string[0])*60 + int(base_split_string[1])
    except ValueError:
        seconds = 0

    return seconds
def macToPicXY(tup):

    ratioX = tup[0] / 1440
    ratioY = tup[1] / 900
    return (2880 * ratioX,1800 * ratioY)

def get_points(base_image,search_image):
    img_rgb = cv2.imread(base_image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(search_image,0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    tup_list = [x for x in zip(*loc[::-1])]

    try:
        max1 = min(tup_list,key = lambda x : x[0] + x[1])
    except ValueError:
        raise ValueError("Bot crashed, might be delay in wifi connection")
    (puzzleHeight, puzzleWidth) = img_rgb.shape[:2]
    screenWidth, screenHeight = pyautogui.size()
    click_x = (max1[0] / 2880) * screenWidth
    click_y = (max1[1] / 1800) * screenHeight
    cv2.rectangle(img_rgb, max1, (max1[0] + w, max1[1] + h), (255,255,0), 2)
    cv2.imwrite(cur_dir_screen_caps+'/multiple img match output.png',img_rgb)
    #print(click_x,click_y,max1,puzzleWidth,puzzleHeight)
    return (click_x,click_y)


def get_middle_point1(base_image,search_image):
    import time
    s1 = time.time()
    puzzle = cv2.imread(base_image)
    waldo = cv2.imread(search_image)
    #cv2.imwrite("test base screen.png",puzzle)
    #cv2.imwrite("test search.png",waldo)
    (waldoHeight, waldoWidth) = waldo.shape[:2]
    (puzzleHeight, puzzleWidth) = puzzle.shape[:2]
    screenWidth, screenHeight = pyautogui.size()
    result = cv2.matchTemplate(puzzle, waldo, cv2.TM_CCOEFF)
    (_, _, minLoc, maxLoc) = cv2.minMaxLoc(result)
    topLeft = maxLoc
    botRight = (topLeft[0] + waldoWidth, topLeft[1] + waldoHeight)
    roi = puzzle[topLeft[1]:botRight[1], topLeft[0]:botRight[0]]

    mask = np.zeros(puzzle.shape, dtype = "uint8")
    puzzle = cv2.addWeighted(puzzle, 0.25, mask, 0.75, 0)

    puzzle[topLeft[1]:botRight[1], topLeft[0]:botRight[0]] = roi

    click_x = (topLeft[0] / puzzleWidth) * screenWidth
    click_y = (topLeft[1] / puzzleHeight) * screenHeight

    #pyautogui.moveTo(click_x,click_y)
    #click_x += ((waldoWidth / puzzleWidth) * screenWidth) / 2
    #click_y += ((waldoHeight / puzzleHeight) * screenHeight) / 2

    #print((puzzleHeight/screenHeight),puzzleWidth/screenWidth)

    #cv2.imwrite("penis.png",puzzle)

    #time.sleep(3)


    e1 = time.time() - s1

    #print(e1)

    return (topLeft[0],topLeft[1])
def get_middle_point(base_image,search_image):
    import time
    s1 = time.time()
    puzzle = cv2.imread(base_image)
    waldo = cv2.imread(search_image)
    #cv2.imwrite("test base screen.png",puzzle)
    #cv2.imwrite("test search.png",waldo)
    (waldoHeight, waldoWidth) = waldo.shape[:2]
    (puzzleHeight, puzzleWidth) = puzzle.shape[:2]
    screenWidth, screenHeight = pyautogui.size()
    result = cv2.matchTemplate(puzzle, waldo, cv2.TM_CCOEFF)
    (_, _, minLoc, maxLoc) = cv2.minMaxLoc(result)
    topLeft = maxLoc
    botRight = (topLeft[0] + waldoWidth, topLeft[1] + waldoHeight)
    roi = puzzle[topLeft[1]:botRight[1], topLeft[0]:botRight[0]]

    mask = np.zeros(puzzle.shape, dtype = "uint8")
    puzzle = cv2.addWeighted(puzzle, 0.25, mask, 0.75, 0)

    puzzle[topLeft[1]:botRight[1], topLeft[0]:botRight[0]] = roi

    click_x = (topLeft[0] / puzzleWidth) * screenWidth
    click_y = (topLeft[1] / puzzleHeight) * screenHeight

    #click_x += ((waldoWidth / puzzleWidth) * screenWidth) / 2
    #click_y += ((waldoHeight / puzzleHeight) * screenHeight) / 2

    #print((puzzleHeight/screenHeight),puzzleWidth/screenWidth)

    #cv2.imwrite("penis.png",puzzle)

    #time.sleep(3)


    e1 = time.time() - s1

    #print(e1)

    return (click_x,click_y)


def pause_soundcloud():
    os.system("open -a /Applications/Google\ Chrome.app")
    time.sleep(0.5)
    pyautogui.click(161, 805)
def pause_spotify():
    os.system("open -a Spotify")
    time.sleep(0.3)
    pyautogui.click(84, 796)
def search_spotify_song(song):

    #positioned at the x to clear any previous result
    pyautogui.click(393, 45)
    pyautogui.typewrite(song)
    pyautogui.hotkey('enter')
    time.sleep(0.5)

def play_song_from_search_spotify():
    pyautogui.click(251, 423)

def go_to_soundcloud_tab():
    try:
        screenshot = ImageGrab.grab()
        screenshot = screenshot.crop((0,0,2880,160))
        screenshot.save(cur_dir_screen_caps+"/current soundcloud tab screen.png","PNG")

        if "sc tab" in cache_image_analysis:
            tab_location = cache_image_analysis["sc tab"]
        else:
            tab_location = get_points(cur_dir_screen_caps+"/current soundcloud tab screen.png",cur_dir_imgs+"/soundcloud image match.png")
            cache_image_analysis["sc tab"] = tab_location
        pyautogui.moveTo(tab_location[0]+10,tab_location[1]+10)
        pyautogui.click()
        return True
    except ValueError:
        return False

def go_to_youtube_tab():
    try:
        screenshot = ImageGrab.grab()
        screenshot = screenshot.crop((0,0,2880,160))
        screenshot.save("current youtube tab screen.png","PNG")

        if "yt tab" in cache_image_analysis:
            tab_location = cache_image_analysis["yt tab"]
        else:
            tab_location = get_points(cur_dir_screen_caps+"/current youtube tab screen.png",cur_dir_imgs+"/youtube image match.png")
            cache_image_analysis["yt tab"] = tab_location
        #print(tab_location)
        pyautogui.moveTo(tab_location[0]+10,tab_location[1]+10)
        pyautogui.click()
        return True
    except ValueError:
        return False

def search_chrome_url(url,tab_img):
    import os,time
    os.system("open -a /Applications/Google\ Chrome.app")
    #print("opening Chrome")

    time.sleep(1.0)
    if tab_img == "sc":
        active_sc_tab = go_to_soundcloud_tab()
    elif tab_img == "yt":
        active_sc_tab = go_to_youtube_tab()
    #print(active_sc_tab)
    if not active_sc_tab:

        pyautogui.moveTo(393, 76)
        pyautogui.click()
        pyautogui.hotkey('command', 't')

        pyautogui.typewrite(url)
        pyautogui.hotkey('enter')
        #print("finished typing, searching")
        time.sleep(1.6)
def pause_youtube():
    os.system("open -a /Applications/Google\ Chrome.app")
    time.sleep(0.5)
    pyautogui.moveTo(500, 391)
    pyautogui.click()

def search_youtube_song(song):
    time.sleep(0.3)
    pyautogui.moveTo(245, 119)
    pyautogui.click()
    pyautogui.hotkey('command', 'a','delete')
    pyautogui.typewrite(song)
    pyautogui.hotkey('enter')
    time.sleep(1.0)

def play_song_from_search_youtube():
    pyautogui.moveTo(431, 254)
    pyautogui.click()
    time.sleep(0.9)

def fetch_song_length_youtube():
    screenshot = ImageGrab.grab()
    screenshot.save(cur_dir_screen_caps+"/current youtube code screen.png","PNG")

    puzzle = cv2.imread(cur_dir_screen_caps+"/current youtube code screen.png")
    newXY1 = macToPicXY((252, 607))
    newXY2 = macToPicXY((283, 633))
    img = puzzle[int(newXY1[1]):int(newXY2[1]),int(newXY1[0]):int(newXY2[0])]

    cv2_im = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im)
    base_split_string = pytesseract.image_to_string(pil_im).split(":")
    #print(base_split_string)
    try:
        seconds = int(base_split_string[0])*60 + int(base_split_string[1])
        output_str = "debug song length youtube(%d secs).png"%(seconds)
        cv2.imwrite(output_str,img)
    except BaseException:
        raise Exception("BlahBlahBlah")

    return seconds

def search_play_youtube(song):
    search_chrome_url("https://www.youtube.com/","yt")
    search_youtube_song(song)
    play_song_from_search_youtube()
    song_length = fetch_song_length_youtube()
    print("youtube |",datetime.datetime.now(),"'%s' sleeping for %d seconds" % (song,song_length))
    #time.sleep(song_length - 3)
    time.sleep(debug_time)
    pause_youtube()

    pass



def search_play_soundcloud(song):
    search_chrome_url("https://soundcloud.com/stream","sc")
    search_soundcloud_song(song)
    click_track_from_search()
    click_play_from_click_track()

    song_length = fetch_song_length_soundcloud()

    print("soundcloud |",datetime.datetime.now(),"'%s' sleeping for %d seconds" % (song,song_length))
    #time.sleep(song_length - 3)
    time.sleep(debug_time)
    pause_soundcloud()

def search_play_spotify(song):
    import os,time

    os.system("open -a Spotify")

    time.sleep(0.5)

    search_spotify_song(song)
    #play_song_from_search_spotify()
    time.sleep(0.2)
    img = ImageGrab.grab()
    img.save(cur_dir_screen_caps+"/spotify ss.png","PNG")
    print(cur_dir_imgs+"/song header spotify.png")
    spot_click = get_points(cur_dir_screen_caps+"/spotify ss.png",cur_dir_imgs+"/song header spotify.png")
    #spot_click = get_middle_point("spotify ss.png","song header spotify.png")
    #print(spot_click)
    #x:-42
    #y:+72
    pyautogui.moveTo(spot_click[0]-52,spot_click[1]+40)

    pyautogui.click()
    time.sleep(1)
    #pyautogui.moveTo(spot_click[0]-52+813,spot_click[1]+40)
    tup = (spot_click[0]-52+813,spot_click[1]+40)
    song_length = fetch_song_length_spotify(tup)
    #print(song_length)
    print("spotify| ",datetime.datetime.now(),"'%s' sleeping for %d seconds" % (song,song_length))
    #time.sleep(song_length - 3)
    time.sleep(debug_time)
    pause_spotify()


def close_tab():
    pyautogui.hotkey('command','w')



def play_songs(song_list):
    #,"soundcloud|Best I Ever Had -(ISLAND VIBE REMIX)"]
    for entry in song_list:
        split_entry = entry.split("|")
        outlet = split_entry[0]
        song = split_entry[1]

        if outlet == "spotify":
            search_play_spotify(song)

        elif outlet == "soundcloud":
            search_play_soundcloud(song)

        elif outlet == "itunes":
            pass

        elif outlet == "youtube":
            search_play_youtube(song)

def play_song(song):
    split_entry = song.split("|")
    outlet = split_entry[0]
    song = split_entry[1]

    if outlet == "spotify":
        search_play_spotify(song)

    elif outlet == "soundcloud":
        search_play_soundcloud(song)

    elif outlet == "itunes":
        pass

    elif outlet == "youtube":
        search_play_youtube(song)

#["youtube|love yourself vanic remix","soundcloud|kamikaze boxinbox","spotify|starboy"]
if __name__ == "__main__":
    #import argparse
    import os
    #parser = argparse.ArgumentParser(description='Short sample app')

    #parser.add_argument('-song', action="store",dest='song')
    #results = parser.parse_args()
    #print(results.song)
    start_time = time.time()
    song_list = ["spotify|starboy"]
    play_songs(song_list)
    #play_song(results.song)

    end_time = time.time() - start_time
    print("total time is %d seconds"%end_time)
    #pyautogui.hotkey("browsersearch")