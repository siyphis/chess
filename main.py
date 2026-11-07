import random
import pygame
import chess

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
        self.x = x
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
    pygame.display.flip()


def draw_peices():
    global board_state,Black_images,Black_pieces
    for square in chess.SQUARES: #update peices by itterating over board_state
        if str(board_state.piece_at(square)) in Black_pieces:
            screen.blit(Black_images[Black_pieces.index(str(board_state.piece_at(square)))], (board[square].x * 50 + 5, board[square].y * 50 + 5))
        if str(board_state.piece_at(square)) in White_pieces:
            screen.blit(White_images[White_pieces.index(str(board_state.piece_at(square)))], (board[square].x * 50 + 5, board[square].y * 50 + 5))
    pygame.display.flip()


def get_space():
    for item in board_rects:
        letter=["a","b","c","d","e","f","g","h"]
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
    else:
        return
    draw_board()
    draw_peices()
    if board_state.is_checkmate() or board_state.is_stalemate():
        running = False


def get_moves(space):
    global board_state
    origin = chess.parse_square(space)

    moves_from_origin = [
        chess.square_name(move.to_square)
        for move in board_state.legal_moves
        if move.from_square == origin
    ]
    print(moves_from_origin)
    draw_board()
    draw_peices()

    return moves_from_origin
def draw_moves(space):
    letter = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for move in get_moves(space):
        print(str(letter.index(move[0]))+move[1])
        pygame.draw.circle(screen, "honeydew3",((letter.index(move[0])* 50) +25 ,  ((int(move[1])-1)* 50)+25,),20)
        pygame.display.flip()

def smart_bot():
    global board_state
    legal_moves = list(board_state.legal_moves)
    move = random.choice(legal_moves)
    board_state.push(move)
def value_calc(board):
    PIECE_VALUES = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }

    white_total = 0
    black_total = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                white_total += value
            else:
                black_total += value

    return white_total - black_total

def smarter_bot(board_state,depth):

    best_score = -9999
    best_move = None
    for move in board_state.legal_moves:
        score2 = 9999
        temp = board_state.copy()
        temp.push(move)
        score = value_calc(temp)

        for move2 in temp.legal_moves:
            temp2 = temp.copy()
            temp2.push(move2)
            if value_calc(temp2) < score2:
                score2 = value_calc(temp2)

        if score2 > best_score:
            best_score = score2
            best_move = move
    return best_move
counter=0
def minmax(board_state, depth, maximizing_player, alpha=-9999, beta=9999, initial_depth=3):
    global counter
    counter += 1
    print(counter)
    if depth == 0 or board_state.is_game_over():
        return value_calc(board_state)

    best_move = None

    if maximizing_player:
        max_eval = -9999
        for move_obj in board_state.legal_moves:
            board_state.push(move_obj)
            score = minmax(board_state, depth - 1, False, alpha, beta, initial_depth)
            board_state.pop()
            
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
        min_eval = 9999
        for move_obj in board_state.legal_moves:
            board_state.push(move_obj)
            score = minmax(board_state, depth - 1, True, alpha, beta, initial_depth)
            board_state.pop()
            
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if board_state.turn == chess.BLACK:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_just_pressed()[0]:
                    print("press")
                    if len(sel_space) < 1:
                        sel_space.append(get_space())
                        draw_moves(sel_space[0])
                    else:
                        sel_space.append(get_space())
                        move(sel_space[0],sel_space[1])
                        sel_space=[]
        else:
            #board_state.push(smarter_bot(board_state,1))
            ai_move, score = minmax(board_state, depth=4, maximizing_player=True, initial_depth=4)           
            board_state.push(ai_move)
            draw_board()
            draw_peices()
