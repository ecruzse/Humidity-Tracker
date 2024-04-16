from tkinter import * 
import customtkinter as ct
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
import requests
import datetime
import os 
import logging
import traceback
from requests import HTTPError

APP_LEVEL = os.getenv("ENV", "DEV")
logging.basicConfig(level=logging.DEBUG if APP_LEVEL == "DEV" else logging.INFO)

humidity_api_URL = os.getenv('HUMIDITY_API_URL')
nws_api = 'https://api.weather.gov/gridpoints/HGX/65,97/forecast' # National Weather Service API URL for Houston



ct.set_appearance_mode('dark')
ct.set_default_color_theme('green')

root = ct.CTk()
root.title('Humidity Tracker')
root.geometry('600x540')
root.minsize(600,540)
root.maxsize(600,700)

class HumidityTracker():
    def __init__(self, main) -> None:
        self.LABEL_COLOR = '#9ea1a2'
        self.BUTTON_COLOR = '#1167b1'
        self.WARNING_LABEL_YELLOW = '#eed202'
        self.WARNING_LABEL_ORANGE = '#ff9966'
        self.BALANCED_LABEL = '#339900' #00FF00
        self.LABEL_FONT = ct.CTkFont(size=20, family='Arial')
        self.warning_label_font = ct.CTkFont(size=17, family='Arial', weight='bold')
        
        self.warning_frame = ct.CTkFrame(main)
        self.warning_frame.pack()
        
        self.pie_graph_frame = ct.CTkFrame(main)
        self.pie_graph_frame.pack()
        
        self.user_information_frame = ct.CTkFrame(main)
        self.user_information_frame.pack()
        
        self.desired_humidity = 0
        self.sensor_humidity = 0
        
        self.create_PieGraph()
        self.create_widgets()
        
    def create_PieGraph(self, humidity=None):
        fig = plt.figure(figsize=(6,3), dpi=100)
        fig.set_size_inches(2,1)
        fig.patch.set_facecolor('black') #changes background of canvas that contains the pie graph
        
        labels = 'Dry','Humid'
        # sizes = (100 - humidity), humidity
        sizes = 40, 60
        explode = (0.1,0)

        plt.style.use('ggplot') #changes the pie graph's color using matplotlib

        plt.pie(sizes, 
                explode=explode, 
                labels=labels, 
                pctdistance=.3, 
                labeldistance=.3)
        plt.axis('equal')
        plt.legend(sizes, 
                    title='%',
                    loc="center right",
                    bbox_to_anchor=(.4, 0, .70, .85),
                    prop = { "size": 6 })

        canvasbar = FigureCanvasTkAgg(fig, master=self.pie_graph_frame)
        canvasbar.draw()
        canvasbar.get_tk_widget().pack()
    
    def create_widgets(self, forecast=None):
        
        self.update_button = ct.CTkButton(self.user_information_frame, text='Update Humidity Status')
        self.limits = ct.CTkLabel(self.user_information_frame, text='Set Desired Humidity Percentage (3 unit tolerance)', font=self.LABEL_FONT)
        self.clicked = StringVar()
        self.clicked.set('Choose Percentage')
        self.percentages = [
                    '0%',
                    '5%', 
                    '10%',
                    '15%',  
                    '20%',
                    '25%',  
                    '30%',
                    '35%',  
                    '40%',
                    '45%',  
                    '50%',
                    '55%',  
                    '60%',
                    '65%',  
                    '70%',
                    '75%',  
                    '80%',
                    '85%',  
                    '90%',
                    '95%',  
                    '100%'    
                ]
        self.nws_label = ct.CTkLabel(self.user_information_frame, text=f'National Weather Service Forecast', font=self.LABEL_FONT)

        self.add_water = ct.CTkLabel(self.warning_frame, text='ADD WATER', bg_color=self.WARNING_LABEL_ORANGE, width=600, font=self.warning_label_font, text_color='black')
        self.less_water = ct.CTkLabel(self.warning_frame, text='TOO HUMID', bg_color=self.WARNING_LABEL_YELLOW, width=600, font=self.warning_label_font, text_color='black')
        self.desired_conditions = ct.CTkLabel(self.warning_frame, text='Desired Conditions', bg_color=self.BALANCED_LABEL, width=600, font=self.warning_label_font)
        
        self.dry_drop_down = ct.CTkOptionMenu(self.user_information_frame, values=self.percentages, command=self.display_required_action)
        # self.dry_drop_down = ct.CTkOptionMenu(self.user_information_frame, values=self.percentages)
        self.forecast_label = ct.CTkLabel(self.user_information_frame, text=f'{forecast}')

        # status, user take action
        self.update_button.pack()
        
        self.nws_label.pack()
        self.forecast_label.pack()

        # drop_down down boxes 
        self.limits.pack()
        self.dry_drop_down.pack()
        
    def display_required_action(self, desired_humidity_percentage):
        self.desired_humidity = float(desired_humidity_percentage.strip('%'))
        # self.desired_humidity = 60
        self.sensor_humidity = 40
        
        if self.sensor_humidity > self.desired_humidity + 3:
            self.add_water.forget()
            self.desired_conditions.forget()
            print(' less_water')
            self.less_water.pack()
        elif self.sensor_humidity < self.desired_humidity - 3:
            self.less_water.forget()
            self.desired_conditions.forget()
            print(' add_water')
            self.add_water.pack()
        elif self.sensor_humidity - self.desired_humidity <= 3 or self.sensor_humidity - self.desired_humidity <= -3:
            self.less_water.forget()
            self.add_water.forget()
            print('desired ')
            self.desired_conditions.pack()       
                
HumidityTrackerApp = HumidityTracker(root)
root.mainloop()
