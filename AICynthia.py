#!/usr/bin/python3
# -*- coding: utf-8 -*-
#https://likegeeks.com/python-sqlite3-tutorial/
#https://metamost.com/controlling-window-position-from-the-terminal/
#https://github.com/ageitgey/face_recognition
#https://stackoverflow.com/questions/58838265/open-cv-compare-two-face-embeddings
#https://realpython.com/face-recognition-with-python/
#https://www.geeksforgeeks.org/cropping-faces-from-images-using-opencv-python/
#https://stackoverflow.com/questions/42108972/how-to-identify-the-position-of-detected-face
#https://github.com/kripken/speak.js
from gtts import gTTS
import os,time,datetime,sys,subprocess,sqlite3,random,_thread , cv2
from os.path import exists
from datetime import timedelta
from sqlite3 import Error
import pygame , wikipedia , webbrowser
import speech_recognition as sr
from termcolor import colored
import colorama
colorama.init()

logo = '''
 ________________   _______         _      _________       ________________ 
(  ___  \__   __/  (  ____ |\     /( (    /\__   __|\     /\__   __(  ___  )
| (   ) |  ) (     | (    \( \   / |  \  ( |  ) (  | )   ( |  ) (  | (   ) |
| (___) |  | |     | |      \ (_) /|   \ | |  | |  | (___) |  | |  | (___) |
|  ___  |  | |     | |       \   / | (\ \) |  | |  |  ___  |  | |  |  ___  |
| (   ) |  | |     | |        ) (  | | \   |  | |  | (   ) |  | |  | (   ) |
| )   ( ___) (___  | (____/\  | |  | )  \  |  | |  | )   ( ___) (__| )   ( |
|/     \\________/  (_______/  \_/  |/    )_)  )_(  |/     \\________|/     \|
                                                                            
'''
os.system("cls")
print(colored(logo,"blue"))
global trash
trash = []
#############################################################################\
# RANDOM STRING
#############################################################################
def randomName():
    chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
    rt = ""
    for rtx in range(0,64):
        rt += chars[random.randint(0,len(chars)-1)]
    return rt
#############################################################################
# GET DAY
#############################################################################
def getDay(d):
    now = datetime.datetime.now() + timedelta(days=d)
    day = str(now.strftime("%A"))
    if day=="Monday":
        day = "Δευτέρα"
    if day=="Tuesday":
        day = "Τρίτη"
    if day=="Wednesday":
        day = "Τετάρτη"
    if day=="Thursday":
        day = "Πέμπτη"
    if day=="Friday":
        day = "Παρασκευή"
    if day=="Saturday":
        day = "Σαββάτο"
    if day=="Sunday":
        day = "Κυριακή"
    return day
def getTime():    
    now = datetime.datetime.now()
    hour = now.strftime("%H")
    minutes = now.strftime("%M")
    return "Η ώρα είναι "+str(hour)+" και "+str(minutes)+" λεπτά"
def getMonth():    
    now = datetime.datetime.now()
    date = str(now.strftime("%m"))
    datem = datetime.datetime.strptime(date, "%m")
    m=int(datem.month)
    if m == 1:
        month = "Ιανουάριος"
    if m == 2:
        month = "Φεβρουάριος"
    if m == 3:
        month = "Μάρτιος"
    if m == 4:
        month = "Απρίλιος"
    if m == 5:
        month = "Μάϊος"
    if m == 6:
        month = "Ιούνιος"
    if m == 7:
        month = "ιούλιος"
    if m == 8:
        month = "Άυγουστος"
    if m == 9:
        month = "Σεπτέμβριος"
    if m == 10:
        month = "Οκτώβρης"
    if m == 11:
        month = "Νοέμβριος"
    if m == 12:
        month = "Δεκέμβριος"
    a = random.randint(0,2)
    if a == 0:
        return "Ο τρέχων μήνας είναι ο "+month
    elif a==1:
        return "Ο μήνας είναι "+month
    else:
        return "Ο μήνας που διανύουμε είναι ο "+month
def getYear():
    now = datetime.datetime.now()
    date = str(now.strftime("%Y"))
    datem = datetime.datetime.strptime(date, "%Y")
    m=str(datem.year) 
    a = random.randint(0,2)
    if a == 0:
        return "Το τρέχον έτος είναι tο "+m
    elif a==1:
        return "Είμαστε στο "+m
    else:
        return m+" είναι το έτος που διανύουμε"
