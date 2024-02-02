# very nice game
from tkinter import *
import random

# Create the window
window = Tk()
window.title("Lobotomization In porgess")

# Create the canvas
canvas = Canvas(window, width=425, height=450, bg="lightblue")
canvas.pack()

# Set up home screen with title and directions
title = canvas.create_text(200, 200, text="Lobotomizer", fill="grey", font=("Helvetica", 25))
directions = canvas.create_text(200, 300, text="Collect difficulties but avoid the exterm demone", fill="grey", font=("Helvetica", 17))

# Score setup
score = 0
scoreDisp = Label(window, text="Score :" " " + str(score))
scoreDisp.pack()

# Level setup
lvl = 1
lvlDisp = Label(window, text="Level :" " " + str(lvl))
lvlDisp.pack()

# Load the player character image
img = PhotoImage(file = "normal.png")
playerImg = img.subsample(30, 30)

img2 = PhotoImage(file = "auto.png")
auto = img2.subsample(33, 33)

img3 = PhotoImage(file = "easy.png")
easy = img3.subsample(25, 25)

img4 = PhotoImage(file = "hard.png")
hard = img4.subsample(30, 30)

img5 = PhotoImage(file = "harder.png")
harder = img5.subsample(30, 30)

img6 = PhotoImage(file = "insane.png")
insane = img6.subsample(30, 30)

img7 = PhotoImage(file = "extremeDem.png")
extremeDem = img7.subsample(10, 10)




# Create the player character on the canvas
mainChar = canvas.create_image(200, 360, image=playerImg)

#vars + list 4 face
faceList = []
avoidFace = []
faceSpeed = 2
faceImgList = [auto, easy, hard, harder, insane, extremeDem]

def makeFace():
    #random x pos
    xpos = random.randint(1, 400)
    #random color
    faceImg = random.choice(faceImgList)
    #create size 30 face w/ selected col & pos
    face = canvas.create_image(xpos, 0, image = faceImg)
    #add face to list but if extreme add 2 avoidFace
    if faceImg == extremeDem:
        avoidFace.append(face)
        faceList.append(face)
    else:
        faceList.append(face)
    #schedule this func. again
    window.after(1000, makeFace)

#func. moves face down
def moveFace():
    #loop thru list of face
    for face in faceList:
        canvas.move(face, 0, faceSpeed)
        if canvas.coords(face)[1] > 400:
            xpos = random.randint(1, 400)
            canvas.coords(face, xpos, 0)
    window.after(50, moveFace)

def updateScoreLvl():
    global score, lvl, faceSpeed
    score += 1
    scoreDisp.config(text = " Score :" + str(lvl))
    #update lvl + speed
    if score > 5 and score <= 10:
        faceSpeed += 1
        lvl = 2
        lvlDisp.config(text = "Level :" + str(lvl))
    elif score > 10:
        faceSpeed += 1
        lvl = 3
        lvlDisp.config(text = "Level :" + str(lvl))

#func. to destry game
def gameOver():
    window.destroy()

#destroys instruction screen
def endTitle():
    canvas.delete(title)
    canvas.delete(directions)

def collision(item1, item2, dist):
    xDist = abs(canvas.coords(item1)[0] - canvas.coords(item2)[0])
    yDist = abs(canvas.coords(item1)[1] - canvas.coords(item2)[1])
    overlap = xDist < dist and yDist < dist
    return overlap

#checks if char hit avoid face, schedule game over
#if char hits face, remove from screen, list, update score
def checkHits():
    for face in avoidFace:
        if collision(mainChar, face, 30):
            gameOver = canvas.create_text(200, 200, text = "Game Over", fill = "royalblue4", font = ("Helvetica", 25))
            window.after(2000, gameOver) #end game + let user see score
            # dont check any other face, window will be destroyed
            return
    #check if good face hit
    for face in faceList:
        if collision(mainChar, face, 30):
            canvas.delete(face) #remove from canvas
            #find where in list, remove, update score
            faceList.remove(face)
            updateScoreLvl()
    #schedule check hits again
    window.after(100, checkHits)

moveDir = 0 #track which player is moving
def checkInput(event):
    global moveDir
    key = event.keysym
    if key == "Right":
        moveDir = "Right"
    elif key == "Left":
        moveDir = "Left"

#function handles when user stops pressing arrow keys
def endInput(event):
    global moveDir
    moveDir = "None"

#func checks if not on edge and updates x coords based on right/left
def moveChar():
    if moveDir == "Right" and canvas.coords(mainChar)[0] < 400: 
        canvas.move(mainChar, 10, 0)
    if moveDir == "Left" and canvas.coords(mainChar)[0] > 0:
        canvas.move(mainChar, -10, 0)
    window.after(16, moveChar) #move char at 60fps

#bind keys to the char
canvas.bind_all("<KeyPress>", checkInput) #bind keypress
canvas.bind_all("<KeyRelease>", endInput)
window.after(1000, endTitle)
window.after(1000, makeFace)
window.after(1000, moveFace)
window.after(1000, checkHits)
window.after(1000, moveChar)
window.mainloop()