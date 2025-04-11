import math


class HexBoard:
    def __init__(self, size: int):
        self.size = size  # Tamaño N del tablero (NxN)
        self.board = [[0] * size for _ in range(size)]  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
        self.player_positions = {1: set(), 2: set()}  # Registro de fichas por jugador

    # def clone(self) -> HexBoard:
    #     """Devuelve una copia del tablero actual"""
    #     pass

    def place_piece(self, row: int, col: int, player_id: int) -> bool:            
        self.board[row][col]=player_id
        return True
        
        
    
    def get_possible_moves(self) -> list:
        possible_moves=[]
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col]==0:
                    possible_moves.append((row,col))
                    
        return possible_moves
    
    
    
    def check_connection(self) -> int:   # 1 if 2 win , -1 if 1 , and 0 if nobady win yet
        mask= [[False] * self.size for _ in range(self.size)] 
        
        for row in range(self.size):
            if self.board[row][0]!=1: continue
            mask[row][0]=True
            res=self.check_connection_player1(row,0,1,mask)
            mask[row][0]=False
            if res:return -math.inf
            
            
        for col in range(self.size):
            if self.board[0][col]!=2: continue
            mask[0][col]=True
            res=self.check_connection_player2(0,col,2,mask)
            mask[0][col]=False
            if res:return math.inf
        return 0

    def check_connection_player1(self,c_row,c_col,player_id,board_mask):
        if c_col==self.size-1:return True
        
        row_moves=[0,1,-1,-1, 1, 0]#right,down,up-right,up, down-left,left
        col_moves=[1,0, 1, 0,-1,-1]#right,down,up-right,up, down-left,left
        
        for pos in range(6):
            r=c_row+row_moves[pos]
            c=c_col+col_moves[pos]
            if r<0 or r>=self.size: continue
            if c<0 or c>=self.size: continue
            
            if  not board_mask[r][c] and self.board[r][c]==player_id:
                board_mask[r][c]=True
                res= self.check_connection_player1(r,c,player_id,board_mask)
                board_mask[r][c]=False
                if res:return True
               
        
        return False      
       
    def check_connection_player2(self,c_row,c_col,player_id,board_mask):
        if c_row==self.size-1:return True
        
        row_moves=[1, 1, 0,0,-1,-1]#down,down-left,left,,right,up,up-right
        col_moves=[0,-1,-1,1, 0, 1]#down,down-left,left,,right,up,up-right
        
        for pos in range(6):
            r=c_row+row_moves[pos]
            c=c_col+col_moves[pos]
            if r<0 or r>=self.size: continue
            if c<0 or c>=self.size: continue
            
            if  not board_mask[r][c] and self.board[r][c]==player_id:
                board_mask[r][c]=True
                res= self.check_connection_player2(r,c,player_id,board_mask)
                if res:return True
                board_mask[r][c]=False
        
        return False      
 
    def show(self,space="            ",row=0):
        r=""+space
        for col in range(self.size):
            r+=str(self.board[row][col])+" "
        print(r)
        
        if row==self.size-1 :return
        self.show(space+" ",row+1)
        


# (i, j - 1) → Izquierda
# (i, j + 1) → Derecha
# (i - 1, j) → Arriba
# (i + 1, j) → Abajo
# (i - 1, j + 1) → Arriba-Derecha
# (i + 1, j + 1) → Abajo-Derecha

# - Para filas impares (i impar):
# (i, j - 1) → Izquierda
# (i, j + 1) → Derecha
# (i - 1, j) → Arriba
# (i + 1, j) → Abajo
# (i - 1, j - 1) → Arriba-Izquierda
# (i + 1, j - 1) → Abajo-Izquierda
            
        
        
        

        