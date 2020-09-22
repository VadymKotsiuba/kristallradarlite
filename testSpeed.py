import serial
import time
from tkinter import *
from PIL import *
from PIL import Image
from PIL import ImageTk
from PIL import ImageFont
from PIL import ImageDraw

#constants
digit_width = 18
screen_width = 64;
y_shift = -8

serial_port = '/dev/ttyUSB0'
serial_speed = 9600

font_name = "/home/pi/scripts/MachineBT.ttf"
#font_name = "/home/pi/scripts/radarfont.ttf"
font_size = 40

myColor = 'black'
myX = 0
myY = 0

#variables
speedValue = 84
data = [0,0,0,0]
logNoData = False

def setColor(color):#string
    global myColor
    myColor = color

def setPosition(x_pos,y_pos):
    global myX
    global myY
    myX = x_pos
    myY = y_pos

def exitProgram(event):
    COMport.close()
    exit()

def checkSpeed():
    if 0<speedValue<=50:
        setColor('green')
       #setColor('#00af00')
    elif speedValue>50:
        setColor('red')
    else:
        setColor('blue')
    if 0<=speedValue<10:
       setPosition((screen_width - digit_width)/2, y_shift)
    elif 10<=speedValue<100:
       setPosition((screen_width/2)-(42/2)+3, y_shift)
    else:
       setPosition(0+4, y_shift)

def updateImage():
    global myImg
    toolDraw.rectangle([0,0,buffer.width-1,buffer.height-1], fill='black')
    toolDraw.text((myX,myY), str(speedValue), font=myFont, fill=myColor)
    pixels = buffer.load();
    for y in range(4):
        for x in range(64):
            pixels[x,y], pixels[x,y+4] = pixels[x,y+4], pixels[x,y]
            pixels[x,y+8], pixels[x,y+8+4] = pixels[x,y+8+4], pixels[x,y+8]
            pixels[x,y+16], pixels[x,y+16+4] = pixels[x,y+16+4], pixels[x,y+16]
            pixels[x,y+24], pixels[x,y+24+4] = pixels[x,y+24+4], pixels[x,y+24]
    myImg = ImageTk.PhotoImage(buffer)
    myLabel.config(image=myImg)
    myLabel.image = myImg

def readData():
    global data
    global speedValue
    global logNoData
    if COMport.is_open:
        if COMport.in_waiting >= 4:
            data = COMport.read(4)
            if data[0] == 252 and data[1] == 250:
                if data[3] == 0:
                    speedValue = data[2]
                    logNoData = False
                else:
                    speedValue = 0
        else:
            if logNoData == False:
                time.sleep(1.5)
                if COMport.in_waiting == 0:
                    speedValue = 0
                    logNoData = True
    if speedValue < 10:
        speedValue = 0
    if speedValue > 199:
        speedValue = 199
    #comLabel.config(text = str(data[0])+' '+str(data[1])+' '+str(data[2])+' '+str(data[3]))

#Init
#COMport = serial.Serial(serial_port, serial_speed, timeout = 1)
#COMport.close()
#COMport.open()

GUI = Tk()
GUI.title('Radar v0.1.1')
GUI.overrideredirect(True)
GUI.resizable(False, False)
GUI.geometry('64x32+500+400')
GUI.configure(bg='black')
GUI.bind('<Escape>', exitProgram)
#GUI.bind('<T>', testShow)

#myFont = ImageFont.truetype("Segment7Standard.otf", 36)
myFont = ImageFont.truetype(font_name,font_size)

buffer = Image.new("RGB", (64,32), "black")
toolDraw = ImageDraw.Draw(buffer)
toolDraw.text((0,0), str(speedValue), font=myFont, fill='black')

myImg = ImageTk.PhotoImage(buffer)

myLabel = Label(GUI, image=myImg)
myLabel.image = myImg
myLabel.place(x = -1, y = -1)


dataFile = open("/home/pi/scripts/started.txt", "r")
countStart = int(dataFile.readline())
dataFile.close()

countStart+=1

dataFile = open("/home/pi/scripts/started.txt", "w")
dataFile.write(str(countStart))
dataFile.close()

#comLabel = Label(GUI, text = str(data), bg = 'black', fg = 'white', font = 'arial 14')
#comLabel.place(x=0, y=0)
#Init


while 1:
    #readData()
    for i in range(200):
        speedValue = i
        time.sleep(1)
        checkSpeed()
        updateImage()
        GUI.update_idletasks()
        GUI.update()
