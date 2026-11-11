import math
import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
import chess.engine
from chess.engine import Cp,Mate,MateGiven
import chess
import random


def value_calc(board):

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

def board_to_tensor(board):
    tensor = torch.zeros((12, 8, 8), dtype=torch.float32)
    piece_map = board.piece_map()
    for square, piece in piece_map.items():
        row = 7 - (square // 8)
        col = square % 8
        piece_index = piece.piece_type - 1 + (6 if piece.color == chess.BLACK else 0)
        tensor[piece_index, row, col] = 1.0
    return tensor

def make_data(num):
    board_states = []
    evals = []
    board = chess.Board()

    with chess.engine.SimpleEngine.popen_uci("stockfish/stockfish") as engine:

        while len(board_states) < num:
            if board.is_game_over():
                board.reset()
            moves = list(board.legal_moves)
            if not moves:
                board.reset()
                continue
            board.push(random.choice(moves))
            board_states.append(board_to_tensor(board))
            score = engine.analyse(board,chess.engine.Limit(depth=8))
            info = chess.engine.PovScore.white(score['score'])
            
            eval = info.score(mate_score=100000)
            eval = math.tanh(eval / 400)
            evals.append(eval)
        return torch.tensor(np.array(board_states), dtype=torch.float32), torch.tensor(np.array(evals), dtype=torch.float32).unsqueeze(1)

class Whatsitman(nn.Module):
    def __init__(self):
        super(Whatsitman, self).__init__()
        self.flatten = nn.Flatten()
        self.hidden = nn.Linear(12 * 8 * 8, 64)
        self.output = nn.Linear(64, 1)


    def forward(self, x):
        x = self.flatten(x)
        x = torch.relu(self.hidden(x))
        score = torch.tanh(self.output(x))
        return score


def train_model(model,epochs, batch_size, learning_rate):
    model = model
    try: 
        model.load_state_dict(torch.load("fakefish.pth",weights_only=True))
    except:
        print("no modely")
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.MSELoss()


    for epoch in range(epochs):
        print("Generating training data")
        data,targets = make_data(batch_size)
        print("Training data generated")

        for i in range(100):
            optimizer.zero_grad()
            predictions = model(data)
            loss = criterion(predictions, targets)
            loss.backward()
            optimizer.step()
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}")
    torch.save(model.state_dict(), "fakefish.pth")
    print("Model saved as fakefish.pth")
def train(epochs,batch,lr):
    training = True
    while training:
        train_model(Whatsitman(), epochs=epochs, batch_size=batch, learning_rate=lr)
        if input("Do you want to continue training? (y/n): ").lower() != 'y':
            break