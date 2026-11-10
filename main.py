import random
import pygame
import chess
ai = False
pygame.init()
screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('Comic Sans MS', 40)
running = True
board=[]
board_rects=[]
sel_space=[]
board_state = chess.Board()
black_total=0
white_total=0

def load_images():
    global Black_images,White_images,Black_pieces,White_pieces
    Black_images=[pygame.image.load("Images/B_Pawn.png"),pygame.image.load("Images/B_Bishop.png"),pygame.image.load("Images/B_Knight.png"),pygame.image.load("Images/B_Rook.png"),pygame.image.load("Images/B_Queen.png"),pygame.image.load("Images/B_King.png")]
    Black_pieces=["p","b","n","r","q","k"]
    White_images=[pygame.image.load("Images/W_Pawn.png"),pygame.image.load("Images/W_Bishop.png"),pygame.image.load("Images/W_Knight.png"),pygame.image.load("Images/W_Rook.png"),pygame.image.load("Images/W_Queen.png"),pygame.image.load("Images/W_King.png")]
    White_pieces=["P","B","N","R","Q","K"]

    for i in range(len(Black_images)):
        Black_images[i] = pygame.transform.scale(Black_images[i], (30, 40))
    for i in range(len(White_images)):
        White_images[i] = pygame.transform.scale(White_images[i], (30, 40))
load_images()

class board_space():
    def __init__(self,x,y,color):
        numbers = [0,1,2,3,4,5,6,7]
        self.x = numbers[-x-1]
        self.y = y
        self .color = color

for y in range(8): #defines colour to make checkerboard pattern
    for x in range(8):
        if (x + y) % 2 == 0:
            color = "aquamarine4"
        else:
            color = "azure"
        board.append(board_space(x,y,color))

def draw_board(): #itterates through all spaces and draws them
    for object in board:
        board_rects.append(pygame.Rect(object.x * 50, object.y * 50, 50, 50))
        pygame.draw.rect(screen,object.color,pygame.Rect(object.x*50,object.y*50,50,50))


def draw_peices():
    global board_state,Black_images,Black_pieces
    for square in chess.SQUARES: #update peices by itterating over board_state
        if str(board_state.piece_at(square)) in Black_pieces:
            screen.blit(Black_images[Black_pieces.index(str(board_state.piece_at(square)))], (board[square].x * 50 + 5, board[square].y * 50 + 5))
        if str(board_state.piece_at(square)) in White_pieces:
            screen.blit(White_images[White_pieces.index(str(board_state.piece_at(square)))], (board[square].x * 50 + 5, board[square].y * 50 + 5))


def get_space():
    for item in board_rects:
        letter=["h","g","f","e","d","c","b","a"]
        if item.collidepoint(pygame.mouse.get_pos()):
            return letter[int(item.x / 50)]+str(int(item.y / 50+1))

def move(space_1,space_2):
    global board_state , running
    if space_1==space_2:
        return
    move_note=space_1+space_2
    move_obj = chess.Move.from_uci(move_note)
    rank_to = chess.square_rank(move_obj.to_square)
    piece = board_state.piece_at(move_obj.from_square)
    if piece and piece.piece_type == chess.PAWN and rank_to in (0, 7):
        promo = input("enter promotion peice eg q")
        if promo in ["q","r","b","n"]: move_note +=promo
        move_obj = chess.Move.from_uci(move_note)
    if chess.Move.from_uci(move_note) in board_state.legal_moves:
        board_state.push(move_obj)
        return True
    else:
        return



def get_moves(space):
    global board_state
    origin = chess.parse_square(space)

    moves_from_origin = [
        chess.square_name(move.to_square)
        for move in board_state.legal_moves
        if move.from_square == origin
    ]
    draw_board()
    draw_peices()
    return moves_from_origin
def draw_moves(space):
    letter = ["h", "g", "f", "e", "d", "c", "b", "a"]
    for move in get_moves(space):
        pygame.draw.circle(screen, "honeydew3",((letter.index(move[0])* 50) +25 ,  ((int(move[1])-1)* 50)+25,),20)

