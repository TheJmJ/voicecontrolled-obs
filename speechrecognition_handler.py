import speech_recognition as sr

def selectMicrophone():
    miclist = sr.Microphone.list_microphone_names()

    for x in range(len(miclist)):
        print("["+ str(x) +"]" + miclist[x])

    print("Enter your mic of choice:")
    choice = int(input())
    return choice

# create recognizer and mic instances
recognizer = sr.Recognizer()
microphone = sr.Microphone(device_index=(selectMicrophone()))

def recognizeSpeech(recognizer, mic):
    # Function for recognizing the speech from the given mic and recognizer

    # Returns a dictionary with 3 keys:
    # "success":        a boolean indicating whether or not the API request was
    #                   successful
    # "error":          `None` if no error occured, otherwise a string containing
    #                   an error message if the API could not be reached or
    #                   speech was unrecognizable
    # "text":           `None` if speech could not be transcribed,
    #                   otherwise a string containing the transcribed text
    # "rawtext":        `None` if speech could not be transcribed,
    #                   otherwise raw undestood text
    # "phase":          The phase of audio recognition
    
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(mic, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with mic as source:
        audio = recognizer.listen(source, phrase_time_limit=5)

    # set up the response
    response = {
        "success": True,
        "error": None,
        "text": None,
        "rawtext": None,
        "phase": 0
    }

    # Recognizer APIS Cheat-Sheet
    # recognize_sphinx(): CMU Sphinx - requires installing PocketSphinx
    # # Works offline, will give questionable results, however
    # Other APIs seem to have limited calls

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        print("Done listening, trying to recognize speech")
        response["rawtext"] = recognizer.recognize_sphinx(audio)
        print("\traw: " + response["rawtext"])
        response["phase"] = 1
        response["text"] = recognizer.recognize_sphinx(audio, keyword_entries=[("cheers", 0.97), ("bottoms up", 1.0), ("adjust ambience", 1)])
        response["phase"] = 2
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech at phase " + str(response["phase"])

    if response["error"] is None:
        # Hard code for ambient noise adjustment
        if "adjust ambience" in response["text"].lower():
            print("\t\tAdjusting for ambient noise")
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
            print("\t\tDone adjusting for ambient noise")

    return response
