from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import Desk_Backend
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
from tkinter.ttk import Progressbar
CropList = Desk_Backend.CropTypes()
CityList = Desk_Backend.Get_CityData()

SoilList = Desk_Backend.Import_SoilTypes()
def DoneFun():
    global Crop
    global Location
    global Dentry
    global editRoot
    global Soil
    global progress
    status = Desk_Backend.Update_Location_Database(Location.get(),Crop.get(),Dentry.get(),Soil.get())

    if status == 1:
        progress['value'] = value
        Duration_Label['text'] = str(Duration) + " Days"
        Growth_Label['text'] = Season
        Eto = Desk_Backend.Check_Eto(Location.get())
        Eto_label['text'] = Eto
        Date,month = Desk_Backend.Set_Date(Dentry.get())
        DateStemp['text'] = Date
        SoilName_Label['text'] = Soil.get()
        CropName_Label['text'] = Crop.get()
        Location_Label['text'] = Location.get()
        if len(Crop.get()) > 6:
            CropName_Label['font'] = ("Times 10")
        editRoot.destroy()
    else:
        tk.messagebox.showerror("Database Error","Unable To store data in local database, Please Try again")
def Cancel():
    global editRoot
    editRoot.destroy()
def Add_Soil():
    AddSoilRoot = Tk()
    AddSoilRoot.geometry('560x230')
    AddSoilRoot.title("ADD NEW SOIL")
    soilFrame = Frame(AddSoilRoot, bg=BarColor)
    soilFrame.pack(fill=BOTH, expand=1)
    SoilLabel = Label(soilFrame,text = "Soil Type:",bg=BarColor,fg="white",font=("Times 12"))
    SoilLabel.pack()
    SoilLabel.place(x=20,y=30)
    SoilEntry = Entry(soilFrame,width = 10,font = ("Times 12"),bg=BarColor,borderwidth=3)
    SoilEntry.pack()
    SoilEntry.place(x=80,y=30)
def edit_func():
    global editEntry
    global editRoot
    editRoot = Tk()
    editRoot.geometry('560x230')
    editRoot.title("Settings")
    editFrame = Frame(editRoot,bg=BarColor)
    editFrame.pack(fill=BOTH,expand=1)
    editTitle=Label(editFrame,text="District/Region: ",bg=BarColor,fg="white",font=("Times 12 bold"))
    editTitle.pack()
    editTitle.place(x=20,y=30)
    global Crop
    global Location
    global Dentry
    global Soil
    Location = ttk.Combobox(editFrame, state="readonly",  width=30,
                            font=("Times 12"))
    Location['values'] = CityList

    Location.place(x=150, y=30)
    Location.current(13)
    CropLabel = Label(editFrame,text="Select Crop: ",bg=BarColor,font=("Times 12"),fg="white")
    CropLabel.pack()
    CropLabel.place(x=20,y=70)

    Crop = ttk.Combobox(editFrame, state="readonly", values=CropList, width=30,
                            font=("Times 12"))
    Crop.pack()
    Crop.place(x=150,y=70)
    Crop.current(0)
    SoilLabel = Label(editFrame, text="Soil Type: ", bg=BarColor, font=("Times 12"), fg="white")
    SoilLabel.pack()
    SoilLabel.place(x=20, y=110)

    Soil = ttk.Combobox(editFrame, state="readonly", values=SoilList, width=30,
                        font=("Times 12"))
    Soil.pack()
    Soil.place(x=150, y=110)
    Soil.current(0)
    BLabel = Label(editFrame, text="Bowing Date: ", bg=BarColor, font=("Times 12"), fg="white")
    BLabel.pack()
    BLabel.place(x=20, y=150)
    Dentry = DateEntry(editFrame,font=("Times 12"), width=30)
    Dentry.pack()
    Dentry.place(x=150,y=150)
    doneBtn =  Button(editFrame,text="Done",bg=BackColor,fg="white",font=("Times 12"),width=13,command=DoneFun)
    doneBtn.pack()
    doneBtn.place(x=430,y=20)
    AddBtn = Button(editFrame, text="Add District", bg=BackColor, fg="white", font=("Times 12"),width=13)
    AddBtn.pack()
    AddBtn.place(x=430, y=60)
    CropBtn = Button(editFrame, text="Add Crop", bg=BackColor, fg="white", font=("Times 12"),width=13)
    CropBtn.pack()
    CropBtn.place(x=430, y=100)
    SoilBtn = Button(editFrame, text="Add Soil/WHC", bg=BackColor, fg="white", font=("Times 12"), width=13,command=Add_Soil)
    SoilBtn.pack()
    SoilBtn.place(x=430, y=140)
    CancelBtn = Button(editFrame, text="Cancel", bg=BackColor, fg="white", font=("Times 12"),width=13,command=Cancel )
    CancelBtn.pack()
    CancelBtn.place(x=430, y=180)
