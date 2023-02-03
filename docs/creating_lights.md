excerpt: Adding lights with Extra Lights.
nav_order: 0
nav_exclude: false
search_exclude: false
---

# Creating Lights with Extra Lights

All of Extra Light's presets can be found in the 3D View's Add menu. 

If you purchased the Blender Market version, you'll also have an asset browser ready file with each of the lights marked as assets. Using the asset version may be preferred in some situations, but you won't be able to adjust each light using Lumens after creation. 

When you add a light with Extra Lights, you'll have the option to adjust its parameters via Blender's redo panel (F9). 

## Lumens

This is how bright the light is as measured in Lumens. Blender's lights need to be set in Watts, and the add-on will do the conversion for you. 

## Set Color With

Here, you can choose to either set a Kelvin color temperature or a RGB color. Regardless of which one you choose, the light's strength in watts will be adjusted based on the color's luminous efficacy, so that the total number of lumens and its perceptual brightness will remain the same. 

## Use Nodes

Use Nodes is great to have enabled if you're using Cycles, because it adds a lumens conversion node to the light which allows you to change the lumens and color after creation. Since Eevee lights cannot use nodes, this option does not work in Eevee, and the only opportunity to change the brightness and color with lumens is during creation. 

## Set Exposure

Some lights may be far too dim or bright for Blender's default exposure. Checking Set Exposure will automatically adjust the scene's exposure to match the brightness of the newly added light. 

This will also adjust the Light Threshold, which is the minimum amount of light that is detected while rendering. If the Light threshold is not set while using a very dim light, even with the exposure set very high, the result will be unrealistically dim and/or extremely noisy. It is always recommended that you use this option when working with dim lights such as candles or moonlight. 

## Create Linked Sky

When adding a sun type light, you'll have an additional option to create a new world sky texture that's linked to the rotation of the new sun. 