import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import font
from tkinter import messagebox
from datetime import date,datetime,timedelta
import time,random
import threading
import pandas as pd
import numpy as np
import csv
import os
import json
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import importlib.util
import json

def neural_net_console():
    win=tk.Toplevel()
    win.title('Neural Net')
    win.geometry('900x535')
    win.resizable(0,0)
    win.configure(bg='#1c1c1c')

    ######################################################################################################################################################

    #CANVAS LINES:

    line1=tk.Canvas(win,width=2,height=380,bg='#1c1c1c',bd=0,highlightthickness=0,highlightbackground='#FF0000')    #verical
    line1.place(x=145,y=0)
    line1.create_line(1,0,1,360,width=1,fill='grey')

    line2=tk.Canvas(win,width=145,height=2,bg='#1c1c1c',bd=0,highlightthickness=0,highlightbackground='#FF0000')    #horizontal 1
    line2.place(x=0,y=110)
    line2.create_line(0,1,145,1,width=1,fill='gray')

    line3=tk.Canvas(win,width=145,height=2,bg='#1c1c1c',bd=0,highlightthickness=0,highlightbackground='#FF0000')    #horizontal 2
    line3.place(x=0,y=140)
    line3.create_line(0,1,145,1,width=1,fill='gray')

    line4=tk.Canvas(win,width=145,height=2,bg='#1c1c1c',bd=0,highlightthickness=0,highlightbackground='#FF0000')    #horizontal 3
    line4.place(x=0,y=215)
    line4.create_line(0,1,145,1,width=1,fill='gray')

    line5=tk.Canvas(win,width=145,height=2,bg='#1c1c1c',bd=0,highlightthickness=0,highlightbackground='#FF0000')    #horizontal 4
    line5.place(x=0,y=303)
    line5.create_line(0,1,145,1,width=1,fill='gray')

    line6=tk.Canvas(win,width=900,height=2,bg='#1c1c1c',bd=0,highlightthickness=0,highlightbackground='#FF0000')    #horizontal 5
    line6.place(x=0,y=360)
    line6.create_line(0,1,900,1,width=1,fill='gray')

    ######################################################################################################################################################

    #LOAD DATA WIDGETS:
    data_count={'from':1,'to':1000}
    spin_from_data=ttk.Spinbox(win,from_=1,to=data_count['to'])
    spin_from_data.set(1)
    spin_to_data=ttk.Spinbox(win,from_=1,to=data_count['to'])
    spin_to_data.set(data_count['to'])
    pbar_load_data=ttk.Progressbar(win,orient='horizontal',mode='determinate',maximum=data_count['to'])
    label_count_data=tk.Label(win,text=f"0/{data_count['to']}",bg='#1c1c1c',fg='white')

    #COMBO SYMBOL:
    label_symbol=tk.Label(win,text='Symbol',bg='#1c1c1c',fg='white').place(x=5,y=5)
    symbols=['EURUSDm','BTCUSDm','XAUUSDm','SP500m']
    combo_symbol=ttk.Combobox(win,values=symbols)
    combo_symbol.place(x=60,y=5,width=80)

    #LABEL FILE:
    label_file=tk.Label(win,text='No File',width=18,anchor='w', justify='left',fg='white',bg='#1c1c1c')
    label_file.place(x=5,y=25)

    #COMBO INTERVAL:
    label_interval=tk.Label(win,text='Interval',fg='white',bg='#1c1c1c').place(x=5,y=45)
    intervals=['M1','M5','M15','M30','H1','H4','D1']
    combo_interval=ttk.Combobox(win,values=intervals)
    combo_interval.place(x=60,y=45,width=80)
    combo_interval.set('M1')

    #DATES:
    label_from=tk.Label(win,text='From',fg='white',bg='#1c1c1c').place(x=5,y=65)
    cal_from=DateEntry(win,selectmode='days',date_pattern='dd/mm/yy')
    cal_from.place(x=60,y=65,width=80)
    cal_from.set_date(date(2022,1,3))
    label_to=tk.Label(win,text='To',fg='white',bg='#1c1c1c').place(x=5,y=85)
    cal_to=DateEntry(win,selectmode='days',date_pattern='dd/mm/yy')
    cal_to.place(x=60,y=85,width=80)
    cal_to.set_date(date(2022,1,4))

    ######################################################################################################################################################

    #WILLIAM INDICATORS:

    will_indicators=['Alligator','Fractals','AO']
    alligator_values={'lips':[5,'green'],'teeths':[8,'red'],'jaw':[13,'blue']}
    fractals_values={'fractal':2,'up':'#3ba3bc','down':'#264f5a'}
    awesome_values={'slow':34,'fast':5,'up':'#3ba3bc','down':'#264f5a'}
    
    #COMBO WILLIAM INDICATORS:
    def select_will_values(event):
        will_vals={
            'Alligator':f"({alligator_values['lips'][0]},{alligator_values['teeths'][0]},{alligator_values['jaw'][0]})",
            'Fractals':f"({fractals_values['fractal']})",
            'AO':f"({awesome_values['fast']},{awesome_values['slow']})"
        }[combo_will.get()]
        label_will_values.config(text=will_vals)
    combo_will=ttk.Combobox(win,values=will_indicators)
    combo_will.place(x=5,y=115,width=65,height=20)
    combo_will.set(will_indicators[0])
    combo_will.bind('<<ComboboxSelected>>',select_will_values)
    
    #LABEL CONFIG WILLIAM INDICATOR:
    alligator_vals=f"({alligator_values['lips'][0]}, {alligator_values['teeths'][0]}, {alligator_values['jaw'][0]})"
    label_will_values=tk.Label(win,text=alligator_vals,bg='#1c1c1c',fg='white')
    label_will_values.place(x=70,y=115)

    #BUTTON CONFIG WILLIAM:

    def alligator_window():
        win_alligator=tk.Toplevel()
        win_alligator.title('Alligator settings')
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
        elif combo_will.get()=='AO':
            awesome_window()

    button_config_will=tk.Button(win,text='...',bg='black',fg='white',activebackground='#333333',activeforeground='white',command=config_william)
    button_config_will.place(x=120,y=115,width=22,height=20)
    
    ######################################################################################################################################################

    #LOAD DATA:
    
    LoadData=[False]

    #variables:
    candle_variables=['id','tick_time','bid','ask','time','open','high','low','close']
    william_variables=['lips','teeth','jaw','up','down','fast_ao','slow_ao','ao']
    variables=candle_variables+william_variables
    var={i:[] for i in variables}

    spin_from_data.place(x=5,y=145,width=65,height=20)

    spin_to_data.place(x=75,y=145,width=65,height=20)

    pbar_load_data.place(x=5,y=170,width=65,height=15)

    label_count_data.place(x=70,y=168)

    def load_data_settings():
        get_load_settings={'symbol':combo_symbol.get(),'symbol_file':label_file.cget('text'),'interval':combo_interval.get(),'date_from':cal_from.get(),
            'date_to':cal_to.get(),'will_indicator':will_indicators,'alligator':alligator_values,'fractals':fractals_values,'awesome':awesome_values,
            'data_from':spin_from_data.get(),'data_to':spin_to_data.get()}
        return get_load_settings
    
    def load_data_widgets():
        get_load_widgets={'load_data':LoadData,'button_load_data':button_load_data,'button_stop_load':button_stop_load,'pbar_load_data':pbar_load_data,
            'label_count_data':label_count_data}
        return get_load_widgets

    button_load_data=tk.Button(win,text='Load Data',bg='black',fg='white',activebackground='#333333',activeforeground='white')
    button_load_data.place(x=5,y=192,width=65,height=20)

    button_stop_load=tk.Button(win,text='Stop Load',bg='black',fg='white',activebackground='#333333',activeforeground='white',state='disable')
    button_stop_load.place(x=75,y=192,width=65,height=20)

    ######################################################################################################################################################

    #BATCH SPIN:
    spin_batch_val=tk.IntVar(value=1)
    label_batch=tk.Label(win,text='Batchs',fg='white',bg='#1c1c1c').place(x=5,y=220)
    spin_batch=tk.Spinbox(win,from_=1,to=1000,textvariable=spin_batch_val)
    spin_batch.place(x=65,y=220,width=75)

    #EPOCH SPIN:
    spin_epoch_val=tk.IntVar(value=10000)
    label_epoch=tk.Label(win,text='Epochs',fg='white',bg='#1c1c1c').place(x=5,y=240)
    spin_epoch=tk.Spinbox(win,from_=1,to=1000000,textvariable=spin_epoch_val)
    spin_epoch.place(x=65,y=240,width=75)

    #LEARING RATE SPIN:
    spin_lrate_val=tk.IntVar(value=0.001)
    label_lrate=tk.Label(win,text='L. Rate',fg='white',bg='#1c1c1c').place(x=5,y=260)
    spin_lrate=tk.Spinbox(win,from_=0.000001,to=10,increment=0.000001,format='%.6f',textvariable=spin_lrate_val)
    spin_lrate.place(x=65,y=260,width=75)

    #OPTIMIZER COMBO:
    label_optimizer=tk.Label(win,text='Optimizer',fg='white',bg='#1c1c1c').place(x=5,y=280)
    optimizers=['SGD','Adam','Momentum','RMSProp']
    combo_optimizer=ttk.Combobox(win,values=optimizers)
    combo_optimizer.place(x=65,y=280,width=75)
    combo_optimizer.set('SGD')

    ######################################################################################################################################################

    #NEURAL NET:

    #NEURAL NET MODEL:

    def update_nn_radio_bg(*args):
        for rb in (radio_ann,radio_lstm,radio_gru):
            if rb.cget('value')==var_neural.get():
                rb.config(bg='gray',fg='black')
            else:
                rb.config(bg='black', fg='white')

    var_neural=tk.StringVar()
    radio_ann=tk.Radiobutton(win,text='ANN',variable=var_neural,value='ann',indicatoron=False)
    radio_ann.place(x=5,y=310,width=42,height=20)
    radio_lstm=tk.Radiobutton(win,text='LSTM',variable=var_neural,value='lstm',indicatoron=False)
    radio_lstm.place(x=52,y=310,width=42,height=20)
    radio_gru=tk.Radiobutton(win,text='GRU',variable=var_neural,value='gru',indicatoron=False)
    radio_gru.place(x=98,y=310,width=42,height=20)
    var_neural.trace_add("write",update_nn_radio_bg)
    var_neural.set('ann')

    #NEURAL NET REG/CLASS:
        
    def select_model(*args):
        if combo_nn_model.get()=='Regression':
            radio_lstm.config(state='normal')
            radio_gru.config(state='normal')
        elif combo_nn_model.get()=='Classification':
            radio_lstm.config(state='disable')
            radio_gru.config(state='disable')
            var_neural.set('ann')

    label_nn_type=tk.Label(win,text='Model',bg='#1c1c1c',fg='white').place(x=5,y=335)

    combo_nn_model=ttk.Combobox(win,values=['Regression','Classification'])
    combo_nn_model.place(x=52,y=335,width=87,height=20)
    combo_nn_model.set('Regression')
    combo_nn_model.bind('<<ComboboxSelected>>',select_model)
    select_model()

    #-----------------------------------------------------------------------------------------------------------------------------------------------------

    #ANN CONCOLE:

    params={'ann':None,'lstm':None,'gru':None}
    ct0=[None]
    ht0=[None]

    frame_nn=tk.Frame(win,bg='black')
    frame_nn.place(x=2,y=365,width=896,height=145)
    
    #NN SET PLOT NEURAL NET: -----------------------------------------------------------------------------------------------------------------------------

    fig_nn=plt.figure(figsize=(2.1,1.35))
    ax_nn=fig_nn.add_subplot()
    fig_nn.set_facecolor('#1c1c1c')
    fig_nn.subplots_adjust(top=0.98,bottom=0.02,right=0.98,left=0.02,hspace=0,wspace=0)

    ax_nn.clear()
    ax_nn.set_facecolor('#1c1c1c')
    ax_nn.set_xticks([])
    ax_nn.set_yticks([])
    nn_spines=['top','bottom','right','left']
    for i in nn_spines:
        ax_nn.spines[i].set_color('dimgray')
    
    #NN PLOT CANVAS:
    canvas_plot_nn=FigureCanvasTkAgg(fig_nn,master=frame_nn)
    canvas_plot_nn.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
    canvas_plot_nn.get_tk_widget().place(x=680,y=5)

    def neurons_per_layer():
        
        inputs,layers,outputs=[],[],[]
        
        #INPUTS:
        if len(input_widgets['count'])>0:
            inputs.append(len(input_widgets['count']))
        #LAYERS:
        if len(layer_widgets['count'])>0:
            for i in range(len(layer_widgets['count'])):
                layers.append(int(layer_widgets['spin'][i].get()))
        #OUTPUTS:
        if len(output_widgets['count'])>0:
            outputs.append(len(output_widgets['count']))

        total_neurons=inputs+layers+outputs

        #PLOT NEURONS:
        ax_nn.clear()
        ax_nn.set_facecolor('#1c1c1c')
        ax_nn.set_xticks([])
        ax_nn.set_yticks([])
        nn_spines=['top','bottom','right','left']
        for i in nn_spines:
            ax_nn.spines[i].set_color('dimgray')

        if len(total_neurons)>=1:
            for i in range(len(total_neurons)):
                ax_nn.scatter([i+1]*total_neurons[i],[(j+1)-total_neurons[i]/2 for j in range(total_neurons[i])],c='white',s=10)
                if i==len(total_neurons)-1:break
                for j in range(total_neurons[i]):
                    for k in range(total_neurons[i+1]):
                        ax_nn.plot([i+1,i+2],[j+1-total_neurons[i]/2,k+1-total_neurons[i+1]/2],c='white',lw=0.2)

        canvas_plot_nn.draw()

    #NN CANVAS ENTRIES: -----------------------------------------------------------------------------------------------------------------------------------

    canvas_input_nn=tk.Canvas(frame_nn,bg='#1c1c1c',bd=0,highlightthickness=0)
    canvas_input_nn.place(x=5,y=25,width=207,height=115)
    scrollbar_input_nn=tk.Scrollbar(frame_nn,orient='vertical',command=canvas_input_nn.yview)
    canvas_input_nn.configure(yscrollcommand=scrollbar_input_nn.set)
    scrollbar_input_nn.place(x=212,y=25,width=10,height=115)

    #NN FRAME ENTRIES:
    frame_input_nn=tk.Frame(canvas_input_nn,bg='#1c1c1c')
    canvas_input_nn.create_window((0,0),window=frame_input_nn,anchor='nw')

    #NN LABEL ENTRIES:
    label_rows_input=tk.Label(frame_nn,text='I: 0',bg='black',fg='white')
    label_rows_input.place(x=105,y=4)

    #NN SPIN ENTRIES:
    spin_input=tk.Spinbox(frame_nn,from_=1,to=100)
    spin_input.place(x=5,y=5,width=45)

    input_widgets={'count':[],'label':[],'combo':[],'variables':[f'input {i+1}' for i in range(10)]}

    def add_input():
        dist=20
        
        if 0<=len(input_widgets['count'])<100:
            for i in range(int(spin_input.get())):
                input_widgets['count'].append(len(input_widgets['count'])+1)

                #INPUT LABEL:
                label_input_neural=tk.Label(frame_input_nn,text=f"Input {input_widgets['count'][-1]} "+'-'*15,bg='#1c1c1c',fg='white')
                label_input_neural.place(x=5,y=dist*(input_widgets['count'][-1]-1))
                input_widgets['label'].append(label_input_neural)
                #INPUT COMBO:
                combo_input_neural=ttk.Combobox(frame_input_nn,values=input_widgets['variables'])
                combo_input_neural.place(x=120,y=dist*(input_widgets['count'][-1]-1),width=70)
                input_widgets['combo'].append(combo_input_neural)

            label_rows_input.config(text=f"I: {len(input_widgets['count'])}")

        #UPDATE CANVAS AND FRAME:
        frame_input_nn.config(width=200,height=dist*input_widgets['count'][-1])
        canvas_input_nn.config(scrollregion=(0,0,frame_input_nn.winfo_width(),frame_input_nn.winfo_height()))

        neurons_per_layer()

    def remove_input():
        dist=20
    
        for i in range(int(spin_input.get()) if len(input_widgets['count'])>int(spin_input.get()) else len(input_widgets['count'])):
            del input_widgets['count'][-1]

            #INPUT LABEL
            input_widgets['label'][-1].destroy()
            del input_widgets['label'][-1]
            #INPUT COMBO:
            input_widgets['combo'][-1].destroy()
            del input_widgets['combo'][-1]

        label_rows_input.config(text=f"I: {len(input_widgets['count'])}")
        
        #UPDATE CANVAS AND FRAME:
        frame_input_nn.config(width=200,height=dist*input_widgets['count'][-1] if len(input_widgets['count'])>0 else 0)
        canvas_input_nn.config(scrollregion=(0,0,frame_input_nn.winfo_width(),frame_input_nn.winfo_height()))

        neurons_per_layer()

    #NN BUTTON ADD ENTRY:
    button_font=font.Font(family='Helvetica',size=12,weight='bold')
    button_add_input=tk.Button(frame_nn,text='+',font=button_font,bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=add_input)
    button_add_input.place(x=50,y=5,width=25,height=20)

    #NN BUTTON REMOVE ENTRY:
    button_rem_input=tk.Button(frame_nn,text='-',font=button_font,bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=remove_input)
    button_rem_input.place(x=75,y=5,width=25,height=20)

    #NN CANVAS LAYER: -------------------------------------------------------------------------------------------------------------------------------------------

    canvas_layer_nn=tk.Canvas(frame_nn,bg='#1c1c1c',bd=0,highlightthickness=0)
    canvas_layer_nn.place(x=227,y=25,width=212,height=115)
    scrollbar_layer_nn=tk.Scrollbar(frame_nn,orient='vertical',command=canvas_layer_nn.yview)
    canvas_layer_nn.configure(yscrollcommand=scrollbar_layer_nn.set)
    scrollbar_layer_nn.place(x=439,y=25,width=10,height=115)

    #NN FRAME LAYERS:
    frame_layer_nn=tk.Frame(canvas_layer_nn,bg='#1c1c1c')
    canvas_layer_nn.create_window((0,0),window=frame_layer_nn,anchor='nw')

    #NN LABEL LAYERS:
    label_rows_layer=tk.Label(frame_nn,text='L: 0',bg='black',fg='white')
    label_rows_layer.place(x=327,y=4)

    #NN SPIN LAYERS:
    spin_layer=tk.Spinbox(frame_nn,from_=1,to=100)
    spin_layer.place(x=227,y=5,width=45)

    layer_widgets={'count':[],'label':[],'spin':[],'combo':[]}

    def add_layer():
        dist=20

        if 0<=len(layer_widgets['count'])<100:
            for i in range(int(spin_layer.get())):
                layer_widgets['count'].append(len(layer_widgets['count'])+1)

                #LAYER LABEL:
                label_layer_neural=tk.Label(frame_layer_nn,text=f"Layer {layer_widgets['count'][-1]} "+'-'*18,bg='#1c1c1c',fg='white')
                label_layer_neural.place(x=5,y=dist*(layer_widgets['count'][-1]-1))
                layer_widgets['label'].append(label_layer_neural)
                #LAYER SPIN:
                spin_layer_neural=tk.Spinbox(frame_layer_nn,from_=1,to=100,command=neurons_per_layer)
                spin_layer_neural.place(x=65,y=dist*(layer_widgets['count'][-1]-1),width=50)
                layer_widgets['spin'].append(spin_layer_neural)
                #LAYER COMBO:
                combo_layer_neural=ttk.Combobox(frame_layer_nn,values=['lineal','relu','sigmoid','softmax'])
                combo_layer_neural.place(x=135,y=dist*(layer_widgets['count'][-1]-1),width=65)
                combo_layer_neural.set('relu')
                layer_widgets['combo'].append(combo_layer_neural)
            
            label_rows_layer.config(text=f"L: {len(layer_widgets['count'])}")

        #UPDATE CANVAS AND FRAME:
        frame_layer_nn.config(width=200,height=dist*layer_widgets['count'][-1])
        canvas_layer_nn.config(scrollregion=(0,0,frame_layer_nn.winfo_width(),frame_layer_nn.winfo_height()))

        neurons_per_layer()

    def remove_layer():
        dist=20

        for i in range(int(spin_layer.get()) if len(layer_widgets['count'])>int(spin_layer.get()) else len(layer_widgets['count'])):
            del layer_widgets['count'][-1]

            #LAYER LABEL:
            layer_widgets['label'][-1].destroy()
            del layer_widgets['label'][-1]
            #LAYER SPIN:
            layer_widgets['spin'][-1].destroy()
            del layer_widgets['spin'][-1]
            #LAYER COMBO:
            layer_widgets['combo'][-1].destroy()
            del layer_widgets['combo'][-1]
            
        label_rows_layer.config(text=f"L: {len(layer_widgets['count'])}")

        #UPDATE CANVAS AND FRAME:
        frame_layer_nn.config(width=200,height=dist*layer_widgets['count'][-1] if len(layer_widgets['count'])>0 else 0)
        canvas_layer_nn.config(scrollregion=(0,0,frame_layer_nn.winfo_width(),frame_layer_nn.winfo_height()))

        neurons_per_layer()

    #NN BUTTON ADD LAYER:
    button_add_layer=tk.Button(frame_nn,text='+',font=button_font,bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=add_layer)
    button_add_layer.place(x=272,y=5,width=25,height=20)

    #NN BUTTON REMOVE LAYER:
    button_rem_layer=tk.Button(frame_nn,text='-',font=button_font,bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=remove_layer)
    button_rem_layer.place(x=297,y=5,width=25,height=20)

    #NN CANVAS OUTPUTS: -------------------------------------------------------------------------------------------------------------------------------------------

    canvas_output_nn=tk.Canvas(frame_nn,bg='#1c1c1c',bd=0,highlightthickness=0)
    canvas_output_nn.place(x=455,y=25,width=207,height=95)
    scrollbar_output_nn=tk.Scrollbar(frame_nn,width=12,orient='vertical',command=canvas_output_nn.yview)
    canvas_output_nn.configure(yscrollcommand=scrollbar_output_nn.set)
    scrollbar_output_nn.place(x=662,y=25,height=95)

    #NN FRAME OUTPUTS:
    frame_output_nn=tk.Frame(canvas_output_nn,bg='#1c1c1c')
    canvas_output_nn.create_window((0,0),window=frame_output_nn,anchor='nw')

    #NN LABEL OUTPUTS:
    label_rows_output=tk.Label(frame_nn,text='O: 0',bg='black',fg='white')
    label_rows_output.place(x=560,y=4)

    #NN SPIN OUTPUTS:
    spin_output=tk.Spinbox(frame_nn,from_=1,to=100)
    spin_output.place(x=455,y=5,width=50)

    output_widgets={'count':[],'label':[],'combo':[],'variables':[f'output {i+1}' for i in range(10)]}

    def add_output():
        dist=20

        if 0<=len(output_widgets['count'])<100:
            for i in range(int(spin_output.get())):
                output_widgets['count'].append(len(output_widgets['count'])+1)

                #OUTPUT LABEL:
                label_output_neural=tk.Label(frame_output_nn,text=f"Output: {output_widgets['count'][-1]} "+'-'*15,bg='#1c1c1c',fg='white')
                label_output_neural.place(x=5,y=dist*(output_widgets['count'][-1]-1))
                output_widgets['label'].append(label_output_neural)
                #OUTPUT COMBO:
                combo_output_neural=ttk.Combobox(frame_output_nn,values=output_widgets['variables'])
                combo_output_neural.place(x=120,y=dist*(output_widgets['count'][-1]-1),width=70)
                output_widgets['combo'].append(combo_output_neural)

            label_rows_output.config(text=f"O: {len(output_widgets['count'])}")

        #UPDATE CANVAS AND FRAME:
        frame_output_nn.config(width=200,height=dist*output_widgets['count'][-1])
        canvas_output_nn.config(scrollregion=(0,0,frame_output_nn.winfo_width(),frame_output_nn.winfo_height()))

        neurons_per_layer()

    def remove_output():
        dist=20

        for i in range(int(spin_output.get()) if len(output_widgets['count'])>int(spin_output.get()) else len(output_widgets['count'])):
            del output_widgets['count'][-1]

            #OUTPUT LABEL:
            output_widgets['label'][-1].destroy()
            del output_widgets['label'][-1]
            #OUTPUT COMBO:
            output_widgets['combo'][-1].destroy()
            del output_widgets['combo'][-1]

        label_rows_output.config(text=f"O: {len(output_widgets['count'])}")

        #UPDATE CANVAS AND FRAME:
        frame_output_nn.config(width=200,height=dist*output_widgets['count'][-1] if len(output_widgets['count'])>0 else 0)
        canvas_output_nn.config(scrollregion=(0,0,frame_output_nn.winfo_width(),frame_output_nn.winfo_height()))

        neurons_per_layer()

    #NN BUTTON ADD OUTPUT:
    button_add_output=tk.Button(frame_nn,text='+',font=button_font,bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=add_output)
    button_add_output.place(x=505,y=5,width=25,height=20)

    #NN BUTTON REMOVE OUTPUT:
    button_rem_output=tk.Button(frame_nn,text='-',font=button_font,bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white',command=remove_output)
    button_rem_output.place(x=530,y=5,width=25,height=20)

    #NN LABEL ACTIVATION FUNCION OUTPUT:
    label_activation_output=tk.Label(frame_nn,text='Activation '+'-'*14,bg='black',fg='white').place(x=455,y=120)

    #NN COMBO ACTIVATION FUNCTION OUTPUT:
    combo_activation_output=ttk.Combobox(frame_nn,values=['lineal','relu','sigmoid','softmax'])
    combo_activation_output.place(x=592,y=120,width=82)
    combo_activation_output.set('lineal')

    ######################################################################################################################################################

    #EDITOR, TABLE, GRAPH:

    def update_EditTableGraph_radio(*args):
        for rb in (radio_EditTable,radio_Graph):
            if rb.cget('value')==var_EditTableGraph.get():
                rb.config(bg='gray',fg='black')
            else:
                rb.config(bg='#1c1c1c',fg='white')

    def show_EditGraph_frame():
        if var_EditTableGraph.get()=='edit':
            frame_EditTable.tkraise()
        elif var_EditTableGraph.get()=='graph':
            frame_Graph.tkraise()

    var_EditTableGraph=tk.StringVar()
    radio_EditTable=tk.Radiobutton(win,text='Edit Data',variable=var_EditTableGraph,value='edit',indicatoron=False,command=show_EditGraph_frame)
    radio_EditTable.place(x=150,y=4,width=370,height=20)
    radio_Graph=tk.Radiobutton(win,text='Plot Data',variable=var_EditTableGraph,value='graph',indicatoron=False,command=show_EditGraph_frame)
    radio_Graph.place(x=526,y=4,width=370,height=20)
    var_EditTableGraph.trace_add('write',update_EditTableGraph_radio)
    var_EditTableGraph.set('edit')
    
    #-----------------------------------------------------------------------------------------------------------------------------------------------------

    df_tables={'df_table':pd.DataFrame(),'df_input':pd.DataFrame(),'df_output':pd.DataFrame(),'df_input_time':pd.DataFrame(),'df_output_time':pd.DataFrame()}
    file_tables={'file_table':None,'file_input':None,'file_output':None,'file_input_time':None,'file_output_time':None}
    table_rows={}
    train_data={
            'x_train':{'normal_type':'None','n_train':None,'df_original':pd.DataFrame(),'df_train':pd.DataFrame(),'min':None,'max':None,'mean':None,'std':None},
            'y_train':{'normal_type':'None','n_train':None,'df_original':pd.DataFrame(),'df_train':pd.DataFrame(),'min':None,'max':None,'mean':None,'std':None}
    }

    #EDIT - TABLE FRAME:

    frame_EditTable=tk.Frame(win,bg='#1c1c1c')
    frame_EditTable.place(x=150,y=30,width=745,height=330)

    paned_EditTable=tk.PanedWindow(frame_EditTable,orient=tk.HORIZONTAL,bg='gray')
    paned_EditTable.place(x=1,y=20,width=743,height=290)

    edit_frame=tk.Frame(paned_EditTable,bg='#1c1c1c')
    table_frame=tk.Frame(paned_EditTable,bg='#1c1c1c')

    paned_EditTable.add(edit_frame,stretch='always',minsize=100)
    paned_EditTable.add(table_frame,stretch='always',minsize=100)

    #TEXT EDITOR:

    text_edit=tk.Text(edit_frame,wrap="none",bg="black", fg="white",insertbackground="white")
    text_edit.configure(tabs=("32"))

    vsb_edit=tk.Scrollbar(edit_frame,width=12,orient="vertical", command=text_edit.yview)
    vsb_edit.pack(side="right", fill="y")

    hsb_edit=tk.Scrollbar(edit_frame,width=12,orient="horizontal", command=text_edit.xview)
    hsb_edit.pack(side="bottom", fill="x")

    text_edit.configure(xscrollcommand=hsb_edit.set,yscrollcommand=vsb_edit.set)
    text_edit.pack(expand=True,fill='both')

    #BUTTONS EDITOR:

    button_run_script=tk.Button(frame_EditTable,text='Run',bg='black',fg='white',activebackground='#333333',activeforeground='white',state='disabled')
    button_run_script.place(x=2,y=0,width=50,height=20)

    button_save_script=tk.Button(frame_EditTable,text='Save',bg='black',fg='white',activebackground='#333333',activeforeground='white')
    button_save_script.place(x=52,y=0,width=50,height=20)

    button_upload_script=tk.Button(frame_EditTable,text='Upload',bg='black',fg='white',activebackground='#333333',activeforeground='white')
    button_upload_script.place(x=102,y=0,width=50,height=20)

    label_file_script=tk.Label(frame_EditTable,text='No File',bg='#1c1c1c',fg='white',width=25,anchor='w',justify='left')
    label_file_script.place(x=155,y=0,height=20)

    #TABLE:

    style_table=ttk.Style()
    style_table.theme_use('default')
    style_table.configure(              #head column style:
        'Custom.Treeview.Heading',
        background='black',
        foreground='white',
        font=('Helvetica',10,'bold'))
    style_table.configure(              #cell table style
        'Custom.Treeview',
        background='black',
        foreground='lightgray',
        rowheight=25,
        fieldbackground='black',
        bordercolor='black',
        borderwidth=1)

    style_table.map("Custom.Treeview",background=[('selected', '#2c2c2c')])
    table=ttk.Treeview(table_frame,columns=['col1','col2','col3','col4'],show='headings',style='Custom.Treeview')

    vsb_table=tk.Scrollbar(table_frame,width=12,orient='vertical',command=table.yview)
    vsb_table.pack(side='right',fill='y')

    hsb_table=tk.Scrollbar(table_frame,width=12,orient='horizontal',command=table.xview)
    hsb_table.pack(side='bottom',fill='x')

    table.configure(yscrollcommand=vsb_table.set, xscrollcommand=hsb_table.set)
    table.pack(expand=True, fill='both')

    #BUTTONS TABLE:

    button_save_table=tk.Button(frame_EditTable,text='Save',bg='black',fg='white',activebackground='#333333',activeforeground='white',state='disabled')
    button_save_table.place(x=375,y=0,width=40,height=20)

    button_upload_table=tk.Button(frame_EditTable,text='Upload',bg='black',fg='white',activebackground='#333333',activeforeground='white')
    button_upload_table.place(x=415,y=0,width=50,height=20)

    combo_table=ttk.Combobox(frame_EditTable,values=['Table','Input','Output'])
    combo_table.place(x=465,y=0,width=65)
    combo_table.set(combo_table.cget('values')[0])
    
    #TRAIN - TEST PROPORTION SLIDER:

    var_train=tk.IntVar()
    var_validate=tk.IntVar()
    var_test=tk.IntVar()

    label_train=tk.Label(frame_EditTable,text='Train:',bg='#1c1c1c',fg='white').place(x=0,y=310)

    spin_train=tk.Spinbox(frame_EditTable,from_=0,to=100,textvariable=var_train)
    spin_train.place(x=35,y=310,width=55)
    var_train.set(0)

    style_scale=ttk.Style()
    style_scale.configure('TScale',troughcolor="grey", background="gray", thickness=10,sliderlength=15)

    scale_train=ttk.Scale(frame_EditTable,from_=0,to=100,orient='horizontal',style='TScale')
    scale_train.place(x=95,y=312,width=100,height=16)
    scale_train.bind('<Enter>',style_scale.configure("TScale", background="#2c2c2c"))

    label_validate=tk.Label(frame_EditTable,text='Validate:',bg='#1c1c1c',fg='white').place(x=200,y=310)

    spin_validate=tk.Spinbox(frame_EditTable,from_=0,to=100,textvariable=var_validate)
    spin_validate.place(x=250,y=310,width=55)
    var_validate.set(0)

    scale_ValTest=ttk.Scale(frame_EditTable,from_=0,to=100,orient='horizontal',style='TScale')
    scale_ValTest.place(x=310,y=312,width=100,height=16)
    scale_ValTest.bind('<Enter>',style_scale.configure("TScale", background="#2c2c2c"))

    label_test=tk.Label(frame_EditTable,text='Test:',bg='#1c1c1c',fg='white').place(x=415,y=310)

    spin_test=tk.Spinbox(frame_EditTable,from_=0,to=100,textvariable=var_test)
    spin_test.place(x=445,y=310,width=55)
    var_test.set(100)

    label_proportion_percent=tk.Label(frame_EditTable,text='0/0/100 %',bg='#1c1c1c',fg='white')
    label_proportion_percent.place(x=500,y=310)
    
    def percent_TrainValTest(train,validate,test):
        train_percent=(float(var_train.get())/float(spin_train.cget('to')))*100
        validate_percent=(float(var_validate.get())/float(spin_train.cget('to')))*100
        test_percent=(float(var_test.get())/float(spin_train.cget('to')))*100

        return f'{train_percent:.2f}/{validate_percent:.2f}/{test_percent:.2f} %'

    def set_scale_train():
        scale_train.set(spin_train.get())
        spin_validate.config(to=int(int(spin_train.cget('to'))-var_train.get()))
        var_validate.set(0)
        spin_test.config(to=int(int(spin_train.cget('to'))-var_train.get()))
        var_test.set(int(int(spin_train.cget('to'))-var_train.get()))
        scale_ValTest.config(to=int(int(spin_train.cget('to'))-var_train.get()))
        scale_ValTest.set(0)
        label_proportion_percent.config(text=percent_TrainValTest(spin_train.get(),spin_validate.get(),spin_test.get()))

    def set_spin_train(*args):
        var_train.set(int(scale_train.get()))
        spin_validate.config(to=int(int(spin_train.cget('to'))-var_train.get()))
        var_validate.set(0)
        spin_test.config(to=int(int(spin_train.cget('to'))-var_train.get()))
        var_test.set(int(int(spin_train.cget('to'))-var_train.get()))
        scale_ValTest.config(to=int(int(spin_train.cget('to'))-var_train.get()))
        scale_ValTest.set(0)
        label_proportion_percent.config(text=percent_TrainValTest(spin_train.get(),spin_validate.get(),spin_test.get()))

    def set_scaleValTest_SpinTest():
        var_test.set(int(spin_validate.cget('to'))-var_validate.get())
        scale_ValTest.set(var_validate.get())
        label_proportion_percent.config(text=percent_TrainValTest(spin_train.get(),spin_validate.get(),spin_test.get()))

    def set_SpinVal_SpinTest(*args):
        var_validate.set(int(scale_ValTest.get()))
        var_test.set(int(int(scale_ValTest.cget('to'))-scale_ValTest.get()))
        label_proportion_percent.config(text=percent_TrainValTest(spin_train.get(),spin_validate.get(),spin_test.get()))

    def set_SpinVal():
        scale_ValTest.set(int(spin_test.cget('to'))-var_test.get())
        label_proportion_percent.config(text=percent_TrainValTest(spin_train.get(),spin_validate.get(),spin_test.get()))

    spin_train.config(command=set_scale_train)
    scale_train.config(command=set_spin_train)
    spin_validate.config(command=set_scaleValTest_SpinTest)
    scale_ValTest.config(command=set_SpinVal_SpinTest)
    spin_test.config(command=set_SpinVal)

    #NORMALIZE TABLE DATA:

    label_normalize=tk.Label(frame_EditTable,text='| Normal->',bg='#1c1c1c',fg='white').place(x=530,y=0,height=20)
                
    label_normal_input=tk.Label(frame_EditTable,text='X:',bg='#1c1c1c',fg='white').place(x=590,y=0,height=20)
    combo_normal_input=ttk.Combobox(frame_EditTable,values=['None','MinMax','Zscore'])
    combo_normal_input.place(x=605,y=0,width=60)
    combo_normal_input.set('None')

    label_normal_output=tk.Label(frame_EditTable,text='Y:',bg='#1c1c1c',fg='white').place(x=665,y=0,height=20)
    combo_normal_output=ttk.Combobox(frame_EditTable,values=['None','MinMax','Zscore'])
    combo_normal_output.place(x=680,y=0,width=60)
    combo_normal_output.set('None')

    #APPLY TRAIN,VAL,TEST PROPORTION IN TABLE:
    combo_show_table=ttk.Combobox(frame_EditTable,values=['Show All','Show Train','Show Validate','Show Test'])
    combo_show_table.place(x=610,y=310,width=94)
    combo_show_table.set('Show All')

    #APPLY BUTTON TO CHANGE TRAIN DATASET ACCORDING TO NORMALIZATION OF X AND Y AND TRAIN PROPORTION:
    button_apply_table=tk.Button(frame_EditTable,text='Apply',bg='black',fg='white',activebackground='#333333',activeforeground='white')
    button_apply_table.place(x=705,y=310,width=40,height=20)

    #-----------------------------------------------------------------------------------------------------------------------------------------------------

    #GRAPH FRAME:

    loss,acc=[],[]

    frame_Graph=tk.Frame(win,bg='#1c1c1c')
    frame_Graph.place(x=150,y=30,width=745,height=330)

    #NN SET PLOT NEURAL NET:

    fig=plt.figure(figsize=(7.45,3.1))
    ax=fig.add_gridspec(6,10)
    ax1=fig.add_subplot(ax[0:5,0:7])
    ax2=fig.add_subplot(ax[5:6,0:7])
    ax3=fig.add_subplot(ax[0:3,7:10])
    ax4=fig.add_subplot(ax[3:6,7:10])
    fig.set_facecolor('black')
    fig.subplots_adjust(top=0.98,bottom=0.02,right=0.99,left=0.01,hspace=0,wspace=0)

    #NN PLOT CANVAS:
    canvas_plot_ann=FigureCanvasTkAgg(fig,master=frame_Graph)
    canvas_plot_ann.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_plot_ann.get_tk_widget().place(x=0, y=0)
    #toolbar=NavigationToolbar2Tk(canvas_plot_ann,frame_Graph)
    #toolbar.pack(side='bottom',fill='x')

    #PLOT EMPTY DEFAULT:

    #MAIN GRAPH
    ax1.clear()
    ax1.set_facecolor('black')
    ax1.set_xticks([])
    ax1.set_yticks([])
    nn_spines=['top','bottom','left','right']
    for i in nn_spines:
        ax1.spines[i].set_color('dimgray')

    #AWESOME OSCILATOR:
    ax2.clear()
    ax2.set_facecolor('black')
    ax2.set_xticks([])
    ax2.set_yticks([])
    for i in nn_spines:
        ax2.spines[i].set_color('dimgray')

    #LOSS CURVE:
    ax3.clear()
    ax3.set_facecolor('black')
    ax3.set_xticks([])
    ax3.set_yticks([])
    for i in nn_spines:
        ax3.spines[i].set_color('dimgray')

    #ACCURACY CURVE:
    ax4.clear()
    ax4.set_facecolor('black')
    ax4.set_xticks([])
    ax4.set_yticks([])
    for i in nn_spines:
        ax4.spines[i].set_color('dimgray')

    #SLIDER GRAPH:

    scale_graph=tk.Scale(frame_Graph,from_=0,to=99,orient='horizontal',showvalue=False,bg='#1c1c1c',highlightbackground='#1c1c1c',highlightthickness=0)
    scale_graph.place(x=0,y=310,width=520)

    #DATA SEARCH GRAPH:

    combo_search_date=ttk.Combobox(frame_Graph,values=[i for i in range(100)])
    combo_search_date.place(x=525,y=310,width=165)
    combo_search_date.set(0)

    button_search_date=tk.Button(frame_Graph,text='search',bg='#1c1c1c',fg='white',activebackground='#333333',activeforeground='white')
    button_search_date.place(x=695,y=310,width=50,height=20)

    #-----------------------------------------------------------------------------------------------------------------------------------------------------

    show_EditGraph_frame()

    ######################################################################################################################################################

    #TRAIN PROGRESS BAR:
    
    label_BatchEpoch=tk.Label(win,text='Batch/Epoch:',bg='#1C1C1C',fg='white').place(x=225,y=513)

    #BATCH PROGRESS BAR:
    pbar_batch=ttk.Progressbar(win,orient='horizontal',mode='determinate')
    pbar_batch.place(x=305,y=515,width=130,height=15)

    #EPOCH PROGRESS BAR:
    pbar_epoch=ttk.Progressbar(win,orient='horizontal',mode='determinate')
    pbar_epoch.place(x=440,y=515,width=130,height=15)

    #BATCH/EPOCHS LABEL:
    label_train=tk.Label(win,text='0/0',bg='#1c1c1c',fg='white')
    label_train.place(x=575,y=513)

    #LOSS LABEL:
    label_loss=tk.Label(win,text='Loss:',bg='#1c1c1c',fg='white')
    label_loss.place(x=680,y=513)

    #ACCURACY LABEL
    label_accuracy=tk.Label(win,text='Acc:',bg='#1c1c1c',fg='white')
    label_accuracy.place(x=800,y=513)

    #-----------------------------------------------------------------------------------------------------------------------------------------------------

    #START, STOP, SAVE BUTTONS:

    active_training=[False]

    def start_train_settings():
        if active_training[0]==False:
            active_training[0]=True
            button_stop_train.config(state='normal')
            button_start_train.config(state='disable')
            button_save_train.config(state='disable')
            button_upload_train.config(state='disable')

    def start_training():
        threading.Thread(target=start_train_settings,daemon=True).start()

    def stop_training():
        if active_training[0]==True:
            active_training[0]=False
            button_start_train.config(state='normal')
            button_stop_train.config(state='disable')
            button_save_train.config(state='normal')
            button_upload_train.config(state='normal')

 
    button_start_train=tk.Button(win,text='Start',bg='darkgreen',fg='white',activebackground='#333333',activeforeground='white',command=start_training)
    button_start_train.place(x=5,y=513,width=50,height=20)

    button_stop_train=tk.Button(win,text='Stop',bg='darkred',fg='white',activebackground='#333333',activeforeground='white',state='disable',command=stop_training)
    button_stop_train.place(x=60,y=513,width=50,height=20)

    button_save_train=tk.Button(win,text='Save',bg='darkblue',fg='white',activebackground='#333333',activeforeground='white')
    button_save_train.place(x=115,y=513,width=50,height=20)

    button_upload_train=tk.Button(win,text='Upload',bg='darkblue',fg='white',activebackground='#333333',activeforeground='white')
    button_upload_train.place(x=170,y=513,width=50,height=20)


