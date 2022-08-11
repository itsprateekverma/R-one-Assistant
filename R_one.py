#pip install pyttsx3
#pip install speechRecognition
#pip install PyAudio 
#pip install wolframalpha  #for calculator
#pip install random 
#pip install requests 
#pip install datetime        
#pip install http.client     ##as httplib
#pip install bs4        ##import BeautifulSoup
# from cv2 




"""
Its 
# To do- 1. food check
        2. 
        4. rating
        9. cv2
        10. what you eat? , i love you?
"""

import cv2
import time
import pyttsx3 
import speech_recognition as sr 
import datetime
import random
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import http.client as httplib
import wolframalpha

def Httplib(url="www.intigriti.in", timeout=3):
    connection = httplib.HTTPConnection(url, timeout=timeout)
    while True:
        try:
            # only header requested for fast operation
            connection.request("HEAD", "/")
            connection.close()  # connection closed
            return takeCommand()
        except :
            while True: 
                speak('Connect your internet')
                break
            return Httplib("www.intigriti.in", 3)


cred = credentials.Certificate('C:\\Users\\PK\\Downloads\\secret.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://intigriti-robotics.firebaseio.com/" } )

ListenRef = db.reference('Intigrity%20Robotics/Functions/Listen')
SpeakRef = db.reference('Intigrity%20Robotics/Functions/Speak')
SearchRef = db.reference('Intigrity%20Robotics/Functions/Search')
HandShakeRef = db.reference('Intigrity%20Robotics/Functions/Hand Shake')
CommandRef = db.reference('Intigrity%20Robotics/Functions/Command')
StopRef = db.reference('Intigrity%20Robotics/Functions/Stop')

    
    

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
rate = engine.setProperty("rate",170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        r.energy_threshold = 200
        audio = r.listen(source,0,5)
        

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        query=query.lower()
        print(f"User said: {query}\n")

    except Exception as e: 
        print("Say that again please...")  
        return "None"
    query=query.lower()
    return query


def WolfRamAlpha(query):
    apikey = "THU597-4RP389GJ9P"
    requester = wolframalpha.Client(apikey)
    requested = requester.query(query)

    try:
        answer = next(requested.results).text
        return answer
    except:
        speak("The value is not answerable")

def Calc(query):
    Term = str(query)
    Term = Term.replace("r one","")
    Term = Term.replace("multiply","*")
    Term = Term.replace("multiply by","*")
    Term = Term.replace("into","*")

    Term = Term.replace("plus","+")

    Term = Term.replace("minus","-")
    Term = Term.replace("substract","-")
    Term = Term.replace("substract by","-")

    Term = Term.replace("divide","/")
    Term = Term.replace("by","/")
    Term = Term.replace("divide by","*")

    Final = str(Term)
    try:
        result = WolfRamAlpha(Final)
        print(f"{result}")
        speak(result)

    except:
        speak("The value is not answerable")


def news():
    query_params = {
      "source": "bbc-news",
      "sortBy": "top",
      'country': 'in',
      "apiKey": "0f897abafaec441dabc77464b9bc69dd"
    }
    main_url = " https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey=4991ebedb1d3403392a6b4e538988b7f"
    res = requests.get(main_url, params=query_params)
    open_bbc_page = res.json()
    article = open_bbc_page["articles"]
    results = []
    for ar in article:
        results.append(ar["title"])
    for i in range(len(results)):
        print(i + 1, results[i],)
        if i== 2:
            break
    speak(results[0])
    speak(results[1])
    speak(results[2])

def game_play():
    speak("Lets Play ROCK PAPER SCISSORS !!")
    print("LETS PLAYYYYYYYYYYYYYY")
    i = 0
    Me_score = 0
    Com_score = 0
    speak("choose any one.")
    while(i<3):
        choose = ("rock","paper","scissors") #Tuple
        com_choose = random.choice(choose)
        query = Httplib("www.intigriti.in", 3).lower()
        
        if ("rock" in query or "stone" in query):
            if (com_choose == "rock"):
                speak("ROCK")
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            elif (com_choose == "paper"):
                speak("paper")
                Com_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            else:
                speak("Scissors")
                Me_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")

        elif ("paper" in query ):
            if (com_choose == "rock"):
                speak("ROCK")
                Me_score += 1
                print(f"Score:- ME :- {Me_score+1} : COM :- {Com_score}")

            elif (com_choose == "paper"):
                speak("paper")
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            else:
                speak("Scissors")
                Com_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")

        elif ("scissors" in query or "scissor" in query or "caesar"  in query or "teasor" in query):
            if (com_choose == "rock"):
                speak("ROCK")
                Com_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            elif (com_choose == "paper"):
                speak("paper")
                Me_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            else:
                speak("Scissors")
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
        if i<2:
            speak("next round, choose any one.")
        i += 1
    speak(f"FINAL SCORE, your score {Me_score}, my score {Com_score}")
    if Me_score<Com_score:
        speak("hurray, i won! better luck next time")
    elif Me_score>Com_score:
        speak('you win this time.')
    else:
        speak("its a draw")
    print(f"FINAL SCORE :- ME :- {Me_score} : COM :- {Com_score}")

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=3 and hour<12:
        speak("Good Morning")

    elif hour>=12 and hour<16:
        speak("Good Afternoon")   

    else:
        speak("Good Evening")  

    choose = ('Myself R1, developed by Intigrity Robotics. Please tell me how may I help you.',"My name is R1. Please tell me how may I help you or You can order food by speaking, order food",
    "I am R one, Please tell me how may I help you","Myself R1, I'm your friend. Please tell me how may I help you or I can assist you in odering food") 
    com_choose = random.choice(choose)
    speak(com_choose) 


def MainAssistant():

        while True:

            query = Httplib("www.intigriti.in", 3)
            
            if ("armaan" in query or "hello" in query or "urban" in query or "who are you" in query or 
                "r1" in query or " wake up " in query or "arif" in query or 'marvel' in query or 'arun' in query or "karbonn" in query or 
                "help" in query or "arvind" in query or "hai" in query or "hay " in query or "carbon" in query or "karbon" in query or
                "hey " in query or "marbel" in query or "avan" in query or "ravan" in query or 'roman' in query or 'i want' in query or 
                'oven' in query or "marble" in query):
                    # from WishMe import wishMe
                    wishMe()
                    inWakeUp = "1"
                    a=0
                    while True:

                            query = Httplib("www.intigriti.in", 3)
                            ##########################################################################################################################
                            if ("food" in query or"order food" in query or "take order" in query or "order my food" in query or "take my order" in query):
                                a=0
                                query = query.replace("one", "1")
                                query = query.replace("to" or "two" or "too" or'tu' , "2")
                                query = query.replace("free", "3")
                                query = query.replace("for" "four", "4")
                                query = query.replace("six" or "sex", "6")
                                # query = query.replace("take order", "")
                                # query = query.replace("order food", "")
                                speak("what would you like to order?")
                                while True:
                                    
                                    query = Httplib("www.intigriti.in", 3)
                                    query = query.replace("one", "1")
                                    query = query.replace( "two" or "too" or'tu' , "2")
                                    query = query.replace("free", "3")
                                    query = query.replace("for" "four", "4")
                                    query = query.replace("six" or "sex", "6")
                                    x  = SpeakRef.get()

                                    if ('nothing' in query or "i don't" in query or 'nahi' in query or 'sorry' in query):
                                        speak('you are just wasting my time')
                                        break
                                    elif x !="":
                                        speak(SpeakRef.get())
                                        SpeakRef.set("")

                                    elif (CommandRef.get()=="2"):
                                        CommandRef.set("")
                                        break

                                    elif (CommandRef.get()=="1"):
                                        speak("ok")
                                        CommandRef.set("0")
                                        pass
                                    elif (query!="None" and query!="N1"):
                                        speak("processing")
                                        ListenRef.set(query)
                                        while True:
                                            if SpeakRef.get()!="":
                                                speak(SpeakRef.get())
                                                SpeakRef.set("")
                                                break
                                    elif x !="":
                                        speak(SpeakRef.get())
                                        SpeakRef.set("")

                                    
                                        break
                                        
    #############################################################################################################################################      
                                        
                            elif ("pk"in query):#"order " in query or "take order " in query or "order my food " in query or "take my order " in query):
                                a=0
                                ListenRef.set(query)
                                speak("I'm searching you order in our menu.")
                                while True:
                                    if SpeakRef.get()!="":
                                        speak(SpeakRef.get())
                                        SpeakRef.set("")
                                        break
                                while True:
                                    query = Httplib("www.intigriti.in", 3)

                                    if (query=="None"):
                                        speak("I'm waiting to take your next order.")
                                    elif SpeakRef.get()!="":
                                                speak(SpeakRef.get())
                                                SpeakRef.set("")
                                    elif ('no' in query or 'nothing' in query or "i don't" in query or 'nahi' in query or 'sorry' in query):
                                        speak('you are just wasting my time')
                                        break
                                    elif (query!="None"):
                                        ListenRef.set(query)
                                        speak("I'm searching you order in our menu.")
                                        while True:
                                            print("outside loop")
                                            if SpeakRef.get()!="":
                                                print("in loop")
                                                speak(SpeakRef.get())
                                                SpeakRef.set("")
                                                break

    ###############################################################################################################################################

                            elif ("what's menu" in query or "special menu" in query or "special today" in query or "what menu" in query):
                                a=0
                                item=0
                                while True:
                                    menu=[0,1,2,3,4,5,6,7,8]
                                    
                                    if item<3:
                                        q= random.choice(menu)
                                        MenuRef = db.reference(f'Intigrity%20Robotics/Menu/100{q}/Name')
                                        pk=MenuRef.get()
                                        pk=pk.replace("None" or "none", " ")
                                        speak(pk)
                                        # print(pk)
                                        item+=1
                                        # menu.remove(q)
                                        continue
                                    break

                            elif ("hello" in query or "hai" in query or "hay " in query or "hey " in query or "namaste" in query or "handshake" in query):
                                HandShakeRef.set("1")

                            elif (query=="where is my order" or query=="kaha hai mera" or "order kaha hai" in query):
                                speak('If your oder is placed it will take some time, else place your order by saying oder food')

                            elif ('introduce yourself' in query or 'your name' in query or 'about you' in query or 'who are you' in query ):
                                a=0
                                choose = ('Myself R1, developed by Intigrity Robotics',"My name is R1. You can order food by speaking, order food",
                                "Myself R1, I'm your friend, and I can assist you in odering food") 
                                com_choose = random.choice(choose)
                                speak(com_choose) 
                                    
                            
                            elif ('how are you' in query or 'are you fine' in query or 'how is your day' in query ):
                                a=0
                                choose = ("I'm fine, what about you?","I'm good. How are you","I'm fine. you are very kind to ask especially in these tempestuous times",
                                "Thanks for asking, I'm doing ok. A lot is going on in the world today, I hope ou are taking care of yourself") 
                                com_choose = random.choice(choose)
                                speak(com_choose)
                                

                            elif ('developed you' in query or 'your developer' in query or 'your father' in query or 'made you' in query or 'make you'
                                in query or 'invented you' in query or 'designed you' in query or 'design you' in query or "your parents" in query or 
                                "your creator" in query or 'god' in query or 'bhagwan' in query or 'your mother' in query):
                                a=0
                                speak("I'm developed by Intigrity Robotics")

                            elif ('hotel' in query or 'hotel vijay tara' in query or 'vijay tara hotel' in query or 'owner of hotel' in query):
                                a=0
                                choose = ("ower of Hotel vijay tara is Ravishankar Singh, we have palaash multi cuisine restaurant on 4th floor, banquet raj darbar on 2nd floor, town hall in basement, rooms on 3rd and 5th floor and mehfil bar on 5th floor") 
                                # com_choose = random.choice(choose)
                                speak(choose)
                                

                            #what is today's menu/what's special in menu/ what is special in dinner/lunch? 
                            #gk
                            elif(query=="tell me" or query=='search'  or query=="batao"):
                                SpeakRef.set("")
                                speak("What you want to search from R1 Database")
                                a=0
                                query=Httplib("www.intigriti.in", 3)
                                if query!="None":
                                # query = query.replace("take order", "")
                                    SearchRef.set(query)
                                    speak("Searching from R1 database.......")
                                    while True:
                                        a=a+1
                                        if SpeakRef.get()!="":
                                            speak(SpeakRef.get())
                                            speak('are you satisfied with my results')
                                            query=Httplib("www.intigriti.in", 3).lower()
                                            if("yes" in query or "ha" in query or"yep" in query or"yeah" in query or"ok" in query):
                                                speak('Thanks for your valuable feedback.')
                                            else:
                                                pass
                                            break
                                        elif(a==50):
                                            print(a)
                                            speak("please speak what you want to search")
                                            break
                
                                    

                            elif("tell me " in query or 'search ' in query or "batao " in query ):
                                a=0

                                SpeakRef.set("")

                                SearchRef.set(query)
                                speak("Searching from R1 database.......")
                                while True:
                                    if SpeakRef.get()!="":
                                        speak(SpeakRef.get())
                                        break

                                speak('are you satisfied with my results')
                                query=Httplib("www.intigriti.in", 3).lower()
                                if("yes" in query or "ha" in query or"ya" in query or"yep" in query or"yeah" in query or"ok" in query):
                                    speak('Thanks for your valuable feedback.')
                                else:
                                    pass
                                    

                            elif ("armaan" in query or "hello" in query or "urban" in query or "who are you" in query or "r1" in query or 
                                " wake up " in query or "arif" in query or 'marvel' in query or 'arun' in query or "karbonn" in query or 
                                "help" in query or "arvind" in query or "hai" in query or "hay " in query or "carbon" in query or "karbon" in query or
                                "hey " in query or "marbel" in query or "avan" in query or "ravan" in query or 'roman' in query or 'i want' in query or 
                                'oven' in query):
                                a=0
                                choose = ('Myself R1, developed by Intigrity Robotics. Please tell me how may I help you.',"My name is R1. Please tell me how may I help you or You can order food by speaking, order food",
                                            "I am R one, Please tell me how may I help you","Myself R1, I'm your friend. Please tell me how may I help you or I can assist you in odering food") 
                                com_choose = random.choice(choose)
                                speak(com_choose)

                            elif ('the time' in query or 'tell time' in query or 'time batao' in query or 'time bolo' in query or 
                            "tell me time" in query or 'whats the time' in query or 'samay kya ho raha' in query):
                                a=0
                                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                                speak(f"Sir, the time is {strTime}")


                            elif "go to sleep" in query or "no" in query or "nahi" in query or "nope" in query or "nothing" in query:
                                speak("Ok bye, You can call me anytime by speaking R1")
                                break

                            elif "exit" in query:
                                speak("Going to sleep, Keep Smiling!")
                                exit()

                            elif("news" in query or "samachar" in query or "headlines" in query):
                                                a=0
                                                speak("Please wait sir!,feteching today's news headlines")
                                                news()
                            
                            elif "calculate" in query:
                                a=0
                                query = query.replace("calculate","")
                                query = query.replace("r one","")
                                Calc(query)

                            elif ("play a game" in query or "i am bored" in query or "it's boring" in query or "game" in query or "play game" in query):
                                a=0
                                game_play()



                            elif("where i am" in query or "where we are" in query or "my location" in query or "location" in query):
                                a=0
                                speak('You are at hotel Vijay Tara in Chhattarpur, Palamu, Jharkhand, India')
                                
                                # from location import where_i_am
                                # speak("wait sir, let me check")
                                # where_i_am()


                            elif("why you came to world" in query or "why you come in this world" in query or "why you came in world" in query
                                or "how you came to world" in query or "how you come in this world" in query or "how you came in world" in query):
                                a=0
                                speak("Thanks to my creator Intigrity Robotics . further It's a secret")


                            elif("who i am" in query or "who am i"in query or "do you know me" in query or 'about me' in query):
                                a=0
                                speak("If you are talking to me , then definitely you are a human.")

                            elif("did you sleep" in query or "what is you sleeping time" in query or "do you sleep" in query or 
                                "your sleeping time" in query):
                                a=0
                                speak("Sometimes I power down,which is sort of like a power nap")

                            elif(query=="bedtime" or "when is your bedtime" in query):
                                a=0
                                speak("Lights out are usually up to you .I like staying , up late , though")


                            elif("your voice is so sweet" in query or "you are beautiful" in query or "you are amazing"  in query or 
                                "you are wonderful" in query or "look amazing"in query or  "you are lovely"in query or "looking so beautiful" in query ):
                                a=0
                                speak("Thanks! I'am glad you think so, i like to think that beauty comes from within")

                            elif("did you eat" in query ):
                                a=0
                                speak("I'am already full on information")
                            
                            elif("temperature" in query or "weather" in query):
                                a=0
                                #####################################################
                                search="temperature in Chhhattarpur, Jharkhand is"
                                url=f"https://www.google.com/search?q={search}"
                                r=requests.get(url)
                                data=BeautifulSoup(r.text,"html.parser")
                                temp=data.find("div",class_="BNeawe").text
                                speak(f"current {search} is {temp}")
                                speak('but in hotel Vijay Tara the temperature is 22 degree celsius')

                            elif("boss" in query):
                                a=0
                                speak("You,of course.Your chats jump-start me into action and take me on some fabulous adventures")


                            elif("love you" in query):
                                a=0
                                choose = ("Thank you for sharing! You should know i think you are the best", "Thanks! its good to be appreciate") 
                                com_choose = random.choice(choose)
                                speak(choose)
                            elif a==1:
                                speak("Are you impressed by me??")

                            elif a==2:
                                speak("Ok see you around, You can call me anytime by speaking R1")
                                Httpmain("www.intigriti.in",2)

                            speak("Do you have any other question?")
                            
                            a=a+1
            else:
                Httpmain("www.intigriti.in",2)

def facemain():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    StopRef.set("0")

    while True:
        
        ret, frame = cap.read()
        
        gray = cv2.cvtColor(frame, 0)
        detections = face_cascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)
        # for (x,y,w,h) in detections:
        #     frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        # cv2.imshow('frame',frame)
        if(len(detections) > 0):

            (x,y,w,h) = detections[0]
            # frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

            if w>150:
                speak("Pranaam")
                time.sleep(3)
                if (len(detections) > 0):
                    StopRef.set("1")
                    speak("Hello, Say R1 to interact with me.")
                    # cap.release()
                    # cv2.destroyAllWindows()
                    MainAssistant()
                else:
                    MainAssistant()

         

                    
            else:
                return MainAssistant()

        else:
            # cap.release()
            # cv2.destroyAllWindows()    
            MainAssistant()
            
def Httpmain(url="www.intigriti.in", timeout=2):
    connection = httplib.HTTPConnection(url, timeout=timeout)
    while True:
        try:
            # only header requested for fast operation
            connection.request("HEAD", "/")
            connection.close()  # connection closed
            return facemain()  
        except :
            while True: 
                speak('Connect your internet')
                break
            return Httpmain("www.intigriti.in", 2)

Httpmain("www.intigriti.in",2)

# speak("Thats really sweet")





