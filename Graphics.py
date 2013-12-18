#Boggle!!
#Graphics.py
#This document is based off of the notes on classes on
#http://www.kosbie.net/cmu/fall-12/15-112/ in the file Animation.py

from Tkinter import *
import random


class Animation(object):
    def mousePressed(self,event): pass
    def keyPressed(self,event): pass
    def timerFired(self): pass
    def redrawAll(self): pass
    def init(self):
        pass

    def run(self, width=300, height=300):
        #set up root and canvas
        global root
        root = Tk()
        root.resizable(width=FALSE, height=FALSE)
        self.width = width
        self.height = height
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack()
        #set up events
        def redrawAllWrapper():
            self.canvas.delete(ALL)
            self.redrawAll()
        def mousePressedWrapper(event):
            self.mousePressed(event)
            redrawAllWrapper()
        def keyPressedWrapper(event):
            self.keyPressed(event)
            redrawAllWrapper()
        root.bind("<Button-1>", mousePressedWrapper)
        root.bind("<Key>", keyPressedWrapper)
        #set up timerFired events
        self.timerFiredDelay = 250 #milliseconds
        def timerFiredWrapper():
            self.timerFired()
            redrawAllWrapper()
            self.canvas.after(self.timerFiredDelay,timerFiredWrapper)
        #run init and timerFired
        self.init(root)
        timerFiredWrapper()
        #launch the app
        root.mainloop()


class Color(object):
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    @classmethod
    def randomColor(cls):
        r = random.randrange(256)
        g = random.randrange(256)
        b = random.randrange(256)
        return Color(r, g, b)

    def rgbString(self):
        return "#%02x%02x%02x" % (self.red, self.green, self.blue)

    def __eq__(self,other):
        return (self.red==other.red) and (self.green==other.green) and \
               (self.blue==other.blue)

class Shape(object):
    def __init__(self, left, top, right, bottom):
        #print left, top, right, bottom
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.fill = None
        self.line = Color(0, 0, 0)
        self.lineWidth = 1
    
    def getFill(self):
        try:
            self.fill == None
            return None if (self.fill == None) else self.fill.rgbString()
        except:
            return self.fill.rgbString()
        
    def getLine(self):
        try:
            self.line == None
            return None if (self.line == None) else self.line.rgbString()
        except:
            return self.line.rgbString()

class Rectangle(Shape):
    def draw(self, canvas):
        canvas.create_rectangle(self.left, self.top, self.right, self.bottom,
                                fill=self.getFill(),
                                outline=self.getLine(), width=self.lineWidth)

    def inside(self, x,y):
        return x>self.left and x<self.right and y>self.top and y<self.bottom

class Triangle(Shape):
    def __init__(self, x0,y0,x1,y1,x2,y2):
        (self.x0,self.y0,self.x1,self.y1,self.x2,self.y2) = (x0,y0,x1,y1,x2,y2)
        # Call superclass's __init__ method
        super(Triangle, self).__init__(0, 0, 0, 0)

    def draw(self, canvas):
        canvas.create_polygon(self.x0,self.y0,self.x1,self.y1,self.x2,self.y2,
                              fill=self.getFill(),outline=self.getLine(),
                              width=self.lineWidth)

class Oval(Shape):       
    def draw(self, canvas):
        m = 10
        canvas.create_oval(self.left+m, self.top+m, self.right-m, self.bottom-m,
                           fill=self.getFill(),
                           outline=self.getLine(), width=self.lineWidth)

class Line(Shape):
    def draw(self, canvas):
        canvas.create_line(self.left, self.top, self.right, self.bottom,
                           fill=self.getFill(), width=self.lineWidth)

class Circle(Oval):
    def __init__(self, cx, cy, r):
        (left, top, right, bottom) = (cx-r, cy-r, cx+r, cy+r)
        # Call superclass's __init__ method
        super(Circle, self).__init__(left, top, right, bottom)


