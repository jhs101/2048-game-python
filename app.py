import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="2048 Game", layout="centered")

def new_game(size=4):
    board = np.zeros((size, size), dtype=int)
    board = add_new_tile(board)
    board = add_new_tile(board)
    return board

def add_new_tile(board):
    empty = list(zip(*np.where(board == 0)))
    if empty:
        x, y = random.choice(empty)
        board[x, y] = 2 if random.random() < 0.9 else 4
    return board

def compress(board):
    new_board = np.zeros_like(board)
    for i in range(board.shape[0]):
        pos = 0
        for j in range(board.shape[1]):
            if board[i, j] != 0:
                new_board[i, pos] = board[i, j]
                pos += 1
    return new_board

def merge(board):
    score = 0
    for i in range(board.shape[0]):
        for j in range(board.shape[1]-1):
            if board[i, j] == board[i, j+1] and board[i, j] != 0:
                board[i, j] *= 2
                board[i, j+1] = 0
                score += board[i, j]
    return board, score

def reverse(board):
    return np.array([row[::-1] for row in board])

def transpose(board):
    return board.T

def move_left(board):
    compressed = compress(board)
    merged, score = merge(compressed)
    final = compress(merged)
    return final, score

def move_right(board):
    reversed_board = reverse(board)
    new_board, score = move_left(reversed_board)
    final = reverse(new_board)
    return final, score

def move_up(board):
    transposed = transpose(board)
    new_board, score = move_left(transposed)
    final = transpose(new_board)
    return final, score

def move_down(board):
    transposed = transpose(board)
    new_board, score = move_right(transposed)
    final = transpose(new_board)
    return final, score

def game_over(board):
    if 0 in board:
        return False
    for i in range(4):
        for j in range(3):
            if board[i, j] == board[i, j+1] or board[j, i] == board[j+1, i]:
                return False
    return True

st.title("🎮 2048 Game")

if "board" not in st.session_state:
    st.session_state.board = new_game()
    st.session_state.score = 0

board = st.session_state.board

st.write(f"**Score:** {st.session_state.score}")
st.table(board)

col1, col2, col3, col4, col5 = st.columns(5)
if col2.button("⬅️ Left"):
    new_board, score = move_left(board)
elif col3.button("⬆️ Up"):
    new_board, score = move_up(board)
elif col4.button("⬇️ Down"):
    new_board, score = move_down(board)
elif col5.button("➡️ Right"):
    new_board, score = move_right(board)
else:
    new_board, score = board, 0

if not np.array_equal(board, new_board):
    st.session_state.board = add_new_tile(new_board)
    st.session_state.score += score

if game_over(st.session_state.board):
    st.error("💀 Game Over! Click 'New Game' to restart.")

if st.button("🔄 New Game"):
    st.session_state.board = new_game()
    st.session_state.score = 0
    st.experimental_rerun()
