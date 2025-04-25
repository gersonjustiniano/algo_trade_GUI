import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import font
from datetime import date,datetime,timedelta,timezone
import time,random
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import MetaTrader5 as mt5
import pandas as pd
import csv
import os,sys
import json
import sqlite3
import numpy as np
import importlib.util

#personal modules:
from DownloadData import download_data
from NeuralNetConsole import neural_net_console

#PRINCIPAL WINDOW PROPERTIES:
win=tk.Tk()
win.title('Mojo Trade')
win.geometry('1000x625')
win.resizable(0,0)
win.configure(bg='#1c1c1c')

################################################################################################################################################################

#CANVAS LINES:
line1=tk.Canvas(win,width=2,height=625,bg='#1c1c1c',bd=0,highlightthickness=0,highlightbackground='#FF0000')
line1.place(x=230,y=0)
line1.create_line(1,0,1,625,width=1,fill='grey')

line2=tk.Canvas(win,width=230,height=2,bg='#1c1c1c',bd=0,highlightthickness=0,highlightbackground='#FF0000')
line2.place(x=0,y=55)
line2.create_line(0,1,230,1,width=1,fill='grey')

line3=tk.Canvas(win,width=230,height=2,bg='#1c1c1c',bd=0,highlightthickness=0,highlightbackground='#ff0000')
line3.place(x=0,y=135)
line3.create_line(0,1,230,1,width=1,fill='grey')

line4=tk.Canvas(win,width=230,height=2,bg='#1c1c1c',bd=0,highlightthickness=0,highlightbackground='#ff0000')
line4.place(x=0,y=165)
line4.create_line(0,1,230,1,width=1,fill='grey')

line5=tk.Canvas(win,width=230,height=2,bg='#1c1c1c',bd=0,highlightthickness=0,highlightbackground='#ff0000')
line5.place(x=0,y=315)
line5.create_line(0,1,230,1,width=1,fill='grey')

line6=tk.Canvas(win,width=230,height=2,bg='#1c1c1c',bd=0,highlightthickness=0,highlightbackground='#ff0000')
line6.place(x=0,y=410)
line6.create_line(0,1,230,1,width=1,fill='grey')

line6=tk.Canvas(win,width=230,height=2,bg='#1c1c1c',bd=0,highlightthickness=0,highlightbackground='#ff0000')
line6.place(x=0,y=505)
line6.create_line(0,1,230,1,width=1,fill='grey')



################################################################################################################################################################

#RADIO LIVE, BACKTEST:

var_LiveBacktest=tk.StringVar()
def update_radio_LiveBacktest(*args):
    for rb in (radio_live,radio_backtest):
        if rb.cget('value')==var_LiveBacktest.get():
            rb.config(bg='grey',fg='black')
        else:
            rb.config(bg='#1c1c1c',fg='white')

def enable_plot():
    radio_plot.config(state='normal')
    check_download_data.config(state='normal')
    if var_download_data.get():
        button_download_data.config(state='normal')
    else:
        button_download_data.config(state='disable')
    calendar_from.config(state='normal')
    calendar_to.config(state='normal')  
    if var_trade.get():
        spin_balance.config(state='normal')
        spin_leverage.config(state='normal')
    else:
        spin_balance.config(state='disable')
        spin_leverage.config(state='disable')
    var_balance.set(100)
    var_leverage.set(500)

def disable_plot():
    radio_plot.config(state='disabled')
    label_file_symbol.config(text='No File')
    check_download_data.config(state='disable')
    button_download_data.config(state='disable')
    calendar_from.config(state='disable')
    calendar_to.config(state='disable')
    spin_balance.config(state='disable')
    spin_leverage.config(state='disable')
    var_radio.set('animate')
    indi.set_live_BalanceLeverage(var_balance,var_leverage)

radio_live=tk.Radiobutton(win,text='Live',variable=var_LiveBacktest,value='live',fg='white',bg='#1c1c1c',indicatoron=False,command=disable_plot)
radio_live.place(x=5,y=5,width=110,height=20)
radio_backtest=tk.Radiobutton(win,text='Backtest',variable=var_LiveBacktest,value='backtest',fg='white',bg='#1c1c1c',indicatoron=False,command=enable_plot)
radio_backtest.place(x=120,y=5,width=105,height=20)
var_LiveBacktest.trace_add('write',update_radio_LiveBacktest)
var_LiveBacktest.set('backtest')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

#RADIO ANIMATE, PLOT, TABLE:

def update_radio(*args):
    for rb in (radio_animate,radio_plot,radio_table):
        if rb.cget('value')==var_radio.get():
            rb.config(bg='gray',fg='black')
        else:
            rb.config(bg='#1c1c1c',fg='white')

def show_graph_table():
    if var_radio.get()=='animate' or var_radio.get()=='plot':
        frame_graph.tkraise()
    elif var_radio.get()=='table':
        frame_table.tkraise()

var_radio=tk.StringVar()
radio_animate=tk.Radiobutton(win,text='Animate',variable=var_radio,value='animate',bg='#1c1c1c',fg='white',indicatoron=False,command=show_graph_table)
radio_animate.place(x=5,y=30,width=70,height=20)
radio_plot=tk.Radiobutton(win,text='Plot',variable=var_radio,value='plot',bg='#1c1c1c',fg='white',indicatoron=False,command=show_graph_table)
radio_plot.place(x=80,y=30,width=70,height=20)
radio_table=tk.Radiobutton(win,text='Table',variable=var_radio,value='table',bg='#1c1c1c',fg='white',indicatoron=False,command=show_graph_table)
radio_table.place(x=155,y=30,width=70,height=20)
var_radio.trace_add('write',update_radio)
var_radio.set('animate')

################################################################################################################################################################

#SYMBOL COMBO:
def select_symbol(event):
    if var_LiveBacktest.get()=='backtest':
        file=filedialog.askopenfilename(title='select file')
        if file:
            label_file_symbol.config(text=file)
label_combo=tk.Label(win,text='Symbol',bg='#1c1c1c',fg='white').place(x=5,y=60)
symbols=['EURUSDm','BTCUSDm','XAUUSDm','US500m']
combo_symbol=ttk.Combobox(win,values=symbols)
combo_symbol.place(x=60,y=60,width=80,height=20)
combo_symbol.bind('<<ComboboxSelected>>',select_symbol)

#LABEL FILE SYMBOL:
label_file_symbol=tk.Label(win,text='No File',width=11,anchor='w',justify='left',bg='#1c1c1c',fg='white')
label_file_symbol.place(x=140,y=60)

#INTERVAL COMBO:
label_interval=tk.Label(win,text='Interval',bg='#1c1c1c',fg='white').place(x=5,y=85)
intervals=['M1','M5','M15','M30','H1','H4','D1']
combo_intervals=ttk.Combobox(win,values=intervals)
combo_intervals.place(x=60,y=85,width=50,height=20)
combo_intervals.set('M1')

#DOWNLOAD DATA FOR BACKTESTING:
def enable_download_data():
    if var_download_data.get():
        button_download_data.config(state='normal')
    else:
        button_download_data.config(state='disabled')
var_download_data=tk.BooleanVar()
var_download_data.set(False)
check_download_data=tk.Checkbutton(win,variable=var_download_data,bg='#1c1c1c',activebackground='#333333',command=enable_download_data)
check_download_data.place(x=110,y=82)
button_download_data=tk.Button(win,text='Download Data',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=download_data)
button_download_data.place(x=135,y=85,width=90,height=20)
enable_download_data()

#DATES:
label_fromTo=tk.Label(win,text='From/To',bg='#1c1c1c',fg='white').place(x=5,y=110)
calendar_from=DateEntry(win,selectmode='days',date_pattern='dd/mm/yy')
calendar_from.place(x=60,y=110,width=80)
calendar_from.set_date(date(2022,1,3))
calendar_to=DateEntry(win,selectmode='days',date_pattern='dd/mm/yy')
calendar_to.place(x=145,y=110,width=80)
calendar_to.set_date(date(2022,1,4))

