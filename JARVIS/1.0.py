import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import smtplib
import webbrowser as wb
import psutil
import pyjokes
import os
import pyautogui
import random
import json
import requests
from urllib.request import urlopen
import wolframalpha
import time
import cv2
from twilio.rest import Client


engine = pyttsx3.init()
wolframalpha_app_id = ""#use your own  


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def time_():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is ")
    speak(Time)


def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    date = datetime.datetime.now().day
    speak("The current date is")
    speak(date)
    speak(month)
    speak(year)


def wishme():
    speak("Welcome Gopi")
    time_()
    date_()
    hour = datetime.datetime.now().hour

    if hour >= 6 and hour < 12:
        speak("Good Morning sir!")
    elif hour >= 12 and hour < 18:
        speak("good Afternoon sir!")
    elif hour >= 18 and hour < 24:
        speak("Good Evening Sir!!")
    else:
        speak("Good Night Sir!!")

    speak("RamuKaka at your service Please tell me how can I help you today?")


def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...... ")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing......")
        query = r.recognize_google(audio, language='en-US')
        print(query)

    except Exception as e:
        print(e)
        print("Say That Again please...")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    server.login('sender's mailid', 'password')
    server.sendmail('sender's mailid', to, content)
    server.close()

def screenshot():
    img=pyautogui.screenshot()
    img.save('C:/Users/Gopi/Desktop/screenshot.png')


def cpu():
    usage=str(psutil.cpu_percent())
    speak('Cpu is at'+usage)

    battery=psutil.sensors_battery()
    speak("battery is at")
    speak(battery)

def joke():
    speak(pyjokes.get_joke())

def intro():
    speak("I am Ramukaka,I am Adi's Creation and his Personal Assistant ")




if __name__ == "__main__":

    wishme()

    while True:
        query = TakeCommand().lower()

        if 'time' in query:
            time_()

        if 'date' in query:
            date_()

        elif 'wikipedia' in query:
            speak("Serching....")
            query = query.replace('wikipedia', '')
            result = wikipedia.summary(query, sentences=3)
            speak('According to wikipedia')
            print(result)
            speak(result)

        elif 'send email' in query:
            try:
                speak("What should I say")
                content = TakeCommand()
                speak("Who is the reciever?")
                reciever = input("enter Receiever's Email")

                to = reciever
                sendEmail(to, content)
                speak(content)
                speak("Email has been sent")

            except Exception as e:
                print(e)
                speak("Unable to send Email")

        elif "search in chrome" in query:
            speak("What should I search?")
            chromedir ='C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

            search = TakeCommand().lower()
            wb.get(chromedir).open_new_tab(search +'.com')

        elif 'search youtube' in query:
            speak("Which video will you watch?")
            search_Term= TakeCommand().lower()
            speak("Here we go to youtube")
            wb.open("https://www.youtube.com/results?search_query="+search_Term)


        elif 'search google' in query:
            speak("What should I search?")
            search_Term= TakeCommand().lower()
            speak("Searching")
            wb.open("https://google.com/?#q="+search_Term)

        elif 'cpu' in query:
            cpu()

        elif 'joke' in query:
            joke()

        elif 'sleep' in query:
            speak("As you wish Sir")
            quit()

        elif 'word' in query:
            speak("Opening MS Word.....  ")
            ms_word = r'C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Microsoft Office/Microsoft Office Word 2007'
            os.startfile(ms_word)

        elif 'write a note' in query:
            speak("What should I write sir")
            notes = TakeCommand()
            file =open('notes.txt','w')
            speak("Sir should I include date and time")
            ans=TakeCommand()
            if 'yes' or 'sure' in ans:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(":-")
                file.write(notes)
                speak("Notes are taken")

            else:
                file.write(notes)

        elif 'show notes' in query:
            speak("showing notes")
            file = open('notes.txt','r')
            print(file.read())
            speak(file.read())

        elif 'screenshot' in query:
            screenshot()

        elif 'play music' in query:
            song_dir='E:\song'
            music = os.listdir(song_dir)
            speak("What should I play")
            speak("select a number")

            ans = TakeCommand().lower()
            while('number' not in ans and ans != 'random' and ans !='you choose'):
                speak("I cant understand please repeat again")
                ans= TakeCommand().lower()
            if 'number' in ans:
                no = int(ans.replace('number',''))

            elif 'random' or 'you choose' in ans:
                no=random.randint(0,2)

            os.startfile(os.path.join(song_dir,music[no]))

        elif 'remember that' in query:
            speak("What should I remember")
            memory=TakeCommand()
            speak("you asked me to remember that"+memory)
            remember = open('memory.txt','w')
            remember.write(memory)
            remember.close()

        elif 'do you remember anything' in query:
            remember= open('memory.txt','r')
            speak("You asked me to remember that"+remember.read())


        elif 'news' in query:
            try:
                jsonObj = urlopen("use own news api")
                data = json.load(jsonObj)
                i=1

                speak("Here are top news from Tech crunh")
                print("========TOP HEADLINES========")
                for item in data['articles']:
                    print(str(i)+'. '+item['title']+'\n')
                    print(item['description']+'\n')
                    speak(item['title'])
                    i+=1

            except Exception as e:
                print(str(e))

        elif 'where is' in query:
            query = query.replace("where is","")
            location=query
            speak("user asked to locate"+location)
            wb.open_new_tab("https://www.google.com/maps/place/"+location)


        elif 'calculate' in query:
            client= wolframalpha.Client(wolframalpha_app_id)
            indx= query.lower().split().index("calculate")
            query= query.split()[indx + 1 :]
            res =client.query("".join(query))
            answer = next(res.results).text
            print("The answer is  "+answer)
            speak("the answer is "+answer)

        elif 'what is' in query or 'who is' in query:
            client= wolframalpha.Client(wolframalpha_app_id)
            res = client.query(query)

            try:
                print(next(res.results).text)
                speak(next(res.results).text)

            except StopIteration:
                print("No results")

        elif 'stop listening' in query:
            speak("For how many seconds you want me to stop")
            ans = int(TakeCommand())
            time.sleep(ans)
            print(ans)

        elif 'log out' in query:
            os.system("shutdown -l")

        elif 'restart' in query:
            os.system("shutdown /r /t 1")

        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")

        elif 'who am i' in query:
            speak("if you can talk then definitely you are human ")



        elif 'what is love' in query:
            speak("I told you not to watch romantic movies")

        elif 'tell me about yourself' in query:
            intro()
                    
        elif 'take picture' in query:
                    video=cv2.VideoCapture(0)
                    while True:
                        check,frame =video.read()
                        cv2.imshow("Master",frame)
                        cv2.waitKey(0)
                        time.sleep(5)
                    video.release()
                    cv2.destroyAllWindows()
        elif 'whatsapp me' in query:
            speak("What is your message")
            ans=TakeCommand()
            account_sid = ''#your account id
            auth_token = ''#your token
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                from_='whatsapp:#number from twilio',
                body=ans,
                to='whatsapp:#your number'

            )

            print(message.sid)

        elif "call me" in query:
            account_sid = ''
            auth_token = ''
            client = Client(account_sid, auth_token)
            call=client.calls.create(
                url='http://demo.twilio.com/docs/voice.xml',
                to ='',
                from_=''
            )
            print(call.sid)
                    
         elif "message me" in query:
                    account_sid = ''
                    auth_token = 'your_auth_token'
                    client = Client(account_sid, auth_token)

                                message = client.messages.create(
                                        body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                                        from_='',
                                        to=''
                 )

                 print(message.sid)
                    
                    

       