def SubmitFun():
    global PassEntry
    global UserEntry
    global UserRoot
    error =0
    Msg = Desk_Backend.Validation(PassEntry.get())
    if Msg == "Empty":
        tk.messagebox.showerror("LOGIN FAILED","Please Enter your password")
        error = 1
    Msg = Desk_Backend.Validation(UserEntry.get())
    if Msg == "Empty":
        tk.messagebox.showerror("LOGIN FAILED", "Please Enter your Username")
        error = 1
    elif Msg == "Digit Entry":
        tk.messagebox.showerror("LOGIN FAILED", "Please Enter Valid Username")
        error = 1
    if error == 0:
        msg = Desk_Backend.Login_Validation(UserEntry.get(),PassEntry.get())
        if msg == "Successful":
            UserRoot.destroy()
            edit_func()
        else:
            tk.messagebox.showerror(msg,"Please Retry "+msg)
            PassEntry.delete(0,"end")
            UserEntry.delete(0,"end")
def Sub_event(event):
    SubmitFun()
def User_Validation():
    global UserRoot
    UserRoot = Tk()
    UserRoot.geometry('300x200')
    UserRoot.title("Validate Yourself")
    global PassEntry
    global UserEntry
    UserFrame = Frame(UserRoot,bg=BarColor)
    UserFrame.pack(fill=BOTH,expand=1)
    LogoLabel = Label(UserFrame,text="Varification",bg=BarColor,fg="white",font=("Times 14 bold"))
    LogoLabel.pack()
    LogoLabel.place(x=100,y=50)
    LoginLabel = Label(UserFrame,text="Username:",bg=BarColor,fg="white",font=("Times 12 bold"))
    LoginLabel.pack()
    LoginLabel.place(x=20,y=80)
    PassLabel = Label(UserFrame, text="Password:", bg=BarColor, fg="white", font=("Times 12 bold"))
    PassLabel.pack()
    PassLabel.place(x=20, y=120)
    UserEntry = Entry(UserFrame, bg=BarColor,fg="white",font=("Times 12"), width=20,borderwidth=4)
    UserEntry.pack()
    UserEntry.place(x=100,y=80)
    PassEntry = Entry(UserFrame, bg=BarColor,fg="white", font=("Times 12"), width=20, borderwidth=4,show="*")
    PassEntry.pack()
    PassEntry.place(x=100, y=120)
    UserEntry.focus_force()
    UserEntry.config(insertbackground="white")
    PassEntry.config(insertbackground="white")
    UserEntry.bind("<Return>", Sub_event)
    PassEntry.bind("<Return>", Sub_event)
    SubmitButton = Button(UserFrame,text="SUBMIT",bg=ButtonColor,fg="white",relief=RAISED,font=("Times 10 bold"),command=SubmitFun)
    SubmitButton.pack()
    SubmitButton.place(x=200,y=155)
    CButton = Button(UserFrame, text="CANCEL", bg=Button2Color, fg="white", relief=RAISED, font=("Times 10 bold"))
    CButton.pack()
    CButton.place(x=100, y=155)
def Add_Duration():
    AddRoot = Tk()
    AddRoot.geometry('200x300')
    AddRoot.title("Add Crop Duration")
    Addframe = Frame(AddRoot,bg=BarColor,relief = RIDGE)
    Addframe.pack(fill= BOTH,expand=1)
    NameLabel = Label(Addframe,text="Crop: ",bg=BarColor,font=("Times 12"),fg=grayColor)
    NameLabel.pack()
    NameLabel.place(x=10,y=20)
    Name = Label(Addframe,text=Crop_Name,bg=BarColor,font=("Time 12 bold"),fg="white")
    Name.pack()
    Name.place(x=70,y=20)
    DaysLabel = Label(Addframe, text="Duration (Days): ", bg=BarColor, font=("Times 12"), fg=grayColor)
    DaysLabel.pack()
    DaysLabel.place(x=10, y=20)
