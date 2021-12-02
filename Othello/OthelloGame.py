import uuid
import json
import sys
import Othello

def generateFile():
    jsonString = json.dumps(game, indent=4)
    filename = fileLocation + "request-" + gameUID + ".json"
    print(filename)
    gameFile = open(filename,'w')
    gameFile.write(jsonString)
    gameFile.close()

def createGame(): 
    gameFile = {}
    gameFile['requestGUID'] = gameUID
    gameFile['playerName'] = "David-Python-Bot"
    gameFile['opponentName'] = "Server-Random"
    gameFile['minimumGameLengthInSeconds'] = 1
    gameFile['maximumGameLengthInSeconds'] = 999999
     
    return gameFile

#fileLocation = "D:\\dholliday\\Othello\\Python\\"
fileLocation = "D:\\Othello\\V1\\"

gameUID = uuid.uuid4().hex
game = createGame() 
generateFile()

#gameUID = "1ef383f4-0196-11eb-a512-005056bb84e6"
game = Othello.OthelloBot(fileLocation,"David-Bot")
game.othelloBot(gameUID)