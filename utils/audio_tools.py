import torchaudio
import soundfile as sf
import numpy as np
import tempfile


def load_audio(file):
    """Charge un fichier audio en waveform + sample rate."""
    waveform, sr = torchaudio.load(file)
    return waveform, sr


def trim_audio(waveform, sr, start_sec, end_sec):
    """Découpe un waveform entre deux timestamps."""
    start_idx = int(start_sec * sr)
    end_idx = int(end_sec * sr)
    return waveform[:, start_idx:end_idx]


def save_temp_wav(waveform, sr):
    """Sauvegarde un waveform dans un fichier WAV temporaire."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        path = tmp.name
        audio_np = waveform.squeeze(0).numpy()
        sf.write(path, audio_np, sr)
    return path
