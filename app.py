import streamlit as st

st.set_page_config(page_title="Kruisje en nulletje", page_icon="⭕", layout="centered")


def init_game() -> None:
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = ""
    st.session_state.game_over = False


def check_winner(board: list[str]) -> str:
    winning_lines = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]

    for a, b, c in winning_lines:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if all(board):
        return "gelijkspel"

    return ""


def play_move(index: int) -> None:
    if st.session_state.game_over or st.session_state.board[index]:
        return

    st.session_state.board[index] = st.session_state.current_player
    result = check_winner(st.session_state.board)

    if result:
        st.session_state.game_over = True
        st.session_state.winner = result
    else:
        st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"


if "board" not in st.session_state:
    init_game()

st.title("🎮 Tic-tac-toe (kruisje en nulletje)")
st.write("Speel met z'n tweeën op hetzelfde scherm.")

if st.session_state.game_over:
    if st.session_state.winner == "gelijkspel":
        st.success("Het is gelijkspel!")
    else:
        st.success(f"Speler {st.session_state.winner} wint! 🏆")
else:
    st.info(f"Beurt: speler {st.session_state.current_player}")

for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        i = row * 3 + col
        label = st.session_state.board[i] if st.session_state.board[i] else " "
        cols[col].button(
            label,
            key=f"cell_{i}",
            on_click=play_move,
            args=(i,),
            use_container_width=True,
        )

st.button("🔄 Nieuw spel", on_click=init_game, use_container_width=True)
