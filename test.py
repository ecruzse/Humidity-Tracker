from tkinter import * 
import customtkinter as ct
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
import requests
import datetime

humidity_api_URL = 'http://192.168.68.79:5001/metrics'

class app():
    def __init__(self):
        pass
    
    def create_widgets():
        self.update_button = ct.CTkButton(self.main, text='Update Humidity Status', command=update_humidity_info)
        self.informational_label = ct.CTkLabel(self.main, text='Press the "Update Humidity Status" button to see updated graph', bg_color='yellow', text_color='black')
        self.add_water = ct.CTkLabel(self.main, text='ADD WATER', bg_color=WARNING_LABEL_ORANGE, width=600, font=warning_label_font, text_color='black')
        self.less_water = ct.CTkLabel(self.main, text='TOO HUMID', bg_color=WARNING_LABEL_YELLOW, width=600, font=warning_label_font, text_color='black')
        self.status = ct.CTkLabel(self.main, text='Humidity Status', font=label_font)
        self.desired_conditions = ct.CTkLabel(self.main, text='Desired Conditions', bg_color=BALANCED_LABEL, width=600, font=warning_label_font)
        self.limits = ct.CTkLabel(self.main, text='Set Desired Humidity Percentage (3 unit tolerance)', font=label_font)
        self.dry_drop_down = ct.CTkOptionMenu(master=root, values=self.percentages, command=display_required_action)
        self.api_forecast = ct.CTkLabel(self.main, text=f'National Weather Service Forecast', font=label_font)
        self.probability_pf_precipitation = ct.CTkLabel(self.main, text=f'{self.probability_pf_precipitation}')
        