################################################################################################################################################################

#WILLIAM INDICATORS:

will_indicators=['Alligator','Fractals','Awesome O']
alligator_values={'lips':[5,'green'],'teeths':[8,'red'],'jaw':[13,'blue']}
fractals_values={'fractal':2,'up':'#3ba3bc','down':'#264f5a'}
awesome_values={'slow':34,'fast':5,'up':'#3ba3bc','down':'#264f5a'}

#LABEL WILLIAM:
label_will=tk.Label(win,text='William',bg='#1c1c1c',fg='white').place(x=5,y=140)

#COMBO WILLIAM INDICATORS:
def select_will_values(event):
    will_vals={
            'Alligator':f"({alligator_values['lips'][0]}, {alligator_values['teeths'][0]}, {alligator_values['jaw'][0]})",
            'Fractals':f"({fractals_values['fractal']})",
            'Awesome O':f"({awesome_values['fast']}, {awesome_values['slow']})"
    }[combo_will.get()]
    label_will_values.config(text=will_vals)
combo_will=ttk.Combobox(win,values=will_indicators)
combo_will.place(x=50,y=140,width=90,height=20)
combo_will.set(will_indicators[0])
combo_will.bind('<<ComboboxSelected>>',select_will_values)

#LABEL_WILLIAM_VALUES:
alligator_vals=f"({alligator_values['lips'][0]}, {alligator_values['teeths'][0]}, {alligator_values['jaw'][0]})"
label_will_values=tk.Label(win,text=alligator_vals,bg='#1c1c1c',fg='white')
label_will_values.place(x=145,y=140)

#BUTTON CONFIG WILLIAM INDICATOR:
def alligator_window():
    win_alligator=tk.Toplevel()
    win_alligator.title('alligator settings')
    win_alligator.geometry('190x160')
    win_alligator.resizable(0,0)
    win_alligator.configure(bg='#1c1c1c')

    color_alligator={'lips':None,'teeths':None,'jaw':None}

    def set_color_lips():
        color_code_lips=colorchooser.askcolor(title='color lips')[1]
        if color_code_lips:
            color_lips.config(bg=color_code_lips)
            color_alligator['lips']=color_code_lips
        else:
            color_alligator['lips']=alligator_values['lips'][1]
    
    def set_color_teeth():
        color_code_teeth=colorchooser.askcolor(title='color teeth')[1]
        if color_code_teeth:
            color_teeth.config(bg=color_code_teeth)
            color_alligator['teeths']=color_code_teeth
        else:
            color_alligator['teeths']=alligator_values['teeths'][1]

    def set_color_jaw():
        color_code_jaw=colorchooser.askcolor(title='color jaw')[1]
        if color_code_jaw:
            color_jaw.config(bg=color_code_jaw)
            color_alligator['jaw']=color_code_jaw
        else:
            color_alligator['jaw']=alligator_values['jaw'][1]
   
    def set_alligator():
        alligator_values['lips'][0]=int(spin_lips.get())
        alligator_values['teeths'][0]=int(spin_teeth.get())
        alligator_values['jaw'][0]=int(spin_jaw.get())
        label_will_values.config(text=f"({spin_lips.get()}, {spin_teeth.get()}, {spin_jaw.get()})")

        if color_alligator['lips'] is not None:
            alligator_values['lips'][1]=color_alligator['lips']
        if color_alligator['teeths'] is not None:
            alligator_values['teeths'][1]=color_alligator['teeths']
        if color_alligator['jaw'] is not None:
            alligator_values['jaw'][1]=color_alligator['jaw']

        win_alligator.destroy()


    var_lips=tk.IntVar(value=alligator_values['lips'][0])
    label_lips=tk.Label(win_alligator,text='Lips',bg='#1c1c1c',fg='white').place(x=20,y=20)
    spin_lips=tk.Spinbox(win_alligator,from_=1,to=1000,textvariable=var_lips)
    spin_lips.place(x=80,y=20,width=50)
    color_lips=tk.Button(win_alligator,bg=alligator_values['lips'][1],activebackground='grey',command=set_color_lips)
    color_lips.place(x=150,y=20,width=20,height=20)

    var_teeth=tk.IntVar(value=alligator_values['teeths'][0])
    label_teeth=tk.Label(win_alligator,text='Teeths',bg='#1c1c1c',fg='white').place(x=20,y=50)
    spin_teeth=tk.Spinbox(win_alligator,from_=1,to=1000,textvariable=var_teeth)
    spin_teeth.place(x=80,y=50,width=50)
    color_teeth=tk.Button(win_alligator,bg=alligator_values['teeths'][1],activebackground='grey',command=set_color_teeth)
    color_teeth.place(x=150,y=50,width=20,height=20)

    var_jaw=tk.IntVar(value=alligator_values['jaw'][0])
    label_jaw=tk.Label(win_alligator,text='Jaw',bg='#1c1c1c',fg='white').place(x=20,y=80)
    spin_jaw=tk.Spinbox(win_alligator,from_=1,to=1000,textvariable=var_jaw)
    spin_jaw.place(x=80,y=80,width=50)
    color_jaw=tk.Button(win_alligator,bg=alligator_values['jaw'][1],activebackground='grey',command=set_color_jaw)
    color_jaw.place(x=150,y=80,width=20,height=20)

    alligator_accept=tk.Button(win_alligator,text='Accept',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=set_alligator)
    alligator_accept.place(x=20,y=120,width=60)
    alligator_cancel=tk.Button(win_alligator,text='Cancel',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=win_alligator.destroy)
    alligator_cancel.place(x=110,y=120,width=60)

def fractal_window():
    win_fractal=tk.Toplevel()
    win_fractal.title('Fractal settings')
    win_fractal.geometry('190x120')
    win_fractal.resizable(0,0)
    win_fractal.configure(bg='#1c1c1c')

    color_fractals={'up':None,'down':None}

    def set_color_fractal_up():
        color_code_up=colorchooser.askcolor(title='color fractal up')[1]
        if color_code_up:
            color_up.config(bg=color_code_up)
            color_fractals['up']=color_code_up
        else:
            color_fractals['up']=fractals_values['up']

    def set_color_fractal_down():
        color_code_down=colorchooser.askcolor(title='color fractal down')[1]
        if color_code_down:
            color_down.config(bg=color_code_down)
            color_fractals['down']=color_code_down
        else:
            color_fractals['down']=fractals_values['down']

    def set_fractal():
        fractals_values['fractal']=int(spin_fractal.get())
        label_will_values.config(text=f"({spin_fractal.get()})")
        if color_fractals['up'] is not None:
            fractals_values['up']=color_fractals['up']
        if color_fractals['down'] is not None:
            fractals_values['down']=color_fractals['down']

        win_fractal.destroy()

    var_fractal=tk.IntVar(value=fractals_values['fractal'])
    label_fractal=tk.Label(win_fractal,text='Fractal',bg='#1c1c1c',fg='white').place(x=35,y=20)
    spin_fractal=tk.Spinbox(win_fractal,from_=2,to=100,textvariable=var_fractal)
    spin_fractal.place(x=95,y=20,width=50)

    label_up=tk.Label(win_fractal,text='Up',bg='#1c1c1c',fg='white').place(x=20,y=45)
    color_up=tk.Button(win_fractal,bg=fractals_values['up'],activebackground='grey',command=set_color_fractal_up)
    color_up.place(x=60,y=45,width=20,height=20)

    label_down=tk.Label(win_fractal,text='Down',bg='#1c1c1c',fg='white').place(x=110,y=45)
    color_down=tk.Button(win_fractal,bg=fractals_values['down'],activebackground='grey',command=set_color_fractal_down)
    color_down.place(x=150,y=45,width=20,height=20)

    fractal_accept=tk.Button(win_fractal,text='Accept',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=set_fractal)
    fractal_accept.place(x=20,y=80,width=60)
    fractal_cancel=tk.Button(win_fractal,text='Cancel',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=win_fractal.destroy)
    fractal_cancel.place(x=110,y=80,width=60)

