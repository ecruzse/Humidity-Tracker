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
import mysql.connector 

APP_LEVEL = os.getenv("ENV", "DEV")
logging.basicConfig(level=logging.DEBUG if APP_LEVEL == "DEV" else logging.INFO)

HUMIDITY_API_URL = os.getenv('HUMIDITY_API_URL')
NWS_API = os.getenv('NWS_API') # National Weather Service API URL for Houston
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
USER = os.getenv("USER")
PASW = os.getenv("PASW")

ct.set_appearance_mode('dark')
ct.set_default_color_theme('green')

root = ct.CTk()
root.title('Humidity Tracker')
root.geometry('600x540')
root.minsize(700,540)
root.maxsize(800,800)
# root.resizable(False,False)

class HumidityTracker():
    def __init__(self, main) -> None:
        self.LABEL_COLOR = '#9ea1a2'
        self.BUTTON_COLOR = '#1167b1'
        self.WARNING_LABEL_YELLOW = '#eed202'
        self.WARNING_LABEL_ORANGE = '#ff9966'
        self.BALANCED_LABEL = '#339900' #00FF00
        self.LABEL_FONT = ct.CTkFont(size=20, family='Arial')
        self.WARNING_LABEL_FONT = ct.CTkFont(size=17, family='Arial', weight='bold')
        
        self.warning_frame = ct.CTkFrame(main, width=600, height=25)
        self.warning_frame.pack()
        
        self.pie_graph_frame = ct.CTkFrame(main, width=400, height=300)
        self.pie_graph_frame.pack()
        
        self.user_information_frame = ct.CTkFrame(main, width=500)
        self.user_information_frame.pack(fill=BOTH)
        
        self.desired_humidity = 0
        self.sensor_humidity = Data().humidity
        
        self.forecast = Data().get_forecast()
        
        self.create_widgets()
        self.update_humidity_status()
        
        # try:
        #     self.error_label.forget()
        #     self.create_PieGraph() 
        # except Exception as e:
        #     self.error_label.pack()
        
    def create_PieGraph(self):
        fig = plt.figure(figsize=(1,1), dpi=100)
        fig.set_size_inches(6,3)
        fig.patch.set_facecolor('black') #changes background of canvas that contains the pie graph
        self.error_label.forget()
        labels = 'Dry','Humid'
        sizes = (100 - self.sensor_humidity), self.sensor_humidity
        # sizes = 40, 60
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
                    prop = { "size": 14 })

        canvasbar = FigureCanvasTkAgg(fig, master=self.pie_graph_frame)
        canvasbar.draw()
        canvasbar.get_tk_widget().grid(row=1)
    
    def create_widgets(self):
        self.error_label = ct.CTkLabel(self.pie_graph_frame, text='Error Retrieving Data. Please Try Again.', width=100, height=200)
        
        self.update_button = ct.CTkButton(self.user_information_frame, text='Update Humidity Status', command=self.update_humidity_status)
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
        self.forecast_label = ct.CTkLabel(self.user_information_frame, text=f'{self.forecast}')
        
        self.add_water = ct.CTkLabel(self.warning_frame, text='ADD WATER', bg_color=self.WARNING_LABEL_ORANGE, width=600, font=self.WARNING_LABEL_FONT, text_color='black')
        self.less_water = ct.CTkLabel(self.warning_frame, text='TOO HUMID', bg_color=self.WARNING_LABEL_YELLOW, width=600, font=self.WARNING_LABEL_FONT, text_color='black')
        self.desired_conditions = ct.CTkLabel(self.warning_frame, text='Desired Conditions', bg_color=self.BALANCED_LABEL, width=600, font=self.WARNING_LABEL_FONT)
        
        self.dry_drop_down = ct.CTkOptionMenu(self.user_information_frame, values=self.percentages, command=self.display_required_action)
        
        # status, user take action
        self.update_button.pack()
        
        self.nws_label.pack()
        self.forecast_label.pack()

        # drop_down down boxes 
        self.limits.pack()
        self.dry_drop_down.pack()
        
    def display_required_action(self, desired_humidity_percentage):
        self.desired_humidity = float(desired_humidity_percentage.strip('%'))
        
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
        
    def update_humidity_status(self):
        try:
            self.error_label.forget()
            self.sensor_humidity = Data().humidity
            self.create_PieGraph() 
        except Exception as e:
            self.error_label.pack()
        
class Data:
    def __init__(self) -> None:
        self._last_update = None
        self.cached_humidity = None
        # self.setUp()

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
            response = requests.get(HUMIDITY_API_URL)
            response.raise_for_status()
            humidity = response.json()['humidity'] # separated to catch response errors
            # lazy logging. Let logger format str *only* if called. Avoiding work
            logging.debug("Received data: %s", humidity)
            self._last_update = datetime.datetime.now()
            
        except HTTPError:
            error_code = getattr(response, "status_code", 500)
            reason = getattr(response, "reason", "Unknown")
            text = getattr(response, "text", None)
            logging.error("HTTP Error: %s %s %s", error_code, reason, text)
            
        except Exception as e:
            # display_error()
            logging.error(traceback.format_exc())
        return humidity
    
    def get_temperature(self):
        try:
            response = requests.get(HUMIDITY_API_URL)
            temperature = response.json()['temperature']
        except:
            logging.error(traceback.format_exc())
        return temperature
        
    def get_forecast(self):
        try:
            response = requests.get(NWS_API) 
            current_time = datetime.datetime.now()
            forecast = response.json()['properties']['periods'][int(current_time.day / 14 )]['detailedForecast']
            return forecast
        except Exception as e:
            logging.error(traceback.format_exc())


class db_communication():
    
    def __init__(self) -> None:
        # super().__init__()
        self.temp = 0
        self.date = ''
        self.condition = ''
        self.database = 0
        self.QUERY = ''
    
    def connect_to_database(self):    
        self.database = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASW,
        database='sensor_data'
        # buffered=True,
        )
        data = {}
        # self.QUERY = f'INSERT INTO sensor_metrics (temperature, humidity, day, condition) VALUES ({self.temp}, {self.sensor_humidity}, {self.date}, {self.condition});'
        self.QUERY = "INSERT INTO `sensor_data`.`sensor_metrics` (`temperature`, `humidity`, `day`, `condition`) VALUES ('21', '22.2', '2022-10-12', 'too humid');"

        with self.database.cursor(dictionary=True) as cursor:
            cursor.execute(self.QUERY)
            self.database.commit()
            # data = cursor.fetchall()
        
        # self.database.close()
        return data

database = mysql.connector.connect(
    host=HOST,
    port=PORT,
    user=USER,
    password=PASW,
    database='sensor_data'
    # buffered=True,
)
 
data = {}
# self.QUERY = f'INSERT INTO sensor_metrics (temperature, humidity, day, condition) VALUES ({self.temp}, {self.sensor_humidity}, {self.date}, {self.condition});'
QUERY = "INSERT INTO `sensor_data`.`sensor_metrics` (`temperature`, `humidity`, `day`, `condition`) VALUES ('21', '22.2', '2022-10-12', 'too humid');"

with database.cursor(dictionary=True) as cursor:
    cursor.execute(QUERY)
    database.commit()
    data = cursor.fetchall()
    print(data)
    # self.database.close()



# HumidityTrackerApp = HumidityTracker(root)
# root.mainloop()
    