def Draw_Plot():

    print_Data = ["0",str(I_Days), str(D_Days), str(Mid_Days), str(Late_Days)]
    date_Data = [str(BDate), str(Initial_Date), str(Development_Date), str(Mid_Date), str(Late_Date)]
    titles = ["Soing Date","Initial Stage","Development Stage","Mid Season","Late Season"]
    plt.figure(figsize=(20, 5))
    plt.plot(titles,date_Data,marker="o")
    for i in range(4):
        i += 1
        plt.annotate(print_Data[i] + " Days", xy=(titles[i], date_Data[i]),
                     xytext=(titles[i], date_Data[i]))

    plt.title(Crop_Name)
    plt.xlabel("Dates")
    plt.ylabel("Days")
    plt.show()


def View_Duration():
    xAlign = 150
    AddRoot = Tk()
    AddRoot.geometry('500x300')
    AddRoot.title("Add Crop Duration")

    Addframe = Frame(AddRoot, bg=BarColor, relief=RIDGE)
    Addframe.pack(fill=BOTH, expand=1)

    NameLabel = Label(Addframe, text="Crop: ", bg=BarColor, font=("Times 12"), fg=grayColor)
    NameLabel.pack()
    NameLabel.place(x=10, y=50)
    Name = Label(Addframe, text=Crop_Name, bg=BarColor, font=("Time 12 bold"), fg="white")
    Name.pack()
    Name.place(x=xAlign, y=50)

    # Dates View
    Label_data = ["Duration: ", "Initial Stage: ", "Development Stage: ", "Mid Season Stage: ", "Late Season Stage: "]
    print_Data = [str(Duration), str(I_Days), str(D_Days), str(Mid_Days), str(Late_Days)]
    date_Data = [Late_Date, Initial_Date, Development_Date, Mid_Date, Late_Date]
    Y_Axis = 80
    for i in range(5):
        LateLabel = Label(Addframe, text=Label_data[i], bg=BarColor, font=("Times 12"), fg=grayColor)
        LateLabel.pack()
        LateLabel.place(x=10, y=Y_Axis)
        Duration_Frame = LabelFrame(Addframe, bg=BarColor, fg="white", width=230, height=30)
        Duration_Frame.pack()
        Duration_Frame.place(x=xAlign, y=Y_Axis)
        Days_Label = Label(Duration_Frame, text=print_Data[i] + " Days:", bg=BarColor, font=("Times 12 bold"),
                           fg="white")
        Days_Label.pack()
        Days_Label.place(x=5, y=1)
        D_Label = Label(Duration_Frame, text=date_Data[i], bg=BarColor, fg="white", font=("Times 12 bold"))
        D_Label.pack()
        D_Label.place(x=100, y=1)
        Y_Axis += 40
def View_ProgressBar():
    global progress
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", foreground='red', background=BackColor)
    progress = Progressbar(frame, orient=HORIZONTAL, style="red.Horizontal.TProgressbar",
                           length=400, mode='determinate')
    progress.pack()
    progress.place(x=950, y=280)
    progress['value'] = value
    DaysLabel = Label(frame,bg=BackColor,text="Days Spent:",font=("Times 12"),fg=grayColor)
    DaysLabel.pack()
    DaysLabel.place(x=1210,y=310)
    ValueLabel = Label(frame,bg=BackColor,text=str(Days_Spent)+"/"+str(Duration),fg=grayColor,font=("Times 12"))
    ValueLabel.pack()
    ValueLabel.place(x=1290,y=310)
def KcGraph():
    KcList = []
    stages = ["Initial Stage","Development Stage", "Mid Season stage", "Late Season Stage"]
    date_Data = [str(BDate), str(Initial_Date), str(Development_Date), str(Mid_Date), str(Late_Date)]
    KcList = [Kc_List[0],Kc_List[0],Kc_List[2],Kc_List[2],Kc_List[3]]
    #date_Data = [str(Initial_Date), str(Development_Date), str(Mid_Date), str(Late_Date)]
    plt.figure(figsize=(20, 5))
    plt.plot(date_Data, KcList,linestyle='--', marker='o')
    for i in range(4):
        if i == 0 or i == 2:
            plt.annotate("  "+stages[i], xy=(date_Data[i], KcList[i]),xytext=(date_Data[i], KcList[i]))
        if i == 1 or i == 3:
            plt.annotate(stages[i], xy=(date_Data[i], KcList[i]),xytext=(date_Data[i], KcList[i]))
        else:
            pass
    plt.title(Crop_Name)
    plt.xlabel("Stages")
    plt.ylabel("Kc")
    plt.show()
