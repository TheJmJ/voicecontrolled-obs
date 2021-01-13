# Done by following https://realpython.com/python-speech-recognition/
# Depends on pyaudio, pocketsphinx and SpeechRecognition
import speech_recognition as sr

def recognizeSpeech(recognizer, mic):
    # Method for recognizing the speech from the given mic and recognizer

    # Returns a dictionary with 3 keys:
    # "success":        a boolean indicating whether or not the API request was
    #                   successful
    # "error":          `None` if no error occured, otherwise a string containing
    #                   an error message if the API could not be reached or
    #                   speech was unrecognizable
    # "transcription":  `None` if speech could not be transcribed,
    #                   otherwise a string containing the transcribed text
    
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(mic, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with mic as source:
        #recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response
    response = {
        "success": True,
        "error": None,
        "text": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["text"] = recognizer.recognize_sphinx(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

# Recognizer APIS Cheat-Sheet
# recognize_sphinx(): CMU Sphinx - requires installing PocketSphinx
# # Works offline, will give questionable results, however
# Other APIs seem to have limited calls

print('using SpeechRecognition version: ' + sr.__version__)

# set the list of words, maxnumber of guesses, and prompt limit
WORDS = ["cheese", "communism"]

# create recognizer and mic instances
recognizer = sr.Recognizer()
microphone = sr.Microphone()

a = 1

while (a==1):
    print('Listening for a prompt again!')
    guess = recognizeSpeech(recognizer, microphone)

    #Success checking
    if guess["text"]:
        print("Heard speech!")
        #break
    if not guess["success"]:
        continue
    print("There was no prompt.")

    # if there was an error, stop the game by breaking from while loop
    if guess["error"]:
        print("ERROR: {}".format(guess["error"]))
        continue
    
    # If we have managed to get to this point, we have
    # # Not hit an error
    # # There's some text that has been understood through mic
    contains_trigger_word = False
    for word in WORDS:
        if word.lower() in guess["text"].lower():
            contains_trigger_word = True
            print("found: " + word)
            break

    if contains_trigger_word:
        print("Found a triggerword!")
    else:
        print("Didn't find a trigger word in: \n\t-" + guess["text"])