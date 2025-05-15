import time
import bcrypt
import streamlit as st
import pandas as pd

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def welcome():
    st.title('Üdv!')

    #st.sidebar.subheader("Counter - Strike: Analytics")
    #st.sidebar.image('logo.png')


    with st.expander("Erről az oldalról"):
        st.write("Ez egy demo alkalmazás, ami a ChatGPT segítségével készült.")
        st.write("Lehetővé teszi egy tantárgyon tartott szóbeli vizsgák lebonyolítását.")

    #st.file_uploader('Testing config.toml')
    #st.write(f"testing secrets.toml: {st.secrets['test']}")

def login():
    @st.dialog("Belépés 🔑")
    def login_auth():
        with st.form("my_form", border=False):
            auth_code = st.text_input("Kérlek írd be az autentikációs kódot", help = "Kérlek írd be az autentikációs kódot a belépéshez")# type = "password", 
            if st.form_submit_button("Belépés"):
                if bcrypt.checkpw(auth_code.encode('utf-8'), st.secrets['auth_key_hash'].encode("utf-8")):
                    st.success("Sikeres belépés...átirányítás 3 mp-en belül", icon = ":material/check_circle:")
                    time.sleep(3)
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    invalid = st.error("Érvénytelen belépés, kérlek próbáld újra!", icon=":material/priority_high:")
                    


    st.info("Az alkalmazásba történő belépéshez nyomd meg a lenti gombot!", icon=":material/info:")

    #st.sidebar.image('logo.png')
    
    if st.button("Belépés 🔑"):
        login_auth()

def logout():
    st.info("Az alkalmazásból történő kilépéshez nyomd meg a lenti gombot!", icon=":material/info:")
    if st.button("Kijelentkezés ❌"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Bejelentkezés", icon=":material/login:")
logout_page = st.Page(logout, title="Kijelentkezés", icon=":material/logout:")

# default layout settings
st.set_page_config(layout="wide",page_title='Szóbeliztető Webapp', page_icon='logo.png')
st.markdown(
    """
    <style>
    * {
        font-family: 'Georgia', serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.sidebar.subheader("data_exam_app")

#pg = st.navigation([st.Page(page1), st.Page(page2)])
if st.session_state.logged_in:
    pg = st.navigation(
            {
                "Vizsgáztatás": [st.Page("pages_py/exam_session.py", title = "Vizsga Indítása", icon=":material/slow_motion_video:")],
                "Kérdések": [st.Page("pages_py/questions_page.py", title = "Kérdések beállítása", icon=":material/quiz:")],
                # "Past Exams": [st.Page("pages_py/past_exams.py", title = "Past Exams", icon=":material/history:")],
                "Kijelentkezés": [logout_page]
            }
        )
else:
    pg = st.navigation([st.Page(welcome, title="Üdv!", default=True, icon = ":material/waving_hand:"),login_page])
pg.run()
st.sidebar.image('logo.png')
st.sidebar.info("Demo verzió...", icon=":material/warning:")


