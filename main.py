from HexBoard import HexBoard
from player import IAPlayer, Player


def main():
    print("Bienvenido a HEX")
    try:
        size = int(input("Ingrese el tamaño del tablero (por ejemplo, 5): "))
    except ValueError:
        print("Tamaño inválido. Usando tamaño 5 por defecto.")
        size = 5
    board = HexBoard(size)
    board.show()
    player_id=1



         
            
    def Vs_ia():
        player=Player(1)
        ia_player=IAPlayer(2)
        is_ia=False
        current_player=player

        while(True):
            move=current_player.play(board)
            board.place_piece(move[0],move[1],current_player.player_id)
            board.show()
            
            if  board.check_connection()!= 0:
            
                print(f"Ha ganado el jugador: {current_player.player_id}")
                break
            
            if is_ia:
                is_ia=False
                current_player=player
            else : 
                is_ia=True
                current_player=ia_player
            
            
            
     
        
    def Vs_Player2():
        player=Player(1)
        ia_player=Player(2)
        is_ia=False
        current_player=player
        while(True):
            move=current_player.play(board)
            board.place_piece(move[0],move[1],current_player.player_id)
            
            board.show()
            
            if  board.check_connection()!=0:
            
                print(f"Ha ganado el jugador: {current_player.player_id}")
                break
            
            if is_ia:
                is_ia=False
                current_player=player
            else : 
                is_ia=True
                current_player=ia_player
            
            
        
    def choice():
        choice=int(input("1 para jugar vs ia , "))
        if choice==1:
            Vs_ia()
        else:
            Vs_Player2()
            
           
    choice()  
        

if __name__ == "__main__":
    main()


##    1 1 
## 2  0 0  2
##  2  0 0  2
##      
##