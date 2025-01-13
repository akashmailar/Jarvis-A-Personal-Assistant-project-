import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia
import pywhatkit
import user_config
import smtplib, ssl
import openai_request as ai
import mtranslate
import image_generation

engine = pyttsx3.init()

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)


def speak(audio):
    # audio = mtranslate.translate(audio, to_language="hi", from_language="en-in")
    engine.say(audio)
    engine.runAndWait()


def command():
    content = " "
    while content == " ":
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        # recognize speech using Google Speech Recognition
        try:
            content = r.recognize_google(audio, language='en-in')
            # content = mtranslate.translate(content, to_language="en-in")
            print("You Said.... " + content)
        except Exception as e:
            print("Please Try Again...")

    return content


def main_process():
    jarvis_chat = []
    while True:
        request = command().lower()
        if 'hello' in request:
            speak("Welcome, How can I help You?")
        elif 'who are you' in request:
            speak("My name is Jarvis, How can I help you.")
        elif 'play music' in request:
            speak("Playing Music")
            song = random.randint(1, 6)
            if song == 1:
                webbrowser.open("https://www.youtube.com/watch?v=Cus-6cnyt1s")
            elif song == 2:
                webbrowser.open("https://www.youtube.com/watch?v=FGNc3BibU3o&pp=ygUXYmhvb2wgYmh1bGFpeWFhIHNvbmdzIDM%3D")
            elif song == 3:
                webbrowser.open("https://www.youtube.com/watch?v=WpA8vg5PmuQ&pp=ygUXYmhvb2wgYmh1bGFpeWFhIHNvbmdzIDM%3D")
            elif song == 4:
                webbrowser.open("https://www.youtube.com/watch?v=TMY1g8pAktk")
            elif song == 5:
                webbrowser.open("https://www.youtube.com/watch?v=4ol65QlFc3k")
            elif song == 6:
                webbrowser.open("https://www.youtube.com/watch?v=fgbZGDjzXUc")
        elif 'say time' in request:
            now_time = datetime.datetime.now().strftime("%H:%M %p")
            speak("Current time is "+ str(now_time))
        elif 'say date' in request:
            now_date = datetime.datetime.now().strftime("%d %B %Y")
            speak("Today's date is "+ str(now_date))
        elif "add task" in request:
            request = request.replace('jarvis', '')
            task = request.replace("add task", "")
            task = task.strip()
            if task != "":
                speak("Adding Task: "+ task)
                with open('todo.txt', 'a') as file:
                    file.write(task+"\n")
        elif "delete task" in request:
            request = request.replace('jarvis', '')
            task = request.replace("delete task", "")
            task = task.strip()
            new_tasks = []
            if task != "":
                speak("Deleting Task:"+ task)
                with open('todo.txt', 'r') as file:
                    tasks = file.readlines()
                    for i in tasks:
                        if i.strip() != task:
                            new_tasks.append(i.strip())
            with open('todo.txt', 'w') as file:
                for task in new_tasks:
                    file.write(task+'\n')
        elif "speak to do list" in request:
            with open('todo.txt', 'r') as file:
                speak("Your Todo list: "+ file.read())
        elif "show to do" in request:
            with open('todo.txt', 'r') as file:
                tasks =  file.read()
            notification.notify(
                title = "Today's Work:",
                message = tasks
            )
        elif "open youtube" in request:
            speak("Opening Youtube")
            webbrowser.open("www.youtube.com")
        elif "open google" in request:
            speak("Opening Google")
            webbrowser.open("www.google.com")
        elif "open" in request:
            request = request.replace('jarvis', '')
            query = request.replace("open", "")
            speak("Opening"+query)
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
        elif "wikipedia" in request:
            request = request.replace("jarvis", "")
            request = request.replace("search wikipedia", "")
            print(request)
            result = wikipedia.summary(request, sentences=2)
            print(result)
            speak(result)
        elif "search google" in request:
            request = request.replace('jarvis', '')
            request = request.replace('search google', '')
            webbrowser.open("https://in.search.yahoo.com/search?p="+request)
        elif "send whatsapp" in request:
            pywhatkit.sendwhatmsg("+919123456780", "Hi, How are you?", 13, 32, 30)
        elif "send mail" in request:
            s = smtplib.SMTP("smtp.gmail.com", 587)
            s.starttls()
            s.login("abcd1234@gmailcom", user_config.gmail_password)
            message = """
            This the Message
            Thanks by Code Gurukul
            """
            s.sendmail("abcd1234@gmailcom", "ximorep320@kvegg.com", message)
            s.quit()
            speak("Email sent")
        elif "image" in request:
            request = request.replace('jarvis', '')
            image_generation.generate_image(request)
        elif "ask ai" in request:
            jarvis_chat = []
            request = request.replace('jarvis', '')
            request = request.replace('ask ai', '')

            jarvis_chat.append({"role":"user", "content":request})

            response = ai.send_request(jarvis_chat)

            speak(response)
        elif "clear chat" in request:
            jarvis_chat = []
            speak("Chat Cleared")
        else:
            request = request.replace('jarvis', '')
            
            jarvis_chat.append({"role":"user", "content":request})

            response = ai.send_request(jarvis_chat)

            jarvis_chat.append({"role":"assistant", "content":response})
            speak(response)
        

if __name__ == '__main__':
    main_process()        