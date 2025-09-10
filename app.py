import streamlit as st
import random

SIZE = 4

def init_board():
    board = [[0]*SIZE for _ in range(SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty = [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    if empty:
        i, j = random.choice(empty)
        board[i][j] = 2 if random.random() < 0.9 else 4

def compress(row):
    new_row = [num for num in row if num != 0]
    new_row += [0]*(SIZE - len(new_row))
    return new_row

def merge(row):
    for i in range(SIZE-1):
        if row[i] != 0 and row[i] == row[i+1]:
            row[i] *= 2
            row[i+1] = 0
    return row

def move_left(board):
    new_board = []
    for row in board:
        row = compress(row)
        row = merge(row)
        row = compress(row)
        new_board.append(row)
    return new_board

def move_right(board):
    new_board = [row[::-1] for row in board]
    new_board = move_left(new_board)
    new_board = [row[::-1] for row in new_board]
    return new_board

def transpose(board):
    return [list(row) for row in zip(*board)]

def move_up(board):
    new_board = transpose(board)
    new_board = move_left(new_board)
    new_board = transpose(new_board)
    return new_board

def move_down(board):
    new_board = transpose(board)
    new_board = move_right(new_board)
    new_board = transpose(new_board)
    return new_board

def can_move(board):
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0:
                return True
            if j < SIZE-1 and board[i][j] == board[i][j+1]:
                return True
            if i < SIZE-1 and board[i][j] == board[i+1][j]:
                return True
    return False


# --- Streamlit UI ---
st.title("2048 게임 🎮")

if "board" not in st.session_state:
    st.session_state.board = init_board()

board = st.session_state.board

# 버튼 UI
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("⬆️ 위"):
        new_board = move_up(board)
        if new_board != board:
            board[:] = new_board
            add_new_tile(board)
with col2:
    if st.button("⬇️ 아래"):
        new_board = move_down(board)
        if new_board != board:
            board[:] = new_board
            add_new_tile(board)
with col3:
    if st.button("🔄 새 게임"):
        st.session_state.board = init_board()
        board = st.session_state.board

col4, col5 = st.columns([1,1])
with col4:
    if st.button("⬅️ 왼쪽"):
        new_board = move_left(board)
        if new_board != board:
            board[:] = new_board
            add_new_tile(board)
with col5:
    if st.button("➡️ 오른쪽"):
        new_board = move_right(board)
        if new_board != board:
            board[:] = new_board
            add_new_tile(board)

# 보드 출력
for row in board:
    st.write(" | ".join(str(x) if x != 0 else "." for x in row))

if not can_move(board):
    st.error("Game Over! 😢 새 게임 버튼을 눌러 다시 시작하세요.")

