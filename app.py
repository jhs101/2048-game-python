import streamlit as st
import random
import os

SIZE = 4

# ---------- 이미지 경로 매핑 ----------

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
    new_row += [0] * (SIZE - len(new_row))
    return new_row

def merge(row):
    score = 0
    for i in range(SIZE - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            score += row[i]
            row[i + 1] = 0
    return row, score

def move_left(board):
    new_board = []
    total_score = 0
    for row in board:
        row = compress(row)
        row, s = merge(row)
        total_score += s
        row = compress(row)
        new_board.append(row)
    return new_board, total_score

def move_right(board):
    reversed_board = [row[::-1] for row in board]
    moved, s = move_left(reversed_board)
    moved = [row[::-1] for row in moved]
    return moved, s

def transpose(board):
    return [list(row) for row in zip(*board)]

def move_up(board):
    trans = transpose(board)
    moved, s = move_left(trans)
    return transpose(moved), s

def move_down(board):
    trans = transpose(board)
    moved, s = move_right(trans)
    return transpose(moved), s

def can_move(board):
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0:
                return True
            if j < SIZE - 1 and board[i][j] == board[i][j + 1]:
                return True
            if i < SIZE - 1 and board[i][j] == board[i + 1][j]:
                return True
    return False

# ---------- UI ----------
st.title("2048")

if "board" not in st.session_state:
    st.session_state.board = init_board()
if "score" not in st.session_state:
    st.session_state.score = 0
if "best_score" not in st.session_state:
    st.session_state.best_score = 0

# 점수판
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Score", st.session_state.score)
with col2:
    st.metric("Best", st.session_state.best_score)
with col3:
    if st.button("🔄 새 게임"):
        st.session_state.board = init_board()
        st.session_state.score = 0

# ---------- 키 입력 ----------

if key_event:
    new_board, gained = None, 0
    if key_event == "ArrowUp":
        new_board, gained = move_up(st.session_state.board)
    elif key_event == "ArrowDown":
        new_board, gained = move_down(st.session_state.board)
    elif key_event == "ArrowLeft":
        new_board, gained = move_left(st.session_state.board)
    elif key_event == "ArrowRight":
        new_board, gained = move_right(st.session_state.board)

    if new_board and new_board != st.session_state.board:
        st.session_state.board = new_board
        st.session_state.score += gained
        add_new_tile(st.session_state.board)

# ---------- 보드 렌더링 ----------
for row in st.session_state.board:
    cols = st.columns(SIZE)
    for j, val in enumerate(row):
        if val == 0:
            cols[j].markdown("⬜️") # 빈칸
        else:
            if val in IMG_MAP and os.path.exists(IMG_MAP[val]):
                cols[j].image(IMG_MAP[val], use_column_width=True)
            else:
                cols[j].markdown(f"**{val}**")

# 최고 점수 업데이트
if st.session_state.score > st.session_state.best_score:
    st.session_state.best_score = st.session_state.score

# 게임 오버
if not can_move(st.session_state.board):
    st.error("Game Over! 😢 새 게임 버튼을 눌러 다시 시작하세요.")
