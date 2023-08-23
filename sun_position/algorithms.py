
from datetime import datetime

import math
import calendar
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class SunPosition:
    def __init__(self, lat, lon, date_time, is_daylight):
        self.lat = lat
        self.lon = lon
        self.date_time = date_time # local date and time
        self.is_daylight = is_daylight # boolean, is Daylight Saving Time
        # TODO put here? the constants for epochs

    def sun_position(self):
        """Returns a tuple holding the azimuth and elevation angles of the sun"""
        # TODO verify somewhere date_time is ISO format

        # Get date and time as a datetime Python object
        dt_obj = datetime.fromisoformat(self.date_time)

        year, month, day = self.__lct2ut(dt_obj, self.is_daylight, self.lon)

        numdays = self.__date2daynumber(year, month, day)
        dse = self.__days_since_epoch(year, numdays)
        juliandate = self.__juliandate(year, month, day)
        sun_longitude = self.__sun_longitude(dse, juliandate)
        right_asc, declination = self.__rightasc_declin(sun_longitude, juliandate)
        azimuth, altitude = self.__azim_altit(right_asc, declination, self.lat,
                                              self.lon, year, month, day)
        #lst_r, lst_s = self.__riseset_times(right_asc, declination, self.lat)

        print("year, month, day: " + str(year) + ", " + str(month) + ", " + str(day))
        print("numdays: " + str(numdays))
        print("D: " + str(dse))
        print("juliandate: " + str(juliandate))
        print("sun_longitude: " + str(sun_longitude))
        print("right_asc, declin: " + str(right_asc) + ", " + str(declination))
        print("azimuth, altitude: " + str(azimuth) + ", " + str(altitude))
        #print("lst_r, lst_s: " + str(lst_r) + ", " + str(lst_s))

    def __date2daynumber(self, year, month, day):
        """Converts the date to date number"""
        if month > 2:
            month = int((month + 1)*30.6)
            if calendar.isleap(year):
                month = month - 62
            else:
                month = month - 63
            day_number = month + day
        else:
            month = month - 1
            if calendar.isleap(year):
                month = month * 62
            else:
                month = month * 63
            month = int(month/2)
            day_number = month + day

        return day_number

    def __days_since_epoch(self, year, numdays):
        """Gets the number of days since epoch 2010"""
        
        d = 0

        if year > 2010:
            step = 1
        else:
            step = -1

        for i in range(2010, year, step):
            if calendar.isleap(i):
                days = 366
            else:
                days = 365
            d = d + days*(step)

        if year < 2010 and calendar.isleap(year):
            d = d - 1

        return d + numdays

    def __sun_longitude(self, dse, juliandate):
        """Calculates the sun's geocentric ecliptic longitude"""

        jd_epoch1900 = 2415020.0 # julian date for epoch January 0.5 1900
        #jd_epoch2010 = 2455196.5 # julian date for epoch 2010.0

        t = (juliandate - jd_epoch1900)/36525.0

        eg = 279.6966778 + 36000.76892*t + 0.0003025*t*t
        wg = 281.2208444 + 1.719175*t + 0.000452778*t*t
        e = 0.01675104 - 0.0000418*t - 0.000000126*t*t

        if eg > 360:
            eg = eg%360

        if wg > 360:
            wg = wg%360

        print("T: " + str(t))
        print("eg: " + str(eg))
        print("wg: " + str(wg))
        print("e: " + str(e))

        n = 360/365.242191*dse

        if n > 360 or n < 0:
            n = n%360

        mean_anomaly = eg - wg

        if mean_anomaly < 0:
            mean_anomaly = mean_anomaly + 360

        # Find eccentric anomaly by the second, more precise, method
        ea = math.radians(mean_anomaly)
        ea_ = math.radians(mean_anomaly)
        m = math.radians(mean_anomaly)

        delta = ea - e*math.sin(ea) - m
        while abs(delta) > 0.00000001:
            ea_ = ea_ - delta/(1 - e*math.cos(ea_))
            delta = ea_ - e*math.sin(ea_) - m

        tmp = math.sqrt((1 + e)/(1 - e))*math.tan(ea_/2)
        true_anomaly = math.degrees(math.atan(tmp)*2)

        if true_anomaly < 0:
            true_anomaly = true_anomaly + 360

        print("mean_anomaly: " + str(mean_anomaly))
        print("true_anomaly: " + str(true_anomaly))

        sun_longitude = true_anomaly + wg

        if sun_longitude > 360:
            sun_longitude = sun_longitude - 360

        return sun_longitude

    def __rightasc_declin(self, sun_longitude, juliandate):
        """Calculates the rigth ascencion and declination angles"""

        #jd_epoch2010 = 2455196.5 # julian date for epoch 2010.0
        jd_epoch2000 = 2451545.0 # julian date for epoch January 1.5 2000
        #jd_epoch1900 = 2415020.0 # julian date for epoch January 0.5 1900

        t = (juliandate - jd_epoch2000)/36525.0
        de = (46.815*t + 0.0006*t*t - 0.00181*t*t*t)/3600.0
        eo = 23.439292 - de # eo is the ecliptic_obliquity

        sin_eo = math.sin(math.radians(eo))
        cos_eo = math.cos(math.radians(eo))
        sin_sl = math.sin(math.radians(sun_longitude))
        cos_sl = math.cos(math.radians(sun_longitude))

        declination = math.asin(sin_eo*sin_sl)

        y = sin_sl*cos_eo
        x = cos_sl

        if x > 0 and y > 0:
            right_asc = math.atan(y/x)
        elif x < 0 and y > 0:
            right_asc = math.atan(y/x) + math.pi
        elif x > 0 and y < 0:
            right_asc = math.atan(y/x) + 2*math.pi
        elif x < 0 and y < 0:
            right_asc = math.atan(y/x) + math.pi
        else:
            logging.error("__equatorial_coords -> x and y are not defined")

        return math.degrees(right_asc), math.degrees(declination)

    def __azim_altit(self, right_asc, declin, latitude, longitude,
                     year, month, day):
        """Returns sun's azimuth and altitude"""

        gst = self.__ut2gst(year, month, day)

        lst = gst + longitude/15.0

        if lst < 0:
            lst = lst + 24
        elif lst > 24:
            lst = lst - 24

        h = lst - right_asc/15.0

        if h < 0:
            h = h + 24

        sin_declin = math.sin(math.radians(declin))
        cos_declin = math.cos(math.radians(declin))

        sin_lat = math.sin(math.radians(latitude))
        cos_lat = math.cos(math.radians(latitude))

        sin_ra = math.sin(math.radians(h*15))
        cos_ra = math.cos(math.radians(h*15))

        sin_a = sin_declin*sin_lat + cos_declin*cos_lat*cos_ra
        altitude = math.asin(sin_a)

        y = -1*cos_declin*cos_lat*sin_ra
        x = sin_declin - sin_lat*sin_a

        if x > 0 and y > 0:
            azimuth = math.atan(y/x)
        elif x < 0 and y > 0:
            azimuth = math.atan(y/x) + math.pi
        elif x > 0 and y < 0:
            azimuth = math.atan(y/x) + 2*math.pi
        elif x < 0 and y < 0:
            azimuth = math.atan(y/x) + math.pi
        else:
            logging.error("__equatorial_coords -> x and y are not defined")

        return math.degrees(azimuth), math.degrees(altitude)

    def __riseset_times(self, right_asc, declin, latitude):
        """Calculates rise and set times in Local Sidereal Time (LST)"""

        alpha = right_asc/15.0
        tan_lat = math.tan(math.radians(latitude))
        tan_decl = math.tan(math.radians(-1*declin))

        lst_r = 24 + alpha - math.acos(-1*tan_lat*tan_decl)/15

        if lst_r > 24:
            lst_r = lst_r - 24

        lst_s = alpha + math.acos(-1*tan_lat*tan_decl)/15

        alpha = right_asc/15.0
        sin_decl = math.sin(math.radians(declin))
        tan_decl = math.tan(math.radians(declin))
        cos_lat = math.cos(math.radians(latitude))
        tan_lat = math.tan(math.radians(latitude))

        a_r = sin_decl/cos_lat

        if abs(a_r) > 1:
            logging.error("__riseset_times -> undefined")
            return

        r = math.acos(a_r)
        s = 360 - r
        h1 = tan_lat*tan_decl

        if abs(h1) > 1:
            logging.error("__riseset_times -> undefined")
            return

        h2 = math.acos(-1*h1)/15

        lst_r = 24 + alpha - h2

        if lst_r > 24:
            lst_r = lst_r - 24

        lst_s = alpha + h2

        #sin_decl = math.sin(math.radians(declination))
        #tan_decl = math.tan(math.radians(declination))
        #cos_lat = math.cos(math.radians(latitude))
        #tan_lat = math.tan(math.radians(latitude))

        return lst_r, lst_s

    def __juliandate(self, year, month, day):
        """Calculates the julian date for a Greenwich calendar date"""
        if month < 3:
            year = year - 1
            month = month + 12

        # Here we asume all years are > 1582
        a = int(year/100.0)
        b = 2 - a + int(a/4.0)

        if year < 0:
            c = int((365.25*year) - 0.75)
        else:
            c = int(365.25*year)

        d = int(30.6001*(month + 1))

        return b + c + d + day + 1720994.5

    def __lct2ut(self, dt_obj, is_daylight, longitude):
        """Converts local civil time (lct) to universal time (ut)"""

        year = dt_obj.year
        month = dt_obj.month
        day = dt_obj.day
        hour = dt_obj.hour
        minute = dt_obj.minute
        second = dt_obj.second

        lct = hour + minute/60.0 + second/3600.0

        if is_daylight:
            lct = lct - 1

        ut = lct - round(longitude/15.0)
        g_day = day + ut/24.0
        juliandate = self.__juliandate(year, month, g_day)
        year_, month_, day_ = self.__juliandate2gcd(juliandate)

        return year_, month_, day_

    def __juliandate2gcd(self, juliandate):
        """Converts julianday to Greenwich Calendar Date (gcd)"""

        jd = juliandate + 0.5
        frac, inte = math.modf(jd)

        if inte > 2299160:
            a = int((inte - 1867216.25)/36524.25)
            b = inte + a -int(a/4) + 1
        else:
            b = inte

        c = b + 1524
        d = int((c - 122.1)/365.25)
        e = int(365.25*d)
        g = int((c - e)/30.6001)
        day = c - e + frac - int(30.6001*g)

        if g < 13.5:
            month = g - 1
        else:
            month = g - 13

        if month > 2.5:
            year = d - 4716
        else:
            year = d - 4715

        return year, month, day

    def __ut2gst(self, year, month, day):
        """Converts universal time (ut) to Greenwich Standard Time (gst)"""

        day_ = int(day)
        juliandate = self.__juliandate(year, month, day_)
        juliandate_0 = self.__juliandate((year-1), 12, 31)
        elaps_days = juliandate - juliandate_0

        # 2415020.0 is the julian date for epoch Jan 0.5 1900
        t = (juliandate_0 - 2415020.0)/36525.0
        r = 6.6460656 + 2400.051262*t + 0.00002581*t*t
        b = 24 - r + 24*(year - 1900)
        t_0 = 0.0657098*elaps_days - b
        ut = (day - int(day))*24
        gst = t_0 + 1.002738*ut

        if gst < 0:
            gst = gst + 24
        elif gst > 24:
            gst = gst - 24

        return gst

#test = SunPosition(51.48, 0, "2003-07-27T00:00:00", True)
test = SunPosition(38, -78, "2015-02-05T12:00:00", False)
#test = SunPosition(51.48, 0, "1988-07-27T00:00:00", False)
test.sun_position()
