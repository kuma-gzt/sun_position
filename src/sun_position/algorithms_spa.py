"""This module contains all the algorithms and formulas necesary for the 
calculation of the sun-path charts"""
from datetime import datetime, timedelta
import math
from math import degrees as deg
from math import radians as rad
import calendar
import tables as tb


class SunPosition:
    """Formulas and algorithms to calculate the sun position"""
    def __init__(self, lat, lon, date_time, is_daylight, obs_elev, press,
                 temp):
        self.lat = lat
        self.lon = lon
        self.date_time = date_time  # local date and time
        self.is_daylight = is_daylight  # boolean, is Daylight Saving Time
        self.obs_elev = obs_elev  # observer's elevation in meters
        self.press = press  # atmospheric pressure in mbar
        self.temp = temp  # temperature in Celcius degrees

    def sun_position(self):

        tmp = datetime.fromisoformat(self.date_time)
        year = tmp.year
        month = tmp.month
        day = tmp.day

        jdates = self.__juliandates(year, month, day)
        jd = jdates['julianday']
        jdE = jdates['julian_ephemeris_day']
        jc = jdates['juliancentury']
        jce = jdates['julian_ephemeris_century']
        jme = jdates['julian_ephemeris_millenium']
        print('jd: ' + str(jd) + ' jdE: ' + str(jdE) + ' jc: ' + str(jc) + ' jce: ' + str(jce) + ' jme: ' + str(jme))

        hc = self.__heliocentric_params(jme)
        L = hc['heliocentric_lon']
        B = hc['heliocentric_lat']
        R = hc['earth_radius']
        print('L: ' + str(L) + ' B: ' + str(B) + ' R: ' + str(R))

        glatlon = self.__geocentric_latlon(B, L)
        geocentric_lat = glatlon['geocentric_lat']
        geocentric_lon = glatlon['geocentric_lon']
        print('geocentric_lat: ' + str(geocentric_lat) + ' geocentric_lon: ' + str(geocentric_lon))

        nto = self.__nutations(jce)
        nutation_longitude = nto['nutation_longitude']
        nutation_obliquity = nto['nutation_obliquity']
        print('nutation_longitude: ' + str(nutation_longitude) + ' nutation_obliquity: ' + str(nutation_obliquity))

        true_obliquity = self.__true_obliq_ecliptic(jme, nutation_obliquity)
        print('true_obliquity: ' + str(true_obliquity))

        app_sun_longitude = self.__apparent_app_sun_lon(geocentric_lon, nutation_longitude, R)
        print('app_sun_longitude: ' + str(app_sun_longitude))

        sidereal_time = self.__apparent_sidereal_time(jd, jc, nutation_longitude,
                                             true_obliquity)
        print('sidereal_time: ' + str(sidereal_time))

        geocentric_right_asc = self.__geocentric_right_asc(app_sun_longitude, true_obliquity,
                                                 geocentric_lat)
        print('geocentric_right_asc: ' + str(geocentric_right_asc))

        declination = self.__geocentric_declination(geocentric_lat, true_obliquity,
                                         app_sun_longitude)
        print('declination: ' + str(declination))

        local_hour_angle = self.__local_hour_angle(sidereal_time, self.lon,
                                                   geocentric_right_asc)
        print('local_hour_angle: ' + str(local_hour_angle))

        ta = self.__topocentric_angles(R, self.lat, self.obs_elev,
                                       local_hour_angle, declination,
                                       geocentric_right_asc)

        topo_right_asc = ta['topo_right_asc']
        topo_declination = ta['topo_declination']
        topo_localhour_ang = ta['topo_localhour_ang']
        print('topo_right_asc: ' + str(topo_right_asc))
        print('topo_declination: ' + str(topo_declination))
        print('topo_localhourang: ' + str(topo_localhour_ang))

        el_az = self.__elevation_azimuth(self.lat, topo_declination,
                                         topo_localhour_ang, self.press,
                                         self.temp)
        topo_elev_ang = el_az['topo_elev_ang']
        topo_azim_ang = el_az['topo_azim_ang']

        print('topo_elevation_angle: ' + str(topo_elev_ang))
        print('topo_azimuth_angle: ' + str(topo_azim_ang))

    def __juliandates(self, year, month, day):
        """
        Gets the Julian day (jd), Julian Century (jc),
        Julian Ephemeris Day (jdE), Julian Ephemeris Century (jce) and
        Julian Ephemeris Millenium (jme)
        :param year: year - universal time
        :param month: month - universal time
        :param day: day - universal time
        :returns: a dictionary holding all the Julian dates
        """
        # delta_t is diff between earth rotation time and terrestrial time
        delta_t = self.__delta_t(year, month)

        if month < 3:
            year = year - 1
            month = month + 12

        # a and b are intermediate calculation variables
        a = int(year/100)
        b = 2 - a + int(a/4)

        julianday = (int(365.25*(year + 4716)) + int(30.6001*(month + 1)) +
                     day + b - 1524.5)

        julian_ephday = julianday + delta_t/86400  # julian ephemeris day
        juliancentury = (julianday - 2451545)/36525
        julian_ephcentury = (julian_ephday - 2451545)/36525
        julian_ephmillenium = julian_ephcentury/10

        return {'julianday': julianday,
                'julian_ephemeris_day': julian_ephday,
                'juliancentury': juliancentury,
                'julian_ephemeris_century': julian_ephcentury,
                'julian_ephemeris_millenium': julian_ephmillenium}

    def __heliocentric_params(self, jme):
        """
        Gets the earth's heliocentric longitude, latitude and radius vector
        :param jme: julian_ephemeris_millenium
        :returns: a dictionary holding the heliocentric parameters
        """
        # earth heliocentric longitude
        l0 = self.__calc_l0(tb.l0_A, tb.l0_B, tb.l0_C, jme)
        l1 = self.__calc_l0(tb.l1_A, tb.l1_B, tb.l1_C, jme)
        l2 = self.__calc_l0(tb.l2_A, tb.l2_B, tb.l2_C, jme)
        l3 = self.__calc_l0(tb.l3_A, tb.l3_B, tb.l3_C, jme)
        l4 = self.__calc_l0(tb.l4_A, tb.l4_B, tb.l4_C, jme)
        l5 = self.__calc_l0(tb.l5_A, tb.l5_B, tb.l5_C, jme)

        l_rad = (l0 + l1*jme + l2*pow(jme, 2) + l3*pow(jme, 3) +
                 l4*pow(jme, 4) + l5*pow(jme, 5))/pow(10, 8)

        helio_lon = self.__limit_360(deg(l_rad))

        # earth heliocentric latitude
        b0 = self.__calc_l0(tb.b0_A, tb.b0_B, tb.b0_C, jme)
        b1 = self.__calc_l0(tb.b1_A, tb.b1_B, tb.b1_C, jme)

        b_rad = (b0 + b1*jme)/pow(10, 8)
        helio_lat = deg(b_rad)

        # earth radius vector
        r0 = self.__calc_l0(tb.r0_A, tb.r0_B, tb.r0_C, jme)
        r1 = self.__calc_l0(tb.r1_A, tb.r1_B, tb.r1_C, jme)
        r2 = self.__calc_l0(tb.r2_A, tb.r2_B, tb.r2_C, jme)
        r3 = self.__calc_l0(tb.r3_A, tb.r3_B, tb.r3_C, jme)
        r4 = self.__calc_l0(tb.r4_A, tb.r4_B, tb.r4_C, jme)

        earth_radius = (r0 + r1*jme + r2*pow(jme, 2) + r3*pow(jme, 3) +
                        r4*pow(jme, 4))/pow(10, 8)

        return {'heliocentric_lon': helio_lon,
                'heliocentric_lat': helio_lat,
                'earth_radius': earth_radius}

    def __geocentric_latlon(self, helio_lat, helio_lon):
        """
        Calculates geocentric latitude and longitude,
        :param helio_lat: heliocentric latitude
        :param helio_lon: heliocentric longitude
        :returns: a dictionary holding the geocentric latitude and longitude
        """
        geo_lat = -helio_lat
        geo_lon = self.__limit_360(helio_lon + 180)

        return {'geocentric_lon': geo_lon,
                'geocentric_lat': geo_lat}

    def __nutations(self, jce):
        """
        Calculates the nutation in longitude and obliquity
        :param jce: Julian Ephemeris Century
        :returns: a dictionary holding the nutation in longitude and obliquity
        """
        x0 = (297.85036 + 445267.111480*jce - 0.0019142*pow(jce, 2) +
              pow(jce, 3)/189474)
        x1 = (357.52772 + 35999.050340*jce - 0.0001603*pow(jce, 2) -
              pow(jce, 3)/300000)
        x2 = (134.96298 + 477198.867398*jce + 0.0086972*pow(jce, 2) +
              pow(jce, 3)/56250)
        x3 = (93.27191 + 483202.017538*jce - 0.0036825*pow(jce, 2) +
              pow(jce, 3)/327270)
        x4 = (125.04452 - 1934.136261*jce + 0.0020708*pow(jce, 2) +
              pow(jce, 3)/450000)

        table2 = zip(tb.y0, tb.y1, tb.y2, tb.y3, tb.y4, tb.a, tb.b, tb.c, tb.d)
        tmp_20 = 0  # formula #20
        tmp_21 = 0  # formula #21

        for i in table2:
            xy = x0*i[0] + x1*i[1] + x2*i[2] + x3*i[3] + x4*i[4]
            tmp_20 = tmp_20 + (i[5] + i[6]*jce)*math.sin(xy)
            tmp_21 = tmp_21 + (i[7] + i[8]*jce)*math.cos(xy)

        nut_lon = tmp_20/36000000
        nut_obl = tmp_21/36000000

        return {'nutation_longitude': nut_lon,
                'nutation_obliquity': nut_obl}

    def __true_obliq_ecliptic(self, jme, nut_obl):
        """
        Calculates the true obliquity of the ecliptic
        :param jme: Julian Ephemeris Millenium
        :param nut_obl: nutation in longitude
        :returns: the true obliquity of the ecliptic in degrees
        """
        u = jme/10
        e0 = (84381.448 - 4680.93*u - 1.55*pow(u, 2) + 1999.25*pow(u, 3) -
              51.38*pow(u, 4) - 249.67*pow(u, 5) - 39.05*pow(u, 6) +
              7.12*pow(u, 7) + 27.87*pow(u, 8) + 5.79*pow(u, 9) +
              2.45*pow(u, 10))

        return e0/3600 + nut_obl

    def __apparent_app_sun_lon(self, geo_lon, nut_lon, earth_radius):
        """
        Calculates the apparent sun longitude
        :param geo_lon: geocentric longitude
        :param nut_lon: nutation in longitude
        :param earth_radius: earth_radius
        :returns: apparent sun longitude in degrees
        """
        return geo_lon + nut_lon - 20.4898/(3600*earth_radius)

    def __apparent_sidereal_time(self, jd, jc, nut_lon, true_obliq_eclip):
        """
        Calculates the apparent sidereal time at Greenwich
        :param jd: julian day
        :param jc: julian century
        :param nut_lon: nutation in longitude
        :param true_obliq_eclip: true obliquity of the ecliptic
        :returns: apparent sidereal time in degrees
        """
        v0_ = (280.46061837 + 360.98564736629*(jd - 2451545) +
               0.000387933*pow(jc, 2) - pow(jc, 3)/38710000)
        v0 = self.__limit_360(v0_)  # v0 is the mean sidereal time at Greenwich

        return v0 + nut_lon*math.cos(rad(true_obliq_eclip))

    def __geocentric_right_asc(self, app_sun_lon, true_obliq_eclip, geo_lat):
        """
        Calculates the geocentric sun right ascension
        :param app_sun_lon: apparent sun longitude
        :param true_obliq_eclip: true obliquity of the ecliptic
        :param geo_lat: geocentric latitude
        :returns: sun right ascension in degrees
        """
        app_sun_lon = rad(app_sun_lon)
        true_obliq_eclip = rad(true_obliq_eclip)
        geo_lat = rad(geo_lat)

        a = math.sin(app_sun_lon)*math.cos(true_obliq_eclip)
        b = math.tan(geo_lat)*math.sin(true_obliq_eclip)
        y = a - b
        x = math.cos(app_sun_lon)
        tmp = deg(math.atan2(y, x))

        return self.__limit_360(tmp)

    def __geocentric_declination(self, geo_lat, true_obliq_eclip, app_sun_lon):
        """
        Calculates the geocentric sun declination
        :param geo_lat: geocentric latitude
        :param true_obliq_eclip: true obliquity of the ecliptic
        :param app_sun_lon: apparent sun longitude
        :returns: sun declination in degrees
        """
        geo_lat = rad(geo_lat)
        true_obliq_eclip = rad(true_obliq_eclip)
        app_sun_lon = rad(app_sun_lon)

        a = math.sin(geo_lat)*math.cos(true_obliq_eclip)
        b = math.cos(geo_lat)*math.sin(true_obliq_eclip)*math.sin(app_sun_lon)

        return deg(math.asin(a + b))

    def __local_hour_angle(self, sidereal_time, lon, geocentric_right_asc):
        """
        Calculates the observer local hour angle H
        :param sidereal_time: aparent sidereal time at Greewich
        :param lon: observer's longitude
        :param geocentric_right_asc: sun's geocentric right ascension
        :returns: local hour angle (H) in degrees
        """
        tmp = sidereal_time + lon - geocentric_right_asc

        return self.__limit_360(tmp)

    def __topocentric_angles(self, earth_radius, lat, obs_elev,
                             local_hour_angle, geocentric_declination,
                             geocentric_right_asc):
        """
        Calculates the topocentric sun right ascension,
        the topocentric sun declination, topocentric local hour angle,
        the topocentric zenith angle
        :param earth_radius: earth radius R
        :param lat: observer's latitude
        :param obs_elev: observer's elevation in meters
        :param local_hour_angle: observer's local hour angle
        :param geocentric_declination: geocentric sun declination
        :param geocentric_right_asc: geocentric sun's right ascension
        :returns: a dictionary holding the topocentric sun right ascension,
        the topocentric sun declination and topocentric local hour angle,
        all in degrees
        """
        lat = rad(lat)

        eq_hz_parall = rad(8.794/(3600*earth_radius))  # equatorial hz parallax
        u = math.atan(0.99664719*math.tan(lat))
        x = math.cos(u) + obs_elev/6378140*math.cos(lat)
        y = (0.99664719*math.sin(u) +
             obs_elev/6378140*math.sin(lat))

        # topocentric sun right ascension
        a = -x*math.sin(eq_hz_parall)*math.sin(rad(local_hour_angle))
        b = (math.cos(rad(geocentric_declination)) -
             x*math.sin(eq_hz_parall)*math.cos(rad(local_hour_angle)))
        parall_right_asc = deg(math.atan2(a, b))
        topo_right_asc = geocentric_right_asc + parall_right_asc

        # topocentric sun declination
        a1 = ((math.sin(rad(geocentric_declination)) -
              y*math.sin(eq_hz_parall))*math.cos(rad(parall_right_asc)))
        b1 = (math.cos(rad(geocentric_declination)) -
              y*math.sin(eq_hz_parall)*math.cos(rad(local_hour_angle)))
        topo_declination = deg(math.atan2(a1, b1))

        # topocentric local hour angle (H')
        topo_localhour_ang = local_hour_angle - parall_right_asc

        return {'topo_right_asc': topo_right_asc,
                'topo_declination': topo_declination,
                'topo_localhour_ang': topo_localhour_ang}

    def __elevation_azimuth(self, lat, topo_declination, topo_localhour_ang,
                            press, temp):
        """
        Calculates the topocentric elevation and azimuth angles
        :param earth_radius: earth radius R
        :param lat: observer's latitude
        :param topo_declination: topocentric sun declination
        :param topo_localhour_ang: topocentric local hour angle
        :param press: annual average local pressure in mbars
        :param temp: annual average local temeperature in Celcius degrees
        :returns: the topocentric sun right ascension
        """
        lat = rad(lat)
        topo_localhour_ang = rad(topo_localhour_ang)
        topo_declination = rad(topo_declination)

        # topocentric elevation angle
        a2 = math.sin(lat)*math.sin(topo_declination)
        b2 = math.cos(lat)*math.cos(topo_declination)*math.cos(topo_localhour_ang)
        e0 = deg(math.asin(a2 + b2))

        c2 = rad(e0 + 10.3/(e0 + 5.11))
        atm_corr = (press/1010)*(283/(273 + temp))*(1.02/(60*math.tan(c2)))
        topo_elev_ang = e0 + atm_corr  # topocentric elevation angle
        topo_zenith_ang = 90 - topo_elev_ang  # topocentric zenith angle

        # topocentric azimuth angle
        a3 = math.sin(topo_localhour_ang)
        b3 = (math.cos(topo_localhour_ang)*math.sin(lat) -
              math.tan(topo_declination)*math.cos(lat))
        c3 = deg(math.atan2(a3, b3))
        d3 = self.__limit_360(c3) + 180
        topo_azim_ang = self.__limit_360(d3)

        return {'topo_elev_ang': topo_elev_ang,
                'topo_azim_ang': topo_azim_ang}

    def __calc_l0(self, a, b, c, jme):
        """
        Calculates the formula # 10 in the paper
        :param a: A
        :param b: B
        :param c: C
        :param jme: julian_ephemeris_millenium
        :returns: term L0 (formula # 10)
        """

        if isinstance(a, tuple):
            tmp = zip(a, b, c)
            tmp_ = 0
            for i in tmp:
                tmp_ = tmp_ + i[0] * math.cos(i[1] + i[2]*jme)
        else:
            tmp_ = a * math.cos(b + c*jme)

        return tmp_

    def __limit_360(self, angle):
        """
        Gets a new angle in the range 0 to 360 degrees
        :param angle: angle to be re-calculated in degrees
        :returns: a new angle in the range 0 to 360
        """
        frac, _ = math.modf(angle/360)

        if angle > 0:
            out = 360 * frac
        else:
            out = 360 - 360 * frac

        return out

    def __delta_t(self, year, month):
        """
        Calculates the delta T value. Formulas taken from:
        POLYNOMIAL EXPRESSIONS FOR DELTA T (ΔT)
        https://eclipse.gsfc.nasa.gov/SEcat5/deltatpoly.html
        Note that only the formulas for year > 1600 are implemented.
        :param year: year
        :param month: month
        :returns: delta T in seconds
        """
        y = year + (month - 0.5/12)

        if year >= 1600 and year < 1700:
            t = y - 1600
            dt = 120 - 0.9808*t - 0.01532*pow(t, 2) + pow(t, 3)/7129
        elif year >= 1700 and year < 1800:
            t = y - 1700
            dt = (8.83 + 0.1603*t - 0.0059285*pow(t, 2) +
                  0.00013336*pow(t, 3) - pow(t, 4)/1174000)
        elif year >= 1800 and year < 1860:
            t = y - 1800
            dt = (13.72 - 0.332447*t + 0.0068612*pow(t, 2) +
                  0.0041116*pow(t, 3) - 0.00037436 * pow(t, 4) +
                  0.0000121272*pow(t, 5) - 0.0000001699*pow(t, 6) +
                  0.000000000875*pow(t, 7))
        elif year >= 1860 and year < 1900:
            t = y - 1860
            dt = (7.62 + 0.5737*t - 0.251754*pow(t, 2) + 0.01680668*pow(t, 3) -
                  0.0004473624*pow(t, 4) + pow(t, 5)/233174)
        elif year >= 1900 and year < 1920:
            t = y - 1900
            dt = (-2.79 + 1.494119*t - 0.0598939*pow(t, 2) +
                  0.0061966*pow(t, 3) - 0.000197*pow(t, 4))
        elif year >= 1920 and year < 1941:
            t = y - 1920
            dt = (21.20 + 0.84493*t - 0.076100*pow(t, 2) + 0.0020936*pow(t, 3))
        elif year >= 1941 and year < 1961:
            t = y - 1950
            dt = 29.07 + 0.407*t - pow(t, 2)/233 + pow(t, 3)/2547
        elif year >= 1961 and year < 1986:
            t = y - 1975
            dt = 45.45 + 1.067*t - pow(t, 2)/260 - pow(t, 3)/718
        elif year >= 1986 and year < 2005:
            t = y - 2000
            dt = (63.86 + 0.3345*t - 0.060374*pow(t, 2) + 0.0017275*pow(t, 3) +
                  0.000651814*pow(t, 4) + 0.00002373599*pow(t, 5))
        elif year >= 2005 and year < 2050:
            t = y - 2000
            dt = 62.92 + 0.32217*t + 0.005589*pow(t, 2)
        else:
            print('Error: year not in the range 1600 to 2050')

        return dt

if __name__ == '__main__':
    app = SunPosition(40.76, -73.984, '2003-07-27T00:00:00', True, 27, 0, 0)
    app.sun_position()