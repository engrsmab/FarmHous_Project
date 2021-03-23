import pandas as pd
import sqlite3
import time
import datetime
from datetime import date
import gspread
from playsound import playsound
import numpy as np
from matplotlib import pyplot as plt
def PlaySound():
   playsound('Notification_Track.mp3')
def Get_MAD():
   MAD = pd.read_excel(
      'Soil Plant Water-Aamir(100-125).xlsx',
      sheet_name='MAD',
      header=0)

   conn = sqlite3.connect("Location.db")
   cursor = conn.cursor()
   cursor.execute(
      "CREATE TABLE IF NOT EXISTS MAD_Type(Crop_Name TEXT,MAD INTEGER)")
   for i in range(28):
       list = MAD.loc[i, :]
       cursor.execute(
        "INSERT INTO MAD_Type(Crop_Name, MAD)VALUES(?,?)",
        (list[0], list[1]))
   conn.commit()
   cursor.close()
   conn.close()
def Import_MAD(CropName):
   CropName = Set_Crop_Capitalization(CropName)
   try:
      conn = sqlite3.connect("Location.db")
      cursor = conn.cursor()
      cursor.execute("SELECT MAD FROM MAD_Table WHERE Soil_Name = ?", (CropName,))
      MAD = cursor.fetchone()
      MAD = MAD[0]
      print(MAD)
      return MAD
   except:
      print("No MAD")
      return "NONE"
def Get_SoilTypes():
   Soil_Types = pd.read_excel(
      'Soil Plant Water-Aamir(100-125).xlsx',
      sheet_name='Soil Types',
      header=2)

   conn = sqlite3.connect("Location.db")
   cursor = conn.cursor()
   cursor.execute(
      "CREATE TABLE IF NOT EXISTS Soil_Type(Soil_Name TEXT,Fc INTEGER,PWP INTEGER, Available_Water_cm_per_m INTEGER, Available_Water_inch_feet INTEGER,AW_mm INTEGER,AW_inch_foot INTEGER)")
   #for i in range(5):
   list = Soil_Types.loc[0, :]
   cursor.execute(
       "INSERT INTO Soil_Type(Soil_Name, Fc, PWP, Available_Water_cm_per_m, Available_Water_inch_feet,AW_mm,AW_inch_foot)VALUES(?,?,?,?,?,?,?)",
       (list[0], list[1], list[2], list[3], list[4],list[5],list[6]))
   conn.commit()
   cursor.close()
   conn.close()
def ImportSoil_Data(SoilName):
   SoilName = Set_Crop_Capitalization(SoilName)
   try:
      conn = sqlite3.connect("Location.db")
      cursor = conn.cursor()
      cursor.execute("SELECT AW_mm,AW_inch_foot, Available_Water_cm_per_m, Available_Water_inch_feet FROM Soil_Type WHERE Soil_Name = ?", (SoilName,))
      for i in cursor.fetchall():
         AW = i[0][0]
         AW_inch = i[1][0]
         Holding_Capacity_cm = i[2][0]
         Holding_Capacity_inch = i[3][0]
      print(AW,AW_inch,Holding_Capacity_cm,Holding_Capacity_inch)
      return AW,AW_inch,Holding_Capacity_cm,Holding_Capacity_inch
      conn.commit()
      cursor.close()
      conn.close()
   except:
      print("No Data")
      return "NONE","NONE","NONE","NONE"
def Import_SoilTypes():
   conn = sqlite3.connect("Location.db")
   cursor = conn.cursor()
   cursor.execute("SELECT Soil_Name FROM Soil_Type")
   Soils = []
   for i in cursor.fetchall():
      Soils.append(i[0])
   conn.commit()
   cursor.close()
   conn.close()
   return Soils
def Get_Data():
   try:
      gc = gspread.service_account(filename='Data.json')
      sh = gc.open('Care_Lab_Server').sheet1
      col_2 = sh.col_values(1)[1:]
      col_3 = sh.col_values(3)[1:]
      Date = []
      k = 0
      for i in col_2:
         if i != 'second':
            Date.append(col_2[k])
         k += 1
      Sensor_2 = []
      j = 0
      for i in col_3:
         if i != '3rd':
            Sensor_2.append(int(col_3[j]))
         j += 1
      Notification = "Wifi Connected! Online Data is being Displayed"
   except:
      Sensor_2 = ""
      Date = "NO NETWORK"
      Notification = "NO Network Available! Connect to a Network"
   """
   max_int_list = max(int_list)
   min_int_list = min(int_list)
   if max_int_list != min_int_list:
      plt.ylim(min_int_list, max_int_list)
   print(min_int_list, max_int_list)
   """

   return Date, Sensor_2,Notification


