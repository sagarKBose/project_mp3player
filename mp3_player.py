#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install pygame


# In[2]:


#pip install mutagen


# In[4]:


#pip install ttkthemes


# In[10]:


#pip install cx_freeze


# In[2]:


import os
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from pygame import mixer
import time
import threading


# In[4]:



root = tk.ThemedTk()
root.get_themes()
root.set_theme("plastik")

statusbar = ttk.Label(root, text="Welcome to Mujjiic", relief=SUNKEN, anchor=W,font='Times 10 roman')
statusbar.pack(side=BOTTOM, fill=X)

# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)


# Create the submenu

subMenu = Menu(menubar, tearoff=0)

play_list = []

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_song_file(filename_path)

def add_song_file(file_name):
    file_name=os.path.basename(file_name)
    index=0
    play_list_box.insert(index,file_name)
    play_list.insert(index,filename_path)
    index+=1

menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Mujjiic', 'This is a music player built using Python Tkinter by Sagar')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initializing the mixer

root.title("Mujjiic")
root.iconbitmap(r'images/headphones.ico')

leftframe=Frame(root)
leftframe.pack(side=LEFT,padx=10,pady=30)

play_list_box=Listbox(leftframe)
play_list_box.pack()

add_bt = ttk.Button(leftframe,text='Add',command=browse_file)
add_bt.pack(side=LEFT,padx=10)

def remove_fun():
    selected_song = play_list_box.curselection()
    selected_song = int(selected_song[0])
    play_list_box.delete(selected_song)
    play_list.pop(selected_song)
    
remove_bt = ttk.Button(leftframe,text='Remove',command=remove_fun)
remove_bt.pack(side=LEFT)


rightframe=Frame(root)
rightframe.pack(pady=10)

topframe=Frame(rightframe)
topframe.pack()

filelabel = ttk.Label(topframe, text='Play Some Mujjiic !',font='Comic 8 normal')
filelabel.pack(pady=10)

lengthlabel = ttk.Label(topframe, text='Total Duration : --:--')
lengthlabel.pack(pady=10)

currentlengthlabel = ttk.Label(topframe,text='Current Duration : --:--',relief=GROOVE)
currentlengthlabel.pack()


def show_details(play_song):
    filelabel['text'] = "Playing" + ' - ' + os.path.basename(play_song)

    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat
    
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()
    
def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currentlengthlabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = play_list_box.curselection()
            selected_song = int(selected_song[0])
            play_it = play_list[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Mujjiic could not find the file. Please load the file first.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightframe)
middleframe.pack(pady=40, padx=30)

playPhoto = PhotoImage(file='images/icons8-play-48.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=1, column=2, padx=10)

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=1, column=4, padx=10)

pausePhoto = PhotoImage(file='images/icons8-pause-52.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=1, column=3, padx=10)

rewindPhoto = PhotoImage(file='images/icons8-rewind-26.png')
rewindBtn = ttk.Button(middleframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=1, column=1)

# Bottom Frame for volume, rewind, mute etc.

bottomframe = Frame(rightframe)
bottomframe.pack(pady=10)

mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=1, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=1, column=2)


def on_closing():
    stop_music()
    root.destroy()
root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()


# In[ ]:





# In[ ]:




