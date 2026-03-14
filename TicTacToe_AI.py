board=[" "," "," "," "," "," "," "," "," "]
turn=1

def printBoard():
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def playMode():
    print("Enter 1 for Single-Player mode (Play against AI).")
    print("Enter 2 for Double-Player mode (Play against another person).\n")
    while True:
        try:
            mode=int(input("Enter your Choice: "))
            if mode==1:
                print("\nYou are 'X', AI is 'O'")
                break
            elif mode==2:
                print("\nPlayer-1 is 'X', Player-2 is 'O'")
                break
            else:
                print("Invalid Input! Choose from the given Options")
        except ValueError:
            print("Invalid input! Choose from the given Options.")
    print("\n")
    return mode

def winCheck(board, player):
    for i in range(0, 9, 3):
        if board[i]==board[i+1]==board[i+2]==player:
            return True
        
    for i in range(3):
        if board[i]==board[i+3]==board[i+6]==player:
            return True
        
    if board[0]==board[4]==board[8]==player:
        return True
    if board[2]==board[4]==board[6]==player:
        return True
    return False

def drawCheck(board):
    return " " not in board

def minimax(board, depth, is_maximizing):
    if winCheck(board, "X"):
        return -1
    elif winCheck(board,"O"):
        return 1
    elif drawCheck(board):
        return 0
    
    if is_maximizing:
        best_score=-float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i]="O"
                score=minimax(board,depth+1,False)
                board[i]=" "
                best_score=max(best_score,score)
        return best_score
    else:
        best_score=float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i]="X"
                score=minimax(board,depth+1,True)
                board[i]=" "
                best_score=min(best_score,score)
        return best_score

def best_moves(board):
    best_score=-float("inf")
    best_move=(-1,-1)
    for i in range(9):
        if board[i] == " ":
                board[i]="O"
                score=minimax(board,0,False)
                board[i]=" "
                if score>best_score:
                    best_score=score
                    best_move=i
    return best_move

def resetGame():
    global board,turn

    board=[" "," "," "," "," "," "," "," "," "]
    turn=1

while True:    
    print("\n _____Tic Tac Toe Game_____ ")
    print("\t 1 | 2 | 3 ")
    print("\t---|---|---")
    print("\t 4 | 5 | 6 ")
    print("\t---|---|---")
    print("\t 7 | 8 | 9 ")
    print("For playing a move, just enter a no. according to the above grid.")
    print("\n")

    mode=playMode()

    while True:
        if turn==1:
            print("X's Chance")
            try:
                inp = int(input("Enter your position choice: "))
                if inp<1 or inp>9:
                    print("Invalid input! Enter a number 1-9.")
                    continue
            except ValueError:
                print("Invalid input! Enter a number 1-9.")
                continue

            if board[inp-1] != " ":
                print("Position is occupied! Enter another position.")
                continue
            else:
                board[inp-1]="X"

            if winCheck(board,"X"):
                printBoard()
                print(f"Congratulations! The winner is X.")
                break
            elif drawCheck(board):
                printBoard()
                print("It's a Draw!!")
                break
            turn=0
        elif turn==0:
            if mode==1:        # Single-Player Mode (Play against AI)
                print("O's Chance")
                inp=best_moves(board)
                board[inp]="O"

                if winCheck(board,"O"):
                    printBoard()
                    print(f"The winner is O.")
                    break
                elif drawCheck(board):
                    printBoard()
                    print("It's a Draw!!")
                    break
                turn=1
            elif mode==2:       # Double-Player Mode (Play against another person)
                print("O's Chance")
                try:
                    inp = int(input("Enter your position choice: "))
                    if inp<1 or inp>9:
                        print("Invalid input! Enter a number 1-9.")
                        continue
                except ValueError:
                    print("Invalid input! Enter a number 1-9.")
                    continue

                if board[inp-1] != " ":
                    print("Position is occupied! Enter another position.")
                    continue
                else:
                    board[inp-1]="O"

                if winCheck(board,"O"):
                    printBoard()
                    print(f"Congratulations! The winner is O.")
                    break
                elif drawCheck(board):
                    printBoard()
                    print("It's a Draw!!")
                    break
                turn=1
        printBoard()
    
    con=input("Do you want to Play Again?: ")
    if not con.lower().startswith("y"):
        break

    resetGame()
    print("\n")
    print("_*_"*20)