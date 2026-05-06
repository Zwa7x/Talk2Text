# app.py
import streamlit as st
import logging
import time
import importlib

st.set_page_config(page_title="Talk2Text", layout="centered")
st.title("Talk2Text")

logger = logging.getLogger("talk2text")
logger.setLevel(logging.INFO)

st.write("Démarrage de l'application… (interface prête même si les modèles ne sont pas installés)")

def check_optional_packages():
    info = {"torch": False, "torchaudio": False, "whisper": False, "whisperx": False}
    for pkg in list(info.keys()):
        try:
            importlib.import_module(pkg)
            info[pkg] = True
        except Exception:
            info[pkg] = False
    return info

pkg_info = check_optional_packages()
st.write("Dépendances détectées :", pkg_info)

@st.cache_resource
def load_model_safe(model_name: str = "small"):
    try:
        import whisperx
        model = whisperx.load_model(model_name)
        return model
    except Exception as e:
        raise RuntimeError(f"Impossible de charger whisperx: {e}")

st.sidebar.header("Paramètres")
model_choice = st.sidebar.selectbox("Choisir le modèle (si installé)", ["tiny", "small", "medium"], index=1)

st.write("L'application est prête. Si les paquets lourds ne sont pas installés, la transcription ne fonctionnera pas ici.")

if st.button("Tester l'interface"):
    st.success("Interface OK — l'app répond.")

uploaded_file = st.file_uploader("Dépose un fichier audio pour transcrire", type=["wav","mp3","m4a"])
if uploaded_file is not None:
    st.write("Fichier reçu:", uploaded_file.name)
    if st.button("Transcrire le fichier"):
        if not pkg_info.get("whisperx", False):
            st.error("Le paquet whisperx (ou ses dépendances) n'est pas installé sur ce serveur.")
            st.info("Options : 1) Déployer sur un environnement compatible 2) Utiliser une API distante 3) Installer les paquets et redéployer.")
        else:
            with st.spinner("Chargement du modèle et transcription..."):
                try:
                    model = load_model_safe(model_choice)
                    time.sleep(1)
                    st.success("Transcription terminée (exemple).")
                except Exception as e:
                    st.error(f"Erreur pendant la transcription: {e}")
