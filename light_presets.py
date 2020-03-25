import bpy
from . import light_classes
PointLight = light_classes.PointLight
SunLight = light_classes.SunLight
SpotLight = light_classes.SpotLight
AreaLight = light_classes.AreaLight

lights = {
    'natural' : [
        PointLight(
            name = 'Candle',
            tag = 'candle',
            radius = 0.015,
            temp = 1800,
            lumens = 12,
            exposure = 4.6,
        ),
        PointLight(
            name = 'Fireplace',
            tag = 'fireplace',
            radius = 0.228,
            temp = 2000,
            lumens = 500, 
            exposure = 5.6,
        ),
        SunLight(
            name = 'Sunset',
            tag = 'sunset',
            angle = 0.75, 
            temp = 3000, 
            irradiance = 500, 
            exposure = -5.4,
            rotation = [1.4835, 0.785398, 0],
            skyStrength = 250,
            skyTurbidity = 3,
        ),
        SunLight(
            name = 'Overcast Sun',
            tag = 'overcastsun',
            angle = 50, 
            temp = 7000, 
            irradiance = 250, 
            exposure = -6.25,
            rotation = [0.785398, 0.785398, 0],
            skyStrength = 100,
            skyTurbidity = 8,
        ),
        SunLight(
            name = 'Partly Cloudy Sun',
            tag = 'cloudysun',
            angle = 5, 
            temp = 6000, 
            irradiance = 650, 
            exposure = -6.4,
            rotation = [0.785398, 0.785398, 0],
            skyStrength = 750,
            skyTurbidity = 2,
        ),
        SunLight(
            name = 'Direct Sun',
            tag = 'directsun',
            angle = 0.526, 
            temp = 5200, 
            irradiance = 1000, 
            exposure = -6.4,
            rotation = [0.785398, 0.785398, 0],
            skyStrength = 750,
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
            name = '200 lm A15 Appliance Light',
            tag = '200a15',
            radius = 0.0216,
            temp = 2700,
            lumens = 200, 
            exposure = 7,
        ),
        PointLight(
            name = '250 lm Vintage Decorative Light',
            tag = '250vintage',
            radius = 0.025,
            temp = 2700,
            lumens = 250, 
            exposure = 6,
        ),
        PointLight(
            name = '400 lm A15 Appliance Light',
            tag = "400a15",
            radius = 0.0216, 
            temp = 2700, 
            lumens = 400, 
            exposure = 5.5,
        ),
        PointLight(
            name = '1000 lm A19 Lamp Light',
            tag = "1000a19",
            radius = 0.03, 
            temp = 2700, 
            lumens = 1000, 
            exposure = 4.25,
        ),
        AreaLight(
            name = '2700 lm A21 Ceiling Light',
            tag = "2700a21",
            shape = 'DISK',
            size = [0.033, 0.033],
            temp = 2700, 
            lumens = 2700, 
            exposure = 3.4,
        ),
        SpotLight(
            name = '3000 lm Halogen Car Headlight',
            tag = '3000headlight',
            radius = 0.02,
            angle = 125,
            temp = 4100,
            lumens = 3000,
            exposure = 4.25,
        ),
        AreaLight(
            name = '3800 lm A21 Ceiling Light',
            tag = "3800a21",
            shape = 'DISK',
            size = [0.033, 0.033],
            temp = 2700, 
            lumens = 3800, 
            exposure = 3.6,
        ),
        AreaLight(
            name = '5800 lm PS30 Barn Light',
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
        SpotLight(
            name = '1400 lm Flashlight',
            tag = '1400flashlight',
            radius = 0.0075,
            angle = 65,
            temp = 4000,
            lumens = 1400,
            exposure = 2.5,
        ),
        AreaLight(
            name = '1500 lm PAR38 Floodlight',
            tag = "1500par38",
            shape = 'DISK',
            size = [0.034, 0.034],
            temp = 3000, 
            lumens = 1500, 
            exposure = 1.25,
        ),
        AreaLight(
            name = '1600 lm A21 Ceiling LED',
            tag = "1600a21",
            shape = 'DISK',
            size = [0.034, 0.034],
            temp = 5000, 
            lumens = 1600, 
            exposure = 1,
        ),
        AreaLight(
            name = '2500 lm Photography LED Bar',
            tag = "2500bar",
            shape = 'RECTANGLE',
            size = [0.23, 0.178],
            temp = 5600, 
            lumens = 3350, 
            exposure = 0,
        ),
        SpotLight(
            name = '5000 lm LED Car Headlight',
            tag = 'headlightled',
            radius = 0.02,
            angle = 125,
            temp = 6500,
            lumens = 5000,
            exposure = 1.5,
        ),
        AreaLight(
            name = '9100 lm Industrial LED Wall Pack',
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
            name = '1500 lm Photography Umbrella',
            tag = "1500ubmrella",
            shape = 'DISK',
            size = [0.838, 0.838],
            temp = 5000, 
            lumens = 1500, 
            exposure = -0.5,
        ),
        AreaLight(
            name = '2000 lm Photography Softbox',
            tag = "2000softbox",
            shape = 'SQUARE',
            size = [0.61, 0.61],
            temp = 5000, 
            lumens = 2000, 
            exposure = -0.5,
        ),
        PointLight(
            name = '2250 lm Photography CFL',
            tag = "2250cfl",
            radius = 0.03, 
            temp = 5500, 
            lumens = 2250, 
            exposure = 2,
        ),
        AreaLight(
            name = '2500 lm Fluorescent Tube',
            tag = "2500tube",
            shape = 'RECTANGLE',
            size = [0.05, 1.22],
            temp = 5000, 
            lumens = 2500, 
            exposure = 1,
        ),
        PointLight(
            name = '4500 lm Daylight CFL',
            tag = "4500cfl",
            radius = 0.03, 
            temp = 6500, 
            lumens = 4500, 
            exposure = 1.5,
        ),
    ],
}

"""
    nat_01 = Light("Candle", "candle", "POINT", 0.015, 1800, 12, 4.6)
    nat_02 = Light("Fireplace", "fireplace", "POINT", 0.228, 2000, 500, 5.6)
    nat_03 = Light("Sunset", "sunset", "SUN", 0.75, 3000, 500, -5.4)
    nat_04 = Light("Overcast Sun", "overcast", "SUN", 50, 7000, 250, -6.25)
    nat_05 = Light("Cloudy Sun", "cloudy", "SUN", 5, 6500, 650, -6.4)
    nat_06 = Light("Direct Sun", "directsun", "SUN", 0.526, 5250, 1000, -6.4)
    natural_lights = [nat_01, nat_02, nat_03, nat_04, nat_05, nat_06]

    inc_01 = Light("70 lm C7 Candelabra Appliance Light", "70c7", "POINT", 0.015, 2700, 70, 8)
    inc_02 = Light("200 lm A15 Appliance Light", "200a15", "POINT", 0.0216, 2700, 200, 7)
    inc_03 = Light("250 lm Vintage Tungsten Decorative Light", "vintage", "POINT", 0.025, 2700, 250, 6)
    inc_04 = Light("400 lm A15 Appliance Light", "400a15", "POINT", 0.0216, 2700, 400, 5.5)
    inc_05 = Light("1000 lm A19 Lamp Light", "1000a19", "POINT", 0.03, 2700, 1000, 4.25)
    inc_06 = Light("2700 lm A21 Ceiling Light", "2700a21", "AREA", ["DISK", 0.033], 2700, 2700, 3.4)
    inc_07 = Light("3000 lm Halogen Car Headlight", "3000headlight", "SPOT", [125, 0.02], 4100, 3000, 4.25)
    inc_08 = Light("3800 lm A21 Ceiling Light", "3800a21", "AREA", ["DISK", 0.033], 2700, 3800, 3.6)
    inc_09 = Light("5800 lm PS30 Barn Light", "5800ps30", "AREA", ["DISK", 0.038], 2700, 5800, 3.25)
    incandescent_lights = [inc_01, inc_02, inc_03, inc_04, inc_05, inc_06, inc_07, inc_08, inc_09]

    led_01 = Light("400 lm Flashlight", "400flashlight", "SPOT", [65, 0.0075], 2700, 400, 5.25)
    led_02 = Light("800 lm A19 Lamp LED", "800a19", "POINT", 0.034, 3000, 800, 4.75)
    led_03 = Light("1400 lm Flashlight", "1400flashlight", "SPOT", [65, 0.0075], 4000, 1400, 2.5)
    led_04 = Light("1500 lm PAR38 Outdoor Floodlight", "1400par38", "AREA", ["DISK", 0.06], 3000, 1500, 1.25)
    led_05 = Light("1600 lm A21 Ceiling LED", "1600a21", "AREA", ["DISK", 0.034], 5000, 1600, 1)
    led_06 = Light("2500 lm Photography LED Bar", "2500bar", "AREA", ["RECTANGLE", 0.03, 0.4], 5500, 2500, 0.5)
    led_07 = Light("2600 lm PAR38 Outdoor Floodlight", "2600par38", "AREA", ["DISK", 0.06], 3000, 2600, 0.5)
    led_08 = Light("3350 lm Photography LED Pack", "3350pack", "AREA", ["RECTANGLE", 0.23, 0.178], 5600, 3350, 0)
    led_09 = Light("5000 lm LED Car Headlight", "headlightled", "SPOT", [125, 0.02], 6500, 5000, 1.5)
    led_10 = Light("9100 lm Industrial LED Wall Pack", "9100flood", "AREA", ["RECTANGLE", 0.23, 0.178], 5000, 9100, -0.5)
    led_lights = [led_01, led_02, led_03, led_04, led_05, led_06, led_07, led_08, led_09, led_10] 

    fl_01 = Light("1500 lm Photography Umbrella", "1500ubmrella", "AREA", ["DISK", 0.838], 5000, 1500, -0.5)
    fl_02 = Light("2000 lm Photography Softbox", "2000softbox", "AREA", ["SQUARE", 0.61], 5000, 2000, -0.5)
    fl_03 = Light("2250 lm Photography CFL", "2250cfl", "POINT", 0.03, 5500, 2250, 2)
    fl_04 = Light("2500 lm Fluorescent Tube", "2500tube", "AREA", ["RECTANGLE", 0.05, 1.22], 5000, 2500, 1)
    fl_05 = Light("4500 lm Daylight CFL", "4500cfl", "POINT", 0.03, 6500, 4500, 1.5)
    fluorescent_lights = [fl_01, fl_02, fl_03, fl_04, fl_05]

    ies_01 = Light("100 lm LED Bollard", "100bollard", "IES", 0.005, 4000, [0.05, 100], 5.75)
    ies_02 = Light("4100 lm LED Floodlight", "4100flood", "IES", 0.025, 5000, [0.01, 4100], 4.15)
    ies_03 = Light("4100 lm Soft LED Floodlight", "4100softflood", "IES", 0.075, 4000, [0.01, 4100], 4.15)
    ies_04 = Light("5000 lm Halogen Mini Can", "5000minican", "IES", 0.025, 3000, [0.05, 5000], 4.15)
    ies_05 = Light("10000 lm Halogen Mini Can", "10000minican", "IES", 0.05, 3000, [0.05, 10000], 2.4)
    ies_06 = Light("1500 lm Sharp Downlight", "1500downlight", "IES", 0.005, 5000, [0.02, 1500], 4)
    ies_07 = Light("13500 lm Atrium Ceiling Light", "13500atrium", "IES", 0.025, 4500, [0.1, 13500], 3.5)
    ies_08 = Light("240000 lm Stage Htag Spotlight", "240000stagespot", "IES", 0.15, 6000, [0.1, 240000], -3.75)
    ies_09 = Light("2100 lm E27 Halogen Spotlight", "2100spot", "IES", 0.38, 4000, [0.1, 2100, ], 3)
    ies_10 = Light("850 lm Narrow Display Spotlight", "850narrowspot", "IES", 0.38, 5000, [0.03, 850], 3.2)
"""