# voicecontrolled-obs
A Python program that listens to your voice and tries to detect 
any keyword and execute a Request that is tied to the keyword through 
OBS recording software's obs-websocket plugin.

## Requirements
[obs-websocket plugin](https://obsproject.com/forum/resources/obs-websocket-remote-control-obs-studio-from-websockets.466/)

python dependencies:
[simpleobsws](), [speech_recognition](https://pypi.org/project/SpeechRecognition/), [PyAudio](https://pypi.org/project/PyAudio/#description), [PocketSphinx](https://pypi.org/project/pocketsphinx/)

Quick Dependencies install:
```
python -m pip install simpleobsws
python -m pip install SpeechRecognition
python -m pip install PyAudio
python -m pip install --upgrade pocketsphinx
```

## Setup
To setup the keywords and requests, look into requests.py file and read the examples.
To look into all the possible requests, refer to this documentation on 
[obs-websocket github page](https://github.com/Palakis/obs-websocket/blob/4.x-current/docs/generated/protocol.md) 