PST = {
    chess.PAWN: [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
         5,  5, 10, 25, 25, 10,  5,  5,
         0,  0,  0, 20, 20,  0,  0,  0,
         5, -5,-10,  0,  0,-10, -5,  5,
         5, 10, 10,-20,-20, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0
    ],
    chess.KNIGHT: [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50,
    ],
    chess.BISHOP: [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20,
    ],
    chess.ROOK: [
          0,  0,  0,  0,  0,  0,  0,  0,
          5, 10, 10, 10, 10, 10, 10,  5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
          -5,  0,  0,  5,  5,  0,  0,  -5
    ],
    chess.QUEEN: [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ],
    chess.KING: [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
         20, 20,  0,  0,  0,  0, 20, 20,
         20, 30, 10,  0,  0, 10, 30, 20
    ]
}

def value_calc(board):
    if not board.legal_moves:
        if board.is_check():
            outcome = board.outcome()
            if outcome.winner == chess.WHITE:
                return 99999
            elif outcome.winner == chess.BLACK:
                return -99999
            else:
                return 0
    if board.is_repetition(2):
        if board.turn == chess.WHITE:
            return -550
        else:
            return 550
    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0
    }

    white_total = 0
    black_total = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            # Base material calculation
            val = PIECE_VALUES[piece.piece_type]
            
            # Positional score calculation
            if piece.color == chess.WHITE:
                table_square = 56 - (square // 8) * 8 + (square % 8)
                val += PST[piece.piece_type][table_square]
                white_total += val
            else:
                table_square = (square // 8) * 8 + (square % 8)
                val += PST[piece.piece_type][table_square]
                black_total += val

    return white_total - black_total

counter=0

def victim_value(board_state, move):
    if board_state.is_capture(move):
        captured_piece = board_state.piece_at(move.to_square)
        if captured_piece:
            PIECE_VALUES = {
                chess.PAWN: 100,
                chess.KNIGHT: 320,
                chess.BISHOP: 330,
                chess.ROOK: 500,
                chess.QUEEN: 900,
                chess.KING: 0
            }
            return PIECE_VALUES[captured_piece.piece_type]
    return 0

def move_order(board_state):
    moves=list(board_state.legal_moves)
    moves.sort(key=lambda move: victim_value(board_state,move), reverse=True)

    return moves

def minmax(board_state, depth, maximizing_player, alpha=-9999, beta=9999, initial_depth=3):
    global counter
    if depth == 0 or board_state.is_game_over():
        return value_calc(board_state)

    best_move = None

    if maximizing_player:
        max_eval = float("-inf")
        for move_obj in move_order(board_state):
            board_state.push(move_obj)
            score = minmax(board_state, depth - 1, False, alpha, beta, initial_depth)
            board_state.pop()
            counter+=1

            if score > max_eval:
                max_eval = score
                best_move = move_obj
            
            alpha = max(alpha, score)
            
            if alpha >= beta:
                break
                
        if depth == initial_depth:
            return best_move, max_eval
        return max_eval
        
    else:
        min_eval = float("inf")
        for move_obj in move_order(board_state):
            board_state.push(move_obj)
            score = minmax(board_state, depth - 1, True, alpha, beta, initial_depth)
            board_state.pop()
            counter+=1

            if score < min_eval:
                min_eval = score
                best_move = move_obj
            

            beta = min(beta, score)

            if alpha >= beta:
                break
                
        if depth == initial_depth:
            return best_move, min_eval
        return min_eval


draw_board()
draw_peices()
pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if board_state.turn == chess.BLACK:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_just_pressed()[0]:
                    if len(sel_space) <1:
                        sel_space.append(get_space())
                        draw_moves(sel_space[0])
                        pygame.display.flip()
                    else:
                        sel_space.append(get_space())
                        if move(sel_space[0],sel_space[1]):
                            draw_board()
                            draw_peices()
                            pygame.display.flip()
                            sel_space=[]
                        else:
                            sel_space=[sel_space[1]]
                            draw_moves(sel_space[0])
                            pygame.display.flip()
            if not board_state.is_game_over() and ai == True:
                ai_move, score = minmax(board_state, depth=5, maximizing_player=False, initial_depth=5)
                board_state.push(ai_move)
                counter=0
        else:
            if not board_state.is_game_over():
                start_time = pygame.time.get_ticks()
                ai_move, score = minmax(board_state, depth=5, maximizing_player=True, initial_depth=5)
                time_taken = pygame.time.get_ticks() - start_time
                print(f"AI move: {ai_move}, Nps: {counter/(time_taken/1000)}, Time taken: {time_taken} ms")
                board_state.push(ai_move)
                counter=0
                draw_board()
                draw_peices()
                pygame.display.flip()