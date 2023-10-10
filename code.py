import tkinter as tk
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

card_no = []
pins = []
names = []
amounts = []     
 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    pin = (txt5.get())
    amount = (txt4.get())
    if(Id.isnumeric() and name.isalpha() and pin.isnumeric()):
        card_no.append(Id), names.append(name), pins.append(pin), amounts.append(amount)
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                sampleNum=sampleNum+1
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                cv2.imshow('frame',img) 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Face Saved for Card No: " + Id +", Name: "+ name
        row = [Id, name, pin, amount]
        with open('CardHolders\Details.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(not Id.isnumeric()):
            res = "Enter Card No w/o spaces"
            message.configure(text= res)
        if(not name.isalpha()):
            res = "Enter Name as characters"
            message.configure(text= res)
        if(not pin.isnumeric()):
            res = "Enter PIN in digits"
            message.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("Trainer.yml")
    res = "Face Database has been Trained"
    message.configure(text= res)

# def getImagesAndLabels(path):
#     ImagePaths=[os.path.join(path,f) for f in os.listdir(path)]     
#     faces=[]
#     Ids=[]
#     for ImagePath in ImagePaths:
#         ImagePath = "TrainingImage"
#         pilImage=Image.open(ImagePath).convert('L')
#         imageNp=np.array(pilImage,'uint8')
#         Id=int(os.path.split(ImagePath)[-1].split(".")[0])
#         faces.append(imageNp)
#         Ids.append(Id)        
#     return faces,Ids


def getImagesAndLabels(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]     
    faces=[]
    Ids=[]
    for imagePath in imagePaths:
        pilImage=Image.open(imagePath).convert('L')
        imageNp=np.array(pilImage,'uint8')
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids


def TrackImages(flag):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("Trainer.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("CardHolders\Details.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    for i in range(75):
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 50):
                ts = time.time()  
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp] 
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im)
        cv2.waitKey(1)

    if flag:    
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        fileName="Transactions\Transaction_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
        attendance.to_csv(fileName,index=False)
        print(attendance)
    cam.release()
    cv2.destroyAllWindows()
    return flag

#PAYMENT GUI
def ATM():
    def Deposit(amount):
        def submit1(amount, txt):
            i = amounts.index(amount)
            amount = str(int(amount) + int(txt.get()))
            amounts[i] = amount
            res = f'New Balance is {amount}.'
            message1.configure(text = res)
            lbl.destroy(), txt.destroy(), submitbtn.destroy()
        
        lbl = tk.Label(window2, text="Enter Amount to Deposit", width=20, height=2, fg="orange", bg="black" ,font=('Arial', 15, 'bold'))
        lbl.place(x=50, y=450)
        txt = tk.Entry(window2, width=25, bg="white", fg="black", font=('Arial', 15,))
        txt.place(x=400, y=462)
        submitbtn = tk.Button(window2, text="Submit", command=lambda: submit1(amount, txt)  ,fg="white"  ,bg="orange"  ,width=7  ,height=1, activebackground = "yellow",font=('Arial', 10, ' bold '))
        submitbtn.place(x=650, y=462)
        
        
        
    def Withdraw(amount):
        def submit2(amount, txt):
            i = amounts.index(amount)
            if int(txt.get()) < int(amount):
                amount = str(int(amount) - int(txt.get()))
                amounts[i] = amount
                res = f'Remaining Balance is {amount}.'
                message1.configure(text = res)
            else:
                res = 'Requested amount exceeds balance'
                message1.configure(text = res)
            lbl.destroy(), txt.destroy(), submitbtn.destroy()
            
        lbl = tk.Label(window2, text="Enter Amount to Withdraw", width=22, height=2, fg="orange", bg="black" ,font=('Arial', 15, 'bold')) 
        lbl.place(x=50, y=450)
        txt = tk.Entry(window2, width=25, bg="white", fg="black", font=('Arial', 15,))
        txt.place(x=400, y=462)
        submitbtn = tk.Button(window2, text="Submit", command=lambda: submit2(amount, txt)  ,fg="white"  ,bg="orange"  ,width=7  ,height=1, activebackground = "yellow",font=('Arial', 10, ' bold '))
        submitbtn.place(x=650, y=462)
        
    def Balance(i):
        res = f'Balance in Account = {amounts[i]}'
        message1.configure(text=res)
        
    def submit():
        card=(txt.get())
        pin=(txt2.get())
        name=(txt3.get())
        if(card in card_no):
            i = card_no.index(card)
            if(pins[i] == pin and name == names[i]):    
                flag = TrackImages(1)
                if flag:
                    res = 'User Authenticated...Proceed to Transaction.'
                    message1.configure(text=res)
                    deposit = tk.Button(window2, text="Deposit", command=lambda: Deposit(amounts[i])  ,fg="white"  ,bg="orange"  ,width=20  ,height=3, activebackground = "yellow" ,font=('Arial', 15, ' bold '))
                    deposit.place(x=1000, y=180)
                    withdraw = tk.Button(window2, text="Withdraw", command=lambda: Withdraw(amounts[i])  ,fg="white"  ,bg="orange"  ,width=20  ,height=3, activebackground = "yellow" ,font=('Arial', 15, ' bold '))
                    withdraw.place(x=1000, y=320)
                    balance = tk.Button(window2, text="Check Balance", command=lambda: Balance(i)  ,fg="white"  ,bg="orange"  ,width=20  ,height=3, activebackground = "yellow" ,font=('Arial', 15, ' bold '))
                    balance.place(x=1000, y=460)
            else:
                res = 'Card Details are not verified.'
                message1.configure(text=res)
        else:
            res = 'Card Holder does not exist'
            message1.configure(text=res)
            
            
    window2 = tk.Tk()
    window2.title("ATM")
    window2.configure(background='black')
    window_width = 1500
    window_height = 900
    
    # set the position of the window to the center of the screen
    window2.geometry(f'{window_width}x{window_height}')

    topic = tk.Label(window2, text="Automated Teller Machine".upper(), bg="black", fg="white", width=40, height=2, font=('Segoe UI', 28, 'bold'))
    topic.place(x=200, y=20)

    lbl = tk.Label(window2, text="Enter Card Number", width=20, height=2, fg="yellow", bg="black" ,font=('Arial', 15, 'bold')) 
    lbl.place(x=100, y=180)
    txt = tk.Entry(window2, width=20, bg="white", fg="black", font=('Arial', 15,))
    txt.place(x=400, y=192)
    
    lbl3 = tk.Label(window2, text="Enter Name", width=20, height=2, fg="yellow", bg="black" ,font=('Arial', 15, 'bold')) 
    lbl3.place(x=63, y=230)
    txt3 = tk.Entry(window2, width=20, bg="white", fg="black", font=('Arial', 15,))
    txt3.place(x=400, y=245)

    lbl2 = tk.Label(window2, text="Enter PIN", width=20, fg="yellow", bg="black", height=2, font=('Arial', 15, 'bold')) 
    lbl2.place(x=53, y=280)
    txt2 = tk.Entry(window2,width=20, bg="white", fg="black", font=('Arial', 15,))
    txt2.place(x=400, y=300)
    txt2.config(show='*')
    
    submitbtn = tk.Button(window2, text="Submit", command=submit  ,fg="white"  ,bg="orange"  ,width=7  ,height=2, activebackground = "yellow",font=('Arial', 10, ' bold '))
    submitbtn.place(x=480, y=350)

    lbl3 = tk.Label(window2, text="Notification", width=20, fg="orange", bg="black", height=2, font=('Arial', 15, ' bold')) 
    lbl3.place(x=0, y=555)
    message1 = tk.Label(window2, text="", bg="white"  ,fg="black"  ,width=50  ,height=2, activebackground = "white" ,font=('times', 15, ' bold ')) 
    message1.place(x=220, y=560)
    
    quitWindow = tk.Button(window2, text="Quit", command=window2.destroy  ,fg="white"  ,bg="red"  ,width=20  ,height=3, activebackground = "yellow" ,font=('Arial', 15, ' bold '))
    quitWindow.place(x=1000, y=600)
  


