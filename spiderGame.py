# very nice game
from tkinter import *
from PIL import Image, ImageTk  # Import the Image and ImageTk modules from the PIL library
import random

# Create the window
window = Tk()
window.title("Spider Game")

# Create the canvas
canvas = Canvas(window, width=425, height=450, bg="lightblue")
canvas.pack()

# Set up home screen with title and directions
title = canvas.create_text(200, 200, text="Spider Game", fill="grey", font=("Helvetica", 25))
directions = canvas.create_text(200, 300, text="Collect candy but avoid the purple orbs", fill="grey", font=("Helvetica", 17))

# Score setup
score = 0
scoreDisp = Label(window, text="Score :" " " + str(score))
scoreDisp.pack()

# Level setup
lvl = 1
lvlDisp = Label(window, text="Level :" " " + str(lvl))
lvlDisp.pack()

# Load the player character image
playerImg = Image.open("greenChar.gif")
playerImg = playerImg.resize((30, 30), Image.ANTIALIAS)  # Resize the image to 30x30 pixels
playerImg = ImageTk.PhotoImage(playerImg)  # Convert the image to a format that Tkinter can use

# Create the player character on the canvas
mainChar = canvas.create_image(200, 360, image=playerImg)

#vars + list 4 candy
candyList = []
avoidCandy = []
candySpeed = 2
candyColList = ["SeaGreen", "Cyan", "purple4", "DodgeBlue", "hotpink", "gold1", "salmon", "snow", "SpringGreen"]

def makeCandy():
    #random x pos
    xpos = random.randint(1, 400)
    #random color
    candyCol = random.choice(candyColList)
    #create size 30 candy w/ selected col & pos
    candy = canvas.create_oval(xpos, 0, xpos + 30, 30, fill = candyCol)
    #add candy to list but if purple add 2 avoidCandy
    if candyCol == "purple4":
        avoidCandy.append(candy)
    else:
        candyList.append(candy)
    #schedule this func. again
    window.after(1000, makeCandy)

#func. moves candy down
def moveCandy():
    #loop thru list of candy
    for candy in candyList:
        canvas.move(candy, 0, candySpeed)
        if canvas.coords(candy)[1] > 400:
            xpos = random.randint(1, 400)
            canvas.coords(candy, xpos, 0, xpos + 30, 30)
    window.after(50, moveCandy)

def updateScoreLvl():
    global score, lvl, candySpeed
    score += 1
    scoreDisp.config(text = " Score :" + str(lvl))
    #update lvl + speed
    if score > 5 and score <= 10:
        candySpeed += 1
        lvl = 2
        lvlDisp.config(text = "Level :" + str(lvl))
    elif score > 10:
        candySpeed += 1
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

#checks if char hit avoid candy, schedule game over
#if char hits candy, remove from screen, list, update score
def checkHits():
    for candy in avoidCandy:
        if collision(mainChar, candy, 30):
            gameOver = canvas.create_text(200, 200, text = "Game Over", fill = "royalblue4", font = ("Helvetica", 25))
            window.after(2000, gameOver) #end game + let user see score
            # dont check any other candy, window will be destroyed
            return
    #check if good candy hit
    for candy in candyList:
        if collision(mainChar, candy, 30):
            canvas.delete(candy) #remove from canvas
            #find where in list, remove, update score
            candyList.remove(candy)
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
canvas.bind_all("<KeyRelease", endInput)
window.after(1000, endTitle)
window.after(1000, makeCandy)
window.after(1000, moveCandy)
window.after(1000, checkHits)
window.after(1000, moveChar)
window.mainloop()