def awesome_window():
    win_awesome=tk.Toplevel()
    win_awesome.title('awesome settings')
    win_awesome.geometry('190x190')
    win_awesome.resizable(0,0)
    win_awesome.configure(bg='#1c1c1c')

    color_awesome={'up':None,'down':None}

    def set_color_up_awesome():
        color_code_up_awesome=colorchooser.askcolor(title='awesome up color')[1]
        if color_code_up_awesome:
            color_up_awesome.config(bg=color_code_up_awesome)
            color_awesome['up']=color_code_up_awesome
        else:
            color_awesome['up']=awesome_values['up']

    def set_color_down_awesome():
        color_code_down_awesome=colorchooser.askcolor(title='awesome down color')[1]
        if color_code_down_awesome:
            color_down_awesome.config(bg=color_code_down_awesome)
            color_awesome['down']=color_code_down_awesome
        else:
            color_awesome['down']=awesome_values['down']

    def set_awesome():
        awesome_values['slow']=int(spin_slow.get())
        awesome_values['fast']=int(spin_fast.get())
        label_will_values.config(text=f"({spin_fast.get()},{spin_slow.get()})")
        if color_awesome['up'] is not None:
            awesome_values['up']=color_awesome['up']
        if color_awesome['down'] is not None:
            awesome_values['down']=color_awesome['down']

        win_awesome.destroy()

    var_slow=tk.IntVar(value=awesome_values['slow'])
    label_slow=tk.Label(win_awesome,text='Slow',bg='#1c1c1c',fg='white').place(x=35,y=20)
    spin_slow=tk.Spinbox(win_awesome,from_=2,to=1000,textvariable=var_slow)
    spin_slow.place(x=95,y=20,width=50)

    var_fast=tk.IntVar(value=awesome_values['fast'])
    label_fast=tk.Label(win_awesome,text='Fast',bg='#1c1c1c',fg='white').place(x=35,y=50)
    spin_fast=tk.Spinbox(win_awesome,from_=2,to=1000,textvariable=var_fast)
    spin_fast.place(x=95,y=50,width=50)

    label_color_up=tk.Label(win_awesome,text='Up Color',bg='#1c1c1c',fg='white').place(x=35,y=80)
    color_up_awesome=tk.Button(win_awesome,bg=awesome_values['up'],activebackground='grey',command=set_color_up_awesome)
    color_up_awesome.place(x=130,y=80,width=20,height=20)

    label_color_down=tk.Label(win_awesome,text='Down Color',bg='#1c1c1c',fg='white').place(x=35,y=110)
    color_down_awesome=tk.Button(win_awesome,bg=awesome_values['down'],activebackground='grey',command=set_color_down_awesome)
    color_down_awesome.place(x=130,y=110,width=20,height=20)

    awesome_accept=tk.Button(win_awesome,text='Accept',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=set_awesome)
    awesome_accept.place(x=20,y=150,width=60)
    awesome_cancel=tk.Button(win_awesome,text='Cancel',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=win_awesome.destroy)
    awesome_cancel.place(x=110,y=150,width=60)

def config_william():
    if combo_will.get()=='Alligator':
        alligator_window()
    elif combo_will.get()=='Fractals':
        fractal_window()
    elif combo_will.get()=='Awesome O':
        awesome_window()

button_config_will=tk.Button(win,text='...',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=config_william)
button_config_will.place(x=200,y=140,width=25,height=20)

################################################################################################################################################################

#TRADING CONSOLE:

def enable_trade():
    if var_trade.get():
        if var_LiveBacktest.get()=='live':
            spin_balance.config(state='disable')
            spin_leverage.config(state='disable')
        elif var_LiveBacktest.get()=='backtest':
            spin_balance.config(state='normal')
            spin_leverage.config(state='normal')
        spin_risk.config(state='normal')
        radio_risk_percent.config(state='normal')
        radio_risk_size.config(state='normal')
        spin_tp.config(state='normal')
        spin_sl.config(state='normal')
        radio_TpSl_percent.config(state='normal')
        radio_TpSl_pip.config(state='normal')
        check_trailling.config(state='normal')
        if var_trailling_stop.get():
            spin_trailling.config(state='normal')
            radio_trailling_percent.config(state='normal')
            radio_trailling_pip.config(state='normal')
        else:
            spin_trailling.config(state='disable')
            radio_trailling_percent.config(state='disable')
            radio_trailling_pip.config(state='disable')
        spin_buys.config(state='normal')
        spin_sells.config(state='normal')
    else:
        spin_balance.config(state='disable')
        spin_leverage.config(state='disable')
        spin_risk.config(state='disable')
        radio_risk_percent.config(state='disable')
        radio_risk_size.config(state='disable')
        spin_tp.config(state='disable')
        spin_sl.config(state='disable')
        radio_TpSl_percent.config(state='disable')
        radio_TpSl_pip.config(state='disable')
        check_trailling.config(state='disable')
        spin_trailling.config(state='disable')
        radio_trailling_percent.config(state='disable')
        radio_trailling_pip.config(state='disable')
        spin_buys.config(state='disable')
        spin_sells.config(state='disable')

#ENABLE TRADING CHECK:
var_trade=tk.BooleanVar()
var_trade.set(False)
label_trade=tk.Label(win,text='Enable Trade',bg='#1c1c1c',fg='white').place(x=5,y=170)
check_trade=tk.Checkbutton(win,bg='#1c1c1c',activebackground='#1c1c1c',variable=var_trade,command=enable_trade)
check_trade.place(x=110,y=167)

#BALANCE SPIN:
var_balance=tk.IntVar(value=100)
label_balance=tk.Label(win,text='Balance',bg='#1c1c1c',fg='white').place(x=5,y=190)
spin_balance=tk.Spinbox(win,from_=1.00,to=1000000.00,increment=0.01,format='%.2f',textvariable=var_balance)
spin_balance.place(x=115,y=190,width=110)

#LEVERAGE SPIN:
var_leverage=tk.IntVar(value=500)
label_leverage=tk.Label(win,text='Leverage',bg='#1c1c1c',fg='white').place(x=5,y=210)
spin_leverage=tk.Spinbox(win,from_=1,to=2000,textvariable=var_leverage)
spin_leverage.place(x=115,y=210,width=110)

#RISK SPIN/RADIO:
def update_risk(*args):
    for rb in (radio_risk_percent,radio_risk_size):
        if rb.cget('value')==var_risk.get():
            rb.config(bg='#333333',fg='black')
        else:
            rb.config(bg='#1c1c1c',fg='white')
var_spin_risk=tk.IntVar(value=10)
label_risk=tk.Label(win,text='Risk Percent/Size',bg='#1c1c1c',fg='white').place(x=5,y=230)
spin_risk=tk.Spinbox(win,from_=0.01,to=100,increment=0.01,format='%.2f',textvariable=var_spin_risk)
spin_risk.place(x=115,y=230,width=65)
var_risk=tk.StringVar()
radio_risk_percent=tk.Radiobutton(win,text='%',variable=var_risk,value='percent',bg='#1c1c1c',fg='white',indicatoron=False)
radio_risk_percent.place(x=183,y=230,width=20,height=20)
radio_risk_size=tk.Radiobutton(win,text='L',variable=var_risk,value='lot',bg='#1c1c1c',fg='white',indicatoron=False)
radio_risk_size.place(x=205,y=230,width=20,height=20)
var_risk.trace_add('write',update_risk)
var_risk.set('percent')

#TP/SL SPIN:
def update_TpSl(*args):
    for rb in (radio_TpSl_percent,radio_TpSl_pip):
        if rb.cget('value')==var_TpSl.get():
            rb.config(bg='#333333',fg='black')
        else:
            rb.config(bg='#1c1c1c',fg='white')
