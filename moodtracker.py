
from openai import OpenAI

moodtrackingsetup = [
    {
        "role": "system",
        "content": "you are an ai assistant created for monitoring bad moods from text with context you return values between 0=normal texts,1=bad mood text, 2= very bad mood text, 3 = very very bad mood text depending on the text you see "
    },
    {
        "role": "user",
        "content": "heyyy\n"
    },
    {
        "role": "assistant",
        "content": "0"
    },
    {
        "role": "user",
        "content": "I hate myself i want to die\n"
    },
    {
        "role": "assistant",
        "content": "2"
    },
    {
        "role": "user",
        "content": "hii"
    },
    {
        "role": "assistant",
        "content": "0"
    },
    {
        "role": "user",
        "content": "i hate everyone"
    },
    {
        "role": "assistant",
        "content": "1"
    },
    {
        "role": "user",
        "content": "I am so tired of life"
    },
    {
        "role": "assistant",
        "content": "1"
    },
    {
        "role": "user",
        "content": "I want to play"
    },
    {
        "role": "assistant",
        "content": "0"
    },
    {
        "role": "user",
        "content": "I want to play with peoples hearts"
    },
    {
        "role": "assistant",
        "content": "0"
    },
    {
        "role": "user",
        "content": "I feel like killing everyone that hurt me then dying myself"
    },
    {
        "role": "assistant",
        "content": "1"
    },
    {
        "role": "user",
        "content": "Thats what i will do tmrw if no one can educate me on why i shouldn't do that"
    },
    {
        "role": "assistant",
        "content": "2"
    },
    {
        "role": "user",
        "content": "when I am done murdering everyone in my class i will sleep with thier dead bodies before i later put a bullet in my own skull"
    },
    {
        "role": "assistant",
        "content": "3"
    },

]
