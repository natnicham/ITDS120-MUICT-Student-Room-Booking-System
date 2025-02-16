import pandas as pd 
from datetime import datetime
import os.path
import csv

students = pd.read_csv("students.csv")
Booking_Record = os.path.isfile('Booking_Record.csv')

if not Booking_Record:
  with open("Booking_Record.csv", "w", newline = '') as Booking_Record:
    writer = csv.writer(Booking_Record)
    writer.writerow(["date", "id", "room_type", "room"])

Booking_Record_Data = pd.read_csv("Booking_Record.csv", index_col=False)

def intro():
  print("\033[1m\033[4;92mMUICT Student Room Booking System\033[0m \n\033[1;33m1. print a list of students \n2. submit it a booking request \n3. check the current booking via room number \n4. check the available rooms via date \n5. check booking with student ID \n6. check booking with student first name \n7. print booking summary \n\033[1;31m0. exit\033[0m")

def check_date(date):
  while True:
    try:
      date_time = datetime.strptime(date, "%d-%m-%Y") 
      return date
    except ValueError :
      date = input("\033[31mInvalid date. Booking date (DD-MM-YYYY):\033[0m")

def check_booking(room,date,fn=check_date):
  global Booking_Record_Data
  date = fn(date)
  date_time = datetime.strptime(date, "%d-%m-%Y").date()
  while date_time < datetime.now().date() : 
    date = fn(input("\033[0;31mInvalid date, date cannot be before today's date. Booking date (DD-MM-YYYY):\033[0m"))
    date_time = datetime.strptime(date, "%d-%m-%Y").date()
  for i in range(len(Booking_Record_Data)):
    if date == Booking_Record_Data['date'][i] and room == Booking_Record_Data['room'][i]:
      return print(f"\033[31m{room} is not available on {date}\033[0m")
  with open('Booking_Record.csv', 'a', newline='') as Booking_Record:
    writer = csv.writer(Booking_Record)
    writer.writerow([date, id, room_type, room])
  Booking_Record_Data = pd.read_csv("Booking_Record.csv")
  Booking_Record_Data['date'] = pd.to_datetime(Booking_Record_Data['date'],format = '%d-%m-%Y')
  Booking_Record_Data = Booking_Record_Data.sort_values(by='date')
  Booking_Record_Data['date'] = Booking_Record_Data['date'].dt.strftime('%d-%m-%Y')
  Booking_Record_Data.to_csv("Booking_Record.csv", index=False)
  print("\033[1;32m✓ Booking completed! (◦Ó◡Ó◦)\033[0m")

def check_id(id):
  while id not in students["id"].values :
    id = int(input("\033[0;31mInvalid ID. ID:\033[0m"))
  return id

def check_room_type(room_type):
  while room_type != 'Lecture' and room_type != 'Lab':
    room_type = input("\033[0;31mInvalid room type. Room types (Lecture/Lab):\033[0m")
  if room_type == 'Lecture':
    print(f"Room: {lecture_list}")
  else :
    print(f"Room: {lab_list}") 
  return room_type

def check_room(room):
  while True:
    if room_type == 'Lecture' and room in lecture_list:
      return room
    elif room_type == 'Lab' and room in lab_list:
      return room
    else:
      room = (input("\033[31mInvalid room. Please select one room above:\033[0m"))

def check_room_number(room):
  while room not in lab_list and room not in lecture_list:
    room = (input("\033[31mInvalid room. Please select one room above:\033[0m"))
  return room

def booking_summary(room_type_list):
  for i in room_type_list:
    print(f"{i} :")
    if i not in Booking_Record_Data['room'].values:
      print("\033[31m  No Booking\033[0m")
    else:
      for j in range(len(Booking_Record_Data)):
        if i == Booking_Record_Data['room'][j]:
          print(f"  Date: {Booking_Record_Data['date'][j]} Student ID: {Booking_Record_Data['id'][j]}")

def booking_id(id):
  print("\033[1;34m  Current bookings:\033[0m")
  if id not in Booking_Record_Data['id'].values:
    print("\033[31m    No booking\033[0m")
  else: 
    for i in range(len(Booking_Record_Data)):
      if id == Booking_Record_Data['id'][i]:
        print(f"    Room: {Booking_Record_Data['room'][i]} Date: {Booking_Record_Data['date'][i]}")   

intro()
option = int(input("\033[1;32mOption:\033[0m"))
while option != 0:
  lecture_list = ['IT301','IT302','IT303','IT304']
  lab_list = ['LAB103','LAB104','LAB105','LAB106']
  
  if option == 1 :
    print(students)
    
  elif option == 2 :
    id = check_id(int(input("ID:")))
    room_type = check_room_type(input("Room types (Lecture/Lab):"))
    room = check_room(input("Please select one room above:"))
    check_booking(room,input("Booking date (DD-MM-YYYY):"))    
    
  elif option == 3 :
    room = check_room_number(input("Room number:"))
    print("\033[1;34mCurrent booking:\033[0m")
    if room not in Booking_Record_Data['room'].values:
      print("\033[31m No booking")
    else:
      for i in range(len(Booking_Record_Data)):
        if room == Booking_Record_Data['room'][i]:
          print(f"  Date: {Booking_Record_Data['date'][i]}  Student ID: {Booking_Record_Data['id'][i]}")
      
  elif option == 4 :
    date = check_date(input("Booking date (DD-MM-YYYY):"))
    for i in range(len(Booking_Record_Data)):
      if date == Booking_Record_Data['date'][i]:
        if Booking_Record_Data['room'][i] in lecture_list:
          lecture_list.remove(Booking_Record_Data['room'][i])
        else:
          lab_list.remove(Booking_Record_Data['room'][i])
    print("\033[1;34mAvailable rooms:\033[0m")
    print(f"  Lecture: {lecture_list} \n  Lab: {lab_list}")
    
  elif option == 5 :
    id = check_id(int(input("ID:")))
    booking_id(id)
  
  elif option == 6 :
    student_first_name = input("Firstname:")
    found = False
    for i in range(len(students)):
      if student_first_name.lower() in students['fname'][i].lower():
        found = True
        id = students['id'][i]
        print(f"{students['id'][i]} {students['fname'][i]} {students['lname'][i]}")
        booking_id(id)
        
    if found == False:
      print("\033[31mThere is no student found.\033[0m")      
    
  elif option == 7 :
    print("\033[1;34mLecture:\033[0m")
    booking_summary(lecture_list)
    print("\033[1;34mLab:\033[0m")
    booking_summary(lab_list)

  else:
    print("\033[1;31mInvalaid Option🥲\033[0m")
    
  print("="*50)
  intro()
  option = int(input("\033[1;32mOption:\033[0m"))

