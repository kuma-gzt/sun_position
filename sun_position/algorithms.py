from datetime import datetime

import math, calendar
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class SunPosition:
    def __init__(self, lat, lon, date_time, isDST):
        self.lat = lat
        self.lon = lon
        self.date_time = date_time
        self.isDST = isDST # boolean, is Daylight Saving Time   

    def sun_position(self):
        """Will calculate many parameters. It returns a tuple holding the 
        azimuth and elevation angles of the sun"""
        # TODO verify somewhere date_time is ISO format

        # Get date and time as a datetime Python object
        dt_obj = datetime.fromisoformat(self.date_time)
       
        # day is a decimal number because includes time
        year, month, day = self.__LCT2UT(dt_obj, self.isDST, self.lon)        
        julianday = self.__julianday(year, month, day)
        epsilon_g, omega_g, e = self.__orbital_elems()
        mean_anomaly = self.__mean_anomaly(julianday, epsilon_g, omega_g)
        true_anomaly = self.__true_anomaly(e, mean_anomaly)
        right_asc, declination = self.__equatorial_coords(true_anomaly, omega_g)
        altitude, azimuth = self.__horizon_coords(declination, right_asc, 
                                                  self.lat, self.lon,
                                                  year, month, day)
        
        print("year, month, day: " + str(year) + "," + str(month) + "," + str(day))
        print("epsilon_g: " + str(epsilon_g))
        print("omega_g: " + str(omega_g))
        print("e: " + str(e))
        print("mean_anomaly: " + str(mean_anomaly))
        print("true_anomaly: " + str(true_anomaly))
        print("declination: " + str(declination))
        print("right_asc: " + str(right_asc))        
        print("altitude: " + str(altitude))
        print("azimuth: " + str(azimuth))    
        
    def __julianday(self, year, month, day):
        """"Calculates Julian Day. Parameter day must be decimal number because
            it includes time of the day. Only Gregorian dates."""
        
        if month > 2:
            y = year
            m = month
        else:
            y = year - 1
            m = month + 12
        
        if year < 0:
            t = 0.75
        else:
            t = 0
        
        a = int(y/100)
        b = 2 - a + int(a/4)
        
        return b + int(365.25*y - t) + int(30.6001*(m + 1)) + day + 1720994.5
        
    def __orbital_elems(self):
        """Return the orbital elements for a given epoch."""
        
        # 2455196.5 is the julian day for epoch Jan 0 2010
        #epsilon_g = 279.557208
        #omega_g = 283.112438
        #e = 0.016705
        
        # 2451545.0 is the julian day for epoch Jan 1.5 2000
        epsilon_g = 280.466069
        omega_g = 282.938346
        e = 0.016708

        return epsilon_g, omega_g, e
    
    def __day_number(self, year, month, day):
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
    
    def __mean_anomaly(self, julianday, epsilon_g, omega_g):
        """Calculates the mean anomaly M"""
        
        # 2451545.0 is the julian day for epoch Jan 1.5 2000
        de = julianday - 2451545.0        
        M = 360*de/365.242191 + epsilon_g - omega_g
        
        if M > 360:
            M = M%360

        return M
    
    def __true_anomaly(self, e, mean_anomaly):
        """Calculates the true anomaly Nu"""
        
        # First method
        #Ec = e*math.sin(math.radians(mean_anomaly))*360/math.pi        
        #true_anomaly = mean_anomaly + Ec        
        #if true_anomaly > 360:
            #true_anomaly = true_anomaly%360       
        #return mean_anomaly + Ec
    
        # Second method, more precise
        E = math.radians(mean_anomaly)
        E_ = math.radians(mean_anomaly)
        M = math.radians(mean_anomaly)
        
        delta = E - e*math.sin(E) - M
        while abs(delta) > 0.00000001:
            E_ = E_ - delta/(1 - e*math.cos(E_))
            delta = E_ - e*math.sin(E_) - M
            
        tmp = math.sqrt((1 + e)/(1 - e))*math.tan(E_/2)        
        
        return math.degrees(math.atan(tmp)*2)

    def __equatorial_coords(self, true_anomaly, omega_g):
        """Calculates the right ascension (alpha) and declination (delta).
        In all the following calculations it is assumed that the ecliptic 
        latitude (beta) is zero"""
        
        ecliptic_lon = true_anomaly + omega_g
        
        if ecliptic_lon > 360:
            ecliptic_lon = ecliptic_lon - 360
        
        # 2451545.0 is the julian day for epoch Jan 1.5 2000
        # 23.43929166 is the obliquity of the ecliptic at J2000 standard epoch
        
        # julianday is calculated for epoch Jan 0.0 2010
        julianday = self.__julianday(2010, 1, 0)
        T = (julianday - 2451545.0)/36525.0 # T are julian centuries
        mean_obliquity = 23.43929166 - (46.815 + (0.0006 - 0.00181*T)*T)*T/3600       
        
        sin_l = math.sin(math.radians(ecliptic_lon))
        cos_l = math.cos(math.radians(ecliptic_lon))
        sin_e = math.sin(math.radians(mean_obliquity))
        cos_e = math.cos(math.radians(mean_obliquity))       
        
        y = sin_l*cos_e
        x = cos_l
        a = math.atan(y/x)

        if x > 0 and y > 0:
            a = math.atan(y/x)
        elif x < 0 and y > 0:
            a = math.atan(y/x) + math.pi
        elif x > 0 and y < 0:
            a = math.atan(y/x) + 2*math.pi
        elif x < 0 and y < 0:
            a = math.atan(y/x) + math.pi
        else:
            logging.error("__equatorial_coords -> x and y are not defined")
            
        right_asc = math.degrees(a)
        declination = math.degrees(math.asin(sin_e*sin_l))
        
        return right_asc, declination

    def __horizon_coords(self, declination, right_asc, latitude, longitude,
                         year, month, day):
        """Calculates the azimuth (A) and altitude (h)"""
        
        GST = self.__UT2GST(year, month, day)
        LST = self.__GST2LST(GST, longitude)
        
        H = LST - right_asc/15.0
        if H < 0:
            H = H + 24
            
        sin_d = math.sin(math.radians(declination))
        cos_d = math.cos(math.radians(declination))
        sin_lat = math.sin(math.radians(latitude))
        cos_lat = math.cos(math.radians(latitude))
        cos_H = math.cos(math.radians(H*15))        
        sin_H = math.sin(math.radians(H*15))
        sin_altitude = sin_d*sin_lat + cos_d*cos_lat*cos_H
        altitude = math.asin(sin_altitude)
        cos_altitude = math.cos(altitude)
        cos_A = (sin_d - sin_lat*sin_altitude)/(cos_lat*cos_altitude)
        azimuth = math.degrees(math.acos(cos_A))
        
        if sin_H > 0:
            azimuth = 360 - azimuth
        
        return math.degrees(altitude), azimuth
    
    def __LCT2UT(self, dt_obj, isDST, longitude):
        """Converts local civilian time (LCT) to universal time (UT)"""
        
        year = dt_obj.year
        month = dt_obj.month
        day = dt_obj.day
        hour = dt_obj.hour
        minute = dt_obj.minute
        second = dt_obj.second   
            
        LCT = hour + minute/60.0 + second/3600.0
        
        if isDST:
            LCT = LCT - 1
        
        UT = LCT - round(longitude/15.0)
        g_day = day + UT/24.0
        julianday = self.__julianday(year, month, g_day)        
        year_, month_, day_ = self.__julianday2GCD(julianday)
        
        #decimalhour, hour = math.modf(UT)        
        #minute = decimalhour*60
        #frac, _ = math.modf(minute)
        #second = frac*60

        return year_, month_, day_

    
    def __UT2GST(self, year, month, day):
        """Converts universal time (UT) to Greenwich standard time (GST)"""
        
        day_ = int(day)
        julianday = self.__julianday(year, month, day_)
        julianday_0 = self.__julianday((year-1), 12, 31)
        elaps_days = julianday - julianday_0
        
        # 2415020.0 is the julian day for epoch Jan 0.5 1900
        T = (julianday_0 - 2415020.0)/36525.0
        R = 6.6460656 + 2400.051262*T + 0.00002581*T**2
        B = 24 - R + 24*(year - 1900)
        T_0 = 0.0657098*elaps_days - B
        UT = (day - int(day))*24
        GST = T_0 + 1.002738*UT
        
        if GST < 0:
            GST = GST + 24
        elif GST > 24:
            GST = GST - 24
        
        return GST
    
    def __GST2LST(self, GST, longitude):
        """Converts Greenwich Standard Time (GST) to Local Sidereal Time (LST)"""
        
        LST = GST + longitude/15.0
        
        if LST < 0:
            LST = LST + 24
        elif LST > 24:
            LST = LST - 24
        
        return LST
    
    def __julianday2GCD(self, juliandate):
        """Converts julianday to Greenwich Calendar Date"""
        
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

#test = SunPosition(51.05011, -114.08529, "1988-07-27T00:00:00")
test = SunPosition(38, -78, "2015-02-05T12:00:00", False)
#test = SunPosition(51.1, -114.067, "2023-07-27T16:20:00")
#test = SunPosition(51.1, -60, "2013-07-01T03:37:00", True)
#test = SunPosition(51.1, 0, "2010-02-07T23:30:00", False)
test.sun_position()
