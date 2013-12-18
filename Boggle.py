# EventsExample1Redux.py

from Graphics import *
from Trie import *
import random
import string
import copy



class BoggleEvents(BoggleGraphics):
###########################################
# Overall Functions
###########################################

    #These functions receive calls from the user and from the run() function
    # in Graphics.py. They then distribute the calls to the other event-handler
    #functions in the following sections. There are 4 states, corresponding to
    # 4 screens in the game: launch, load, game and score. 
    def init(self,root):
        self.state = None
        self.initLaunch(root)

    def mousePressed(self, event):
        if self.state == "launch":
            self.mousePressedLaunch(event)
        elif self.state == "load":
            self.mousePressedLoad(event)
        elif self.state == "game":
            self.mousePressedGame(event)
        elif self.state == "score":
            self.mousePressedScore(event)

    def keyPressed(self, event):
        if self.state == "launch":
            self.keyPressedLaunch(event)
        elif self.state == "load":
            self.keyPressedLoad(event)
        elif self.state == "game":
            self.keyPressedGame(event)
        elif self.state == "score":
            self.keyPressedScore(event)

    def timerFired(self):
        if self.state == "launch":
            self.timerFiredLaunch()
        elif self.state == "load":
            self.timerFiredLoad()
        elif self.state == "game":
            self.timerFiredGame()
        elif self.state == "score":
            self.timerFiredScore()

    #This function calls one of the 4 redrawAll functions located in Graphics.py
    # in the BoggleGraphics superclass.
    def redrawAll(self):
        if self.state == "launch":
            super(BoggleEvents, self).redrawAllLaunch()
        elif self.state == "load":
            super(BoggleEvents, self).redrawAllLoad()
        elif self.state == "game":
            super(BoggleEvents, self).redrawAllGame()
        elif self.state == "score":
            super(BoggleEvents, self).redrawAllScore()

###########################################
# Launch Screen Functions
###########################################

    #Draws background and makes button
    def initLaunch(self,root):
        self.state = "launch"
        self.image = PhotoImage(file="Images/1196914829-721-0.gif")
        self.imageSize = ((self.image.width(), self.image.height()))
        self.drawLaunch() 
        self.playButton = MakeButton(450, 450, 250, 60, "Learn and Play!")


    def mousePressedLaunch(self, event):
        if self.playButton.inside(event.x, event.y):
            self.pressPlay()

    def keyPressedLaunch(self, event):
        pass

    def timerFiredLaunch(self):
        self.title.fill = Color.randomColor()
        
    
    def pressPlay(self):
        self.playButton.buttonClick()
        self.initLoad()

    def mouseInRectangle(self, x0, y0, x1, y1, x, y):
        return x>x0 and x<x1 and y>y0 and y<y1

    def drawLaunch(self):
        self.title1 = Text(452, 204, "BOGGLE")
        self.title1.shadow = False
        self.title1.anchor = "c"
        self.title1.font = "Mistral 105 bold"       
        self.title = Text(450, 200, "BOGGLE")
        self.title.shadow = False
        self.title.anchor = "c"
        self.title.font = "Mistral 105 bold"
        self.subtitle = Text(450, 300, "Go word-search crazy!")
        self.subtitle.shadow = False
        self.subtitle.anchor = "c"
        self.subtitle.font = "Calibri 45 italic"
        self.subtitle1 = Text(451, 302, "Go word-search crazy!")
        self.subtitle1.shadow = False
        self.subtitle1.anchor = "c"
        self.subtitle1.font = "Calibri 45 italic"
        self.subtitle1.fill = Color(255, 255, 255)