class Text(Shape):
    def __init__(self, x, y, text):
        (self.x, self.y, self.text) = (x, y, text)
        self.anchor = "c"
        self.font = "Verdana 20"
        self.shadow = True
        self.shadowWeight = 2
        self.shadowFill = "white"
        super(Text, self).__init__(x, y-10, x+50, y+10)

    def draw(self, canvas):
        if self.shadow:
            i = self.shadowWeight
            canvas.create_text(self.x+i, self.y+i, text=self.text,
                    font=self.font,fill=self.shadowFill, anchor=self.anchor)
        canvas.create_text(self.x, self.y, text=self.text, font=self.font,
                           fill=self.getFill(), anchor=self.anchor)

    def __eq__(self,other):
        return (self.text == other.text)

    def __repr__(self):
        string = "Text(%d, %d, %s)" % (self.x, self.y, self.text)

    def inside(self,x,y):
        return x>500 and x<735 and y>(self.y-10) and y<(self.y+10)


#sets up instances for each of the shape classes above, and houses the redrawAll
#funcitons for each state of the game.
class BoggleGraphics(Animation):
    def __init__(self):
        self.shapes = [ ]

    def addShape(self, shape):
        self.shapes.append(shape)
        return shape

    def createTriangle(self, x0,y0,x1,y1,x2,y2):
        return self.addShape(Triangle(x0,y0,x1,y1,x2,y2))

    def createRectangle(self, left, top, right, bottom):
        return self.addShape(Rectangle(left, top, right, bottom))

    def createLine(self, x0, y0, x1, y1):
        return self.addShape(Line(x0, y0, x1, y1))

    def createOval(self, left, top, right, bottom):
        return self.addShape(Oval(left, top, right, bottom))

    def createCircle(self, cx, cy, r):
        return self.addShape(Circle(cx, cy, r))

    def createPiece(self, row, col, ch):
        return self.addShape(Piece(row, col, ch))

    def redrawAllScore(self):
        self.canvas.create_image(0,0,anchor=NW, image=self.loadBackground)
        for shape in self.shapes:
            shape.draw(self.canvas)
        for row in xrange(self.boardRows):
            for piece in self.board[row]:
                piece.draw(self.canvas)
        for solution in self.solutions:
            if solution.wordText.y > 50 and solution.wordText.y < 530:
                solution.wordText.draw(self.canvas)
        try:
            self.solutionPoints.draw(self.canvas)
        except:
            pass
        self.feedback.draw(self.canvas)
        self.score.draw(self.canvas)
        self.restartButton.draw(self.canvas)
        self.drawBoard()

    def redrawAllGame(self):
        self.canvas.create_image(0,0,anchor=NW, image=self.loadBackground)
        for shape in self.shapes:
            shape.draw(self.canvas)
        for row in xrange(self.boardRows):
            for piece in self.board[row]:
                piece.draw(self.canvas)
        if len(self.hintLocs) > 0:
            allHintsFilled = True
            for piece in self.hintLocs:
                if piece.fill == Color(0,0,0):
                    piece.fill = Color(255, 0, 0)
                    piece.ch.fill = Color(0,0,175)
                    allHintsFilled = False
                    break
            if allHintsFilled:
                self.resetAfter5()
                self.hintLocs = []
        #only draws text if it is inside the word box. to control the scrollbar.
        for text in self.answers:
            if text.y > 50 and text.y < 530:
                text.draw(self.canvas)
        if self.pause:
            self.canvas.create_rectangle(self.bLeft, self.bTop,
                        self.bRight, self.bBottom, fill = "maroon")
            self.canvas.create_rectangle(self.wLeft, self.wTop,
                        self.wRight, self.wBottom, fill = "maroon")
            self.canvas.create_text(self.bLeft+self.bWidth/2, self.bTop+
            self.bHeight/2,font="Ariel_black 40 bold", text="Paused",anchor='c')
        self.score.draw(self.canvas)
        self.feedback.draw(self.canvas)
        self.endButton.draw(self.canvas)
        self.restartButton.draw(self.canvas)
        self.timerCounter.draw(self.canvas)
        self.pauseButton.draw(self.canvas)
        self.helpButton.draw(self.canvas)
        self.hintBar.draw(self.canvas)
        self.freezeBar.draw(self.canvas)
        self.hintBarText.draw(self.canvas)
        self.freezeBarText.draw(self.canvas)
        self.powerups.draw(self.canvas)
        self.drawBoard()
        if self.help:
            self.drawTheHelpScreen()
            
    def drawTheHelpScreen(self):
        self.helpRectangle.draw(self.canvas)
        self.helpRectangleText.draw(self.canvas)

    def redrawAllLaunch(self):
        for row in xrange(2):
            for col in xrange(3):
                self.canvas.create_image(348*col,311*row,anchor=NW,
                                         image=self.image)
        self.title1.draw(self.canvas)
        self.title.draw(self.canvas)
        self.subtitle1.draw(self.canvas)
        self.subtitle.draw(self.canvas)
        self.playButton.draw(self.canvas)
        
    def redrawAllLoad(self):
        self.canvas.create_image(0,0,anchor=NW, image=self.loadBackground)
        self.message.draw(self.canvas)
        self.subMessage.draw(self.canvas)
        self.instructions.draw(self.canvas)
        if self.transition == False:
            self.initializeButton.draw(self.canvas)
        try:
            if self.isStartButton:
                self.startButton.draw(self.canvas)
        except:
            pass

