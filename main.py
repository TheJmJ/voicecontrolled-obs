# Done by help of https://realpython.com/python-speech-recognition/
# simpleobsws api https://github.com/Palakis/obs-websocket/blob/4.x-current/docs/generated/protocol.md
# Depends on pyaudio, pocketsphinx, SpeechRecognition, simpleobsws
import simpleobsws as obsws
import asyncio
import speechrecognition_handler as sr

async def sendRequest(request):
    "async method for sending a request to the OBS-Websocket"
    await ws.connect() # connect to the OBS-Websocket
    result = await ws.call(request) # Make a request for StartReplayBuffer
    if result['status'] == 'error':
        print ("\tWebsocket Result:" + str(result))
    await ws.disconnect() # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events.

# set the list of triggerwords, and their respected requests
# Format: 'KEYWORD': {'OBSRequest', KeywordSensitivity}
#               Keyword
#               OBSRequest is the direct request we send to OBS with ws.call(request) command
#               KeywordSensitivity sets the keyword sensitivity where 0 is the most inprecise, 1.0 the most precise
commandDictionary = {
    'cheers': ['SaveReplayBuffer', 0.95],
    'bottoms up': ['SaveReplayBuffer', 1.0]
}

#keyword_dictionary = []
#for x in range(len(commandDictionary)):
#    keyword_dictionary[commandDictionary[x]] = commandDictionary[x][1]

#sr.initKeywordTuples(keyword_dictionary)
#sr.initKeywordTuples(keyword_dictionary = {list(commandDictionary)[x]:commandDictionary[x][1] for x in range(len(commandDictionary))})
sr.initKeywordTuples(keyword_dictionary={k:v[1] for k,v in commandDictionary.items()})

# Create the websocket stuff for OBS
loop = asyncio.get_event_loop()
ws = obsws.obsws(host='127.0.0.1', port=4444, password='plzNoHackerino', loop=loop) # Every possible argument has been passed, but none are required. See lib code for defaults.

# Start the ReplayBuffer
loop.run_until_complete(sendRequest("StartReplayBuffer"))

while (True):
    print('\nListening for a prompt again!')
    guess = sr.recognizeSpeech(sr.recognizer, sr.microphone)

    # if there was an error, skip the loop and retry
    if guess["error"]:
        #if guess["phase"] < 1:
        print("ERROR: {}".format(guess["error"]))
        #else:
            #print("\traw: " + guess["rawtext"])
        continue
    
    # If we have managed to get to this point, we have
    # # Not hit an error
    # # There's some text that has been understood through mic
    contains_trigger_word = None
    for word in commandDictionary.keys():
        if word.lower() in guess["text"].lower():
            contains_trigger_word = word.lower()
            print("\tfound: " + word)
            break

    if contains_trigger_word:
        print("Found a triggerword!")
        print("\t" + guess["text"])
        loop.run_until_complete(sendRequest(commandDictionary[contains_trigger_word][0]))
    else:
        print("Didn't find a trigger word in: \n\t-" + guess["rawtext"])