###########################################
# Loading Screen Functions
###########################################

    def initLoad(self):
        self.state = "load"
        self.drawBackground()
        self.drawMessage()
        self.drawInstructions()
        self.makeInitButton()
        self.isStartButton = False
        self.transition = False

    #This separate init function refers to the second state that the game is in
    #once the user clicks 'Initialize Game'. In this state, the program creates
    # a random board and solves it.
    def initTransition(self):
        self.transition = True
        self.boardRows = 4
        self.boardCols = 4
        self.letters = self.allLetters()
        self.pieceColor = Color(0, 250, 250)
        self.createBoard()
        self.solutions = []
        self.dic = [w.strip() for w in open('dict.txt')] #loads the dictionary
        self.dicIndexes()
 #       print self.chBoard
        self.solveBoard(self.chBoard)
        self.startButton = MakeButton(450, 550, 100, 70, "Start!")
        self.isStartButton = True


    def mousePressedLoad(self, event):
        if self.isStartButton:
            if self.startButton.inside(event.x, event.y):
                self.pressStart()
        if self.transition == False:
            if self.initializeButton.inside(event.x, event.y):
                self.pressInit()

    def keyPressedLoad(self, event):
        pass

    def timerFiredLoad(self):
        pass
    
    def drawBackground(self):
        self.loadBackground = PhotoImage(file="Images/light-blue.gif")
        self.loadBackgroundSize = ((self.loadBackground.width(),
                                    self.loadBackground.height()))

    def drawMessage(self):
        self.message = Text(450, 65, "   Loading...")
        self.message.anchor = 'c'
        self.message.font = "Ariel_black 50 bold"
        self.subMessage = Text(450, 115, "Please wait!")
        self.subMessage.anchor = 'c'
        self.subMessage.font = "Verdana 23 italic"

    #Help instructions
    def drawInstructions(self):
        info = """
                            ***Please Initialize game!***
    The game is played with a 4X4 board of letters.
    The objective is to form as many words as possible by
    concatenating adjacent letters.
    After 1 minute, your score will be computed.
    To key in words: Type them out on your computer and hit Enter.
    Words must be at least 3 letters long.
    Press 1 for Hint, 2 for Freeze
"""
        self.instructions = Text(50, 140, text=info)
        self.instructions.anchor = "nw"
        self.instructions.font = "Times 30"
        self.instructions.shadowWeight = 0.5

    def pressStart(self):
        self.startButton.buttonClick()
        self.initGame()

    def makeInitButton(self):
        self.initializeButton = MakeButton(450, 550, 100, 70, "Initialize Game")
        self.initializeButton.text.font = "Calibri 15 bold"
        self.initializeButton.fill = Color(250, 100, 50)

    def pressInit(self):
        self.initTransition()
        

