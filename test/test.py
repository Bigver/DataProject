from tkinter import *
from PIL import ImageTk , Image
import os
import pygame as pg
import numpy as np
import wave

def btn_clicked():
    print("Button Clicked")

def restart_program():
    window.destroy()
    os.startfile("test.py")



def synth(frequency, duration=1.5, sampling_rate=44100):
        frames = int(duration*sampling_rate)
        arr = np.cos(2*np.pi*frequency*np.linspace(0,duration, frames))
        arr = np.clip(arr*10, -1, 1) # squarish waves
        fade = list(np.ones(frames-4410))+list(np.linspace(1, 0, 4410))
        arr = np.multiply(arr, np.asarray(fade))
        return list(arr)

pg.init()
pg.mixer.init()



a_file = open("noteslist.txt")
file_contents = a_file.read(); a_file.close()
noteslist = file_contents.splitlines()
freq = 16.3516 #starting frequency
freqs = {}

for i in range(len(noteslist)):
    freqs[noteslist[i]]= freq
    freq = freq * 2 ** (1/12)



##############เสริชหาเพลงในไฟล์###########################
def play():
        #นำค่าจาก TextBox เช้ามาเสริช
        fp = "music%s.txt"%e2.get()    
        with open(fp, "r") as file:
            notes = [eval(line.rstrip()) for line in file]
        track = []
        for i in range(int(len(notes)/2)):
            track = track + list(np.zeros(max(0, int(44.1*(notes[i*2][2]-100)))))
            track = track + synth(freqs[notes[i*2][1]], 1e-3*(notes[i*2+1][2]+100))
   
        arr = 32767*np.asarray(track)*0.5
        sound = np.asarray([arr,arr]).T.astype(np.int16)
        sound = pg.sndarray.make_sound(sound.copy())
        sound.play()
        sfile = wave.open('mario.wav', 'w')
        sfile.setframerate(44100)
        sfile.setnchannels(2)
        sfile.setsampwidth(2)
        sfile.writeframesraw(sound)

                


    
window = Tk()
window.geometry("414x736")
window.title("NoteMusic")
#สร้างไฟล์เก็บจำนวนเพลงบนหน้าtk โดยการนับจากความยาวของArray
f = open('file1.txt', 'r')
data = f.read()
AddFrame = []
for i in data:
    if i != ",":
        AddFrame.append(i)
print(len(AddFrame))
#########################################################################################
def raise_frame(frame):
    frame.tkraise()

home = Frame(window,width = 414,height = 736)  
s1 = Frame(window,width = 414,height = 736)  

for frame in (home ,s1):  # ลูปเอาไว้เปลี่ยนเฟรม
    frame.grid(row=1, column=1)
#####################################เพิ่มเพลง-ลบเพลง#######################################
#ลบเพลงโดยการนำไฟล์เทคมาลบอเรออก1ตัว
def deleteframe():
    print("ลบเพลงแล้ว")
    d = open('file1.txt', 'r')
    Deletemc = d.read()
    deletemusic = []
    for i in Deletemc:
        if i != ",":
            deletemusic.append(i)
    #read ไฟล์นำค่าไปเก็บที่ Deletmc แล้วpopออก
    #delete โดนการ popออก
    deletemusic.pop()
    delete = ""
    for j in deletemusic:
        delete = delete+j
    if len(AddFrame)>0:
        rm = len(AddFrame)
    elif len(AddFrame)==0:
        rm = len(AddFrame)
    activage = "music%d.txt"%rm
    os.remove(activage)
    AddFrame.pop()
    d = open("file1.txt", "w")
    d.write(delete)

#เพิ่มเพลงโดยการบวก 1 ตัวเข้าไปในไฟล์แล้วจำนวนArrayจะเพิ่มขึ้น
def addframe():
    a = len(AddFrame)+1
    filemusic = "music%d.txt"%a
    AddFrame.append(1)
    
    Notemusic = "%s"%e1.get()
    m = open(filemusic, "w+")
    m.write(Notemusic)
    print("สร้างเพลงแล้ว")
    f = open("file1.txt", "a")
    f.write("1,")

