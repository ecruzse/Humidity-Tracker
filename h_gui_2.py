import tkinter as tk
from tkinter import ttk
# import customtkinter as ct
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
import requests
import datetime

# label_font = ct.CTkFont(size=20, family='Arial')
# warning_label_font = ct.CTkFont(size=17, family='Arial', weight='bold')

LABEL_COLOR = '#9ea1a2'
BUTTON_COLOR = '#1167b1'
WARNING_LABEL_YELLOW = '#eed202'
WARNING_LABEL_ORANGE = '#ff9966'
BALANCED_LABEL = '#339900' #00FF00


# app
class App(tk.Tk):
    def __init__(self):
        
        # master window
        super().__init__()
        self.title('Humidity Tester')
        self.geometry('600x500')
        self.minsize(600,500)
        
        # widgets
        # self.pie_graph = pie_graph(self)
        self.info_panel = info_panel(self)
    

        
        # running app
        self.mainloop()

# pie graph 
class pie_graph(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
    
    
    # fig = plt.figure(figsize=(3,1), dpi=100)
    # fig.set_size_inches(6,3)
    # fig.patch.set_facecolor('black') #changes background of canvas that contains the pie graph 

    # labels = 'Dry', 'Humid'
    # sizes = 70,30 # CHANGE TO MAKE NON STATIC 
    # explode = (0.3,0)

    # plt.style.use('ggplot') #changes the pie graph's color using matplotlib

    # plt.pie(sizes, 
    #         explode=explode, 
    #         labels=labels, 
    #         pctdistance=.3, 
    #         labeldistance=.3)
    # plt.axis('equal')
    # plt.legend(sizes, 
    #             title='Percentages %',
    #             loc="center right",
    #             bbox_to_anchor=(.4, 0, .70, .85),
    #             prop = { "size": 16 })

    # canvasbar = FigureCanvasTkAgg(fig, master=)
    # canvasbar.draw()
    # canvasbar.get_tk_widget().grid(row=1)
        
        
# Information Panel
class info_panel(ttk.Frame):
      def __init__(self, parent):
        super().__init__(parent)
        # tk.Label(self, background='green', text='joe').pack(expand=True, fill='both')
        self.place(x=0, y=160, relwidth=1, relheight=.6)
        
        self.create_widgets()
        
        def create_widgets(self): 
            
            soil_humidity = tk.Label(self.main, text='Soil Humidity')
        
            # status, user take action
            status = tk.Label(self, text='Humidity Status', font='green')

            add_water = tk.Label(self, text='ADD WATER', bg_color='green', width=600, font='arial', text_color='white')

            less_water = tk.Label(self, text='TOO HUMID', bg_color='green', width=600, font='arial', text_color='white')

            desired_conditions = tk.Label(self, text='Desired Conditions', bg_color='green', width=600, font='arial')
        

            # drop_down down boxes 
            limits = tk.Label(self.main, text='Set Desired Humidity Percentage', font='arial')
            
            # placing
            soil_humidity.pack()
            status.pack()
            add_water.pack()
            less_water.pack()
            desired_conditions.pack()
            limits.pack()
            status.pack()
            limits.pack()
            
            
            
        
        # Humidity status

        # Desired Humidity

        # Weather API

App()