def Location_Database():
   conn = sqlite3.connect("Location.db")
   cursor = conn.cursor()
   data = []

   cursor.execute("SELECT City,Crop,Soil,Bowing_Date FROM Settings_Table WHERE ID = ?",("1",))
   for i in cursor.fetchall():
      data.append(i[0])
      data.append(i[1])
      data.append(i[2])
      data.append(i[3])
   conn.commit()
   cursor.close()
   conn.close()
   return data
def Update_Location_Database(city,crop,date,soil):
   try:
      conn = sqlite3.connect("Location.db")
      cursor = conn.cursor()
      #cursor.execute("CREATE TABLE IF NOT EXISTS Settings_Table(ID TEXT, City TEXT, Crop TEXT,Soil TEXT, Bowing_Date TEXT) ")
      cursor.execute("UPDATE Settings_Table  SET City=?,Crop=?,Soil=?,Bowing_Date=? WHERE ID=?", (city, crop,soil, date,"1"))
      conn.commit()
      cursor.close()
      conn.close()
      status = 1
   except:
      status = 0
   return status
def Importing_CropTypes():
   Crop_Types = pd.read_excel(
      'Soil Plant Water-Aamir(100-125).xlsx',
      sheet_name='Table 11',
      header=0)
   conn = sqlite3.connect("CropsDatabase.db")
   cursor = conn.cursor()
   cursor.execute("CREATE TABLE IF NOT EXISTS CropTypes(Crop_Name TEXT,Initial_Values INTEGER,Crop_Development INTEGER, Mid_Session INTEGER, Last_Session INTEGER)")
   for i in range(24):
     list = Crop_Types.loc[i+1, :]
     cursor.execute("INSERT INTO CropTypes(Crop_Name, Initial_Values, Crop_Development, Mid_Session,Last_Session)VALUES(?,?,?,?,?)",(list[0],list[1],list[2],list[3],list[4]))
   conn.commit()
   cursor.close()
   conn.close()
def CropTypes():
   CropList = []
   Conn = sqlite3.connect("CropsDatabase.db")
   Cursor = Conn.cursor()
   Cursor.execute("SELECT Crop_Name FROM CropTypes")
   for i in Cursor.fetchall():
      CropList.append(i[0])
   Conn.commit()
   return CropList
def Importing_CityData():
   Cities = pd.read_excel(
      'Soil Plant Water-Aamir(100-125).xlsx',
      sheet_name='Table 8',
      header=1)
   conn = sqlite3.connect("CropsDatabase.db")
   cursor = conn.cursor()
   cursor.execute(
      "CREATE TABLE IF NOT EXISTS CityData(District TEXT,Jan INTEGER,Feb INTEGER, March INTEGER, Apr INTEGER,May INTEGER,Jun INTEGER, Jul INTEGER, Aug INTEGER,Sep INTEGER,Oct INTEGER, Nov INTEGER, Dec INTEGER)")
   for i in range(25):

      list = Cities.loc[i + 1, :]
      cursor.execute(
         "INSERT INTO CityData(District, Jan, Feb, March,Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
         (list[0], list[1], list[2], list[3], list[4], list[5],list[6], list[7], list[8], list[9], list[10], list[11],list[12]))
   conn.commit()
   cursor.close()
   conn.close()
def Get_CityData():
   CityList = []
   Conn = sqlite3.connect("CropsDatabase.db")
   Cursor = Conn.cursor()
   Cursor.execute("SELECT District FROM CityData")
   for i in Cursor.fetchall():
      CityList.append(i[0])
   Conn.commit()
   return CityList

def Validation(Entry):
   Msg = ""
   DigitCount = 0
   CharCount = 0
   if Entry != "":
      for i in Entry:
         if i.isdigit():
            DigitCount += 1
            Msg = "Digit Found"
         else:
            CharCount += 1
            Msg = "Char Found"
      if DigitCount == len(Entry):
         Msg = "Digit Entry"
      elif CharCount == len(Entry):
         Msg = "Char Entry"
   else:
      Msg = "Empty"
   return Msg