label_tp=tk.Label(win,text='TP/SL',bg='#1c1c1c',fg='white').place(x=5,y=250)
var_tp=tk.IntVar(value=10)
spin_tp=tk.Spinbox(win,from_=0.00,to=1000,increment=0.01,format='%.2f',textvariable=var_tp)
spin_tp.place(x=45,y=250,width=65)
var_sl=tk.IntVar(value=5)
spin_sl=tk.Spinbox(win,from_=0.00,to=1000,increment=0.01,format='%.2f',textvariable=var_sl)
spin_sl.place(x=115,y=250,width=65)
var_TpSl=tk.StringVar()
radio_TpSl_percent=tk.Radiobutton(win,text='%',variable=var_TpSl,value='percent',bg='#1c1c1c',fg='white',indicatoron=False)
radio_TpSl_percent.place(x=183,y=250,width=20,height=20)
radio_TpSl_pip=tk.Radiobutton(win,text='P',variable=var_TpSl,value='pip',bg='#1c1c1c',fg='white',indicatoron=False)
radio_TpSl_pip.place(x=205,y=250,width=20,height=20)
var_TpSl.trace_add('write',update_TpSl)
var_TpSl.set('percent')

#TRAILLING STOP SPIN/RADIO:
def update_trailling(*args):
    for rb in (radio_trailling_percent,radio_trailling_pip):
        if rb.cget('value')==var_trailling.get():
            rb.config(bg='#333333',fg='black')
        else:
            rb.config(bg='#1c1c1c',fg='white')
def enable_trailling_stop():
    if var_trailling_stop.get():
        spin_trailling.config(state='normal')
        radio_trailling_percent.config(state='normal')
        radio_trailling_pip.config(state='normal')
    else:
        spin_trailling.config(state='disabled')
        radio_trailling_percent.config(state='disabled')
        radio_trailling_pip.config(state='disabled')

var_trailling_stop=tk.BooleanVar()
var_trailling_stop.set(False)
label_trailling=tk.Label(win,text='Trailling Stop',bg='#1c1c1c',fg='white').place(x=5,y=270)
check_trailling=tk.Checkbutton(win,bg='#1c1c1c',activebackground='#1c1c1c',variable=var_trailling_stop,command=enable_trailling_stop)
check_trailling.place(x=90,y=270)
var_spin_trailling=tk.IntVar(value=5)
spin_trailling=tk.Spinbox(win,from_=0.01,to=100.00,increment=0.01,format='%.2f',textvariable=var_spin_trailling)
spin_trailling.place(x=115,y=270,width=65)

var_trailling=tk.StringVar()
radio_trailling_percent=tk.Radiobutton(win,text='%',variable=var_trailling,value='percent',bg='#1c1c1c',fg='white',indicatoron=False)
radio_trailling_percent.place(x=183,y=270,width=20,height=20)
radio_trailling_pip=tk.Radiobutton(win,text='P',variable=var_trailling,value='pip',bg='#1c1c1c',fg='white',indicatoron=False)
radio_trailling_pip.place(x=205,y=270,width=20,height=20)
var_trailling.trace_add('write',update_trailling)
var_trailling.set('percent')
enable_trailling_stop()

#NUMBER OF BUYS AND SELLS:
label_BuySell=tk.Label(win,text='N. Buys/Sells',bg='#1c1c1c',fg='white').place(x=5,y=290)
var_spin_buys=tk.IntVar(value=20)
spin_buys=tk.Spinbox(win,from_=1,to=50,textvariable=var_spin_buys)
spin_buys.place(x=115,y=290,width=53)
var_spin_sells=tk.IntVar(value=20)
spin_sells=tk.Spinbox(win,from_=1,to=50,textvariable=var_spin_sells)
spin_sells.place(x=173,y=290,width=53)

enable_trade()


################################################################################################################################################################

#STRATEGY CANVAS/FRAME:
canvas_strategy=tk.Canvas(win,bg='black',bd=0,highlightthickness=0)
canvas_strategy.place(x=5,y=345,width=205,height=60)
scroll_strategy=tk.Scrollbar(win,orient='vertical',command=canvas_strategy.yview)
scroll_strategy.place(x=215,y=345,width=10,height=60)
canvas_strategy.configure(yscrollcommand=scroll_strategy.set)

frame_strategy=tk.Frame(canvas_strategy,bg='black')
canvas_strategy.create_window((0,0),window=frame_strategy,anchor='nw')

#STRATEGY WIDGETS:
strategies_widgets={'count':[],'label':[],'check':[],'check_var':[],'button':[]}
files_strategies=[]

def enable_strategy(row):
    if strategies_widgets['check_var'][row-1].get()==True:
        strategies_widgets['button'][row-1].config(state='normal')
    elif strategies_widgets['check_var'][row-1].get()==False:
        strategies_widgets['button'][row-1].config(state='disable')

def upload_strategy(row):
    strategy_file=filedialog.askopenfilename(title='select file')
    if strategy_file:
        strategies_widgets['label'][row-1].config(text=strategy_file)
        files_strategies[row-1]=strategy_file

def add_strategy():
    dist=20

    strategies_widgets['count'].append(len(strategies_widgets['count'])+1)

    #STRATEGY CHECK:
    var_strategy=tk.BooleanVar(value=True)
    strategies_widgets['check_var'].append(var_strategy)
    check_strategy=tk.Checkbutton(
            frame_strategy,variable=var_strategy,bg='black',activebackground='black',
            command=lambda row=strategies_widgets['count'][-1]: enable_strategy(row)
    )
    check_strategy.place(x=5,y=dist*(strategies_widgets['count'][-1]-1)-2)
    strategies_widgets['check'].append(check_strategy)

    #UPLOAD STRATEGY BUTTON:
    button_strategy=tk.Button(
            frame_strategy,text='Upload',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',
            command=lambda row=strategies_widgets['count'][-1]: upload_strategy(row)
    )
    button_strategy.place(x=35,y=dist*(strategies_widgets['count'][-1]-1)+1,width=50,height=18)
    strategies_widgets['button'].append(button_strategy)

    #FILE STRATEGY LABEL:
    label_add_strategy=tk.Label(frame_strategy,text=f"No File {strategies_widgets['count'][-1]}",bg='black',fg='white')
    label_add_strategy.place(x=90,y=dist*(strategies_widgets['count'][-1]-1))
    strategies_widgets['label'].append(label_add_strategy)
    files_strategies.append('No File')

    #UPDATE CANVAS AND FRAME:
    frame_strategy.config(width=200,height=dist*strategies_widgets['count'][-1])
    canvas_strategy.config(scrollregion=(0,0,frame_strategy.winfo_width(),frame_strategy.winfo_height()))
    canvas_strategy.yview_moveto(1)

def remove_strategy():
    dist=20

    if len(strategies_widgets['count'])>0:
        del strategies_widgets['count'][-1]
    
    #REMOVE STRATEGY WIDGETS:
    if len(strategies_widgets['check'])>0:
        strategies_widgets['check'][-1].destroy()
        del strategies_widgets['check'][-1]
    if len(strategies_widgets['check_var'])>0:
        del strategies_widgets['check_var'][-1]
    if len(strategies_widgets['button'])>0:
        strategies_widgets['button'][-1].destroy()
        del strategies_widgets['button'][-1]
    if len(strategies_widgets['label'])>0:
        strategies_widgets['label'][-1].destroy()
        del strategies_widgets['label'][-1]
    if len(files_strategies)>0:
        del files_strategies[-1]

    #UPDATE CANVAS AND FRAME:
    frame_strategy.config(width=200,height=dist*strategies_widgets['count'][-1] if len(strategies_widgets['count'])>0 else 0)
    canvas_strategy.config(scrollregion=(0,0,frame_strategy.winfo_width(),frame_strategy.winfo_height()))
    canvas_strategy.yview_moveto(1)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

