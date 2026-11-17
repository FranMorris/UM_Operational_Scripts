#!/usr/bin/env python

import time
from datetime import date
from datetime import timedelta

import os

import cdsapi

c = cdsapi.Client()
output_fpath = '/work/n02/n02/franmorr/data_files/ec_grib_files/2022_v2'

# Set dates for data extraction
idate = date(2022,9,27)
edate = date(2022,10,30)

# Set hours for each date to extract
hours = ['00', '03', '06', '09', '12', '15', '18', '21']
area_limits = ['30', '-5', '-50', '65'] #lat_max lon_min lat_min lon_max

while (idate <= edate):

    iyear = idate.year
    imonth = idate.month
    iday = idate.day

    stryear  = "%04d" % (iyear)
    strmonth = "%02d" % (imonth)
    strday   = "%02d" % (iday)
    strdate = "%d%02d%02d" % (iyear, imonth, iday)
    print(strdate)

    for hour in hours:
        # extract 3D data
        c.retrieve(
            "reanalysis-era5-pressure-levels",
            {
                'product_type': 'reanalysis',
                'format': 'grib',
                'year': stryear,
                'month': strmonth,
                'day': strday,
                'variable': [
                    'specific_humidity', 'temperature', 'u_component_of_wind',
                    'v_component_of_wind'
                ],
                'pressure_level': [
                    '1', '2', '3',
                    '5', '7', '10',
                    '20', '30', '50',
                    '70', '100', '125',
                    '150', '175', '200',
                    '225', '250', '300',
                    '350', '400', '450',
                    '500', '550', '600',
                    '650', '700', '750',
                    '775', '800', '825',
                    '850', '875', '900',
                    '925', '950', '975',
                    '1000',
                ],
                'time': [str(hour).zfill(2)+':00'],
                'area': area_limits,
                'download_format': 'unarchived'
            },
            "preslev.grib")

        # extract surface data
        c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'format': 'grib',
                'year': stryear,
                'month': strmonth,
                'day': strday,
                'variable': [
                    'geopotential', 'land_sea_mask', 'skin_temperature',
                    'surface_pressure', 'sea_surface_temperature', 'sea_ice_cover'
                ],
                'time': [str(hour).zfill(2) + ':00'],
                'area': area_limits,
                'download_format': 'unarchived'
            },
            "surface.grib")

        # combine and rename data files
        os.system('cat preslev.grib surface.grib > ' + output_fpath + '/ec_grib_' + strdate + str(hour).zfill(2) + '00.t+000')
        os.system('rm surface.grib preslev.grib')
 
    # move to next day
    idate = idate + timedelta(days=1) 

print("End.")

