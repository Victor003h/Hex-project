import heapq
import math
from HexBoard import HexBoard


class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    
    def play(self, board: HexBoard) -> tuple:
        print(f"Turno del jugador. ")
        inp=(input("Ingrese fila columna a jugar: "))
        split=inp.split(" ")
        return (int(split[0]),int(split[1]))
    
class IAPlayer(Player):
    round=0
    template=[()]
    
    def play(self,board:HexBoard)-> tuple:
        self.round+=1
        print(f"Turno de la IA ")
        input("Presione cualquier tecla.")
        if self.round<2:
            return self.Opening(board,self.player_id)
        
        return self.bestMove(board,self.player_id)
    
    def bestMove(self,board:HexBoard,player_id):
        possible_moves=board.get_possible_moves()
        move=possible_moves[0]
        maxim= -math.inf
        for i,j in possible_moves:
            board.place_piece(i,j,player_id)
            depth=3
            if len(possible_moves)>40:
                depth=2
            
            score=self.MiniMax(depth,board,1,-math.inf,math.inf)
            if score==math.inf:
                return (i,j)
            score=score+self.Heuristic_2(board,i,j,player_id)
            board.place_piece(i,j,0)
            if score>maxim:
                maxim=score
                move=(i,j)
            
        return move
    
    
    def Dijkstra_Heristic(self,board:HexBoard,player_id):
        w= [[math.inf] * board.size for _ in range(board.size)]
        d= [[math.inf] * board.size for _ in range(board.size)]
        for row in range(board.size):
            for col in range(board.size):
                if board.board[row][col]==player_id:
                    w[row][col]=0
                elif board.board[row][col]==0:
                    w[row][col]=1
        
        row_moves=[0,1,-1,-1, 1, 0]#right,down,up-right,up, down-left,left
        col_moves=[1,0, 1, 0,-1,-1]#right,down,up-right,up, down-left,left
        
        if player_id==2:
            row_moves=[1, 1, 0,0,-1,-1]#down,down-left,left,,right,up,up-right
            col_moves=[0,-1,-1,1, 0, 1]#down,down-left,left,,right,up,up-right
        
        heap=[]
        
        if player_id==1:
            for r in range(board.size):
                c = 0
                cost_here = w[r][c]
                if cost_here < math.inf:
                    d[r][c] = cost_here
                    heapq.heappush(heap, (cost_here, r, c))
        else:
             for c in range(board.size):
                r = 0
                cost_here = w[r][c]
                if cost_here < math.inf:
                    d[r][c] = cost_here
                    heapq.heappush(heap, (cost_here, r, c))
            
        
        while heap:
            c_cost,c_row,c_col=heapq.heappop(heap)
            if player_id==1 and  c_col==board.size-1:
                return c_cost
            elif  player_id==2 and  c_row==board.size-1:
                return c_cost

            if c_cost > d[c_row][c_col]:
                continue
            
            for i in range(6):
                n_row= c_row+row_moves[i]
                n_col= c_col+col_moves[i]
                if n_row<0 or n_row>=board.size: continue
                if n_col<0 or n_col>=board.size: continue
                
                if d[n_row][n_col]> d[c_row][c_col]+ w[n_row][n_col]:
                    d[n_row][n_col]=d[c_row][c_col]+ w[n_row][n_col]
                    heapq.heappush(heap, (d[c_row][c_col]+ w[n_row][n_col], n_row, n_col))
        
        return 0
                    
                
    def Heuristic_1(self,board:HexBoard):
        my_cost=self.Dijkstra_Heristic(board,2)
        #vs_id= 1 if player_id==2 else 2
        vs_cost=self.Dijkstra_Heristic(board,1)
        
        return vs_cost-my_cost
        
    def Heuristic_2(self,board:HexBoard,row,col,player_id):
        
        bridges_pos=[(1,-2),(-1,-1),(1,1),(-1,2),(-2,1),(2,-1)] # a,b,e,d,c,f
        r1=[ 0, 0,0,0,-1,1]
        c1=[-1,-1,1,1, 0,0]
        
        r2=[ 1,-1,1,-1,-1, 1]
        c2=[-1, 0,0, 1, 1,-1]
        
        opp_id=1 if player_id==2 else 1
        
        
        for i in range(len(bridges_pos)):
            n_row=row+bridges_pos[i][0]
            n_col= col+bridges_pos[i][1]
            if n_row<0 or n_row>=board.size: continue
            if n_col<0 or n_col>=board.size: continue
            
            
            if (board.board[n_row][n_col]==opp_id or board.board[n_row][n_col]==player_id) and board.board[row+r1[i]][col+c1[i]]==0==board.board[row+r2[i]][col+c2[i]]:
                
                if player_id==2:
                    if i>=4: return 0.4
                    return 0.8
                else:
                    if i==0 or i==3: return 0.4
                    return 0.8
        
        return 0
             
    def MiniMax(self,depth,board: HexBoard,player_id,alpha,beta):
        
        score=board.check_connection()
        if score!=0: 
            return score
        elif depth==0:
           # id=1 if player_id==2 else 2
        
            return self.Heuristic_1(board)
        
        if(player_id==2):
            maxim= -math.inf
            possible_moves=board.get_possible_moves()
            
            for i,j in possible_moves:
                
                board.place_piece(i,j,player_id)
                score=self.MiniMax(depth-1,board,1,alpha,beta)
                score=score+self.Heuristic_2(board,i,j,player_id)
                board.place_piece(i,j,0)
                if score==math.inf:return score
            
                maxim=max(maxim,score)
                alpha=max(alpha,score)
                if beta<=alpha:
                    break
            return maxim

        else:
            minim= math.inf
            possible_moves=board.get_possible_moves()
            
            for i,j in possible_moves:
                board.place_piece(i,j,player_id)
                score=self.MiniMax(depth-1,board,2,alpha,beta)
                score=score+self.Heuristic_2(board,i,j,player_id)
                board.place_piece(i,j,0)
                if score== -math.inf:return score
                
                minim=min(minim,score)
                beta=min(beta,score)
                if beta<=alpha:
                    break
            return minim
    
        
    def Opening(self,board:HexBoard,player_id):
        oppnt_id=1 if player_id ==2 else 2
        if player_id==2:
            if board.size>5:
                if board.board[4][0]!=oppnt_id:
                    return (4,0)
                else:
                    return (3,0)
            else: 
                if board.board[board.size-1][0]!=oppnt_id:
                    return (board.size-1,0)
                else:
                    return (board.size-1,board.size-1)
        else:
            if board.size>5:
                if board.board[0][4]!=oppnt_id:
                    return (0,4)
                else:
                    return (0,3)
            else: 
                if board.board[0][board.size-1]!=oppnt_id:
                    return (0,board.size-1)
                else:
                    return (board.size-1,board.size-1)
          
    def itsOpening(self,board:HexBoard):
        cont=0
        for i in range(board.size): 
            for j in range(board.size): 
                if board.board[i][j]!=0:cont+=1
        
        if cont>1:return False
        return True
        
        
            
    
        
        
        
#   2 1 0 0 0
#    2 1 0 0 0
#     0 0 0 0 0
#      0 0 0 0 0
    
