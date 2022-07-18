import cv2 as cv
import numpy as np
import face_recognition
import os 
import datetime
import pandas as pd
from csv import writer



path='Images'
def findEncoding(images):
	encodingList=[]
	for img in images:
		img=cv.cvtColor(img,cv.COLOR_BGR2RGB)
		encode=face_recognition.face_encodings(img)[0]
		encodingList.append(encode)
		return encodingList


def MarkAttendance(name):
	try:
		df=pd.read_csv("Attendance.csv")
		df.columns=['name','date']
		now=datetime.date.today().strftime('%Y-%m-%d')
		if(df.empty==False):
			data=df[(df['date']==now) &( df['name']==name)]
			if(data.empty ==False):
				print('Already marked!')
				return True
		list=[name,now]
		with open('Attendance.csv','a') as f:
			obj=writer(f)
			obj.writerow(list)
			f.close()
			return True
	except:
		print("Trying again..")
		return False



def Mark():
	images=[]
	Imagename=[]
	List=os.listdir(path)
	for item in List:
			currImg=cv.imread(f'{path}/{item}')
			images.append(currImg)
			Imagename.append(os.path.splitext(item)[0])
	encodeListKnown=findEncoding(images)
	print('Encoding Complete')
	cap=cv.VideoCapture(0)
	abc=True
	ma=False
	while abc:
		sucess,img=cap.read()
		imgs=cv.resize(img,(0,0),None,0.25,0.25)
		imgs=cv.cvtColor(imgs,cv.COLOR_BGR2RGB)
		facesCutFrame= face_recognition.face_locations(imgs)
		encodesCutFrame=face_recognition.face_encodings(imgs,facesCutFrame)
		for encodeFace, faceLoc in zip(encodesCutFrame, facesCutFrame):
			matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
			faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
		 	#print(faceDis)
			matchIndex = np.argmin(faceDis)
			if matches[matchIndex]:
				name = Imagename[matchIndex].upper()
				y1, x2, y2, x1 = faceLoc
				y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
				cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
				cv.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv.FILLED)
				cv.putText(img, name, (x1 + 6, y2 - 6), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
				if ma==False:
					print(name)
					iss=MarkAttendance(name)
					if iss:
						ma=True
		cv.imshow('Webcam', img)
		if cv.waitKey(25) & 0xFF == ord('q'):
			return





def Add():
	print("Input Your name:")
	print('Be infront of camera!')
	name=input()
	cap=cv.VideoCapture(0)
	sucess, img=cap.read()
	if sucess:
		cv.imshow(name,img)
		cv.imwrite(os.path.join(path , '{}.jpg'.format(name)), img)
		cv.waitKey(20)
		print("Added!")
		cv.destroyWindow(name)
	else:
		print("No image detected. Please! try again")
	




#main

print("Attendance Marker and Manager")
while True:
	print("1. Mark Attendance.")
	print("2. Add Student.")
	choice=int(input("Enter your choice:"))
	if(choice==1):
		Mark()
	if(choice ==2):
		Add()
	else :
		print('Please Enter Valid Response')

