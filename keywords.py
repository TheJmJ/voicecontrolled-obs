# set the list of keywords, and their respected requests
# Format: 'KEYWORD': {'OBSRequest', KeywordSensitivity}
#           Keyword is the word the SpeechRecognition is looking for (Needs to exist in dictionary)
#           OBSRequest is the direct request we send to OBS with ws.call(request) command
#           KeywordSensitivity sets the keyword sensitivity where 0 is the most inprecise, 1.0 the most precise
#       Request format:
#           No data:    [ <RequestName> ]
#           With data:  [ <RequestName>, {<data>} ]
#               where data: <'REQUESTFIELDNAME':VALUE>

keywordDictionary = {
    'cheers': ['SaveReplayBuffer', 0.95],
    'bottoms up': ['SaveReplayBuffer', 1.0],
    'bananas are long oranges': [ ['GetSourceFilters', {'sourceName':'webcam'}], 0.9 ],
    'pineapple': ['GetVideoInfo', 0.7]
}