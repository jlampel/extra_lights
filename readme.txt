Extra Lights is a plugin for Blender that adds physically based, photometric lighting presets to the Add menu. 

The lights are organized into four categories - natural, incandescent, LED, and fluorescent. To keep things simple I've placed halogen lights under incandescent and metal halide & high intensity discharge lights under fluroescent. They're not technically the same, but for artistic uses they're close enough.

Any light ending in IES uses an IES texture to create a realistic pattern corresponding to the type of light that it is and what type of fixture it is commonly found in. IES textures only work in Cycles and not Eevee so Use Nodes is enabled for them by default. To use the light in Eevee without the texture just uncheck Use Nodes. 

To add your own lights, edit light_presets.py and follow the existing conventions for point, spot, sun, and IES lights. IES lights grab the text blocks from real_lights.blend that share the same name as the light.