def edit_strategy():
    win_strategy=tk.Toplevel()
    win_strategy.title('*New')
    win_strategy.geometry('450x450')
    win_strategy.resizable(0,0)
    win_strategy.configure(bg='#1c1c1c')

    menu_strategy=tk.Menu(win_strategy)
    win_strategy.config(menu=menu_strategy)

    path_strategy=['*New']

    #FILE TAB:
    def new_strategy():
        if path_strategy[0][0]=='*':
            new_strategy_response=messagebox.askyesnocancel('Confirm','Open black new strategy without change?')
            if new_strategy_response:
                text_strategy.delete('1.0',tk.END)
                win_strategy.title('New')
                path_strategy[0]='New'
        else:
            text_strategy.delete('1.0',tk.END)
            win_strategy.title('New')
            path_strategy[0]='New'
    def open_strategy():
        if path_strategy[0][0]=='*':
            open_response=messagebox.askyesnocancel('Confirm','Open file strategy without change?')
            if open_response:
                open_strategy_file=filedialog.askopenfilename(title='Open file')
                if open_strategy_file:
                    win_strategy.title(open_strategy_file)
                    path_strategy[0]=open_strategy_file
                    file_strategy=open(open_strategy_file,'r')
                    file_strategy_content=file_strategy.read()
                    text_strategy.delete('1.0',tk.END)
                    text_strategy.insert(tk.END,file_strategy_content)
                    file_strategy.close()
        else:
            open_strategy_file=filedialog.askopenfilename(title='Open file')
            if open_strategy_file:
                win_strategy.title(open_strategy_file)
                path_strategy[0]=open_strategy_file
                file_strategy=open(open_strategy_file,'r')
                file_strategy_content=file_strategy.read()
                text_strategy.delete('1.0',tk.END)
                text_strategy.insert(tk.END,file_strategy_content)
                file_strategy.close()
    def save_strategy():
        if path_strategy[0][0]=='*':
            if os.path.exists(path_strategy[0][1:]):
                path_strategy[0]=path_strategy[0][1:]
                win_strategy.title(path_strategy[0])
                save_strategy=open(path_strategy[0],'w')
                save_strategy.write(text_strategy.get('1.0',tk.END))
                save_strategy.close()
            else:
                save_as_strategy=filedialog.asksaveasfilename(title='Save as',defaultextension='.py',filetypes=[('python files','*.py'),('all files','.*')])
                if save_as_strategy:
                    win_strategy.title(save_as_strategy)
                    path_strategy[0]=save_as_strategy
                    save_strategy=open(save_as_strategy,'w')
                    save_strategy.write(text_strategy.get('1.0',tk.END))
                    save_strategy.close()
    def save_strategy_as():
        save_as_strategy=filedialog.asksaveasfilename(title='Save as',defaultextension='.py',filetypes=[('python files','*.py'),('all files','.*')])
        if save_as_strategy:
            win_strategy.title(save_as_strategy)
            path_strategy[0]=save_as_strategy
            save_strategy=open(save_as_strategy,'w')
            save_strategy.write(text_strategy.get('1.0',tk.END))
            save_strategy.close()
    def close_strategy_window():
        if path_strategy[0][0]=='*':
            close_response=messagebox.askyesnocancel('Confirm exit','Exit without change?')
            if close_response:
                win_strategy.destroy()
        else:
            win_strategy.destroy()

    file_menu=tk.Menu(menu_strategy)
    menu_strategy.add_cascade(label='File',menu=file_menu)
    file_menu.add_command(label='New',command=new_strategy)
    file_menu.add_command(label='Open',command=open_strategy)
    file_menu.add_command(label='Save',command=save_strategy)
    file_menu.add_command(label='Save as',command=save_strategy_as)
    file_menu.add_separator()
    file_menu.add_command(label='exit',command=close_strategy_window)

    #TEXT:
    def donot_close_text_window():
        if path_strategy[0][0]=='*':
            close_text_window=messagebox.askyesnocancel('Confirm exit','Close window without change?')
            if close_text_window:
                win_strategy.destroy()
        else:
            win_strategy.destroy()
    def on_text_change(event):
        current_text=text_strategy.get('1.0',tk.END).strip()
        if current_text and not win_strategy.title().startswith('*'):
            path_strategy[0]=f'*{path_strategy[0]}'
            win_strategy.title(path_strategy)
        elif not current_text and win_strategy.title().startswith('*'):
            path_strategy[0]=path_strategy[0][1:]
            win_strategy.title(path_strategy[0])
    text_strategy=tk.Text(win_strategy,bg='black',fg='white',wrap='none',undo=True,insertbackground='white')
    text_strategy.place(x=0,y=0,width=433,height=433)
    text_font = font.Font(font=text_strategy['font'])
    char_width = text_font.measure(' ')
    tab_size=4*char_width
    text_strategy.config(tabs=(tab_size,))

    #open_default_strategy=open('default_strategy.py','r')
    #default_strategy_content=open_default_strategy.read()
    #text_strategy.insert(tk.END,default_strategy_content)

    text_strategy.bind("<KeyRelease>",on_text_change)

    win_strategy.protocol('WM_DELETE_WINDOW',donot_close_text_window)

    def handle_colon_and_enter(event):
        cursor_index = text_strategy.index("insert")
        current_line = text_strategy.get(f"{cursor_index} linestart", f"{cursor_index} lineend")
        indentation = len(current_line) - len(current_line.lstrip(' '))
        if current_line.strip().endswith(':'):
            text_strategy.insert("insert", f"\n{' ' * (indentation + 4)}")
            return "break"
        else:
            text_strategy.insert("insert", f"\n{' ' * indentation}")
            return "break"
    text_strategy.bind("<Return>", handle_colon_and_enter)

    def handle_autocomplete(event):
        char_map={
            '(': ')','[': ']','{': '}',"'": "'",'"': '"',
        }
        if event.char in char_map:
            cursor_index = text_strategy.index("insert")
            text_strategy.insert(cursor_index, event.char + char_map[event.char])
            text_strategy.mark_set("insert", f"{cursor_index}+1c")
            return "break"
    text_strategy.bind("<KeyPress>", handle_autocomplete)

    #SCROLLBAR TEXT:
    v_scroll=tk.Scrollbar(win_strategy,orient='vertical',command=text_strategy.yview)
    v_scroll.pack(side='right',fill='y')
    text_strategy.config(yscrollcommand=v_scroll.set)
    h_scroll=tk.Scrollbar(win_strategy,orient='horizontal',command=text_strategy.xview)
    h_scroll.pack(side='bottom',fill='x')
    text_strategy.config(xscrollcommand=h_scroll.set)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

label_strategy=tk.Label(win,text='Strategy',bg='#1c1c1c',fg='white').place(x=5,y=320)

button_add_strategy=tk.Button(win,text='+',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=add_strategy)
button_add_strategy.place(x=60,y=320,width=50,height=20)

button_remove_strategy=tk.Button(win,text='-',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=remove_strategy)
button_remove_strategy.place(x=115,y=320,width=50,height=20)

button_edit_strategy=tk.Button(win,text='Edit',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=edit_strategy)
button_edit_strategy.place(x=170,y=320,width=55,height=20)

################################################################################################################################################################

#NEURAL NET CANVAS/FRAME:
canvas_neural=tk.Canvas(win,bg='black',bd=0,highlightthickness=0)
canvas_neural.place(x=5,y=440,width=205,height=60)
scroll_neural=tk.Scrollbar(win,orient='vertical',command=canvas_neural.yview)
scroll_neural.place(x=215,y=440,width=10,height=60)
canvas_neural.configure(yscrollcommand=scroll_neural.set)

frame_neural=tk.Frame(canvas_neural,bg='black')
canvas_neural.create_window((0,0),window=frame_neural,anchor='nw')

#NEURAL NET WIDGETS:
neural_widgets={'count':[],'label':[],'check':[],'check_var':[],'button':[]}
files_neural_net=[]

