# app.py
import streamlit as st
import time
import logging

st.set_page_config(page_title="Talk2Text", layout="centered")
st.title("Talk2Text")

# Affichage immédiat pour debug démarrage
st.write("Démarrage de l'application...")

# Logger simple pour voir les étapes dans les logs
logger = logging.getLogger("talk2text")
logger.setLevel(logging.INFO)

# Indiquer l'état de l'environnement avant imports lourds
st.write("Vérification des imports légers OK")

# Fonction pour charger les dépendances lourdes et le modèle
@st.cache_resource
def load_model(model_name: str = "small"):
    logger.info("Début du chargement du modèle")
    st.write("Chargement du modèle audio, cela peut prendre quelques secondes...")
    # Importer ici pour éviter le blocage au démarrage
    try:
        import torch
        import torchaudio
        import whisperx
    except Exception as e:
        logger.exception("Erreur lors de l'import des dépendances lourdes")
        raise

    # Exemple d'appel à whisperx, adapter selon ton usage réel
    try:
        model = whisperx.load_model(model_name)
    except Exception as e:
        logger.exception("Erreur lors du chargement du modèle whisperx")
        raise
    logger.info("Modèle chargé")
    return model

# Interface utilisateur minimale
st.sidebar.header("Paramètres")
model_choice = st.sidebar.selectbox("Choisir le modèle", ["tiny", "small", "medium"], index=1)
use_lazy = st.sidebar.checkbox("Charger le modèle à la demande", value=True)

st.write("Prêt. Choisissez une action.")

if st.button("Tester démarrage rapide"):
    st.write("L'application répond correctement.")

# Bouton pour charger et tester le modèle
if st.button("Charger le modèle maintenant"):
    with st.spinner("Chargement en cours..."):
        try:
            model = load_model(model_choice)
            st.success("Modèle chargé avec succès")
        except Exception as e:
            st.error(f"Échec du chargement du modèle: {e}")
            st.write("Consulte les logs pour plus de détails")

# Exemple de zone pour uploader un fichier audio et lancer la transcription
uploaded_file = st.file_uploader("Dépose un fichier audio pour transcrire", type=["wav","mp3","m4a"])
if uploaded_file is not None:
    st.write("Fichier reçu:", uploaded_file.name)
    if st.button("Transcrire le fichier"):
        with st.spinner("Transcription en cours..."):
            try:
                model = load_model(model_choice)
                # Remplace la ligne suivante par ton pipeline whisperx réel
                st.write("Ici tu appellerais la fonction de transcription avec le modèle chargé")
                time.sleep(1)
                st.success("Transcription terminée (exemple)")
            except Exception as e:
                st.error(f"Erreur pendant la transcription: {e}")