#################################animation button#########################################
def bttn(x,y,img1,img2, cmd):
    image_a = ImageTk.PhotoImage(Image.open(img1))
    image_b = ImageTk.PhotoImage(Image.open(img2))

    def on_enter(e):
        mybtn['image'] = image_b
    
    def on_leave(e):
        mybtn['image'] = image_a

    mybtn = Button(home, image=image_b,border=0,cursor='hand2',command=cmd,relief=SUNKEN)

    mybtn.bind("<Enter>" , on_enter)
    mybtn.bind("<Leave>" , on_leave)
    mybtn.place( x=x,y=y,
    width = 98,
    height = 35)
#########################################สร้างUIเฟรมhome#########################################

def bttns(x,y,img2,text):
    label = Label(home, text=text,bg="#9966FF", fg="white" ,width=30 ,height=4).place(x=98, y=y)

y=120
i=0
#สร้างmusic
for i in range(len(AddFrame)):
    y= y+90
    bttns(300,y,"img9.png","เพลงที่ %s"%(i+1)) #สร้างโดยการลูปอ่านค่าจาก text



#########################################UI########################################
bttn(50,30,"Group6.png","Group7.png", lambda:raise_frame(s1)) #หน้าแรก
bttn(160,30,"Button.png","Button1.png", restart_program) #หน้าแรก

home.config(bg="#1E1E1E")

e2 = Entry(home,
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

e2.place(
    x = 65, y = 120,
    width = 261,
    height = 46)

def on_enter(e):
    mybtn['image'] = image_b   
image_b = ImageTk.PhotoImage(Image.open("img9.png"))
mybtn = Button(home, image=image_b,border=0,cursor='hand2',relief=SUNKEN,highlightthickness = 0,command = play)
mybtn.bind("<Enter>" , on_enter)

mybtn.place( x=279,y=115,
    width = 63,
    height = 58)

img0 = PhotoImage(file = f"img5.png")
b0= Button(home,
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 47, y = 636,
    width = 92,
    height = 69)

img1 = PhotoImage(file = f"img6.png")
b1 = Button(home,
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = deleteframe,
    relief = "flat")

b1.place(
    x = 289, y = 636,
    width = 85,
    height = 69)

img2 = PhotoImage(file = f"img10.png")
b2 = Button(home,
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:raise_frame(home),
    relief = "flat")

b2.place(
    x = 166, y = 633,
    width = 86,
    height = 69)


##################################Slot1#################################


canvas = Canvas(
    s1,
    bg = "#faeeee",
    height = 736,
    width = 420,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = -3, y = 0)

background_img = PhotoImage(file = f"bg.png")
background = canvas.create_image(
    211.0, 368.0,
    image=background_img)



img0_s1 = PhotoImage(file = f"img5.png")
b0_s1 = Button(s1,
    image = img0_s1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0_s1.place(
    x = 47, y = 636,
    width = 92,
    height = 69)

img1_s1 = PhotoImage(file = f"img6.png")
b1_s1 = Button(s1,
    image = img1_s1,
    borderwidth = 0,
    highlightthickness = 0,
    command = deleteframe,
    relief = "flat")

b1_s1.place(
    x = 289, y = 636,
    width = 85,
    height = 69)

img2_s1 = PhotoImage(file = f"img10.png")
b2_s1 = Button(s1,
    image = img2_s1,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:raise_frame(home),
    relief = "flat")

b2_s1.place(
    x = 166, y = 633,
    width = 86,
    height = 69)





e1 = Entry(s1,
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

e1.place(
    x = 73, y = 442,
    width = 261,
    height = 46)

background_img7 = PhotoImage(file = f"Group7.png")

b_s1 = Button(s1,
    image = background_img7,
    borderwidth = 0,
    highlightthickness = 0,
    command = addframe,
    relief = "flat")

b_s1.place(
    x = 170, y = 500,
    width = 70,
    height = 35)
###################################################################
raise_frame(home)
window.resizable(False, False)
window.mainloop()