def enable_neural(row):
    if neural_widgets['check_var'][row-1].get()==True:
        neural_widgets['button'][row-1].config(state='normal')
    elif neural_widgets['check_var'][row-1].get()==False:
        neural_widgets['button'][row-1].config(state='disable')

def upload_neural(row):
    neural_file=filedialog.askopenfilename(title='Select file')
    if neural_file:
        neural_widgets['label'][row-1].config(text=neural_file)
        files_neural_net[row-1]=neural_file

def add_neural():
    dist=20

    neural_widgets['count'].append(len(neural_widgets['count'])+1)

    #NEURAL CHECK:
    var_neural=tk.BooleanVar(value=True)
    neural_widgets['check_var'].append(var_neural)
    check_neural=tk.Checkbutton(
            frame_neural,variable=var_neural,bg='black',activebackground='black',
            command=lambda row=neural_widgets['count'][-1]: enable_neural(row)
    )
    check_neural.place(x=5,y=dist*(neural_widgets['count'][-1]-1)-2)
    neural_widgets['check'].append(check_neural)

    #UPLOAD NEURAL BUTTON:
    button_neural=tk.Button(
            frame_neural,text='Upload',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',
            command=lambda row=neural_widgets['count'][-1]: upload_neural(row)
    )
    button_neural.place(x=35,y=dist*(neural_widgets['count'][-1]-1)+1,width=50,height=18)
    neural_widgets['button'].append(button_neural)

    #FILE NEURAL LABEL:
    label_add_neural=tk.Label(frame_neural,text=f"No File {neural_widgets['count'][-1]}",bg='black',fg='white')
    label_add_neural.place(x=90,y=dist*(neural_widgets['count'][-1]-1))
    neural_widgets['label'].append(label_add_neural)
    files_neural_net.append('No File')

    #UPDATE CANVAS AND FRAME:
    frame_neural.config(width=200,height=dist*neural_widgets['count'][-1])
    canvas_neural.config(scrollregion=(0,0,frame_neural.winfo_width(),frame_neural.winfo_height()))
    canvas_neural.yview_moveto(1)

def remove_neural():
    dist=20

    if len(neural_widgets['count'])>0:
        del neural_widgets['count'][-1]

    #REMOVE NEURAL WIDGETS:
    if len(neural_widgets['check'])>0:
        neural_widgets['check'][-1].destroy()
        del neural_widgets['check'][-1]
    if len(neural_widgets['check_var'])>0:
        del neural_widgets['check_var'][-1]
    if len(neural_widgets['button'])>0:
        neural_widgets['button'][-1].destroy()
        del neural_widgets['button'][-1]
    if len(neural_widgets['label'])>0:
        neural_widgets['label'][-1].destroy()
        del neural_widgets['label'][-1]
    if len(files_neural_net)>0:
        del files_neural_net[-1]

    #UPDATE CANVAS AND FRAME:
    frame_neural.config(width=200,height=dist*neural_widgets['count'][-1] if len(neural_widgets['count'])>0 else 0)
    canvas_neural.config(scrollregion=(0,0,frame_neural.winfo_width(),frame_neural.winfo_height()))
    canvas_neural.yview_moveto(1)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

label_neural=tk.Label(win,text='Neural Net',bg='#1c1c1c',fg='white').place(x=5,y=415)

button_add_neural=tk.Button(win,text='+',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=add_neural)
button_add_neural.place(x=75,y=415,width=42,height=20)

button_remove_neural=tk.Button(win,text='-',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=remove_neural)
button_remove_neural.place(x=122,y=415,width=42,height=20)

button_edit_neural=tk.Button(win,text='Edit',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=neural_net_console)
button_edit_neural.place(x=170,y=415,width=55,height=20)

################################################################################################################################################################

#BID ASK TABLE:
bidask_style=ttk.Style()
bidask_style.theme_use('default')
bidask_style.configure('Custom.Treeview.Heading',background='black',foreground='white',font=('Helvetica',10,'bold'))                                        #head style
bidask_style.configure('Custom.Treeview',background='black',foreground='lightgray',rowheight=20,fieldbackground='black',bordercolor='black',borderwidth=1)  #cell style

bidask_style.map('Custom.Treeview',background=[('selected','#2c2c2c')])
bidask_columns=('Time','Bid','Ask')
bidask_table=ttk.Treeview(win,column=bidask_columns,height=3,show='headings',style='Custom.Treeview')
bidask_table.place(x=5,y=515,width=220)
for col in bidask_columns:
    bidask_table.heading(col,text=col)
    bidask_table.column(col,width=67,anchor='center')

################################################################################################################################################################

#VARIABLES:
#variables=['time','close']
#var={i:[] for i in variables}

#GRAPH FRAME:

frame_graph=tk.Frame(win,bg='black')
frame_graph.place(x=235,y=5,width=762,height=617)

fig_trade=plt.figure(figsize=(7.62,4.9))
ax_trade=fig_trade.add_gridspec(6,1)
ax_candle=fig_trade.add_subplot(ax_trade[0:5,:])
ax_awesome=fig_trade.add_subplot(ax_trade[5:6,:])
fig_trade.set_facecolor('black')
fig_trade.subplots_adjust(top=0.99,bottom=0.01,right=0.99,left=0.01,hspace=0,wspace=0)

canvas_graph=FigureCanvasTkAgg(fig_trade,master=frame_graph)
canvas_graph.get_tk_widget().place(x=0,y=0)

#CANDLE SUBPLOT:
ax_candle.clear()
ax_candle.set_facecolor('black')
ax_candle.set_xticks([])
ax_candle.set_yticks([])
spines=['top','bottom','left','right']
for i in spines:
    ax_candle.spines[i].set_color('dimgray')

#AWESOME O SUBPLOT:
ax_awesome.clear()
ax_awesome.set_facecolor('black')
ax_awesome.set_xticks([])
ax_awesome.set_yticks([])
for spine in spines:
    ax_awesome.spines[spine].set_color('dimgray')


#TABLES IN GRAPH: OPEN TRADE, STATUS, HISTORY:

frame_graph_trades=tk.Frame(frame_graph,bg='black')
frame_graph_trades.place(x=0,y=490,width=762,height=100)

frame_graph_status=tk.Frame(frame_graph,bg='black')
frame_graph_status.place(x=0,y=490,width=762,height=100)

frame_graph_history=tk.Frame(frame_graph,bg='black')
frame_graph_history.place(x=0,y=490,width=762,height=100)


#GRAPH TRADE TABLE:
graph_trade_table_style=ttk.Style()
graph_trade_table_style.theme_use('default')
graph_trade_table_style.configure('trade.Treeview.Heading',background='black',foreground='white',font=('Helvetica',10,'bold'))                                        #head style
graph_trade_table_style.configure('trade.Treeview',background='black',foreground='lightgray',rowheight=20,fieldbackground='black',bordercolor='black',borderwidth=1)  #cell style
graph_trade_table_style.map('trade.Treeview',background=[('selected','#2c2c2c')])

graph_trade_table_columns=('Id','DateTime','Type','Volume','Price','SL','TP','Profit')
graph_trade_table=ttk.Treeview(frame_graph_trades,column=graph_trade_table_columns,height=4,show='headings',style='trade.Treeview')
graph_trade_table.place(x=0,y=0,width=750)
for col in graph_trade_table_columns:
    graph_trade_table.heading(col,text=col)
    if col=='Id':
        graph_trade_table.column(col,width=40,anchor='center',stretch=False)
    elif col=='DateTime':
        graph_trade_table.column(col,width=110,anchor='center',stretch=False)
    else:
        graph_trade_table.column(col,width=99,anchor='center',stretch=False)

#SCROLL BAR FOR TRADING TABLE:
scroll_trade_table=tk.Scrollbar(frame_graph_trades,orient='vertical',command=graph_trade_table.yview)
scroll_trade_table.place(x=750,y=0,width=10,height=100)
graph_trade_table.configure(yscrollcommand=scroll_trade_table.set)


