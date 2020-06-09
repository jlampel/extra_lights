import bpy, os, glob, json
from pathlib import Path

def load():
    light_presets = {}
    path = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'presets' )
    files = [f for f in glob.glob(os.path.join(path, "*.py"))]
    for f in files:
        data = json.load( open(f) )
        light_presets[f] = data
    return light_presets

"""
Format: 
{
    'light_presets': {
        'Natural': {
            'Candle': {}, 
            'Moonlight': {}, 
            'Overcast Sun': {}, 
            'Direct Sun': {}, 
            'Partly Cloudy Sun': {}, 
            'Sunset Sun': {}, 
            'Fireplace': {}
        }, 
        'Interior': {
            '2,700 lm A21 Ceiling Light': {}, 
            '3,000 lm Halogen Car Headlight': {}, 
            'TV Screen': {}
        }
    }
}
"""