###########################################
# Game Screen Functions
###########################################

    def initGame(self):
        self.state = "game"
        self.timerCounter = Text(370, 570, "60")
        self.timerCounter.anchor = 'c'
        self.timerCounter.font = "Verdana 20 bold"
        self.timer = 60.0
        self.boardRows = 4 #
        self.boardCols = 4 #
        self.letters = self.allLetters() #
        self.word = ""
        self.answers = []
        self.wordX = 617
        self.wordY = 70
        self.legalWords = set()
        self.feedback = Text(370, 500, "Start Playing!")
        self.feedback.font = "Times 30"
        self.feedback.anchor = "center"
        self.feedback.fill = Color(0, 0, 255)
        self.score = Text(370, 540, "0")
        self.score.font = "Ariel_black 20"
        self.score.fill = Color(0,0,75)
        self.score.anchor = "center"
        self.QUword = None
        self.letterPoints = self.scrabblePoints()
        self.hints = 3
        self.allHints = set()
        self.hint = Text(800, 40, "hint")
        self.hint.anchor = "c"
        self.dic = [w.strip() for w in open('dict.txt')] #
        self.dicIndexes() #
        threeboard = [["S", "X", "B"],["T","E", "O"],["D","P","U"]] #for testing
        twoboard = [["S","A"],["T","E"]] #for testing purposes.
        self.greenLight = False
        self.hintLocs = []
        self.black = Color(0,0,0)
        self.white = Color(255, 255, 255)
        self.thisTime = None
        self.hitEnter = False
        self.enterCount = 0
        self.makeButtons()
        self.pause = False
        self.isFreeze = False
        self.makePowerups()
        self.presentTime = None
        self.timer2 = 180.0
        self.help = False
        self.helpScreen()
        (self.bLeft, self.bTop, self.bRight, self.bBottom) = (50, 50, 450, 450)
        (self.wLeft, self.wTop, self.wRight, self.wBottom) = (500, 50, 850, 550)
        self.bWidth = self.bHeight = self.bRight-self.bLeft
        self.pWidth = self.bWidth / self.boardRows
        self.wWidth = self.wRight-self.wLeft
        self.wHeight = self.wBottom - self.wTop
        self.wordsInARow = 19
        self.Yincrement = 25
        self.canFreeze = True
        self.helpScreen()



    def mousePressedGame(self, event):
        if self.pauseButton.inside(event.x, event.y):
            self.pause = not self.pause
        elif self.helpButton.inside(event.x, event.y):
            if self.help == False and self.pause == False:
                self.help = self.pause = True
                self.dimButtons()
            elif self.pause == True and self.help == False:
                self.help = True
                self.dimButtons()
            elif self.pause == True and self.help == True:
                self.help = self.pause = False
                self.undimButtons()
        if self.pause == False:
            if self.endButton.inside(event.x, event.y):
                self.gameOver()
            elif self.restartButton.inside(event.x, event.y):
                self.restartGame()
        
    
    def keyPressedGame(self, event):
        #keyPressed only works when the game is not paused.
        if self.pause == False:
            #stores each letter in a string
            if event.keysym in string.ascii_lowercase:
                self.word = self.word + event.keysym 
            elif event.keysym == "BackSpace":
                if len(self.word) > 0:
                    self.word = "" #backspace deletes the whole word
            #Stores the letters keyed in as an answer, and checks if it is a
            #legal solution.
            elif event.keysym == "Return":
                if self.word != "":
                    self.enterCount += 1
                    self.word = self.word.upper()
                    if len(self.answers) > 0:
                        self.wordY = self.answers[-1].y + self.Yincrement
                    self.wordText = Text(self.wordX, self.wordY, self.word)
                    self.answers.append(self.wordText)
                    #automatically scrolls down to show most recent word
                    while self.wordText.y >= 530:
                        for text in self.answers:
                            text.y -= self.Yincrement
                    #Handles exceptional case: QU in the word. (QU is 1 letter)
                    if "QU" in self.word:
                        self.QUword = self.word
                        uIndex = self.word.index("Q") + 1
                        self.word = self.word[:uIndex] + self.word[uIndex+1:]
                    else: self.QUword = None
                    #checks legality of word
                    legal = self.isLegal(self.word)
                    if legal == True:
                        self.addPoints(self.word)
                        self.feedback.text = "Great!"
                        self.legalWords.add(self.word)
                        if len(self.legalWords) == len(self.solutions):
                            self.gameOver()
                        self.wordText.fill = Color(0, 135, 0)
                    elif legal == False:
                        self.feedback.text = "Wrong :("
                        self.reducePoints(self.word)
                        self.wordText.fill = Color(150, 0, 0)
                    elif legal == None:
                        self.feedback.text = "Word has been made!"
                    elif legal == "too short":
                        self.feedback.text = "At least 3 letters!"
                    self.word = ""
                    if self.thisTime != None: self.hitEnter = True
            #Powerups!
            elif event.keysym == '1':
                self.generateHint()
            elif event.keysym == "2":
                if self.canFreeze == True:
                    self.freezeGame()
                    self.canFreeze = False
            #scroll controls
            elif event.keysym == "Up":
                if len(self.answers)>0 and self.answers[0].y < 70:
                    for text in self.answers:
                        text.y += self.Yincrement
            elif event.keysym == "Down":
                for text in self.answers:
                    text.y -= self.Yincrement

    
    def timerFiredGame(self):
        #Timerfired only works when the game is not paused
        if self.pause == False:
            self.timer2 -= 0.25
            if self.isFreeze: #unfreezes the game after 4 seconds
                if self.presentTime - self.timer2 > 4:
                    self.isFreeze = False
                self.boardBox.line = self.wordBox.line = Color.randomColor()
                return
            if self.timer>0:
                self.timer -= 0.25
                self.timerCounter.text = str(int(self.timer))           
            elif self.timer<=0: self.gameOver() 
            if self.greenLight: #Turns pieces back into their original color
                #after 0.5seconds when the user enters a correct answer
                if self.currentTime - self.timer > 0.5:
                    for row in xrange(self.boardRows):
                        for piece in self.board[row]:
                            piece.fill = self.pieceColor
                            piece.line = self.pieceColor
                            piece.lineWidth = 1
                            piece.ch.fill = Color(0,0,0)
                            piece.ch.shadowFill = "white"
                            self.greenLight = False
            #handles animation for the Hint powerup
            if self.thisTime != None:
                if self.thisTime - self.timer > 4 or self.hitEnter == True:
                    for row in xrange(self.boardRows):
                        for piece in self.board[row]:
                            piece.fill = self.pieceColor
                            piece.lineWidth = 1
                            piece.ch.fill = Color(0,0,0)
                            piece.ch.shadowFill = "white"
                    self.thisTime = None
                    self.hitEnter = False

    #Dims other buttons when help screen is clicked.
    def dimButtons(self):
        dimColor = Color(200, 255, 200)
        self.pauseButton.fill = dimColor
        self.endButton.fill = dimColor
        self.restartButton.fill = dimColor

    #undims the buttons after help screen is closed
    def undimButtons(self):
        normalColor = Color(0, 200, 50)
        self.pauseButton.fill = normalColor
        self.endButton.fill = normalColor
        self.restartButton.fill = normalColor

    #Loads help screen 
    def helpScreen(self):
        self.helpRectangle = Rectangle(50, 50, 850, 450)
        self.helpRectangle.fill = Color(230,230,230)
        info = """
    The game is played with a 4X4 board of letters.
    The objective is to form as many words as possible by
    concatenating adjacent letters.
    After 1 minute, your score will be computed.
    To key in words: Type them out on your computer and hit Enter.
    Words must be at least 3 letters long.
    Press 1 for Hint, 2 for Freeze
"""
        cx = 450
        cy = 250
        self.helpRectangleText = Text(cx, cy, info)
        self.helpRectangleText.font = "Times 30"
        self.helpRectangleText.anchor = "c"
        self.helpRectangleText.shadowWeight = 0.5

    #initializes the powerup bar
    def makePowerups(self):
        self.hintBar = MakeButton(535, 570, 70, 40, "Hints: 3")
        self.hintBar.text.font = "Calibri 15 bold"
        self.hintBar.fill = Color(200, 200, 250)
        self.freezeBar = MakeButton(615, 570, 70, 40, "Freeze")
        self.freezeBar.text.font = "Calibri 15 bold"
        self.freezeBar.fill = Color(200, 200, 250)
        self.hintBarText = Text(535, 576, "Press '1'")
        self.hintBarText.font = "Calibri 11 bold"
        self.hintBarText.anchor = 'n'
        self.freezeBarText = Text(615, 576, "Press '2'")
        self.freezeBarText.font = "Calibri 11 bold"
        self.freezeBarText.anchor = 'n'
        self.powerups = Text(760, 570, "<-- Powerups")
        self.powerups.font = "Verdana 25"
        self.powerups.fill = Color(250, 50, 50)

    #Game over. takes the game to the end of game screen.
    def gameOver(self):
        self.initHighscore()
        self.feedback.text = "Game Over!"
        currentScore = int(self.score.text)
        self.score.text = "Your Score Is: %d" % (currentScore)
        
    
    def restartGame(self):
        self.initLoad()

    #powerup: freeze
    def freezeGame(self):
        self.isFreeze = True
        self.presentTime = self.timer2
        
    #Makes the 4 buttons on the bottom left of the screen
    def makeButtons(self):
        self.endButton = MakeButton(60, 500, 100, 50, "End Game")
        self.endButton.text.font = "Calibri 20 bold"
        self.restartButton = MakeButton(60, 560, 100, 50, "Restart")
        self.restartButton.text.font = "Calibri 20 bold"
        self.pauseButton = MakeButton(170, 560, 100, 50, "Pause")
        self.pauseButton.text.font = "Calibri 20 bold"
        self.helpButton = MakeButton(170, 500, 100, 50, "Help")
        self.helpButton.text.font = "Calibri 20 bold"
        
    #Determines indices of words that start with a particular letter in the
    #dictionary. This makes searching through the large dictionary much faster.
    def dicIndexes(self):
        dicIndex = {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,
                    'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,
                    'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}
        for ch in dicIndex:
            dicIndex[ch] = self.dic.index(ch)
        self.dicIndex = dicIndex

    #Iterates through every starting piece on the board and calls solvePiece to
    #solve the board.
    def solveBoard(self, board):
        solution = []
        (rows,cols) = (len(board),len(board[0]))
        for startingRow in xrange(rows):
            for startingCol in xrange(cols):
                solution.extend(self.solvePiece(board,startingRow,startingCol,
                    board[startingRow][startingCol],[]))
        self.solutions = self.removeDuplicates(solution)

    #Solves the board recursively by going through every possibility until
    #the string of letters formed is not a prefix.
    def solvePiece(self,board,row,col,wordSoFar,prevLoc,depth=0):
        (rows,cols) = (len(board),len(board[0]))
        if len(wordSoFar)>1 and T.isPrefix(wordSoFar.lower())==False: #base case
            return [Solution(wordSoFar.upper(),prevLoc+[(row,col)])]
        else: #recursive case
            solutions = []
            #checks if current word is a solution
            if len(wordSoFar)>2 and T.lookup(wordSoFar.lower()) == True:
                solutions.append(Solution(wordSoFar.upper(),prevLoc+[(row,col)]))
            #for each of the next locations it can go to from this current
            # piece (up to 9), it recursively calls itself.
            for drow in [-1,0,1]:
                for dcol in [-1,0,1]:
                    (newR,newC)=(row+drow,col+dcol)
                    if newR>=0 and newR<rows and newC>=0 and newC<cols and \
                      (newR,newC)!=(row,col) and (newR,newC)\
                      not in prevLoc:
                        if T.isPrefix((wordSoFar+board[newR][newC]).lower()):
                            prevLocCopy = list(prevLoc)
                            prevLocCopy.append((row,col))
                            solutions.extend(self.solvePiece(board,newR,newC,\
                            wordSoFar+board[newR][newC],prevLocCopy,depth+1))
            return solutions

    #removes any duplicate solutions that may arise.
    def removeDuplicates(self, a):
        i = 0
        while i < len(a):
            if a.count(a[i]) > 1:
                a.pop(i)
                i -= 1
            i += 1
        return a

    #Helps with the base case: determines whether or not the current string of
    #letters given is a prefix for any word in the dictionary. If it is, the
    #recursive function will continue, as there is a possibility that this path
    #will lead to a solution.
    def isPrefix(self,word):
        index = self.dicIndex[word[0]]
        if word[0] == "z":
            lastIndex = self.dic.index(self.dic[-1])
        else:
            lastIndex = self.dicIndex[chr(ord(word[0])+1)]
        for element in self.dic[index:lastIndex]:
            if element.startswith(word):
                if self.allCharactersExist(element):
                    return True
        return False

    def startsWith(self, s, word):
        if s.startswith(word):
            return True
        else:
            return False

    def allCharactersExist(self, s):
        #all characters in s exist on the board
        if len(s) > self.boardRows*self.boardCols: return False
        for ch in s[::-1]:
            if ch not in self.listOfLetters:
                return False
        return True

    #Dictionary to define the points system used.
    def scrabblePoints(self):
        return {'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,
                'J':8,'K':5,'L':1,'M':3,'N':1,'O':1,'P':3,'Q':10,'R':1,
                'S':1,'T':1,'U':1,'V':4,'W':4,'X':8,'Y':4,'Z':10}

    #reads the dictionary
    def wordReader(self, filename):
        return (word.strip() for word in open(filename))

    #adds points for a  correct word
    def addPoints(self, word):
        n = len(word)
        if self.QUword != None: n += 1
        points = 0
        for letter in word:
            points += self.letterPoints.get(letter)
        lengthPoints = max(0,n-4)*3
        self.score.text = str(int(self.score.text) + points + lengthPoints)

    #Deducts 5 points for every wrong word
    def reducePoints(self, word):
        self.score.text = str(int(self.score.text) - 5)

    #Generates a random hint from the list of solutions that has not already
    #been made by the user.
    def generateHint(self):
        if self.hints <= 0: return
        word = self.solutions[random.randint(0,len(self.solutions)-1)]
        while word.word in self.legalWords: 
            word = self.solutions[random.randint(0,len(self.solutions)-1)]
        self.hint.text = word.word
        self.allHints.add(word.word)
        for row in xrange(self.boardRows):
            for piece in self.board[row]:
                piece.fill = self.black
                piece.ch.fill = self.white
                piece.ch.shadowFill = "black"
                piece.lineWidth = 8
        for loc in word.locations:
            for row in xrange(self.boardRows):
                for piece in self.board[row]:
                    if loc == piece.location:
                        self.hintLocs.append(piece) 
        self.hints -= 1
        self.hintBar.text.text = "Hints: %d" % (self.hints)

    #Controls the animation for hint generation.
    def resetAfter5(self):
        self.thisTime = self.timer

    #This function generates a random string of letters that exists on the board
    #. For testing purposes. Not used in gameplay.
    def randomWord(self, puzzle):
        (rows, cols) = (len(puzzle), len(puzzle[0]))
        startR = thisR = random.randint(0,3)
        startC = thisC = random.randint(0,3)
        (prevR, prevC) = (None, None)
        wordLength = random.randint(3,5)
        dRowCol = []
        while len(dRowCol) < wordLength-1:
            newR = thisR + random.randint(-1,1)
            newC = thisC + random.randint(-1,1)
            if newR>=0 and newR<rows and newC>=0 and newC<cols and (newR,newC)\
               != (thisR,thisC) and (newR,newC)!=(prevR,prevC):
                dRowCol.append((newR,newC))
                (prevR,prevC) = (thisR,thisC)
                (thisR,thisC) = (newR,newC)
        word = puzzle[startR][startC]
        for i in xrange(len(dRowCol)):
            word += puzzle[dRowCol[i][0]][dRowCol[i][1]]
        return word

    #creates a random board.
    def createBoard(self):
        board = [[""]*self.boardCols for row in xrange(self.boardRows)]
        chBoard = [[""]*self.boardCols for row in xrange(self.boardRows)]
#        chBoard = [['I', 'M', 'W', 'I'], ['B', 'T', 'O', 'QU'],\
#         ['A', 'Z', 'N', 'P'], ['L', 'H', 'U', 'T']]
        listOfLetters = []
        for row in xrange(self.boardRows):
            for col in xrange(self.boardCols):
                ch = self.letters[random.randint(0,len(self.letters)-1)]
 #               ch = chBoard[row][col]
                if ch=="Q": ch = "QU"
                if ch == 'QU':
                    listOfLetters.extend(['q','u'])
                else:
                    listOfLetters.append(ch.lower())
                chBoard[row][col] = ch
                board[row][col] = Piece(row, col, ch)
                board[row][col].fill = self.pieceColor
                board[row][col].line = self.pieceColor
        self.board = board
        self.chBoard = chBoard
        self.listOfLetters = listOfLetters

    #draws the random board.
    def drawBoard(self):
        (self.bLeft, self.bTop, self.bRight, self.bBottom) = (50, 50, 450, 450)
        (self.wLeft, self.wTop, self.wRight, self.wBottom) = (500, 50, 735, 550)
        self.bWidth = self.bHeight = self.bRight-self.bLeft
        self.pWidth = self.bWidth / self.boardRows
        self.wWidth = self.wRight-self.wLeft
        self.wHeight = self.wBottom - self.wTop
        self.wordsInARow = 19
        self.Yincrement = 25
        self.boardBox = self.createRectangle(self.bLeft, self.bTop,
                                             self.bRight, self.bBottom)
        self.boardBox.lineWidth = 10
        self.boardBox.line = Color(200, 255, 150)
        self.wordBox = self.createRectangle(self.wLeft, self.wTop,
                                            self.wRight, self.wBottom)
        self.wordBox.lineWidth = 8
        self.wordBox.line = Color(255, 200, 150)
        for x in xrange(1,self.wordsInARow):
            self.wLine1 = self.createLine(self.wLeft,self.wTop+10+x*self.Yincrement
                                    ,self.wRight,self.wTop+10+x*self.Yincrement)
            self.wLine1.fill = Color(255, 200, 150)
        self.createScrollbar()

    #draws the scroll bar.
    def createScrollbar(self):
        self.scrollOutline = self.createRectangle(self.wRight+4, self.wTop,
                                                  self.wRight+24, self.wBottom)
        self.scrollOutline.fill = Color(200, 255, 150)
        self.scrollTop = self.createTriangle(self.wRight+14, self.wTop,
                    self.wRight+24, self.wTop+20,self.wRight+4, self.wTop+20)
        self.scrollTop.line = Color(255, 200, 150)
        self.scrollBottom = self.createTriangle(self.wRight+14, self.wBottom,
                self.wRight+24, self.wBottom-20,self.wRight+4, self.wBottom-20)
        self.scrollBottom.line = Color(255, 200, 150)

    #stores the frequency of letters in a dictionary so that more common letters
    #appear more frequently ont he board.
    def allLetters(self):
        letterFreq = {'A':9,'B':2,'C':2,'D':4,'E':12,'F':2,'G':3,'H':2,'I':9,
                      'J':1,'K':1,'L':4,'M':2,'N':6,'O':8,'P':2,'Q':1,'R':6,
                      'S':4,'T':6,'U':4,'V':2,'W':2,'X':1,'Y':2,'Z':1}
        letters = ""
        for letter in xrange(26):
            for freq in xrange(letterFreq[chr(ord("A")+letter)]):
                letters = letters + chr(ord("A")+letter)
        return letters
        
    def isLegal(self, word):
        # A word is legal if: 
        # 1 - it has 3 or more characters
        # 2 - it has not already been made by the player.
        # 3 - it is in self.solutions
        if len(word) < 3: return "too short"
        if word in self.legalWords: #it has been made before 
            return None
        for solution in self.solutions: 
            if self.QUword != None:
                word = self.QUword
            if word == solution.word:
                self.lightUpGreen(solution)
                return True
        return False

    #lights up the pieces green when a correct word is made.
    def lightUpGreen(self, solution):
        for row in xrange(self.boardRows):
            for piece in self.board[row]:
                if piece.location in solution.locations:
                    self.greenLight = True
                    piece.fill = Color(0, 255, 0)
                    piece.line = Color(0, 255, 0)
                    piece.lineWidth = 8
        self.currentTime = self.timer
        


###########################################
# End-Of-Game Screen Functions
###########################################

    def initHighscore(self):
        self.state = "score"
        self.presentSolutions()

    #controls actions when user clicks on each solution.
    def mousePressedScore(self, event):
        if self.restartButton.inside(event.x, event.y):
            self.restartGame()
        elif self.wordBox.inside(event.x, event.y):
            for solution in self.solutions:
                if solution.wordText.y > 50 and solution.wordText.y < 530:
                    if solution.wordText.inside(event.x, event.y):
                        self.lightUpSolutionsGreen(solution)
                        self.showPoints(solution)
        

    def keyPressedScore(self, event):
        if event.keysym == "Up":
            if self.solutions[0].wordText.y < 70:
                for solution in self.solutions:
                    solution.wordText.y += self.Yincrement
        elif event.keysym == "Down":
            for solution in self.solutions:
                solution.wordText.y -= self.Yincrement

    def timerFiredScore(self):
        pass

    #loads solutions onto the same word box that the user keyed answers into
    #previously
    def presentSolutions(self):
        yTop = 70
        i = 0
        for solution in self.solutions:
            solution.wordText = Text(617, yTop+i*self.Yincrement, solution.word)
 #           solution.wordText.anchor = 'c'
            i += 1
            if solution.wordText in self.answers:
                solution.wordText.fill = Color(0, 255, 0)
            
    #lights up solutions when the user clicks on a solution
    def lightUpSolutionsGreen(self, solution):
        for row in xrange(self.boardRows):
            for piece in self.board[row]:
                if piece.location in solution.locations:
                    piece.fill = Color(0, 255, 0)
                    piece.line = Color(0, 255, 0)
                    piece.lineWidth = 8
                else:
                    piece.fill = self.pieceColor
                    piece.line = self.pieceColor
                    piece.lineWidth = 1

    #calculates the points of a word that the user clicks on.
    def showPoints(self, solution):
        word = solution.wordText.text
        n = len(word)
        points = 0
        for letter in word:
            points += self.letterPoints.get(letter)
        lengthPoints = max(0,n-4)*3
        totalPoints = points + lengthPoints
        self.solutionPoints = Text(solution.wordText.x+145, solution.wordText.y
                                   , "Points = %d" % (totalPoints))
        self.solutionPoints.anchor = 'w'



app = BoggleEvents()
app.run(900,600)
