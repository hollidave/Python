
class selectedMove():
    def bestMove(allMoves):
        y = 0
        x = 0

        for top, move in allMoves.items():  
            y = move["Row"]
            x = move["Column"] 
             
        return {"Row": y, "Column": x}  