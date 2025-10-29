import streamlit as st
import numpy as np
import random
from streamlit_key_events import key_events

st.set_page_config(page_title="2048 Game (Keyboard Events)", layout="centered")

# --- 게임 로직 (이전과 동일) ---
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

# --- 세션 초기화 ---
if "board" not in st.session_state:
    st.session_state.board = new_game()
    st.session_state.score = 0

board = st.session_state.board

st.title("🎮 2048 (Arrow Keys)")

st.write("Click anywhere on the page (or the board) once, then use the arrow keys.")
st.write(f"**Score:** {st.session_state.score}")
st.table(board)

# --- streamlit-key-events 사용: 키 이벤트를 가져온다 ---
events = key_events(
    key_list=["ArrowLeft", "ArrowUp", "ArrowRight", "ArrowDown", "r", "R"],
    prompt="Focus the page and press arrow keys (r to restart).",
    use_container_width=True,
)

# events는 최근 이벤트들의 리스트(딕셔너리). 가장 최근 이벤트를 처리.
key_pressed = None
if events and isinstance(events, list) and len(events) > 0:
    # events 예시: [{"key":"ArrowLeft","type":"keydown","modifiers":{...},"time":...}, ...]
    last = events[-1]
    key_pressed = last.get("key")

# --- 키에 따른 이동 처리 ---
if key_pressed:
    moved = False
    if key_pressed in ("ArrowLeft",):
        new_board, score = move_left(board); moved = True
    elif key_pressed in ("ArrowRight",):
        new_board, score = move_right(board); moved = True
    elif key_pressed in ("ArrowUp",):
        new_board, score = move_up(board); moved = True
    elif key_pressed in ("ArrowDown",):
        new_board, score = move_down(board); moved = True
    elif key_pressed in ("r", "R"):
        st.session_state.board = new_game()
        st.session_state.score = 0
        st.experimental_rerun()
    else:
        new_board, score = board, 0

    if moved and not np.array_equal(board, new_board):
        st.session_state.board = add_new_tile(new_board)
        st.session_state.score += score
        st.experimental_rerun()

# --- 게임 오버 표시 및 버튼 ---
if game_over(st.session_state.board):
    st.error("💀 Game Over! Press R to restart or click New Game.")

if st.button("🔄 New Game"):
    st.session_state.board = new_game()
    st.session_state.score = 0
    st.experimental_rerun()
