import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="2048 Game", layout="centered")

# --- 게임 로직 함수 ---
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
if "key_pressed" not in st.session_state:
    st.session_state.key_pressed = None

board = st.session_state.board

# --- UI 출력 ---
st.title("🎮 2048 Game (Keyboard Version)")
st.write(f"**Score:** {st.session_state.score}")
st.table(board)

# --- JavaScript 키 입력 감지 ---
key_event = st.components.v1.html(
    """
    <script>
    const streamlitDoc = window.parent.document;
    streamlitDoc.addEventListener('keydown', function(e) {
        const key = e.key;
        if (['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(key)) {
            window.parent.postMessage({ keyPressed: key }, '*');
        }
    });
    </script>
    """,
    height=0,
)

# --- 키 입력 처리 ---
message = st.experimental_get_query_params()
if "_st_msg" in message:
    st.session_state.key_pressed = message["_st_msg"][0]

# Streamlit의 프론트엔드에서 오는 메시지를 처리하기 위한 custom JS listener
st.components.v1.html(
    """
    <script>
    window.addEventListener('message', (event) => {
        const key = event.data.keyPressed;
        if (key) {
            const params = new URLSearchParams(window.location.search);
            params.set('_st_msg', key);
            window.location.search = params.toString();
        }
    });
    </script>
    """,
    height=0,
)

# --- 실제 키 입력으로 보드 이동 ---
key = st.session_state.key_pressed

if key:
    moved = False
    if key == "ArrowLeft":
        new_board, score = move_left(board)
        moved = True
    elif key == "ArrowRight":
        new_board, score = move_right(board)
        moved = True
    elif key == "ArrowUp":
        new_board, score = move_up(board)
        moved = True
    elif key == "ArrowDown":
        new_board, score = move_down(board)
        moved = True
    else:
        new_board, score = board, 0

    if moved and not np.array_equal(board, new_board):
        st.session_state.board = add_new_tile(new_board)
        st.session_state.score += score
        st.session_state.key_pressed = None
        st.experimental_rerun()

# --- 게임 오버 처리 ---
if game_over(st.session_state.board):
    st.error("💀 Game Over! Press R to restart or click the button below.")

# --- 새 게임 버튼 ---
if st.button("🔄 New Game"):
    st.session_state.board = new_game()
    st.session_state.score = 0
    st.session_state.key_pressed = None
    st.experimental_rerun()
