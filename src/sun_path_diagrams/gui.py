"""This module contains the Tkinter GUI code"""
import os
import csv
import tkinter as tk
import datetime
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from sun_path_diagrams.algorithms_spa import SunPosition
from sun_path_diagrams.charting import PlotSunPath


class SunPathGUI():
    "GUI dialog for the input of parameters and running of the program"
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title('Sun Path Diagrams')
        self.main_window.resizable(False, False)
        self.main_window.configure(bg='#dcdad5')

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.__create_variables()
        self.__create_frames()
        self.__create_lbl_frames()
        self.__create_widgets()
        self.__create_layouts()

    def __create_variables(self):
        """Create StringVar variables"""
        dt = datetime.datetime.now()
        self.year = tk.StringVar(value=dt.year)
        self.month = tk.StringVar(value=dt.month)
        self.day = tk.StringVar(value=dt.day)
        self.hour = tk.StringVar(value=dt.hour)
        self.minute = tk.StringVar(value=dt.minute)
        self.timezone = tk.StringVar()
        self.daylight = tk.StringVar(value=0)
        self.latitude = tk.StringVar(value='51.05')
        self.longitude = tk.StringVar(value='-114.08')
        self.obs_elev = tk.StringVar(value='')
        self.press = tk.StringVar(value='')
        self.temp = tk.StringVar(value='')
        self.title = tk.StringVar(value='Chart title')
        self.hz_chart = tk.StringVar(value=1)
        self.vt_chart = tk.StringVar(value=1)
        self.plt_point = tk.StringVar(value=0)
        self.csv_data = tk.StringVar(value=0)
        self.outputdir = tk.StringVar(value=os.path.expanduser('~'))

    def __create_widgets(self):
        """Create widgets"""
        self.val = GUIValidation(self.main_window)
        # year
        self.year_lbl = ttk.Label(self.date_lbl_frame, text='Year: ')
        self.year_spin = ttk.Spinbox(self.date_lbl_frame, from_=1900, to=2100,
                                     increment=1, textvariable=self.year,
                                     width=5, validate='focusout',
                                     validatecommand=self.val.year_vcmd,
                                     invalidcommand=self.val.year_ivcmd)

        # month
        self.month_lbl = ttk.Label(self.date_lbl_frame, text='Month: ')
        self.month_spin = ttk.Spinbox(self.date_lbl_frame, from_=1, to=12,
                                      increment=1, textvariable=self.month,
                                      width=3, validate='focusout',
                                      validatecommand=self.val.month_vcmd,
                                      invalidcommand=self.val.month_ivcmd)

        # day
        self.day_lbl = ttk.Label(self.date_lbl_frame, text='Day: ')
        self.day_spin = ttk.Spinbox(self.date_lbl_frame, from_=1, to=31,
                                    increment=1, textvariable=self.day,
                                    width=3, validate='focusout',
                                    validatecommand=self.val.day_vcmd,
                                    invalidcommand=self.val.day_ivcmd)

        # hour
        self.hour_lbl = ttk.Label(self.date_lbl_frame, text='Hour: ')
        self.hour_spin = ttk.Spinbox(self.date_lbl_frame, from_=0, to=23,
                                     increment=1, textvariable=self.hour,
                                     width=3, validate='focusout',
                                     validatecommand=self.val.hour_vcmd,
                                     invalidcommand=self.val.hour_ivcmd)

        # minute
        self.minute_lbl = ttk.Label(self.date_lbl_frame, text='Minute: ')
        self.minute_spin = ttk.Spinbox(self.date_lbl_frame, from_=0, to=59,
                                       increment=1, textvariable=self.minute,
                                       width=3, validate='focusout',
                                       validatecommand=self.val.minute_vcmd,
                                       invalidcommand=self.val.minute_ivcmd)

        # time zone
        self.timezone_lbl = ttk.Label(self.date_lbl_frame, text='UTC: ')
        ut = ('-12', '-11', '-10', '-9', '-8', '-7', '-6', '-5', '-4', '-3',
              '-2', '-1', '0', '+1', '+2', '+3', '+4', '+5', '+6', '+7', '+8',
              '+9', '+10', '+11', '+12')
        self.timezone_dropdown = ttk.Combobox(self.date_lbl_frame,
                                              textvariable=self.timezone,
                                              state='readonly', justify='left',
                                              width=5, values=ut)
        self.timezone_dropdown.current(5)

        # daylight
        self.daylight_chkbox = ttk.Checkbutton(self.date_lbl_frame,
                                               text='Daylight Saving Time',
                                               variable=self.daylight,
                                               onvalue=1,
                                               offvalue=0)

        # latitud
        self.latitude_lbl = ttk.Label(self.location_lbl_frame,
                                      text='Latitude: ')
        self.latitude_entry = ttk.Entry(self.location_lbl_frame,
                                        textvariable=self.latitude, width=10,
                                        validate='focusout',
                                        validatecommand=self.val.lat_vcmd,
                                        invalidcommand=self.val.lat_ivcmd)

        # longitude
        self.longitude_lbl = ttk.Label(self.location_lbl_frame,
                                       text='Longitude: ')
        self.longitude_entry = ttk.Entry(self.location_lbl_frame,
                                         textvariable=self.longitude, width=10,
                                         validate='focusout',
                                         validatecommand=self.val.lon_vcmd,
                                         invalidcommand=self.val.lon_ivcmd)

        # observer elevation
        self.obs_elev_lbl = ttk.Label(self.other_lbl_frame,
                                      text='Observer elevation (meters): ')
        self.obs_elev_entry = ttk.Entry(self.other_lbl_frame,
                                        textvariable=self.obs_elev, width=11,
                                        validate='focusout',
                                        validatecommand=self.val.obs_elev_vcmd,
                                        invalidcommand=self.val.obs_elev_ivcmd)

        # pressure
        self.press_lbl = ttk.Label(self.other_lbl_frame,
                                   text='Annual avg local pressure (mbars): ')
        self.press_entry = ttk.Entry(self.other_lbl_frame,
                                     textvariable=self.press, width=11,
                                     validate='focusout',
                                     validatecommand=self.val.press_vcmd,
                                     invalidcommand=self.val.press_ivcmd)

        # temp
        self.temp_lbl = ttk.Label(self.other_lbl_frame,
                                  text='Annual avg local temperature (°C): ')
        self.temp_entry = ttk.Entry(self.other_lbl_frame,
                                    textvariable=self.temp, width=11,
                                    validate='focusout',
                                    validatecommand=self.val.temp_vcmd,
                                    invalidcommand=self.val.temp_ivcmd)

        # output
        self.title_entry = ttk.Entry(self.output_lbl_frame,
                                     textvariable=self.title, width=41)

        self.hz_chart_chkbox = ttk.Checkbutton(self.output_lbl_frame,
                                               text='Plot horizontal sun path',
                                               variable=self.hz_chart,
                                               onvalue=1,
                                               offvalue=0)

        self.vt_chart_chkbox = ttk.Checkbutton(self.output_lbl_frame,
                                               text='Plot vertical sun path',
                                               variable=self.vt_chart,
                                               onvalue=1,
                                               offvalue=0)

        self.plt_point_chkbox = ttk.Checkbutton(self.output_lbl_frame,
                                                text='Plot sun symbol',
                                                variable=self.plt_point,
                                                onvalue=1,
                                                offvalue=0)

        self.csv_data_chkbox = ttk.Checkbutton(self.output_lbl_frame,
                                               text='Save plotting data as csv file',
                                               variable=self.csv_data,
                                               onvalue=1,
                                               offvalue=0)

        self.outputdir_btn = ttk.Button(self.output_lbl_frame,
                                        text='Select output directory',
                                        command=self.__output_directory)
        self.outputdir_lbl = ttk.Label(self.output_lbl_frame,
                                       textvariable=self.outputdir, width=40)

        # buttons
        self.quit_button = ttk.Button(self.button_frame, text='Close',
                                      command=self.main_window.destroy)
        self.getcharts_button = ttk.Button(self.button_frame,
                                           text='Plot Charts',
                                           command=self.__get_charts)

    def __create_frames(self):
        """Create frames"""
        self.button_frame = ttk.Frame(self.main_window)

    def __create_lbl_frames(self):
        """Create label frames"""
        self.date_lbl_frame = ttk.LabelFrame(self.main_window,
                                             text='Date and time',
                                             labelanchor='nw',
                                             padding=5)
        self.location_lbl_frame = ttk.LabelFrame(self.main_window,
                                                 text='Location',
                                                 labelanchor='nw',
                                                 padding=5)
        self.other_lbl_frame = ttk.LabelFrame(self.main_window,
                                              text='Other parameters (not mandatory)',
                                              labelanchor='nw',
                                              padding=5)
        self.output_lbl_frame = ttk.LabelFrame(self.main_window,
                                               text='Output chart options',
                                               labelanchor='nw',
                                               padding=5)

    def __create_layouts(self):
        """Create layouts"""
        # year
        self.year_lbl.grid(column=0, row=1, sticky='E', pady=(0, 10))
        self.year_spin.grid(column=1, row=1, sticky='W', pady=(0, 5))

        # month
        self.month_lbl.grid(column=2, row=1, sticky='E', padx=(10, 1),
                            pady=(0, 5))
        self.month_spin.grid(column=3, row=1, sticky='W', pady=(0, 5))

        # day
        self.day_lbl.grid(column=4, row=1, sticky='E', padx=(10, 1),
                          pady=(0, 5))
        self.day_spin.grid(column=5, row=1, sticky='W', pady=(0, 5))

        # hour
        self.hour_lbl.grid(column=0, row=2, sticky='E')
        self.hour_spin.grid(column=1, row=2, sticky='W')

        # minute
        self.minute_lbl.grid(column=2, row=2, sticky='E', padx=(10, 1))
        self.minute_spin.grid(column=3, row=2, sticky='W')

        # time zone
        self.timezone_lbl.grid(column=4, row=2, sticky='E', padx=(10, 1),
                               pady=(5, 5))
        self.timezone_dropdown.grid(column=5, row=2, sticky='W', pady=(5, 5))

        # daylight
        self.daylight_chkbox.grid(column=1, row=3, sticky='W', columnspan=3)

        # latitude
        self.latitude_lbl.grid(column=0, row=4, sticky='E')
        self.latitude_entry.grid(column=1, row=4, sticky='W')

        # longitude
        self.longitude_lbl.grid(column=2, row=4, sticky='E', padx=(20, 1))
        self.longitude_entry.grid(column=3, row=4, sticky='W')

        # observers elevation
        self.obs_elev_lbl.grid(column=0, row=5, sticky='E', pady=(10, 10))
        self.obs_elev_entry.grid(column=1, row=5, sticky='W')

        # pressure
        self.press_lbl.grid(column=0, row=6, sticky='E', pady=(0, 10))
        self.press_entry.grid(column=1, row=6, sticky='W', pady=(0, 10))

        # temperature
        self.temp_lbl.grid(column=0, row=7, sticky='E', pady=(0, 10))
        self.temp_entry.grid(column=1, row=7, sticky='W', pady=(0, 10))

        # chart title
        self.title_entry.grid(column=0, row=8, sticky='W')

        # horizontal checkbox
        self.hz_chart_chkbox.grid(column=0, row=9, sticky='W', pady=(10, 5))

        # vertical checkbox
        self.vt_chart_chkbox.grid(column=0, row=10, sticky='W', pady=(0, 5))

        # plot sun symbol
        self.plt_point_chkbox.grid(column=0, row=11, sticky='W', pady=(0, 5))

        # data checkbox
        self.csv_data_chkbox.grid(column=0, row=12, sticky='W', pady=(0, 10))

        # output directory
        self.outputdir_btn.grid(column=0, row=13, sticky='W', pady=(0, 10))
        self.outputdir_lbl.grid(column=0, row=14, sticky='W')

        # buttons
        self.quit_button.grid(column=0, row=15, padx=5, pady=(10, 5),
                              sticky='WE')
        self.getcharts_button.grid(column=1, row=15, padx=5, pady=(10, 5),
                                   sticky='WE')

        # label frames
        self.date_lbl_frame.grid(column=0, row=1, padx=5, pady=(10, 10),
                                 sticky='WE')
        self.location_lbl_frame.grid(column=0, row=2, padx=5, pady=(10, 10),
                                     sticky='WE')
        self.other_lbl_frame.grid(column=0, row=3, padx=5, pady=(10, 10),
                                  sticky='WE')
        self.output_lbl_frame.grid(column=0, row=4, padx=5, pady=(10, 10),
                                   sticky='WE')
        # frames
        self.button_frame.grid(column=0, row=5, padx=10, pady=(10, 10),
                               sticky='E')

    def __output_directory(self):
        """Dialog to select output directory"""
        self.outputdir.set(filedialog.askdirectory())

    def __test_input(self, input_string, param_name, is_floating):
        """Test input values before assignment"""
        try:
            if is_floating:
                return float(input_string)
            else:
                return int(input_string)
        except ValueError:
            self.val.error_msgbox(f'Invalid {param_name} value', '')
            return

    def __get_charts(self):
        """Class to create the sun position charts"""
        year = self.__test_input(self.year.get(), 'year', False)
        month = self.__test_input(self.month.get(), 'month', False)
        day = self.__test_input(self.day.get(), 'day', False)
        hour = self.__test_input(self.hour.get(), 'hour', False)
        minute = self.__test_input(self.minute.get(), 'minute', False)
        timezone = int(self.timezone.get())
        daylight = self.daylight.get()
        lat = self.__test_input(self.latitude.get(), 'latitude', True)
        lon = self.__test_input(self.longitude.get(), 'longitude', True)
        obs_elev = 0 if self.obs_elev.get() == '' else \
            self.__test_input(self.obs_elev.get(), 'observer elevation', True)
        press = 0 if self.press.get() == '' else \
            self.__test_input(self.press.get(), 'pressure', True)
        temp = 0 if self.temp.get() == '' else \
            self.__test_input(self.temp.get(), 'temperature', True)
        title = self.title.get()
        hz_chart = self.hz_chart.get()
        vt_chart = self.vt_chart.get()
        plt_point = self.plt_point.get()
        csv_data = self.csv_data.get()
        path = self.outputdir.get()

        # test for date and time correctness
        tmp = [self.val.year_validation(year),
               self.val.month_validation(month),
               self.val.day_validation(day),
               self.val.hour_validation(hour),
               self.val.minute_validation(minute)]

        if not all(tmp):
            self.val.error_msgbox('Invalid date or time value', '')
            return
        else:
            try:
                # seconds are zero
                dt = datetime.datetime(year, month, day, hour, minute, 0)
                if int(daylight) == 1:
                    dt = dt - datetime.timedelta(hours=1)
            except ValueError:
                self.val.error_msgbox('Invalid date or time value', '')
                return

        # test for coordinates correctness
        tmp = [self.val.lat_validation(lat), self.val.lon_validation(lon)]

        if not all(tmp):
            self.val.error_msgbox('Invalid coordinate values', '')
            return

        # test for time zone and latitude congruency
        tz_lat_pairs = ((-12, -180), (-11, -165), (-10, -150), (-9, -135),
                        (-8, -120), (-7, -105), (-6, -90), (-5, -75),
                        (-4, -60), (-3, -45), (-2, -30), (-1, 15), (0, 0),
                        (1, 15), (2, 30), (3, 45), (4, 60), (5, 75),
                        (6, 90), (7, 105), (8, 120), (9, 135), (10, 150),
                        (11, 165), (12, 180))
        tz_width = 4

        for item in tz_lat_pairs:
            if item[0] == timezone:
                low_bound = item[1] - tz_width*15
                upp_bound = item[1] + tz_width*15
                if lon <= low_bound or lon >= upp_bound:
                    txt_main = f'Longitude values must be between {tz_width} hours of the selected time zone'
                    txt_detail = f'For the time zone "UTC {timezone}" the minimum and maximum longitude values are: {low_bound} and {upp_bound}'
                    self.val.error_msgbox(txt_main, txt_detail)
                    return

        sunpos = SunPosition(lat, lon, dt.isoformat(), timezone, obs_elev,
                             press, temp)
        horizon_coords = sunpos.sun_position()
        horizon_coords_point = sunpos.sun_position_point()

        # save azimuth and altitude data as a csv file
        if int(csv_data):
            field_names = ['Dates', 'Azimuths', 'Altitudes']
            file_name = f'SunPositions_{year}-{month}-{day}_{hour}-{minute}.csv'
            sun_positions = []

            for key, value in horizon_coords.items():
                sun_positions.append([key, value[0], value[1]])
            with open(os.path.join(path, file_name), 'w', newline='', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(field_names)
                writer.writerows(sun_positions)

        plot = PlotSunPath(horizon_coords, horizon_coords_point, lat,
                           lon, dt, timezone, title, hz_chart, vt_chart,
                           plt_point, path)
        plot.plot_diagrams()


class GUIValidation():
    "GUI validation for the input parameters"
    def __init__(self, main_window):
        self.main_window = main_window

        # year
        self.year_vcmd = (self.main_window.register(self.year_validation),
                          '%P')
        self.year_ivcmd = (self.main_window.register(self.on_year_invalid),)

        # month
        self.month_vcmd = (self.main_window.register(self.month_validation),
                           '%P')
        self.month_ivcmd = (self.main_window.register(self.on_month_invalid),)

        # day
        self.day_vcmd = (self.main_window.register(self.day_validation), '%P')
        self.day_ivcmd = (self.main_window.register(self.on_day_invalid),)

        # hour
        self.hour_vcmd = (self.main_window.register(self.hour_validation),
                          '%P')
        self.hour_ivcmd = (self.main_window.register(self.on_hour_invalid),)

        # minute
        self.minute_vcmd = (
            self.main_window.register(self.minute_validation), '%P')
        self.minute_ivcmd = (
            self.main_window.register(self.on_minute_invalid),)

        # latitude
        self.lat_vcmd = (self.main_window.register(self.lat_validation), '%P')
        self.lat_ivcmd = (self.main_window.register(self.on_lat_invalid),)

        # longitude
        self.lon_vcmd = (self.main_window.register(self.lon_validation), '%P')
        self.lon_ivcmd = (self.main_window.register(self.on_lon_invalid),)

        # observer elevation
        self.obs_elev_vcmd = (
            self.main_window.register(self.obs_elev_validation), '%P')
        self.obs_elev_ivcmd = (
            self.main_window.register(self.on_obs_elev_invalid),)

        # pressure
        self.press_vcmd = (self.main_window.register(self.press_validation),
                           '%P')
        self.press_ivcmd = (self.main_window.register(self.on_press_invalid),)

        # temperature
        self.temp_vcmd = (self.main_window.register(self.temp_validation),
                          '%P')
        self.temp_ivcmd = (self.main_window.register(self.on_temp_invalid),)

    def year_validation(self, year):
        """Validate the year"""
        if int(year) < 1900 or int(year) > 2100:
            return False
        return True

    def on_year_invalid(self):
        """On invalid year"""
        self.error_msgbox('Invalid year',
                          'Year must be in the range 1900 to 2100')

    def month_validation(self, month):
        """Validate the month"""
        if int(month) < 1 or int(month) > 12:
            return False
        return True

    def on_month_invalid(self):
        """On invalid month"""
        self.error_msgbox('Invalid month',
                          'Month must be in the range 1 to 12')

    def day_validation(self, day):
        """Validate the day"""
        if int(day) < 1 or int(day) > 31:
            return False
        return True

    def on_day_invalid(self):
        """On invalid day"""
        self.error_msgbox('Invalid day',
                          'Day must be in the range 1 to 31')

    def hour_validation(self, hour):
        """Validate the hour"""
        if int(hour) < 0 or int(hour) > 23:
            return False
        return True

    def on_hour_invalid(self):
        """On invalid hour"""
        self.error_msgbox('Invalid hour',
                          'Hour must be in the range 0 to 24')

    def on_minute_invalid(self):
        """On invalid minute"""
        self.error_msgbox('Invalid minute',
                          'Minute must be in the range 0 to 59')

    def minute_validation(self, minute):
        """Validate the minute"""
        if int(minute) < 0 or int(minute) > 59:
            return False
        return True

    def lat_validation(self, lat):
        """Validate the latitude"""
        if float(lat) < -90 or float(lat) > 90:
            return False
        return True

    def on_lat_invalid(self):
        """On invalid latitude"""
        self.error_msgbox('Invalid latitude value',
                          'Latitudes must be in the range -90 to 90')

    def lon_validation(self, lon):
        """Validate the longitude"""
        if float(lon) < -180 or float(lon) > 180:
            return False
        return True

    def on_lon_invalid(self):
        """On invalid longitude"""
        self.error_msgbox('Invalid longitude value',
                          'Longitudes must be in the range -180 to 180')

    def obs_elev_validation(self, obs_elev):
        """Validate the observer elevation"""
        if obs_elev == '':
            if float(obs_elev) < -420 or float(obs_elev) > 8850:
                return False
        return True

    def on_obs_elev_invalid(self):
        """On invalid observer elevation"""
        self.error_msgbox('Invalid observer elevation value',
                          'Elevation must be in the range -420 to 8850 meters')

    def press_validation(self, press):
        """Validate the atmospheric pressure"""
        if press == '':
            if float(press) < 850 or float(press) > 1090:
                return False
        return True

    def on_press_invalid(self):
        """On invalid atmospheric pressure"""
        self.error_msgbox('Invalid atmospheric pressure value',
                          'Atmospheric pressure must be in the range 850 to 1090 mbars')

    def temp_validation(self, temp):
        """Validate the temperature"""
        if temp == '':
            if float(temp) < -90 or float(temp) > 57:
                return False
            return True

    def on_temp_invalid(self):
        """On invalid temperature"""
        self.error_msgbox('Invalid temperature value',
                          'Atmospheric pressure must be in the range -90 to 57 C')

    def error_msgbox(self, message, detail):
        """Error message box"""
        messagebox.showerror(title='Input error', message=message,
                             detail=detail)


if __name__ == '__main__':
    app = SunPathGUI()
    app.main_window.mainloop()