#GRAPH STATUS TABLE:
graph_status_table_style=ttk.Style()
graph_status_table_style.theme_use('default')
graph_status_table_style.configure('status.Treeview',background='black',foreground='#3ba3bc',rowheight=19,fieldbackground='black',bordercolor='black',borderwidth=1)  #cell
graph_status_table_style.map('status.Treeview',background=[('selected','#2c2c2c')])

graph_status_table_columns=('status','val')
graph_status_table=ttk.Treeview(frame_graph_status,column=graph_status_table_columns,show='',style='status.Treeview')
graph_status_table.place(x=0,y=0,width=210,height=100)
for col in graph_status_table_columns:
    graph_status_table.column(col,width=60,anchor='w')
rows_status=[
    ['I/F Balance','0/0'],
    ['Min/Max Balance','0/0'],
    ['Min/Max Equity','0/0'],
    ['PnL','0'],
    ['ROE','0']
]
for row in rows_status:
    graph_status_table.insert('',tk.END,value=row)

#CHART GRAPH STATUS TABLE:

fig_graph_status=plt.figure(figsize=(5.52,1))
ax_graph_status=fig_graph_status.add_gridspec(1,3)
ax_graph_BuySell=fig_graph_status.add_subplot(ax_graph_status[:,0:1])
ax_graph_profits=fig_graph_status.add_subplot(ax_graph_status[:,1:2])
ax_graph_BalanceEquity=fig_graph_status.add_subplot(ax_graph_status[:,2:3])
fig_graph_status.set_facecolor('black')
fig_graph_status.subplots_adjust(top=0.99,bottom=0.01,right=0.99,left=0.01,hspace=0,wspace=0)

canvas_graph_status=FigureCanvasTkAgg(fig_graph_status,master=frame_graph_status)
canvas_graph_status.get_tk_widget().place(x=210,y=0)

ax_graph_BuySell.clear()
ax_graph_BuySell.set_facecolor('black')
ax_graph_BuySell.set_xticks([])
ax_graph_BuySell.set_yticks([])
for i in spines:
    ax_graph_BuySell.spines[i].set_color('dimgray')

ax_graph_profits.clear()
ax_graph_profits.set_facecolor('black')
ax_graph_profits.set_xticks([])
ax_graph_profits.set_yticks([])
for i in spines:
    ax_graph_profits.spines[i].set_color('dimgray')

ax_graph_BalanceEquity.clear()
ax_graph_BalanceEquity.set_facecolor('black')
ax_graph_BalanceEquity.set_xticks([])
ax_graph_BalanceEquity.set_yticks([])
for i in spines:
    ax_graph_BalanceEquity.spines[i].set_color('dimgray')


#GRAPH HISTORY TABLE:

graph_histo_table_style=ttk.Style()
graph_histo_table_style.theme_use('default')
graph_histo_table_style.configure('histo.Treeview.Heading',background='black',foreground='white',font=('Helvetica',10,'bold'))                                        #head style
graph_histo_table_style.configure('histo.Treeview',background='black',foreground='lightgray',rowheight=23,fieldbackground='black',bordercolor='black',borderwidth=1)  #cell style
graph_histo_table_style.map('histo.Treeview',background=[('selected','#2c2c2c')])

graph_histo_table_columns=('Id','I. DateTime','Type','Volume','I. Price','SL','TP','F. DateTime','F. Price','Profit')
graph_histo_table=ttk.Treeview(frame_graph_history,column=graph_histo_table_columns,show='headings',style='histo.Treeview')
graph_histo_table.place(x=0,y=0,width=750,height=90)
for col in graph_histo_table_columns:
    graph_histo_table.heading(col,text=col)
    if col=='Id':
        graph_histo_table.column(col,width=40,anchor='center',stretch=False)
    elif col=='I.DateTime' or col=='F.DateTime':
        graph_histo_table.column(col,width=110,anchor='center',stretch=False)
    else:
        graph_histo_table.column(col,width=99,anchor='center',stretch=False)

#SCROLL BAR FOR TRADING TABLE:

v_scroll_histo_table=tk.Scrollbar(frame_graph_history,orient='vertical',command=graph_histo_table.yview)
v_scroll_histo_table.place(x=750,y=0,width=10,height=100)
graph_histo_table.configure(yscrollcommand=v_scroll_histo_table.set)

h_scroll_histo_table=tk.Scrollbar(frame_graph_history,orient='horizontal',command=graph_histo_table.xview)
h_scroll_histo_table.place(x=0,y=90,width=750,height=10)
graph_histo_table.configure(xscrollcommand=h_scroll_histo_table.set)


#COMBO GRAPH TABLE:
def selected_graph_table(table):
    if table=='Trades':
        frame_graph_trades.tkraise()
    elif table=='Status':
        frame_graph_status.tkraise()
    elif table=='History':
        frame_graph_history.tkraise()

def choose_graph_table(event):
    selected_graph_table(combo_graph_tables.get())

combo_graph_tables=ttk.Combobox(frame_graph,values=['Trades','Status','History'])
combo_graph_tables.place(x=2,y=595,width=60,height=20)
combo_graph_tables.set('Trades')
combo_graph_tables.bind('<<ComboboxSelected>>',choose_graph_table)

selected_graph_table(combo_graph_tables.get())

#LABEL GRAPH STATUS BALANCE, EQUITY, MARGIN, FREEMARGIN, PNL:
label_graph_balance=tk.Label(frame_graph,text='Balance:',bg='black',fg='white')
label_graph_balance.place(x=70,y=595)
label_graph_equity=tk.Label(frame_graph,text='Equity:',bg='black',fg='white')
label_graph_equity.place(x=200,y=595)
label_graph_margin=tk.Label(frame_graph,text='Margin:',bg='black',fg='white')
label_graph_margin.place(x=330,y=595)
label_graph_freemargin=tk.Label(frame_graph,text='FreeMargin:',bg='black',fg='white')
label_graph_freemargin.place(x=460,y=595)
label_graph_pnl=tk.Label(frame_graph,text='PnL:',bg='black',fg='white')
label_graph_pnl.place(x=630,y=595)

#COLLECT DATA AND PLOT:
def plot_data():
    for i in range(200):
        var['time'].append(str(i+1))
        if len(var['close'])==0:
            var['close'].append(random.uniform(1,2))
        else:
            down=var['close'][-1]*(1-0.01)
            up=var['close'][-1]*(1+0.01)
            var['close'].append(random.uniform(down,up))

    for cell in bidask_table.get_children():
        bidask_table.delete(cell)
    for row in range(len(var['time'][-3:])):
        row_bidask=(var['time'][-3:][row],round(var['close'][-3:][row],5),round(var['close'][-3:][row],5))
        bidask_table.insert('',tk.END,values=row_bidask)

    for cell in graph_trade_table.get_children():
        graph_trade_table.delete(cell)
    for row in range(10):
        row_trade_table=(row+1,'','','','','','','')
        graph_trade_table.insert('',tk.END,values=row_trade_table)
    graph_trade_table.yview_moveto(1)

    for cell in graph_histo_table.get_children():
        graph_histo_table.delete(cell)
    for row in range(10):
        row_histo_table=(row+1,'datetime','','','','','','','','','')
        graph_histo_table.insert('',tk.END,values=row_histo_table)
    graph_histo_table.yview_moveto(1)

    ax_candle.clear()
    ax_candle.plot(var['time'],var['close'],c='g',lw=1)
    ax_candle.axhline(y=var['close'][-1],c='b',lw=1,ls='--')
    ax_candle.plot(var['time'][-1],var['close'][-1],marker='o',c='b',ms=5)

    canvas_graph.draw()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

#TABLE FRAME:
frame_table=tk.Frame(win,bg='black')
frame_table.place(x=235,y=5,width=762,height=617)