def Create_Validation(Username, Password):
   conn = sqlite3.connect("Location.db")
   cursor = conn.cursor()
   cursor.execute("CREATE TABLE IF NOT EXISTS LoginInfo(Username TEXT, Password TEXT)")
   cursor.execute("INSERT INTO LoginInfo(Username,Password)VALUES(?,?)",(Username,Password))
   conn.commit()
   cursor.close()
   conn.close()
def Login_Validation(Username,Password):
   conn = sqlite3.connect("Location.db")
   cursor = conn.cursor()
   cursor.execute("SELECT Password FROM LoginInfo WHERE Username = ?",(Username,))
   try:
      Pass = cursor.fetchone()
      if Pass[0] == Password:
         msg = "Successful"
      else:
         msg = "Password Failed"
   except:
      msg = "Username Failed"
   return msg
def Check_Eto(City):
   TimeFrame = time.time()
   month = str(datetime.datetime.fromtimestamp(TimeFrame).strftime('%m'))
   month = Check_Month(month)
   conn = sqlite3.connect("CropsDatabase.db")
   cursor = conn.cursor()
   cursor.execute("SELECT "+month+" FROM CityData WHERE District = ?",(City,))
   Eto = cursor.fetchone()
   Eto_List = []
   cursor.execute("SELECT * FROM CityData WHERE District = ?",(City,))
   for i in cursor.fetchall():
      for b in range(1,13):
         Eto_List.append(i[b])
      break
   conn.commit()
   cursor.close()
   conn.close()

   return Eto[0],month,Eto_List
def Check_Month(month):
   global DayNum
   if month == "01":
      month = "Jan"
      DayNum = 30
   if month == "02":
      month = "Feb"
      DayNum = 28
   if month == "03":
      month = "March"
      DayNum = 31
   if month == "04":
      month = "Apr"
      DayNum = 30
   if month == "05":
      month = "May"
      DayNum = 31
   if month == "06":
      month = "Jun"
      DayNum = 30
   if month == "07":
      month = "Jul"
      DayNum = 31
   if month == "08":
      month = "Aug"
      DayNum = 30
   if month == "09":
      month = "Sep"
      DayNum = 30
   if month == "10":
      month = "Oct"
      DayNum = 31
   if month == "11":
      month = "Nov"
      DayNum = 30
   if month == "12":
      month = "Dec"
      DayNum = 31
   return month
def Set_Date(BowingDate):
   global m
   global day
   global year
   countSlash = 0
   m = ""
   day = ""
   year = ""
   for i in BowingDate:
      if countSlash == 2:
         year += i
      elif i == "/":
         countSlash += 1
      elif countSlash == 1:
         day += i

      elif countSlash == 0:
         m += i
   if len(m) == 1:
      m = "0" + m
   month = Check_Month(m)
   year = "20"+year
   BDate = month + " " + day + ", " + year

   return BDate,month
def Import_Crop_Duration():
   Crop_Duration = pd.read_excel(
      'Soil Plant Water-Aamir(100-125).xlsx',
      sheet_name='Growth Days',
      header=2)
   conn = sqlite3.connect("CropsDatabase.db")
   cursor = conn.cursor()

   cursor.execute("CREATE TABLE IF NOT EXISTS Crop_Duration(Crop_Name TEXT,Total_Days INTEGER,Initial_Days INTEGER,Development_Days INTEGER,Mid_Days INTEGER,Last_Days INTEGER)")
   for i in range(31):
      list = Crop_Duration.loc[i + 1, :]
      cursor.execute("INSERT INTO Crop_Duration(Crop_Name, Total_Days,Initial_Days, Development_Days, Mid_Days, Last_Days)VALUES(?,?,?,?,?,?)",(list[0],list[1],list[2],list[3],list[4],list[5]))
   conn.commit()
   cursor.close()
   conn.close()
def Set_Crop_Capitalization(crop):
   crop = crop.lower()
   count = 0
   Crop = ""
   for i in crop:
      if count == 0:
         i = i.upper()

      count += 1
      Crop += i
   return Crop