class Piece(Oval):
    def __init__(self, row, col, ch):
        (self.bLeft, self.bTop, self.bRight, self.bBottom) = (50, 50, 450, 450)
        self.boardRows = 4
        self.row = row
        self.col = col
        self.location = Location(row, col, ch)
        self.bWidth = self.bHeight = self.bRight-self.bLeft
        self.pWidth = self.bWidth / self.boardRows
        super(Piece, self).__init__(self.bLeft+col*self.pWidth, self.bTop+row*\
                                self.pWidth, self.bLeft+(col+1)*self.pWidth, \
                                    self.bTop+(row+1)*self.pWidth)
        (self.cx, self.cy) = (self.left+self.pWidth/2, self.top+self.pWidth/2)
        self.ch = Text(self.cx, self.cy, ch)
        self.ch.font = "Helvetica 40"
        self.ch.anchor = 'c'
    


    def __repr__(self):
        string = "Piece(%d, %d, %s)" % (self.row, self.col, self.ch)
        return string

    def draw(self, canvas):
        super(Piece, self).draw(canvas)
        self.ch.draw(canvas)

    def __eq__(self, other):
        return (self.row==other.row) and (self.col==other.col)


class Location(object):
    def __init__(self, row, col, ch):
        self.row = row
        self.col = col
        self.ch = ch

    def __repr__(self):
        return "Location(%r, %r, %r)" % (self.row, self.col, self.ch)

    def __eq__(self, other):
        return (self.row == other.row) and (self.col == other.col)
    
class Solution(object):
    def __init__(self, word, locations):
        self.word = word
        self.locations = []
        for ch in xrange(len(locations)):
            self.locations.append(Location(locations[ch][0], locations[ch][1],
                                           word[ch]))

    def __eq__(self, other):
        return (self.word == other.word)

    def __repr__(self):
        return "Solution(%r)" % (self.word)
        

class MakeButton(BoggleGraphics):
    def __init__(self, x, y, width, height, text):
        self.x0 = x-width/2
        self.y0 = y-height/2
        self.x1 = x+width/2
        self.y1 = y+height/2
        (self.width, self.height) = (width, height)
        self.text = Text(x, y, text)
        self.text.shadowWeight = 1
        self.text.font = "Calibri 35 bold"
        self.text.anchor = "c"
        self.click = False
        self.fill = Color(0, 200, 50)
        self.width = 3

    def getFill(self):
        try:
            self.fill == None
            return None if (self.fill == None) else self.fill.rgbString()
        except:
            return self.fill.rgbString()
        
    def inside(self, x, y):
        return x>self.x0 and x<self.x1 and y>self.y0 and y<self.y1

    def draw(self, canvas):
        if self.click:
            canvas.create_rectangle(self.x0+2, self.y0+2, self.x1+2, self.y1+2,
                                    fill=self.getFill(),width=self.width)
            self.click = False
        else:
            canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1,
                                    fill=self.getFill(),width=self.width)
        self.text.draw(canvas)
        pass

    def buttonClick(self):
        self.click = True
        

    def buttonPressed(self):
        print "button pressed!"


        
