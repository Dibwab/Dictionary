import json
import difflib
from difflib import get_close_matches
data= json.load(open("data.json"))
def translate(w):
    w=w.lower()
    if(w in data):
        return(data[w])
    elif len(get_close_matches(w,data.keys()))>0:
        x=input("Do you mean %s instead? Y or N :  " % get_close_matches(w,data.keys())[0])
        if (x =='Y'or x =='y'):
            return translate(get_close_matches(w,data.keys())[0])
        else:
            print("Try again")
    else:
        return("No such word found")
y='Y'
while(y=='Y'or y=='y'):
    word=input("Enter word: ")
    print(translate(word))
    y=input("Do you wanna search for another word? Y or N :  ")