def Get_Days_Duration(crop):
   Crop = Set_Crop_Capitalization(crop)
   conn = sqlite3.connect("CropsDatabase.db")
   cursor = conn.cursor()

   try:
      cursor.execute(
         "SELECT Total_Days,Initial_Days, Development_Days, Mid_Days, Last_Days FROM Crop_Duration WHERE Crop_Name = ?",
         (Crop,))
      for i in cursor.fetchall():
         Day = i[0][0]

         Initial_Days = i[1][0]

         Development_Days = i[2][0]

         Mid_Days = i[3][0]

         Late_Days = i[4][0]

      conn.commit()
      cursor.close()
      conn.close()
      return Day, Initial_Days, Development_Days, Mid_Days, Late_Days
   except:
      Day = "NOT FOUND"
      Initial_Days = ""
      Development_Days = ""
      Mid_Days = ""
      Late_Days = ""
      return Day, Initial_Days, Development_Days, Mid_Days, Late_Days

def Calculate_Duration(IDays,DvDays,MDays,LDays):
   global DayNum
   global m
   global day
   global year
   Initial_Date = []
   DayNum = DayNum - int(day)   #Getting Actual days of first month
   IDays = [IDays,DvDays,MDays,LDays]
   month = Check_Month(m)
   for i in range(4):
       while (IDays[i] > 0):
           if IDays[i] > DayNum:  # if First Season is greater than remaining days of Sowing month
               IDays[i] = IDays[i] - DayNum
               if int(m) != 12:
                   m = int(m) + 1
                   if m < 10:
                       m = "0" + str(m)
               else:
                   m = "01"
                   year = int(year) + 1
               month = Check_Month(m)
           else:
               Initial_Date.append(month + " " + str(IDays[i]) + ", " + str(year))
               DayNum = DayNum - IDays[i]
               IDays[i] = 0

   return Initial_Date
def Calculate_Days_Spent(BDate):
   global m
   global day
   global year
   TimeFrame = time.time()
   today = str(datetime.datetime.fromtimestamp(TimeFrame).strftime('%m/%d/%y'))
   d,month = Set_Date(BDate)

   BDate = date(int(year),int(m),int(day))
   d, month = Set_Date(today)
   today = date(int(year),int(m),int(day))
   diff = today - BDate
   day_spent=int(diff.days)
   return day_spent
def Check_Crop_Season(Days_Spent,IDays,DvDays,MDays,LDays):
   if Days_Spent <= IDays:
      Season = "Initial Stage"
   elif Days_Spent > IDays and Days_Spent<=DvDays:
      Season = "Development Stage"
   elif Days_Spent > DvDays and Days_Spent <= MDays:
      Season = "Mid Season Stage"
   elif Days_Spent > MDays and Days_Spent <= LDays:
      Season = "Late Season Stage"
   return Season
def Get_Kc():
   Kc = pd.read_excel(
      'Soil Plant Water-Aamir(100-125).xlsx',
      sheet_name='Kc',
      header=1)
   conn = sqlite3.connect("CropsDatabase.db")
   cursor = conn.cursor()

   cursor.execute(
      "CREATE TABLE IF NOT EXISTS Kc_Table(Crop_Name TEXT,Initial_Days INTEGER,Development_Days INTEGER,Mid_Days INTEGER,Last_Days INTEGER)")
   for i in range(25):
      list = Kc.loc[i + 1, :]
      cursor.execute(
         "INSERT INTO Kc_Table(Crop_Name,Initial_Days, Development_Days, Mid_Days, Last_Days)VALUES(?,?,?,?,?)",
         (list[0], list[1], list[2], list[3], list[4]))
   conn.commit()
   cursor.close()
   conn.close()
def Calculate_Kc(crop,season):
   if season =="Initial Stage":
      season = "Initial_Days"
   elif season == "Development Stage":
      season = "Development_Days"
   elif season == "Mid Season Stage":
      season = "Mid_Days"
   elif season == "Late Season Stage":
      season = "Last_Days"
   crop = Set_Crop_Capitalization(crop)
   conn = sqlite3.connect("CropsDatabase.db")
   cursor = conn.cursor()

   cursor.execute(
      "SELECT "+season+" FROM Kc_Table WHERE Crop_Name=?",(crop,))
   Kc = cursor.fetchone()
   Kc = Kc[0]


   Kc_List = []

   cursor.execute(
      "SELECT * FROM Kc_Table WHERE Crop_Name=?", (crop,))
   for i in cursor.fetchall():

      Kc_List.append(i[1])
      Kc_List.append(i[2])
      Kc_List.append(i[3])
      Kc_List.append(i[4])
      break

   conn.commit()
   cursor.close()
   conn.close()
   return Kc,Kc_List