def Plot_Eto():
    month_List = ["Jan","Feb","March","Apr","May","Jun","July","Aug","Sep","Oct","Nov","Dec"]
    plt.figure(figsize=(20, 5))
    plt.bar(month_List, Eto_List)

    for i in range(12):
        if month_List[i] == today_Month:
            plt.annotate(str(Eto_List[i])+"(Current)", xy=(month_List[i], Eto_List[i]), xytext=(month_List[i], Eto_List[i]),color="green")

        else:
           plt.annotate(Eto_List[i], xy=(month_List[i], Eto_List[i]), xytext=(month_List[i], Eto_List[i]))
    plt.title(Crop_Name)
    plt.xlabel("Months")
    plt.ylabel("Eto")
    plt.show()
def NOTIFICATION_Bar():
    global Count
    Count -= 1
    if Count > 950:
        if Count == 951:
           Desk_Backend.PlaySound()
        NotiFrame.place(x=Count,y=600)
        root.after(2,NOTIFICATION_Bar)
global Count
Count = 1450
BackColor = "#3e4241"
BarColor = "#212423"
ButtonColor = "#e630d9"
ButtonBackColor = "#5e0558"
Button2Color = "#24bd17"
grayColor = "#949699"
lightGreenColor = "#6fde6f"
root = Tk()
root.title("Farm House IUB")
root.geometry('1450x700')
bar_icon = PhotoImage(file="bar-chart-5-16.png")
tempImg= PhotoImage(file="temperature-2-24.png")
locImg=PhotoImage(file="map-marker-2-24.png")
SettingIcon = PhotoImage(file="settings-4-24.png")
Plot_Icon = PhotoImage(file="scatter-plot-24.png")
frame = Frame(root, relief=RIDGE, bg=BackColor)
frame.pack(fill=BOTH, expand=1)
barFrame = Frame(frame,bg=BarColor, relief = RAISED,width=1450,height=100)
barFrame.pack()
barFrame.place(x=0,y=0)
MainLabel=Label(barFrame,text="FARM HOUSE MONITORING SYSTEM",bg=BarColor,fg="white",font=("Times 16 bold"))
MainLabel.pack()
MainLabel.place(x=20,y=40)
#  DATA
data = Desk_Backend.Location_Database()
city = data[0]
Crop_Name = data[1]
Soil_Name = data[2]
BowingDate = data[3]
BDate,month = Desk_Backend.Set_Date(BowingDate)
Available_Water, AW_inch,HOLDING_Capacity_cm,Holding_Capacity_inch = Desk_Backend.ImportSoil_Data(Soil_Name)
MAD = Desk_Backend.Import_MAD(Crop_Name)
LocationLabel=Label(barFrame,image=locImg,bg=BarColor)
LocationLabel.pack()
LocationLabel.place(x=1150,y=20)
Crop_Label = Label(barFrame,text="Crop: ",bg=BarColor,fg="white",font=("Times 12"))
Crop_Label.pack()
Crop_Label.place(x=950,y=20)

Soil_Label = Label(barFrame,text="Soil: ",bg=BarColor,fg="white",font=("Times 12"))
Soil_Label.pack()
Soil_Label.place(x=950,y=60)

TempLabel=Label(barFrame,image=tempImg,bg=BarColor)
TempLabel.pack()
TempLabel.place(x=1150,y=60)

Location_Label = Label(barFrame,text=city,bg=BarColor,fg="white",font=("Times 14"))
Location_Label.pack()
Location_Label.place(x=1200,y=20)

CropName_Label = Label(barFrame,text=Crop_Name,bg=BarColor,fg="white",font=("Times 14"))
CropName_Label.pack()
CropName_Label.place(x=1000,y=20)
if len(Crop_Name) > 6:
    CropName_Label['font'] = ("Times 10")
SoilName_Label = Label(barFrame,text=Soil_Name,bg=BarColor,fg="white",font=("Times 14"))
SoilName_Label.pack()
SoilName_Label.place(x=1000,y=60)

