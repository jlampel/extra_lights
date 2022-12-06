'''
Copyright (C) 2020-2023 Orange Turbine
https://orangeturbine.com
orangeturbine@cgcookie.com

This file is part of Extra Lights, created by Jonathan Lampel. 

All code distributed with this add-on is open source as described below. 

Extra Lights is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses/>.
'''


import bpy
from . import light_classes
PointLight = light_classes.PointLight
SunLight = light_classes.SunLight
SpotLight = light_classes.SpotLight
AreaLight = light_classes.AreaLight
IesLight = light_classes.IesLight

lights = {
    'natural' : [
        PointLight(
            name = 'Candle',
            tag = 'candle',
            radius = 0.015,
            temp = 1800,
            lumens = 12,
            exposure = 6,
        ),
        SunLight(
            name = 'Moonlight',
            tag = 'moonlight',
            angle = 0.75, 
            temp = 4500, 
            irradiance = 0.001, 
            exposure = 12,
            rotation = [0.785398, 0.785398, 0],
            skyStrength = 0.0001,
            skyTurbidity = 5,
        ),
        SunLight(
            name = 'Direct Sun',
            tag = 'directsun',
            angle = 0.526, 
            temp = 5200, 
            irradiance = 1000, 
            exposure = -6.25,
            rotation = [0.785398, 0.785398, 0],
            skyStrength = 200,
            skyTurbidity = 2,
        )
    ],
    'incandescent' : [
        PointLight(
            name = '70 lm C7 Appliance Light',
            tag = '70c7',
            radius = 0.015,
            temp = 2700,
            lumens = 70, 
            exposure = 8,
        ),
        PointLight(
            name = '250 lm Vintage Decorative Light',
            tag = '250vintage',
            radius = 0.025,
            temp = 2700,
            lumens = 250, 
            exposure = 6,
        ),
        IesLight(
            name = '750 lm A19 Wall Lamp IES',
            tag = '750a19wallies',
            spotAngle = 0,
            radius = 0.03,
            temp = 2700,
            strength = 0.4,
            lumens = 750,
            exposure = 5.1,
        ),
        PointLight(
            name = '1,000 lm A19 Lamp Light',
            tag = "1000a19",
            radius = 0.03, 
            temp = 2700, 
            lumens = 1000, 
            exposure = 4.25,
        ),
        AreaLight(
            name = '3,800 lm A21 Ceiling Light',
            tag = "3800a21",
            shape = 'DISK',
            size = [0.033, 0.033],
            temp = 2700, 
            lumens = 3800, 
            exposure = 3.6,
        ),
        AreaLight(
            name = '5,800 lm PS30 Barn Light',
            tag = "5800ps30",
            shape = 'DISK',
            size = [0.038, 0.038],
            temp = 2700, 
            lumens = 5800, 
            exposure = 3.25,
        ),
    ], 
    'led' : [
        SpotLight(
            name = '400 lm Flashlight',
            tag = '400flashlight',
            radius = 0.0075,
            angle = 65,
            temp = 2700,
            lumens = 400,
            exposure = 5.25,
        ),
        PointLight(
            name = '800 lm A19 Lamp LED',
            tag = "800a19",
            radius = 0.034, 
            temp = 3000, 
            lumens = 800, 
            exposure = 4.75,
        ),
        AreaLight(
            name = '1,500 lm PAR38 Floodlight',
            tag = "1500par38",
            shape = 'DISK',
            size = [0.034, 0.034],
            temp = 3000, 
            lumens = 1500, 
            exposure = 1.25,
        ),
        IesLight(
            name = '3,500 lm DD42 Outdoor Lamp IES',
            tag = '3500dd42ies',
            spotAngle = 0,
            radius = 0.05,
            temp = 5000,
            strength = 0.035,
            lumens = 3500,
            exposure = 3.5,
        ),
        SpotLight(
            name = '5,000 lm LED Car Headlight',
            tag = 'headlightled',
            radius = 0.02,
            angle = 125,
            temp = 6500,
            lumens = 5000,
            exposure = 1.5,
        ),
        AreaLight(
            name = '9,100 lm Industrial LED Wall Pack',
            tag = "9100flood",
            shape = 'RECTANGLE',
            size = [0.23, 0.178],
            temp = 5000, 
            lumens = 9100, 
            exposure = -0.5,
        ),
    ],
    'fluorescent' : [
        AreaLight(
            name = '1,500 lm Photography Umbrella',
            tag = "1500ubmrella",
            shape = 'DISK',
            size = [0.838, 0.838],
            temp = 5000, 
            lumens = 1500, 
            exposure = -0.5,
        ),
        AreaLight(
            name = '2,500 lm Fluorescent Tube',
            tag = "2500tube",
            shape = 'RECTANGLE',
            size = [0.05, 1.22],
            temp = 5000, 
            lumens = 2500, 
            exposure = 1,
        ),
        PointLight(
            name = '4,500 lm Daylight CFL',
            tag = "4500cfl",
            radius = 0.03, 
            temp = 6500, 
            lumens = 4500, 
            exposure = 1.5,
        ),
        IesLight(
            name = '12,900 lm ICE Commercial IES',
            tag = '12900iceies',
            spotAngle = 0,
            radius = 0.15,
            temp = 5000,
            strength = 0.015,
            lumens = 12900,
            exposure = 0.75,
        ),
        IesLight(
            name = '20,500 lm ED28 Crisp IES',
            tag = '20500ed28ies',
            spotAngle = 0,
            radius = 0.1,
            temp = 4000,
            strength = 0.01,
            lumens = 20500,
            exposure = 0.5,
        ),
        IesLight(
            name = '240,000 lm Stage HID Spotlight IES',
            tag = '240kstagespot',
            spotAngle = 110,
            radius = 0.15,
            temp = 6000,
            strength = 0.1,
            lumens = 240000,
            exposure = -1,
        ),
    ],
}