import json
import difflib
from difflib import get_close_matches
data= json.load(open("data.json"))
def translate(w):
    w=w.lower()
    if(w in data):
        return(translate(w))
    elif len(get_close_matches(w,data.keys()))>0:
        x=import("Did you mean %s instead? Y or N" % get_close_matches(w,data.keys())[0])
        if x=='Y'||x=='y':
            return translate(get_close_matches(w,data.keys())[0]))
        else:
            print("Try again")
    else:
        return("No such word found")
y='N'
while():
    word=import("Enter word: ")
    print(translate(word))
    y=import("Do you wanna search for another word? Y or N")