#MAIN GUI
window = tk.Tk()
window.title("Bank Registration")
window.configure(background='teal')

window_width = 1500
window_height = 900

# set the position of the window to the center of the screen
window.geometry(f'{window_width}x{window_height}')


topic = tk.Label(window, text="Secure Bank Transactions using Facial Recognition".upper(), bg="teal", fg="white", width=60, height=2, font=('Segoe UI', 28, 'bold'))
topic.place(x=0, y=20)

lbl = tk.Label(window, text="Enter Card Number", width=20, height=2, fg="orange", bg="teal" ,font=('Arial', 15, 'bold')) 
lbl.place(x=100, y=179)
txt = tk.Entry(window, width=20, bg="white", fg="black", font=('Arial', 15,))
txt.place(x=370, y=192)

lbl2 = tk.Label(window, text="Enter Name", width=20, fg="orange", bg="teal", height=2, font=('Arial', 15, 'bold')) 
lbl2.place(x=63, y=230)
txt2 = tk.Entry(window,width=20, bg="white", fg="black", font=('Arial', 15,))
txt2.place(x=370, y=245)

lbl5 = tk.Label(window, text="Enter PIN", width=20, fg="orange", bg="teal", height=2, font=('Arial', 15, 'bold')) 
lbl5.place(x=52, y=285)
txt5 = tk.Entry(window,width=20, bg="white", fg="black", font=('Arial', 15,))
txt5.place(x=370, y=300)
txt5.config(show='*')

lbl4 = tk.Label(window, text="Enter Initial Amount", width=20, fg="orange", bg="teal", height=2, font=('Arial', 15, 'bold')) 
lbl4.place(x=98, y=340)
txt4 = tk.Entry(window,width=20, bg="white", fg="black", font=('Arial', 15,))
txt4.place(x=370, y=355)

lbl3 = tk.Label(window, text="Notification", width=20, fg="orange", bg="teal", height=2, font=('Arial', 15, ' bold')) 
lbl3.place(x=0, y=615)
message = tk.Label(window, text="", bg="white"  ,fg="black"  ,width=50  ,height=2, activebackground = "white" ,font=('times', 15, ' bold ')) 
message.place(x=195, y=620)


takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="black"  ,bg="orange"  ,width=20  ,height=3, activebackground = "yellow",font=('Arial', 15, ' bold '))
takeImg.place(x=100, y=440)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="black"  ,bg="orange"  ,width=20  ,height=3, activebackground = "yellow",font=('Arial', 15, ' bold '))
trainImg.place(x=500, y=440)
trackImg = tk.Button(window, text="Track Images", command=lambda: TrackImages(0)  ,fg="black"  ,bg="orange"  ,width=20  ,height=3, activebackground = "yellow",font=('Arial', 15, ' bold '))
trackImg.place(x=900, y=440)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="white"  ,bg="red"  ,width=20  ,height=3, activebackground = "yellow" ,font=('Arial', 15, ' bold '))
quitWindow.place(x=900, y=600)
atm = tk.Button(window, text = 'Go To ATM', command=ATM, fg='white', bg = 'green', width = 20, height = 3, activebackground='yellow', font=('Segoe UI', 15, 'bold underline'))
atm.place(x=900, y = 160)
 
window.mainloop()