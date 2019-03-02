import requests
import spotipy
import spotipy.util as util
import pyperclip
import datetime
import msvcrt
import os
import sys 
import ctypes
from ctypes import wintypes
import win32con

print (" For Facebook Users, this looks like some random number (1111222333)")
username= input('Input your Spotify Username:')
print (username)
HOTKEYS = {
  1 : (win32con.VK_F1, win32con.MOD_ALT)
}

for id, (vk, modifiers) in HOTKEYS.items ():
  print ("Success! Press Alt + F1 to copy tracks to clipboard")
  if not ctypes.windll.user32.RegisterHotKey (None, id, modifiers, vk):
    print ("Unable to register id", id)



def main():
    while True:
        try:
            msg = ctypes.wintypes.MSG()
            while ctypes.windll.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                if msg.message == win32con.WM_HOTKEY:
                    get_track()
                ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
                ctypes.windll.user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            ctypes.windll.user32.UnregisterHotKey(None, 1)

def get_track():
    scope = 'user-read-currently-playing'
    client_id='yourclientid'
    client_secret ='yourclientsecret'
    redirect_uri='http://localhost/'

    token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_playing_track()
        album= results['item']['album']['name']
        artist=results['item']['artists'][0]['name']
        title=results['item']['name']
        duration=millis(results['item']['duration_ms'])
        progress=millis(results['progress_ms'])
        output="Now playing: " + artist +" - " + title + " [" + progress + "/" + duration + "] "
        print (output)
        pyperclip.copy(output)
    else:
        print ("Can't get token for", username) 

def millis(t):
    converted=datetime.datetime.fromtimestamp(t/1000).strftime('%#M:%#S')
    return converted


main()