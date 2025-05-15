import streamlit as st
import pandas as pd
import random
import time
from io import StringIO
from datetime import datetime

st.title("Szóbeli vizsga indítása")

# Ellenőrzés: kérdésbank betöltve?
if "questions" not in st.session_state or st.session_state.questions is None:
    st.error("Először töltsd fel a kérdésbankot a 'Kérdésbank feltöltése' oldalon.")
    st.stop()

# Vizsga még nem indult → kérjük be az adatokat
if not st.session_state.get("questions_generated", False):
    name = st.text_input("Hallgató neve")
    neptun = st.text_input("Neptun-kód (6 karakter)", max_chars=6)

    if name and neptun:
        if st.button("Vizsga indítása (kérdések generálása)"):
            df = st.session_state.questions
            kérdések = {}
            for idx, col in enumerate(df.columns):
                kérdés_lista = df[col].dropna().tolist()
                if kérdés_lista:
                    kérdések[f"{idx + 1}. kérdés"] = random.choice(kérdés_lista)
                else:
                    kérdések[f"{idx + 1}. kérdés"] = "Nincs kérdés ebben a típusban"

            start_time_human = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # CSV fájl tartalom
            csv_df = pd.DataFrame({
                "Név": [name],
                "Neptun": [neptun],
                "Vizsga kezdete": [start_time_human],
                **{k: [v] for k, v in kérdések.items()}
            })

            output = StringIO()
            csv_df.to_csv(output, index=False, encoding="utf-8")
            csv_content = output.getvalue()

            st.session_state.generated_questions = kérdések
            st.session_state.csv_content = csv_content
            st.session_state.name = name
            st.session_state.neptun = neptun
            st.session_state.questions_generated = True
            st.rerun()

# Kérdések generálva, vizsga még nem fut → jelenítsük meg
elif st.session_state.get("questions_generated", False) and not st.session_state.get("exam_started", False):
    st.success("A kérdések generálva lettek. Töltsd le a vizsga dokumentumát, majd indítsd el a vizsgát.")
    st.download_button(
        label="Kérdések mentése CSV fájlba",
        data=st.session_state.csv_content,
        file_name=f"{st.session_state.neptun}_vizsga.csv",
        mime="text/csv"
    )

    # Kérdések táblázatos megjelenítése
    st.subheader("Kérdések:")
    questions = st.session_state.generated_questions
    markdown_table = "| Kérdés sorszáma | Kérdés |\n|---|---|\n"
    for qtype, qtext in questions.items():
        markdown_table += f"| {qtype} | {qtext} |\n"
    st.markdown(markdown_table)

    if st.button("Vizsga elkezdése"):
        st.session_state.start_time = time.time()
        st.session_state.exam_started = True
        st.rerun()

# Vizsga fut → időzítő elindul
elif st.session_state.get("exam_started", False):
    timer_placeholder = st.empty()
    question_placeholder = st.empty()
    end_button_placeholder = st.empty()

    total_time = 600  # 10 perc

    with end_button_placeholder:
        if st.button("Vizsga befejezése", key="end_exam_button"):
            st.session_state.exam_started = False
            st.session_state.questions_generated = False
            st.success("Vizsga lezárva.")
            st.stop()

    while True:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, total_time - elapsed)

        with timer_placeholder.container():
            st.info(f"Hátralévő idő: {int(remaining // 60)} perc {int(remaining % 60)} másodperc")
            st.progress((total_time - remaining) / total_time)

        with question_placeholder.container():
            st.subheader("Kérdések:")
            questions = st.session_state.generated_questions
            markdown_table = "| Kérdés sorszáma | Kérdés |\n|---|---|\n"
            for qtype, qtext in questions.items():
                markdown_table += f"| {qtype} | {qtext} |\n"
            st.markdown(markdown_table)

        if remaining <= 0:
            st.warning("Lejárt az idő!")
            st.session_state.exam_started = False
            st.session_state.questions_generated = False
            st.stop()

        time.sleep(1)
        timer_placeholder.empty()
        question_placeholder.empty()
