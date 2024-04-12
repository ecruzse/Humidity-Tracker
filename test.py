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

LABEL_COLOR = '#9ea1a2'
BUTTON_COLOR = '#1167b1'
WARNING_LABEL_YELLOW = '#eed202'
WARNING_LABEL_ORANGE = '#ff9966'
BALANCED_LABEL = '#339900' #00FF00

ct.set_appearance_mode('dark')
ct.set_default_color_theme('green')

class App(ct.CTk):
    def __init__(self):
        super().__init__()
        
        # main
        self.title('Humidity Checker')  
        self.geometry('600x540')
        self.minsize(600,540)
        self.maxsize(600,700)
        
        # Data Retrieval
        self.humidity = Data().humidity
        
        
        # widgets
        self.update_data = update_data(self)
        self.pie_graph = pie_graph(self)
        self.pie_graph.create_pie_graph(self.humidity)
        self.data_status = data_status(self)
        self.user_information = user_information(self)

        # run app
        self.mainloop()
 
class update_data(ct.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.update_button = ct.CTkButton(self, text='Update Humidity Status')
        self.update_button.pack()
    
class data_status(ct.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        
        self.informational_label = ct.CTkLabel(self, text='Press the "Update Humidity Status" button to see updated graph', bg_color='yellow', text_color='black')        
        self.informational_label.pack()    
    
class pie_graph(ct.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()    
    
    def create_pie_graph(self, humidity):
        fig = plt.figure(figsize=(6,3), dpi=100)
        fig.set_size_inches(2,1)
        fig.patch.set_facecolor('black') #changes background of canvas that contains the pie graph
        # dry_calculator() 
        self.dry = 100 - humidity
        labels = 'Dry','Humid'
        sizes = self.dry, humidity
        # sizes = 40, 60
        # sizes = humidity
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

        canvasbar = FigureCanvasTkAgg(fig, master=self)
        canvasbar.draw()
        canvasbar.get_tk_widget().pack()

class user_information(ct.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # text design
        self.label_font = ct.CTkFont(size=20, family='Arial')
        self.warning_label_font = ct.CTkFont(size=17, family='Arial', weight='bold')
        self.response = requests.get(nws_api) 
        self.current_time = datetime.datetime.now()
        self.day_num = self.current_time.day            
        self.humidity_data = 0
        self.sensor_humidity = 0
        self.dry = 0
        #TODO: validate if this is where this goes...
        # self.nws_forecast()
        self.create_widgets()    
        self.display_widgets()
        self.pack()
    
    # def nws_forecast(self):
    #     self.nws_precipitation = self.response.json()['properties']['periods'][self.day_num]['detailedForecast']
    
    def create_widgets(self):
        
        self.status = ct.CTkLabel(self, text='Humidity Status', font=self.label_font)
        self.add_water = ct.CTkLabel(self, text='ADD WATER', bg_color=WARNING_LABEL_ORANGE, width=600, font=self.warning_label_font, text_color='black')
        self.less_water = ct.CTkLabel(self, text='TOO HUMID', bg_color=WARNING_LABEL_YELLOW, width=600, font=self.warning_label_font, text_color='black')
        self.desired_conditions = ct.CTkLabel(self, text='Desired Conditions', bg_color=BALANCED_LABEL, width=600, font=self.warning_label_font)
        self.limits = ct.CTkLabel(self, text='Set Desired Humidity Percentage (3 unit tolerance)', font=self.label_font)
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
        self.api_forecast = ct.CTkLabel(self, text=f'National Weather Service Forecast', font=self.label_font)
        
        # self.dry_drop_down = ct.CTkOptionMenu(master=root, values=self.percentages, command=display_required_action)
        self.dry_drop_down = ct.CTkOptionMenu(self, values=self.percentages)
        
        # self.probability_of_precipitation = ct.CTkLabel(self, text=f'{self.nws_precipitation}')
        # self.probability_of_precipitation = ct.CTkLabel(self, text=f'precip prob')

    def display_widgets(self):

        # status, user take action
        self.status.pack()

        self.api_forecast.pack()
        # display_pie_graph()
        
        # self.probability_of_precipitation.pack()

        # drop_down down boxes 
        self.limits.pack()
        self.dry_drop_down.pack()
        
class Data:
    def __init__(self) -> None:
        self._last_update = None
        self.cached_humidity = None
        self.setUp()

    def setUp(self):
        self.cached_humidity = self._get_humidity()
        
    @property
    def humidity(self):
        if not self._last_update or ( (datetime.datetime.now() - self._last_update).seconds > 3 ) :
            self.cached_humidity = self._get_humidity()
        return self.cached_humidity
    
    def _get_humidity(self):
        humidity = self.cached_humidity
        response = None
        try:
            response = requests.get(humidity_api_URL)
            response.raise_for_status()
            humidity = response.json()['humidity'] # separated to catch response errors
            # lazy logging. Let logger format str *only* if called. Avoiding work
            logging.debug("Received data: %s", humidity)
            self._last_update = datetime.datetime.now()
            # display_pie_graph()
        except HTTPError:
            error_code = getattr(response, "status_code", 500)
            reason = getattr(response, "reason", "Unknown")
            text = getattr(response, "text", None)
            logging.error("HTTP Error: %s %s %s", error_code, reason, text)
        except Exception as e:
            # display_error()
            logging.error(traceback.format_exc())
        return humidity
    
App()

# from time import sleep
# for _ in range(5):
#     sleep(3)
#     print(test.humidity)
