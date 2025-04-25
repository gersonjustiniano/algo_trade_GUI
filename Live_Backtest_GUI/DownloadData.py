import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import filedialog
from datetime import date,datetime,timedelta
import time,random,sqlite3,os,threading
import MetaTrader5 as mt5
import pandas as pd

def download_data():
    win=tk.Toplevel()
    win.title('Download Data')
    win.geometry('375x115')
    win.resizable(0,0)
    win.configure(bg='#1c1c1c')

    #DOWNLOAD STATUS:
    canvas_status=tk.Canvas(win,bg='black',bd=0,highlightthickness=0)
    canvas_status.place(x=145,y=5,width=215,height=105)
    scrollbar_status=tk.Scrollbar(win,width=12,orient='vertical',command=canvas_status.yview)
    canvas_status.configure(yscrollcommand=scrollbar_status.set)
    scrollbar_status.place(x=360,y=5,height=105)
    
    frame_status=tk.Frame(canvas_status,bg='black')
    canvas_status.create_window((0,0),window=frame_status,anchor='nw')

    #SYMBOL:
    label_symbol=tk.Label(win,text='Symbol',bg='#1c1c1c',fg='white').place(x=5,y=5)
    symbols=['EURUSDm','BTCUSDm','XAUUSDm','US500m']
    combo_symbol=ttk.Combobox(win,values=symbols)
    combo_symbol.place(x=55,y=5,width=85,height=20)
    combo_symbol.set(symbols[0])

    #DATES:
    label_from=tk.Label(win,text='From',bg='#1c1c1c',fg='white').place(x=5,y=25)
    date_from=DateEntry(win,selectmode='days',date_pattern='dd/mm/yy')
    date_from.place(x=55,y=25,width=85,height=20)
    date_from.set_date(date(2022,1,3))
    label_to=tk.Label(win,text='To',bg='#1c1c1c',fg='white').place(x=5,y=45)
    date_to=DateEntry(win,selectmode='days',date_pattern='dd/mm/yy')
    date_to.place(x=55,y=45,width=85,height=20)
    date_to.set_date(date(2022,1,4))

    #SAVE IN FOLDER:
    def select_folder():
        folder_path=filedialog.askdirectory(title='Select Folder')
        if folder_path:
            label_folder.config(text=folder_path)
            button_download.config(state='normal')
    button_folder=tk.Button(win,text='Folder',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=select_folder)
    button_folder.place(x=5,y=65,width=45,height=20)
    label_folder=tk.Label(win,text='No Folder',bg='#1c1c1c',fg='white',anchor='w',justify='left')
    label_folder.place(x=55,y=65,width=85)

    ################################################################################################################################################################

    #DOWNLOAD/STOP DATA:
    run_download=[False]
    rows_status=[]
    labels_status=[] 

    def start_download():
        if len(labels_status)>0:
            for label in labels_status:
                label.destroy()

        win.protocol('WM_DELETE_WINDOW',lambda:None)
        run_download[0]=True
        button_download.config(state='disabled')
        button_stop.config(state='normal')
        #threading.Thread(target=downloading_data,daemon=True).start()

    def stop_download():
        win.protocol('WM_DELETE_WINDOW',win.destroy)
        run_download[0]=False
        button_download.config(state='normal')
        button_stop.config(state='disabled')

    button_download=tk.Button(win,text='Download',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=start_download)
    button_download.place(x=5,y=90,width=65,height=20)
    button_download.config(state='disabled')
    button_stop=tk.Button(win,text='Stop',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=stop_download)
    button_stop.place(x=75,y=90,width=65,height=20)
    button_stop.config(state='disabled')

    


