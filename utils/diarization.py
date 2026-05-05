import whisperx


def load_models(device="cpu"):
    """Charge Whisper + WhisperX + modèle de diarisation."""
    model = whisperx.load_model("medium", device)
    diarize_model = whisperx.DiarizationPipeline(device=device)
    return model, diarize_model


def run_diarization(model, diarize_model, audio_path):
    """Exécute la diarisation complète."""
    audio = whisperx.load_audio(audio_path)

    # Transcription
    result = model.transcribe(audio)

    # Alignement
    model_a, metadata = whisperx.load_align_model(
        language_code=result["language"], device="cpu"
    )
    result_aligned = whisperx.align(
        result["segments"], model_a, metadata, audio, device="cpu"
    )

    # Diarisation
    diarization = diarize_model(audio)

    # Fusion
    result_final = whisperx.assign_word_speakers(diarization, result_aligned)

    return result_final