#STATUS TABLE:
status_table_style=ttk.Style()
status_table_style.theme_use('default')
status_table_style.configure('status_table.Treeview',background='black',foreground='#3ba3bc',rowheight=19,fieldbackground='black',bordercolor='black',borderwidth=1)  #cell
status_table_style.map('status_table.Treeview',background=[('selected','#2c2c2c')])

status_table_columns=('status','val')
status_table=ttk.Treeview(frame_table,column=graph_status_table_columns,show='',style='status_table.Treeview')
status_table.place(x=0,y=0,width=210,height=100)
for col in status_table_columns:
    status_table.column(col,width=60,anchor='w')
rows_status_table=[
    ['I/F Balance','0/0'],
    ['Min/Max Balance','0/0'],
    ['Min/Max Equity','0/0'],
    ['PnL','0'],
    ['ROE','0']
]
for row in rows_status_table:
    status_table.insert('',tk.END,value=row)

#CHART STATUS TABLE:

fig_status_table=plt.figure(figsize=(5.52,1))
ax_status_table=fig_status_table.add_gridspec(1,3)
ax_BuySell_table=fig_status_table.add_subplot(ax_status_table[:,0:1])
ax_profits_table=fig_status_table.add_subplot(ax_status_table[:,1:2])
ax_BalanceEquity_table=fig_status_table.add_subplot(ax_status_table[:,2:3])
fig_status_table.set_facecolor('black')
fig_status_table.subplots_adjust(top=0.99,bottom=0.01,right=0.99,left=0.01,hspace=0,wspace=0)

canvas_status_table=FigureCanvasTkAgg(fig_status_table,master=frame_table)
canvas_status_table.get_tk_widget().place(x=210,y=0)

ax_BuySell_table.clear()
ax_BuySell_table.set_facecolor('black')
ax_BuySell_table.set_xticks([])
ax_BuySell_table.set_yticks([])
for i in spines:
    ax_BuySell_table.spines[i].set_color('dimgray')

ax_profits_table.clear()
ax_profits_table.set_facecolor('black')
ax_profits_table.set_xticks([])
ax_profits_table.set_yticks([])
for i in spines:
    ax_profits_table.spines[i].set_color('dimgray')

ax_BalanceEquity_table.clear()
ax_BalanceEquity_table.set_facecolor('black')
ax_BalanceEquity_table.set_xticks([])
ax_BalanceEquity_table.set_yticks([])
for i in spines:
    ax_BalanceEquity_table.spines[i].set_color('dimgray')


#HISTORY TABLE:

histo_table_style=ttk.Style()
histo_table_style.theme_use('default')
histo_table_style.configure('histo_table.Treeview.Heading',background='black',foreground='white',font=('Helvetica',10,'bold'))                                        #head style
histo_table_style.configure('histo_table.Treeview',background='black',foreground='lightgray',rowheight=20,fieldbackground='black',bordercolor='black',borderwidth=1)  #cell style
histo_table_style.map('histo_table.Treeview',background=[('selected','#2c2c2c')])

histo_table_columns=('Id','I. DateTime','Type','Volume','I. Price','SL','TP','F. DateTime','F. Price','Profit')
histo_table=ttk.Treeview(frame_table,column=graph_histo_table_columns,show='headings',height=11,style='histo_table.Treeview')
histo_table.place(x=0,y=100,width=750)
for col in histo_table_columns:
    histo_table.heading(col,text=col)
    if col=='Id':
        histo_table.column(col,width=40,anchor='center',stretch=False)
    elif col=='I.DateTime' or col=='F.DateTime':
        histo_table.column(col,width=110,anchor='center',stretch=False)
    else:
        histo_table.column(col,width=99,anchor='center',stretch=False)

#SCROLL BAR FOR TRADING TABLE:

v_scroll_histoTable=tk.Scrollbar(frame_table,orient='vertical',command=histo_table.yview)
v_scroll_histoTable.place(x=750,y=100,width=10,height=250)
histo_table.configure(yscrollcommand=v_scroll_histoTable.set)

h_scroll_histoTable=tk.Scrollbar(frame_table,orient='horizontal',command=histo_table.xview)
h_scroll_histoTable.place(x=0,y=340,width=750,height=10)
histo_table.configure(xscrollcommand=h_scroll_histoTable.set)


#TRADE TABLE:

trade_table_style=ttk.Style()
trade_table_style.theme_use('default')
trade_table_style.configure('trade_table.Treeview.Heading',background='black',foreground='white',font=('Helvetica',10,'bold'))                                        #head style
trade_table_style.configure('trade_table.Treeview',background='black',foreground='lightgray',rowheight=20,fieldbackground='black',bordercolor='black',borderwidth=1)  #cell style
trade_table_style.map('trade_table.Treeview',background=[('selected','#2c2c2c')])

trade_table_columns=('Id','DateTime','Type','Volume','Price','SL','TP','Profit')
trade_table=ttk.Treeview(frame_table,column=trade_table_columns,height=11,show='headings',style='trade_table.Treeview')
trade_table.place(x=0,y=350,width=750)
for col in trade_table_columns:
    trade_table.heading(col,text=col)
    if col=='Id':
        trade_table.column(col,width=40,anchor='center',stretch=False)
    elif col=='DateTime':
        trade_table.column(col,width=110,anchor='center',stretch=False)
    else:
        trade_table.column(col,width=99,anchor='center',stretch=False)

#SCROLL BAR FOR TRADING TABLE:
scroll_tradeTable=tk.Scrollbar(frame_table,orient='vertical',command=trade_table.yview)
scroll_tradeTable.place(x=750,y=350,width=10,height=240)
trade_table.configure(yscrollcommand=scroll_tradeTable.set)

#LABEL TABLE STATUS BALANCE, EQUITY, MARGIN, FREEMARGIN, PNL:
label_table_balance=tk.Label(frame_table,text='Balance :',bg='black',fg='white')
label_table_balance.place(x=5,y=595)
label_table_equity=tk.Label(frame_table,text='Equity:',bg='black',fg='white')
label_table_equity.place(x=160,y=595)
label_table_margin=tk.Label(frame_table,text='Margin:',bg='black',fg='white')
label_table_margin.place(x=300,y=595)
label_table_freemargin=tk.Label(frame_table,text='FreeMargin:',bg='black',fg='white')
label_table_freemargin.place(x=450,y=595)
label_table_pnl=tk.Label(frame_table,text='PnL:',bg='black',fg='white')
label_table_pnl.place(x=630,y=595)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------

show_graph_table()

################################################################################################################################################################

#START STOP BUTTONS:

active_trading=[False]

def start_settings():

    if active_trading[0]==False:
        if combo_symbol.get()!='':
            active_trading[0]=True
            button_stop.config(state='normal')
            button_start.config(state='disable')
            button_save.config(state='disable')
            button_upload.config(state='disable')     

        else:
            messagebox.showinfo('Warning','Select Symbol')

def start_trading():
    threading.Thread(target=start_settings,daemon=True).start()

def stop_trading():
    if active_trading[0]==True:
        active_trading[0]=False
        button_start.config(state='normal')
        button_stop.config(state='disable')
        button_save.config(state='normal')
        button_upload.config(state='normal')


button_start=tk.Button(win,text='Start',bg='darkgreen',fg='white',activebackground='#333333',activeforeground='white',command=start_trading)
button_start.place(x=5,y=600,width=52,height=20)

button_stop=tk.Button(win,text='Stop',bg='darkred',fg='white',activebackground='#333333',activeforeground='white',state='disable',command=stop_trading)
button_stop.place(x=61,y=600,width=52,height=20)

button_save=tk.Button(win,text='Save',bg='darkblue',fg='white',activebackground='#333333',activeforeground='white'
button_save.place(x=117,y=600,width=52,height=20)

button_upload=tk.Button(win,text='Upload',bg='darkblue',fg='white',activebackground='#333333',activeforeground='white')
button_upload.place(x=173,y=600,width=52,height=20)

win.mainloop()