def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "μηδέν", "ένα", "δύο", "τρία", "τέσσερα", "πέντε", "έξι", "επτά", "οκτώ",
         "εννιά", "δέκα", "έντεκα", "δώδεκα", "δεκατρία", "δεκατέσσερα", "δεκαπέντε",
         "δεκαέξι", "δεκαεπτά", "δεκαοκτώ", "δεκαεννέα",
      ]

      tens = ["", "", "είκοσι", "τριάντα", "σαράντα", "πενήντα", "εξήντα", "εβδομήντα", "ογδόντα", "ενενήντα"]

      scales = ["εκατό", "διακόσια", "τριακόσια"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current
#############################################################################
# SPEAK
#############################################################################
def speak(text):
    rword = randomName()
    directory = os.getcwd()
    mytext = text
    language = 'el'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save(directory+"/trash/"+rword+".mp3")
    time.sleep(3)
    pygame.mixer.init()
    pygame.mixer.music.load(directory+'/trash/'+rword+'.mp3')
    pygame.mixer.music.play()
    trash.append(directory+"/trash/"+rword+".mp3")
    ts = int(len(text)/10)
    tnow = datetime.datetime.now()
    current_time = tnow.strftime("%H:%M:%S")
    print("["+colored(current_time,"blue")+"] "+colored("AICynthia Speaking : ","green",attrs=['bold'])+str(text))
    print("["+colored(current_time,"blue")+"] "+colored("AICynthia Sleeping For : ","green",attrs=['bold'])+str(ts)+" Seconds")
    time.sleep(ts)
#############################################################################
# DATABASE FUNCTIONS
#############################################################################
def sql_connection():
    try:
        con = sqlite3.connect('database.db')
        return con
    except Error:
        print(Error)
def getID(con):
    newid=0
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM aicynthia ORDER BY id DESC')
    rows = cursorObj.fetchall()
    for row in rows:
        newid = int(row[0])+1
        break
    return newid
def getID3(con):
    newid=0
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM phil ORDER BY id DESC')
    rows = cursorObj.fetchall()
    for row in rows:
        newid = int(row[0])+1
        break
    return newid
def randomPhil(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM phil ORDER BY RANDOM() limit 1')
    rows = cursorObj.fetchall()
    for row in rows:
        return row[1]
def findAnswer(con,question):
    qx = question.split()
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM aicynthia ORDER BY id DESC')
    rows = cursorObj.fetchall()
    bc = 0
    answer = ""
    for row in rows:
        lc = 0
        q = row[1]
        a = row[2]
        for w in qx:
            lc += q.count(w)
        if lc > bc:
            answer = a
            bc = lc
        if bc == len(qx):
            break
    return answer
def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE aicynthia(id integer PRIMARY KEY, question text, answer text)")
    con.commit()
def sql_table2(con):
    cursorObj = con.cursor()
    #cursorObj.execute("CREATE TABLE faces(id integer PRIMARY KEY, name text, path text)")
    cursorObj.execute("DROP TABLE faces")
    con.commit()
def sql_table3(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE phil(id integer PRIMARY KEY, philosophy text)")
    con.commit()
def checkDB(con,question):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM aicynthia WHERE question='"+question+"'")
    rows = cursorObj.fetchall()
    for row in rows:
        if question == row[1]:
            return True
    return False
def sql_update(con,question,answer):
    cursorObj = con.cursor()
    cursorObj.execute("UPDATE aicynthia SET answer = '"+answer+"' WHERE question = '"+question+"'")
    con.commit()
def insertDB(con,question,answer):
    cdb = checkDB(con,question)
    if cdb == True:
        sql_update(con,question,answer)
    else:
        id =getID(con)
        cursorObj = con.cursor()
        cursorObj.execute("INSERT INTO aicynthia VALUES("+str(id)+", '"+question+"', '"+answer+"')")
        con.commit()
def insertDB3(con,name):
    id =getID3(con)
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO phil VALUES("+str(id)+", '"+name+"')")
    con.commit()
def deleteFromDB(con,id):
    cursorObj = con.cursor()
    cursorObj.execute("DELETE FROM aicynthia WHERE id = '"+str(id)+"'")
    con.commit()
def sql_fetch(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM aicynthia')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)
#############################################################################
# RECORD MIC
#############################################################################
def recordMic(dur=5):        
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            tnow = datetime.datetime.now()
            current_time = tnow.strftime("%H:%M:%S")
            #print("["+colored(current_time,"blue")+"] "+colored("Recording Start for "+str(dur)+" Seconds...","green",attrs=['bold']))
            print("["+colored(current_time,"blue")+"] "+colored("Recording Start...","green",attrs=['bold']))
            text = ""
            while True:
                audio = r.record(source,duration=5)
                try:
                    pretext = r.recognize_google(audio,language="el-GR")
                except:
                    pretext = ""
                    pass    
                #print(pretext)
                if pretext.strip().replace(" ","") == "":
                    break
                else:
                    text += " "+pretext
            #text = r.recognize_google(audio,language="el-GR")
            #print("Final Text : "+text)
            if text[0] == " ":
                text = text[1:]
            tnow = datetime.datetime.now()
            current_time = tnow.strftime("%H:%M:%S")
            print("["+colored(current_time,"blue")+"] "+colored("Recorded Text : ","green",attrs=['bold'])+text)
            return text
        except:
            tnow = datetime.datetime.now()
            current_time = tnow.strftime("%H:%M:%S")
            print("["+colored(current_time,"blue")+"] "+colored("Recording Error","red",attrs=['bold']))
            pass
            return False
#############################################################################
# SETTINGS
#############################################################################
global con,welcome,recCounter,ques,goodansw,happylearn,prefferAns,facesDet,facesAppr
con = sql_connection()
#deleteFromFaces(con,"Νικόλαος μπαζίγος")
#selectFaces(con)
#sys.exit()
#sql_table2(con)
#sys.exit()
welcome = True
recCounter = 0
ques = ["Έχεις να μου κάνεις κάποια ερώτηση ","Ρώτησε με κάτι σε παρακαλώ","Μπορείς να με ρωτήσεις το οτιδήποτε","Αν θέλεις κάνε μια ερώτηση","θα επιθυμούσα να με ρωτήσεις το οτιδήποτε","Μπορείς να μου κάνεις μια ερώτηση","Δώσε μου μια φωνητική εντολή"]
goodansw = ["Ήταν καλή η απάντηση που σου έδωσα , ναι ή όχι" , "Σε ικανοποίησε η απάντηση , ναι ή όχι" , "ήταν σωστή η απάντηση , ναι η όχι" , "θεωρείς καλή την απάντηση , ναι ή όχι" , "Ήταν σχετική η απάντηση , ναι ή όχι" , "ήταν ικανοποιητική απάντηση , ναι ή όχι"]
happylearn = ["Ωραία , χαίρομαι που μαθαίνω από εσένα","Τέλεια , μου αρέσει αυτό." , "μπράβο , με το καιρό αποκτώ περισσότερη γνώση","Όσο αποκτάω δεδομένα θα δίνω καλύτερες απαντήσεις" , "Αυτό είναι καταπληκτικό", "Μπράβο , μου αρέσει που με εμπλουτίζεις με τη γνώση σου","Φανταστικά , θα προσπαθώ να σου δίνω καλύτερες απαντήσεις όσο μαθαίνω από εσένα"]
prefferAns = ["Πες μου μία καλύτερη απάντηση για την ερώτηση ,","Πρότεινε μου μία πιο σχετική απάντηση στην ερώτηση ,","Σε παρακαλώ δώσε μια σχετική απάντηση στην ερώτηση ,","Θέλω να διευρίνω την γνώση μου , πες μου μια πιο σχετική απάντηση στην ερώτηση ,","Χρειάζομαι περισσότερα δεδομένα , πες μου μια καλή απάντηση στην ερώτηση ,"]
#############################################################################
# THREADS
#############################################################################
try:
   #_thread.start_new_thread( brain, (con,welcome,recCounter,ques,goodansw,happylearn,prefferAns) )
   #_thread.start_new_thread( eyes, () )
   a=1
except:
    tnow = datetime.datetime.now()
    current_time = tnow.strftime("%H:%M:%S")
    print("["+colored(current_time,"blue")+"] "+colored("Error (!) Unable To Start Threads.","red",attrs=['bold']))
'''while True:
   pass'''
#############################################################################
# BRAIN LOOP
#############################################################################
#def brain(con,welcome,recCounter,ques,goodansw,happylearn,prefferAns):
while True:
    if welcome == True:
        time.sleep(1)
        speak("Γεια σου")
        speak("Είμαι η Σύνθια , μια τεχνητή νοημοσύνη που προγραμμάτισε ο Νικόλαος Μπαζίγος")
        welcome = False
    random.shuffle(ques)
    speak(ques[0])
    text = recordMic(20)
    if isinstance(text, (int, float)):
        text = False
    if text == False:
        speak("Μάλλον δεν ηχογράφησες με το μικρόφωνο σου την ερώτηση , διαφορετικά υπάρχει κάποιο άλλο πρόβλημα")
        recCounter+=1
        if recCounter%5==0:
            speak("Ίσως απουσιάζεις , θα απενεργοποιηθώ για 20 λεπτά")
            n=20*60
            time.sleep(n)
    elif ("ημέρα" in text or "μέρα" in text) and ("σήμερα" in text or "είναι" in text) and "καλημέρα" not in text.replace("Κ","κ") and "αύριο" not in text:
        speak("Σήμερα είναι "+getDay(0))
    elif ("ημέρα" in text or "μέρα" in text) and "αύριο" in text and "μεθαύριο" not in text and "καλημέρα" not in text.replace("Κ","κ"):
        speak("Αύριο είναι "+getDay(1))
    elif ("ημέρα" in text or "μέρα" in text) and "μεθαύριο" in text and "καλημέρα" not in text.replace("Κ","κ"):
        speak("μεθαύριο είναι "+getDay(2))
    elif ("ώρα" in text and len(text.split())<=4):
        speak(getTime())
    elif ("μήνα" in text and len(text.split())<=4):
        speak(getMonth())
    elif ("έτος" in text and len(text.split())<=4):
        speak(getYear())
    elif "φιλοσοφία" in text or "απόφθεγμα" in text:
        speak(randomPhil(con))
    elif "εγκυκλοπαίδεια" in text:
        def find_nth(haystack, needle, n):
            start = haystack.find(needle)
            while start >= 0 and n > 1:
                start = haystack.find(needle, start+len(needle))
                n -= 1
            return start
        speak("Πες μου απλά και μονολεκτικά το θέμα ή την ονομασία από αυτό που θες να μάθεις")
        wiki = recordMic(12)
        wikipedia.set_lang("el")
        warray = wikipedia.search(wiki)
        speak("Θα σου αναφέρω μερικά σχετικά θέματα και συγκράτησε το νούμερο του θέματος που σε ενδιαφέρει")
        warcou = 1
        for w in warray:
            speak(str(warcou))
            speak(w)
            warcou+=1
        if len(warray)==0:
            speak("Δεν εντόπισα κάποια σχετική πληροφορία")
        else:
            speak("Αν σε ενδιαφέρει κάποιο από τα θέματα πες μου το νούμερο μονολεκτικά , αλλιώς πες ακύρωση")
            wiki2 = recordMic(12)
            if "Ακύρωση" not in wiki2 or "ακύρωση" not in wiki2:
                try:
                    n= int(wiki2.replace(" ",""))
                except:
                    n = text2int(wiki2.replace(" ",""))
                    pass
                n=int(n)-1
                warcou = 0
                for w in warray:
                    if n == warcou:
                        ny = wikipedia.page(w)
                        speak(ny.title)
                        string = ny.content
                        idx = string.find(".", string.find(".") + 3)
                        speak(string[0:idx])
                        speak("Μήπως θες να σου ανοίξω το σύνδεσμο στον περιηγητή , ναι ή όχι")
                        yn = recordMic(8)
                        if isinstance(yn, (int, float)):
                            yn = ""
                        if "ναι" in yn or "Ναι" in yn:
                            webbrowser.open(ny.url, new=0, autoraise=True)
                        break
                    warcou+=1
            else:
                speak("Η διαδικασία ακυρώθηκε")
        
    elif "κοιμήσου για" in text.replace("Κ","κ"):
        try:
            if "λεπτό" in text:
                pos=text.find("λεπτό")+len("λεπτό")
                text = text[0:pos]
        except:
            pass
        try:
            if "λεπτά" in text:
                pos=text.find("λεπτά")+len("λεπτά")
                text = text[0:pos]
        except:
            pass
        text = text.replace("Κ","κ").replace(" λεπτό","").replace(" λεπτά","")
        pos =text.find("κοιμήσου για ")+len("κοιμήσου για ")
        try:
            n= int(text[pos:])
        except:
            n = text2int(text[pos:])
            pass
        a = random.randint(0,2)
        if a == 0:
            speak("Πέφτω για ύπνο για "+str(n)+" λεπτά")
        if a == 1:
            speak("Απενεργοποιούμαι για "+str(n)+" λεπτά")
        if a == 2:
            speak("Σε αφήνω στην ησυχία σου για "+str(n)+" λεπτά")
        l=n
        n=int(n)*60
        tnow = datetime.datetime.now()
        current_time = tnow.strftime("%H:%M:%S")
        print("["+colored(current_time,"blue")+"] "+colored("AICynthia Sleeping For : ","red",attrs=['bold'])+str(l)+ " Minutes")
        time.sleep(n)
    elif ("ναι" in text or "Ναι" in text) and "είναι" not in text:
        speak("Πες μου την ερώτηση , δεν κατάλαβα καλά")
        text = recordMic(20)
        atext = findAnswer(con,text)
        if atext == "":
            speak("Την απάντηση δεν την γνωρίζω , θες να μου δώσεις μια απάντηση να την καταχωρήσω στη μνήμη μου , ναι ή όχι")
            lb = recordMic(12)
            if "ναι" in lb or "Ναι" in lb:
                speak("Ωραία πες μου την απάντηση")
                newAnswer = recordMic(20)
                speak("Να την καταχωρήσω στη μνήμη μου , ναι ή οχι")
                lb2 = recordMic(12)
                if "ναι" in lb2 or "Ναι" in lb2:
                    insertDB(con,text,newAnswer)
                    speak("Την καταχώρησα με επιτυχία")
        else:
            speak(atext)
            random.shuffle(goodansw)
            speak(goodansw[0])
            lb4 = recordMic(12)
            if isinstance(lb4, (int, float)):
                lb4 = ""
            if "ναι" in lb4 or "Ναι" in lb4:
                random.shuffle(happylearn)
                speak(happylearn[0])
            if "όχι" in lb4 or "Όχι" in lb4:
                random.shuffle(prefferAns)
                speak(prefferAns[0]+text)
                newAnswer = recordMic(20)
                speak("Να την καταχωρήσω στη μνήμη μου , ναι ή οχι")
                lb2 = recordMic(12)
                if isinstance(lb2, (int, float)):
                    lb2 = ""
                if "ναι" in lb2 or "Ναι" in lb2:
                    insertDB(con,text,newAnswer)
                    speak("Την καταχώρησα με επιτυχία")
    elif "όχι" in text or "οχι" in text or "Όχι" in text:
        speak("Θες να απενεργοποιηθώ για μία ώρα , ναι ή όχι")
        lb3 = recordMic(12)
        if isinstance(lb3, (int, float)):
            lb3 = ""
        if "ναι" in lb3 or "Ναι" in lb3:
            speak("Ωραία θα επιστρέψω σε μία ώρα")
            tnow = datetime.datetime.now()
            current_time = tnow.strftime("%H:%M:%S")
            print("["+colored(current_time,"blue")+"] "+colored("AICynthia Sleeping For One Hour : ","green",attrs=['bold'])+"ZZZZZZzzzzz")
            time.sleep(3600)
    else:
        atext = findAnswer(con,text)
        if atext == "":
            speak("Την απάντηση δεν την γνωρίζω , θες να μου δώσεις μια απάντηση να την καταχωρήσω στη μνήμη μου , ναι ή όχι")
            lb = recordMic(12)
            if isinstance(lb, (int, float)):
                lb = ""
            if "ναι" in lb or "Ναι" in lb:
                speak("Ωραία πες μου την απάντηση")
                newAnswer = recordMic(20)
                speak("Να την καταχωρήσω στη μνήμη μου , ναι ή οχι")
                lb2 = recordMic(12)
                if isinstance(lb2, (int, float)):
                    lb2 = ""
                if "ναι" in lb2 or "Ναι" in lb2:
                    insertDB(con,text,newAnswer)
                    speak("Την καταχώρησα με επιτυχία")
        else:
            speak(atext)
            random.shuffle(goodansw)
            speak(goodansw[0])
            lb4 = recordMic(12)
            if isinstance(lb4, (int, float)):
                lb4 = ""
            if "ναι" in lb4 or "Ναι" in lb4:
                random.shuffle(happylearn)
                speak(happylearn[0])
            if "όχι" in lb4 or "Όχι" in lb4:
                random.shuffle(prefferAns)
                speak(prefferAns[0]+text)
                newAnswer = recordMic(20)
                speak("Να την καταχωρήσω στη μνήμη μου , ναι ή οχι")
                lb2 = recordMic(12)
                if isinstance(lb2, (int, float)):
                    lb2 = ""
                if "ναι" in lb2 or "Ναι" in lb2:
                    insertDB(con,text,newAnswer)
                    speak("Την καταχώρησα με επιτυχία")
    tnow = datetime.datetime.now()
    current_time = tnow.strftime("%H:%M:%S")
    print("["+colored(current_time,"blue")+"] "+colored("Try To Cleaning Trash Files..","green",attrs=['bold']))
    for x in trash:
        try:
            #os.system("del "+x)
            subprocess.Popen("del "+x, shell=False, stdout=subprocess.PIPE).stdout.read()
        except:
            pass
    try:
        dir = os.getcwd()+'/trash'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
    except:
        pass
    time.sleep(10)