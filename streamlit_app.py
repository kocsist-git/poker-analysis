import streamlit as st
import pandas as pd

# A rangok sorrendje (A-tól 2-ig)
RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

def create_poker_matrix():
    """Létrehozza a 13x13-as range mátrixot Pandas DataFrame formájában."""
    matrix_data = {}
    
    for r1_index, r1 in enumerate(RANKS):
        row_data = {}
        for r2_index, r2 in enumerate(RANKS):
            hand = ""
            if r1_index == r2_index:
                # Pár (Pl. AA, 88) - Ezen az átlón vannak
                hand = f"{r1}{r1}"
            elif r1_index < r2_index:
                # Offsuit (o) (Pl. AKo, JTo) - A főátló alatt vannak
                hand = f"{r2}{r1}o"
            else:
                # Suited (s) (Pl. AKs, JTs) - A főátló felett vannak
                hand = f"{r1}{r2}s"
            
            # Megjegyzés: A szokásos mátrix megjelenítéshez megcseréltük az 'o' és 's' pozícióját
            # hogy a suited lapok legyenek a jobb felső háromszögben.
            if r1_index < r2_index:
                hand = f"{r1}{r2}o" # Pl. K. A alatti sor, A. K o
            elif r1_index > r2_index:
                hand = f"{r2}{r1}s" # Pl. A. K alatti sor, K. A s
            
            row_data[r2] = hand
        matrix_data[r1] = row_data

    # A Pandas DataFrame létrehozása. Transzponáljuk, hogy a nagyobb rangok legyenek a bal felső sarokban.
    matrix_df = pd.DataFrame(matrix_data).T.fillna('')
    return matrix_df

def highlight_range(hand_cell):
    """
    Egy színező függvény a Pandas-hoz.
    A színezés logikája: párok (kék), suited (sárga), offsuit (piros).
    """
    hand = hand_cell.iloc[0] # Minden mező egy DataFrame Series-ként érkezik
    color = 'lightgray'
    
    if hand.endswith('s'):
        color = '#FFFFB3'  # Halvány sárga (Suited)
    elif hand.endswith('o'):
        color = '#FFB3B3'  # Halvány piros (Offsuit)
    elif len(hand) == 2 and hand[0] == hand[1]:
        color = '#B3B3FF'  # Halvány kék (Párok)
        
    return [f'background-color: {color}'] * len(hand_cell)

# ----------------- STREAMLIT ALKALMAZÁS INDÍTÁSA -----------------

st.title("♦️ Alap Range Mátrix")
st.markdown("Kezdésként építsük fel a $13 \\times 13$-as mátrixot a póker kezekkel.")

# A mátrix generálása
matrix = create_poker_matrix()

# A színezés alkalmazása (ez adja a képen látható alap kinézetet)
styled_matrix = matrix.style.apply(highlight_range, axis=1)

# Megjelenítés a Streamlit felületen
st.dataframe(
    styled_matrix, 
    use_container_width=True, # Hogy a mátrix kitöltse a rendelkezésre álló szélességet
    height=550 # Állítsunk be fix magasságot, hogy a 13 sor látszódjon
)

st.caption("A mátrix cellái automatikusan színeződtek a leosztás típusa szerint: Kék=Párok, Sárga=Suited, Piros=Offsuit.")

st.markdown("""---""")