import json
import os
import time
import OthelloBestMove

class OthelloBot:

    def __init__(self, location, name):

        self.player = 0
        self.opponent = 0
        self.boardGrid=[]
        self.data = {}
        self.inviteData = {}
        self.totalCounters = "" 
        self.gameFile = ""
        self.moveFile = ""
        self.gameLocation = location
        self.playerName = name
        self.turnNumber = -1

    def nextMove(self, data):
         
        if self.player == 0:
            if data["whitePlayer"] == self.playerName:
                self.player = 1
                self.playerName = "White"
                self.opponent = 2
            else:
                self.player = 2
                self.playerName = "Black"
                self.opponent = 1

        if data["turnsSoFar"] == self.turnNumber:
            return ""

        self.turnNumber = data["turnsSoFar"]
        return data["nextMove"]

    def checkforFile(self, file): 
        checks = 0

        while checks < 30:
            if os.path.isfile(file):
                return True
            checks += 1
            print("Waiting for " + file)
            time.sleep(5)
        
        return False 

    def othelloBot(self, requestGUID):  
        
        invite = self.gameLocation + "invite-" + requestGUID + ".json"
        
        startGame = self.checkforFile(invite)
        
        #startGame = True
        gameInPlay = True
     
        if startGame == True:
        
            with open(invite) as f:
                self.inviteData = json.load(f) 
            self.gameFile
            #with open(invite) as f:
            #    self.inviteData = json.load(f) 
            #self.gameFile


            #self.gameFile = self.gameLocation + "game-" + "1ef383f4-0196-11eb-a512-005056bb84e6" + "\\game-1ef383f4-0196-11eb-a512-005056bb84e6" + ".json"
            #self.moveFile = self.gameLocation + "game-" + "1ef383f4-0196-11eb-a512-005056bb84e6" + "\\move-" + requestGUID + ".json"
            
            self.gameFile = self.gameLocation + "game-" + self.inviteData["gameGUID"] + "\\game-" + self.inviteData["gameGUID"] + ".json"
            self.moveFile = self.gameLocation + "game-" + self.inviteData["gameGUID"] + "\\move-" + requestGUID + ".json"
        
            f.close()
            #f.close()
            
            print(self.gameFile)
            while gameInPlay == True:
                time.sleep(2) 
            
                gameInPlay = self.checkforFile(self.gameFile)

                try:
                    with open(self.gameFile) as f:
                        self.data = json.load(f) 

                except ValueError:
                    print ("JSON Error")
                    continue

                if 'winner' in self.data:
                    gameInPlay = False
                    print("Winner:" + self.data["winner"])
                    break

                if self.nextMove(self.data) == self.playerName:
                 
                    actualMove = OthelloBestMove.selectedMove.bestMove(self.getMoves(self.data["board"]))
                    self.outputMoveFile(actualMove, self.moveFile, requestGUID)

                f.close()

        else:
            print("Timeout waiting for invite")
 
    def outputMoveFile(self, actualMove, filename, gameGUID): 
    
        print(actualMove)
        data = {}
        moveFile = ""
        data['gameGUID'] = gameGUID
        data['x'] = actualMove["Column"]
        data['y'] = actualMove["Row"]
        data['moveNumber'] = self.turnNumber + 1
    
        jsonString = json.dumps(data, indent=4)
        moveFile = open(filename,'w+')
        moveFile.write(jsonString)
        moveFile.close()

    def checkNext(self,row,column,counters):  

        if self.boardGrid[row][column] == self.opponent:
            counters+=1
            return [counters,row,column]  
     
        if self.boardGrid[row][column] == self.player:
            return [counters,row,column,"End"]  

        if self.boardGrid[row][column] == 0:
            return [0,row,column,"None"]  
     
        return [counters,row,column,"None"]          

    def lineCheck(self,start,end,by,row,column,mode):  

        count = 0
        localCounters = ""
        validMove = False
        if mode == "Both+":
            increment = 1
        elif mode == "Both-":
            increment = -1

        for number in range(start, end + by, by):  
        
            if mode == "Column":
                nextCounter = self.checkNext(row,number,count)
            elif mode == "Row":
                nextCounter = self.checkNext(number,column,count) 
            elif mode == "Both+":
                if row + increment > 7:
                    break
                nextCounter = self.checkNext(row + increment,number,count)
                increment += 1

            elif mode == "Both-":
                if row + increment < 0:
                    break
                nextCounter = self.checkNext(row + increment,number,count)
                increment += -1
            
            count = nextCounter[0]

            if len(nextCounter) == 4 and nextCounter[3] == "None":
                break

            if len(nextCounter) == 4 and nextCounter[3] == "End":
                validMove = True
                break
        
            if mode == "Column":
                localCounters = localCounters + str(row + 1) + "," + str(number + 1) + "|"
            
            if mode == "Both-" or mode == "Both+":
                localCounters = localCounters + str(row + increment) + "," + str(number + 1) + "|" 
        
            if mode == "Row":
                localCounters = localCounters + str(number + 1) + "," + str(column + 1) + "|"

        if validMove == False:
            count = 0

        if count != 0: 
            return[count,localCounters.rstrip("|")]

        return ""

    def reset(self):
        self.totalCounters = "" 
        self.boardGrid=[]


    def getMoves(self,board):  
        try:   
            iNested = 0
            boardMoves={}
            iCheck = 0
            iColumn = 0
            iRow = 0 
            moves = 0

            iRange = 7
            iBy = 1 
         
            self.reset()

            while iNested<len(board):
                self.boardGrid.append(board[iNested:iNested+8])
                iNested+=8
            
            for y in self.boardGrid: 
            
                iColumn = 0

                for x in y: 
             
                    if x == 0: 
                             
                        line = self.lineCheck(iColumn + 1, 7, 1, iRow, iColumn, "Column")
                        if line != "": 
                            self.totalCounters = line[1] + "|"
                            
                        line = self.lineCheck(iColumn + 1, 7, 1, iRow, iColumn, "Both+")
                        if line != "":
                            self.totalCounters = self.totalCounters + line[1] + "|" 
                            
                        line = self.lineCheck(iColumn + 1, 7, 1, iRow, iColumn, "Both-")
                        if line != "":
                            self.totalCounters = self.totalCounters + line[1] + "|" 

                        line = self.lineCheck(iColumn - 1, 0, -1, iRow, iColumn, "Column")
                        if line != "":
                            self.totalCounters = self.totalCounters + line[1] + "|" 
                            
                        line = self.lineCheck(iColumn - 1, 0, -1, iRow, iColumn, "Both+")
                        if line != "":
                            self.totalCounters = self.totalCounters + line[1] + "|" 
                            
                        line = self.lineCheck(iColumn - 1, 0, -1, iRow, iColumn, "Both-")
                        if line != "":
                            self.totalCounters = self.totalCounters + line[1] + "|" 
                                    
                        line = self.lineCheck(iRow + 1, 7, 1, iRow, iColumn, "Row")
                        if line != "":
                            self.totalCounters = self.totalCounters + line[1] + "|"  

                        line = self.lineCheck(iRow - 1, 0, -1, iRow, iColumn, "Row")
                        if line != "":
                            self.totalCounters = self.totalCounters + line[1] + "|" 
                    
                        if self.totalCounters != "": 
                            moves +=1
                            self.totalCounters = self.totalCounters.rstrip("|")
                            boardMoves[moves] = {}
                            boardMoves[moves]['Row'] = iRow + 1
                            boardMoves[moves]['Column'] = iColumn + 1
                            boardMoves[moves]['Number'] = self.totalCounters.count("|") + 1 
                            boardMoves[moves]['Counters'] = self.totalCounters 
                            boardMoves[moves]['Value'] = 0

                    iColumn += 1
                    iLineCounters = 0
                    cLineCounters = ""
                    self.totalCounters = ""
                    iTotalCounts = 0 

                iRow += 1

            return boardMoves

        finally:
            print(boardMoves)