import streamlit as st
import pandas as pd

st.title("Kérdésbank feltöltése")

st.write("Töltsd fel azt az Excel fájlt, amely tartalmazza a szóbelin használt kérdéseket. A fájlnak tartalmaznia kell egy **'Kérdések'** nevű munkalapot, illetve külön oszlopokban kell tartalmaznia a külön típusú kérdéseket, **'{i}. Kérdés: '** elnevezéssel.")

uploaded_file = st.file_uploader("Excel fájl kiválasztása", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Kérdések", engine="openpyxl", names = ['1. kérdés: ', '2. kérdés: ', '3. kérdés: ', '4. kérdés: ', '5. kérdés: ', '6. kérdés: '])
        st.session_state.questions = df

        st.success("A kérdéseket tartalmazó fájl sikeresen betöltve.")
        st.write("Első néhány sor a betöltött kérdésekből:")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Hiba történt a fájl beolvasása során: {e}")
else:
    st.info("Kérlek, tölts fel egy .xlsx fájlt a kérdések beolvasásához.")