temp = "25"
Temp_Label = Label(barFrame,text=temp,bg=BarColor,fg="white",font=("Times 14"))
Temp_Label.pack()
Temp_Label.place(x=1200,y=60)
Degree_Label = Label(barFrame,text="o",bg=BarColor,fg="white",font=("Times 12"))
Degree_Label.pack()
Degree_Label.place(x=1220,y=56)
#Importing ONline Data
Graph_Date, Sensor_2,Notification_Label = Desk_Backend.Get_Data()
#NOTIFICATION WINDOW
def CloseFrame():
    global Count
    Count += 1
    if Count < 1450:
        NotiFrame.place(x=Count, y=600)
        root.after(2, CloseFrame)
        if Count == 1449:
           NotiFrame.destroy()
NotiFrame = Frame(frame,bg="green",width=400,height=50)
NotiFrame.pack()
#NotiFrame.place(x=950,y=600)
Noti = Label(NotiFrame,text=Notification_Label,bg="green",fg="white",font=("Times 12 bold"))
Noti.pack()
Noti.place(x=10,y=10)
closeframeBtn = Button (NotiFrame,text="x",bg="green",fg="white",relief=FLAT,command=CloseFrame,font=("Times 9"))
closeframeBtn.pack()
closeframeBtn.place(x=370,y=5)
closeframeBtn.bind("<Enter>",lambda x: closeframeBtn['bg']==lightGreenColor)
def showtip(text):
    #"Display text in tooltip window"
    #tipwindow = None
    text = text

    #if tipwindow or not text:
     #   return
    x, y, cx, cy = editbtn.bbox("insert")

    x = x + editbtn.winfo_rootx() + 57
    y = y + cy + editbtn.winfo_rooty() + 27

    tipwindow = tw = Toplevel(editbtn)
    tw.wm_overrideredirect(1)
    tw.wm_geometry("+%d+%d" % (x, y))
    label = Label(tw, text=text, justify=LEFT,
                  background="#ffffe0", relief=SOLID, borderwidth=1,
                  font=("tahoma", "8", "normal"))
    label.pack(ipadx=1)
def on_enter(event):

    showtip("SETTINGS")

def on_leave(event):
    editbtn.configure(text="")
editbtn = Button(barFrame,image=SettingIcon,bg=BarColor,relief=FLAT, cursor="plus",command=User_Validation)
editbtn.pack()
editbtn.place(x=1300,y=40)
editbtn.bind("<Enter>",on_enter)
editbtn.bind("<Leave>",on_leave)
# Choose Sensor
ChoiceFrame = LabelFrame(frame,text="Choose Sensor",bg=BackColor,fg="white",width=200,height=520)
ChoiceFrame.pack()
ChoiceFrame.place(x=10,y=110)
Sensor1 = Button(ChoiceFrame,text="Salinity Sensor",bg=ButtonColor,fg="white",font=("Times 14"),width=15)
Sensor1.pack()
Sensor1.place(x=15,y=20)

#Get Eto
Eto,today_Month,Eto_List= Desk_Backend.Check_Eto(city)

#Statistic Frame
StateFrame = LabelFrame(frame,bg=BarColor,width = 400,height=50,fg="white",)
StateFrame.pack()
StateFrame.place(x=950,y=100)

Eo_Label = Button(StateFrame,text="Eto("+today_Month+"):",image=Plot_Icon,bg=BarColor,fg=grayColor,font=("Times 12"),relief=FLAT,compound=LEFT,command=Plot_Eto)
Eo_Label.pack()
Eo_Label.place(x=10,y=9)
Eto_label = Label(StateFrame,text=Eto,font=("Times 12 bold"),bg=BarColor,fg="white")
Eto_label.pack()
Eto_label.place(x=120,y=10)

