import streamlit as st
import websockets
import asyncio
import json
import base64
import pyaudio
from configure import api_key
from dalle import create_and_show_images

if "text" not in st.session_state:
    st.session_state["text"] = ""
    st.session_state["run"] = False
    
st.title("DALL-E Mini")

def start_listening():
    st.session_state["run"] = True
    
st.button("Say something", on_click=start_listening)

text = st.text_input("What should I create?", value=st.session_state["text"])

num_images = st.slider("How many images?", 1, 6)

ok = st.button("GO!")

if ok and text:
    create_and_show_images(text, num_images)
    
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
 
# starts recording
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

async def send_receive():
    print(f'Connecting websocket to url ${URL}')

    async with websockets.connect(
		URL,
		extra_headers=(("Authorization", api_key),),
		ping_interval=5,
		ping_timeout=20
	) as _ws:

        r = await asyncio.sleep(0.1)
        print("Receiving Session begins ...")

        session_begins = await _ws.recv()

        async def send():
            while st.session_state['run']:      
                try:
                    data = stream.read(FRAMES_PER_BUFFER)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data":str(data)})
                    r = await _ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    print(e)
                    assert False, "Not a websocket 4008 error"

                r = await asyncio.sleep(0.01)


        async def receive():
            while st.session_state['run']:
                try:
                    result_str = await _ws.recv()
                    result = json.loads(result_str)['text']
                    
                    if json.loads(result_str)['message_type'] == 'FinalTranscript':
                        result = result.replace('.', '')
                        result = result.replace('!', '')
                        st.session_state['text'] = result
                        st.session_state['run'] = False
                        st.experimental_rerun()
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    print(e)
                    assert False, "Not a websocket 4008 error"
			
        send_result, receive_result = await asyncio.gather(send(), receive())


asyncio.run(send_receive())
