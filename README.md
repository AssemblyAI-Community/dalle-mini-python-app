# DALL-E Mini Python App

A Streamlit app based on the [DALL-E Playground](https://github.com/saharmor/dalle-playground), with the frontent part also in Python.

## Installation

```console
$ pip install requests streamlit websockets pyaudio
```

## Backend:
Go to [DALL-E Playground](https://github.com/saharmor/dalle-playground), run the Google Colab, and copy the backend url into [dalle.py](dalle.py).

## Frontend

1. Grab an API Token from [AssemblyAI](https://www.assemblyai.com) and paste it into [configure.py](configure.py).
2. Run

```console
$ streamlit run main.py
```

Note: If you don't want to use speech recognition, use the [no-speech-rec/main.py](no-speech-rec/main.py) file instead.