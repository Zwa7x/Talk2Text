import streamlit as st
from utils.audio_tools import load_audio, trim_audio, save_temp_wav
from utils.diarization import load_models, run_diarization


st.set_page_config(page_title="Talk2Text – Diarisation", layout="centered")
st.title("🗣️ Talk2Text – Diarisation Audio")
st.write("Upload un fichier audio, coupe-le si besoin, puis lance la diarisation.")


# Upload
audio_file = st.file_uploader("Choisir un fichier audio", type=["wav", "mp3", "m4a", "flac"])

if audio_file:
    waveform, sr = load_audio(audio_file)
    duration = waveform.shape[1] / sr

    st.audio(audio_file)
    st.write(f"Durée : **{duration:.1f} sec**")

    # Découpe optionnelle
    st.subheader("✂️ Découper l'audio (optionnel)")
    start_sec, end_sec = st.slider(
        "Plage à analyser",
        0.0, float(duration),
        (0.0, float(duration)),
        step=0.1
    )

    trimmed = trim_audio(waveform, sr, start_sec, end_sec)
    trimmed_duration = trimmed.shape[1] / sr
    st.write(f"Durée après découpe : **{trimmed_duration:.1f} sec**")

    if st.button("🚀 Lancer la diarisation"):
        with st.spinner("Chargement des modèles…"):
            model, diarize_model = load_models()

        with st.spinner("Analyse en cours…"):
            temp_path = save_temp_wav(trimmed, sr)
            result = run_diarization(model, diarize_model, temp_path)

        st.success("Diarisation terminée !")

        # Affichage
        st.subheader("📋 Résultats")
        st.json(result)

        # Export JSON
        import json
        st.download_button(
            "📥 Télécharger le JSON",
            data=json.dumps(result, indent=2, ensure_ascii=False),
            file_name="diarisation.json",
            mime="application/json"
        )
