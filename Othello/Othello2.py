
import json
#import numpy as np

player = 2
opponent = 1
moves = 0
boardGrid=[]

def checkNext(row,column,counters):  

    if boardGrid[row][column] == opponent:
        counters+=1
        return [counters,row,column]  
    
    if boardGrid[row][column] == 0:
        return [0,row,column,"Break"]  
     
    return [counters,row,column,"Break"]          


def lineCheck(start,end,by,row):  

    count = 0
    localCounters = ""

    for number in range(start, end, by):  
        nextCounter = checkNext(row,number,count)
        count = nextCounter[0]

        if len(nextCounter) == 4:
            break

        localCounters = localCounters + str(iRow + 1) + "," + str(number + 1) + "|"

    if count != 0: 
        return[count,localCounters.rstrip("|")]

    return ""
try:
    with open(r'D:\Othello\V1\David\game-2b5843c6-8fab-11ea-9296-005056bb84e6.json') as f:
        data = json.load(f)

    board = data["board"]
    
    iNested = 0
    boardGrid=[]
    boardMoves={}
    iCheck = 0
    iColumn = 0
    iRow = 0
    iLineCounters = 0
    cLineCounters = ""
    cTotalCounters = ""
    iTotalCounts = 0



    cTest = []

    iRange = 7
    iBy = 1 


    while iNested<len(board):
      boardGrid.append(board[iNested:iNested+8])
      iNested+=8
            
    for y in boardGrid: 
            
        iColumn = 0

        for x in y: 
             
            if x == 0: 

                #for number in range(iColumn - 1 , 0, -1):
                cTest = lineCheck(iColumn + 1, 7, 1, iRow)
                if cTest != "":
                    iTotalCounts = iTotalCounts + cTest[0] 
                    cTotalCounters = cTest[1] 

                for number in range(iRow + 1, 7, 1):  
                    nextCounter = checkNext(number,iColumn,iLineCounters)
                    iLineCounters = nextCounter[0]
                    cLineCounters = cLineCounters + str(iRow) + "," + str(iColumn) + "|"

                    if len(nextCounter) == 4:
                        break
                           
                if iLineCounters != 0:  
                    iTotalCounts = iTotalCounts + iLineCounters
                    cTotalCounters = cTotalCounters + cLineCounters   
                    
                if iTotalCounts != 0: 
                    moves +=1
                    boardMoves[moves] = {}
                    boardMoves[moves]['Row'] = iRow + 1
                    boardMoves[moves]['Column'] = iColumn + 1
                    boardMoves[moves]['Counters'] = iTotalCounts
            
            iColumn += 1
            iLineCounters = 0
            cLineCounters = ""
            cTotalCounters = ""
            iTotalCounts = 0

                ##  iCheck = boardGrid
              ##  while iCheck < 8:
              #  print(i)
               #   i += 1
        iRow += 1

    print(boardMoves)

    #for x in board:
    #    print(x)
    #    thisdict = dict(row=1, column=2, value=x)
    #    
    #thisdict2 = dict(row=4, column=2, value=x)
    #myfamily = {
    #    "child1" : thisdict,
    #    "child2" : thisdict2
    #}
    
    #print(myfamily)

   #othelloGrid = np.array(board)
   # print(othelloGrid)

   # L = [[0, 1, 0, 0, 1, 2, 0, 1],[0, 1, 0, 0, 1, 2, 0, 1],[0, 1, 0, 0, 1, 2, 0, 1],[0, 1, 0, 0, 1, 2, 0, 1],[0, 1, 0, 0, 1, 2, 0, 1],[0, 1, 0, 0, 1, 2, 0, 1],[0, 1, 0, 0, 1, 2, 0, 1]]   
     
   # print(L[3][4]) 
    # Prints 1 2 3 4 5 6 7 8 9

finally:
   f.close()