#Days Frame
DaysFrame = LabelFrame(frame,bg=BarColor,width = 400,height=50,fg="white")
DaysFrame.pack()
DaysFrame.place(x=950,y=160)
DurationLabel = Label(DaysFrame,text="Crop Duration: ",fg=grayColor,bg=BarColor,font=("Times 12"))
DurationLabel.pack()
DurationLabel.place(x=10,y=10)
Duration, I_Days, D_Days, Mid_Days, Late_Days = Desk_Backend.Get_Days_Duration(Crop_Name)
Duration_Label = Button(DaysFrame,text=Duration, bg=BarColor, fg="white",font=("Times 12 bold"),relief= RAISED)
Duration_Label.pack()
Duration_Label.place(x=110,y=9)
View_Bar = Button(DaysFrame,image=bar_icon,bg=BarColor,relief = FLAT,command=Draw_Plot)
View_Bar.pack()
View_Bar.place(x=200,y=9)
View_Growth = Label(DaysFrame,text="Growth:",bg=BarColor,fg=grayColor,font=("Times 12"))
View_Growth.pack()
View_Growth.place(x=220,y=9)
Growth_Label = Label(DaysFrame,bg=BarColor,fg="white",font=("Times 12"))
Growth_Label.pack()
Growth_Label.place(x=275,y=9)
#Kc Frame
KcFrame = LabelFrame(frame,bg=BarColor,width = 400,height=50,fg="white")
KcFrame.pack()
KcFrame.place(x=950,y=220)
KcLabel = Label(KcFrame,text="Kc:",bg=BarColor,fg=grayColor,font=("Times 12"))
KcLabel.pack()
KcLabel.place(x=5,y=9)
KcValue = Button(KcFrame,bg=BarColor,fg="white",font=("Times 12"),relief=RAISED)
KcValue.pack()
KcValue.place(x=50,y=9)
ETcLabel = Label(KcFrame,text="ETc:",bg=BarColor,fg=grayColor,font=("Times 12"))
ETcLabel.pack()
ETcLabel.place(x=100,y=9)
ETcValue = Label(KcFrame,bg=BarColor,fg="white",font=("Times 12"))
ETcValue.pack()
ETcValue.place(x=150,y=9)
if Duration == "NOT FOUND":
    Duration_Label['fg'] = "red"
    Duration_Label['font'] = ("Times 10")
    Duration_Label['command'] = Add_Duration
    View_Bar['state'] = DISABLED
    Growth_Label['text'] = "ADD DETAILS"
    Growth_Label['fg'] = "red"
else:
    Duration_Label['text'] = str(Duration)+" Days"
    Duration_Label['command'] =View_Duration
    Initial_Date,Development_Date,Mid_Date,Late_Date=Desk_Backend.Calculate_Duration(I_Days, D_Days, Mid_Days, Late_Days)
    View_Bar['state'] = NORMAL
    Days_Spent = Desk_Backend.Calculate_Days_Spent(BowingDate)
    Season = Desk_Backend.Check_Crop_Season(Days_Spent,I_Days,I_Days+D_Days,I_Days+D_Days+Mid_Days,Duration)
    Growth_Label['text'] = Season
    value = int((float(Days_Spent) * 100) / float(Duration))
    View_ProgressBar()
    Kc,Kc_List = Desk_Backend.Calculate_Kc(Crop_Name,Season)
    Etc = float(Eto) * float(Kc)
    Etc = "{:.2f}".format(Etc)
    ETcValue['text']=str(Etc)
    KcValue['text'] = str(Kc)
    KcValue['command'] = KcGraph

Date_Label = Label(StateFrame,text="Sowing Date: ",bg=BarColor,fg=grayColor,font=("Times 12"))
Date_Label.pack()
Date_Label.place(x=190,y=10)
DateStemp = Label(StateFrame,text=BDate,bg=BarColor,fg="white",font=("Times 12 bold"))
DateStemp.pack()
DateStemp.place(x=280,y=10)

# Creating Data to be plotted

if Graph_Date == "NO NETWORK":
    data1 = {'Country': ['US', 'CA', 'GER', 'UK', 'FR'],
              'GDP_Per_Capita': [42000, 43000, 49000, 40000, 53000]
              }
    df1 = DataFrame(data1, columns=['Country', 'GDP_Per_Capita'])
else:
    data1 = {'Time': Graph_Date,
             'Sensor 2': Sensor_2
             }
    df1 = DataFrame(data1, columns=['Time', 'Sensor 2'])

"""
"""

Graphframe = LabelFrame(frame,bg=BackColor,fg="white",text="Sensors Data",width=1150,height=500)
Graphframe.pack()
Graphframe.place(x=220,y=110)
figure = plt.Figure(figsize=(6,5), dpi=100)
ax = figure.add_subplot(111)
chart_type = FigureCanvasTkAgg(figure, Graphframe)
chart_type.get_tk_widget().pack()

#df1 = df1[['Time','Sensor Data']].groupby('Time').sum()
df1.plot(kind='line', legend=True, ax=ax)
#df_1 = df_1[['Country','GDP_Per_Capita']].groupby('Country').sum()
#df_1.plot(kind='line', legend=True, ax=ax)
ax.set_title('Land Data')
NOTIFICATION_Bar()
root.mainloop()