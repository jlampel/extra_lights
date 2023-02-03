# About Extra Lights

Extra Lights is an add-on for Blender that adds physically based, photometric light presets to the 3D View Add menu. All lights have their strength and colors based on real world light fixtures and are organized by type and strength.

**[Watch the Extra Lights video tutorial](https://youtu.be/ipqyVWm5JmY)**

**[You can purchase Extra Lights, which comes with 60+ presets, from the Blender Market.](https://blendermarket.com/products/extra-lights)** It is installed the same as any other Blender add-on. 

## Blender's defaults are made to be mathematically convenient, not artistically intuitive.

The default cube is a whopping 6.5 feet tall (2 m), the camera is flying 16 feet (5 m) off the ground, and the default lamp is about 20 feet (5.8 m) from the nearest point on the cube. 

Why does this matter? Because the apparent scale of your scene and the strength of your lights are interconnected. 

Light follows the inverse square law when it’s being emitted in all directions, which states that the amount of light hitting a surface decreases in proportion with the square of its distance from the source. It's a very specific curve that our eyes are used to seeing. If we scale up a room five times, one way we can tell that it’s bigger is by observing the falloff of the light. 

You can imagine that if we’re just guessing about how bright to set the light, we can very easily make something look too large or too small totally by accident. It’s not something we’d notice right away but it can subconsciously tip us off to the fact that something is faked. 

If you use real world measurements for the scale of your models, then using real world measurements for your lights will give you more natural looking results. However, that's easier said than done. 

## Wrong watts, Watson!

Blender’s lights are calculated in watts. A bulb in my lamp at home says 45 watts, so if I set my Blender light to be 45 watts and the same size then it should match, right? Unfortunately, we’d be way off because there are two different measurements going on and both use watts as a unit. 

A lightbulb is listing the amount of electrical watts needed to power it on, while Blender is calculating how many watts are being emitted as light. Since an incandescent light bulb is not that efficient, only a fraction of the input watts are turning into visible light while the rest is turning into heat. 

To make things more confusing, other types of bulbs, like very efficient LEDs, sometimes show a watt equivalent, which is how much energy it would hypothetically use if it were an incandescent bulb of similar brightness, which is neither how much it is using nor how much it’s putting out. Good grief. 

## Lighting with lumens

What most lights are measured in, however, is lumens. Lumens measure how much light appears to the human eye as being emitted from the source. It's a believably consistent way of lighting that uses information we can easily find online. 

Here’s where things get a little weird. As mentioned, lumens are based on how bright something appears to the human eye to be. We can’t do a simple conversion because different RGB hues of the same value appear to us as different brightnesses. If you’ve ever run into the frustration of trying to make something really colorful but also really really bright, or even consistently bright between colors, I feel your pain. The problem isn’t with the computer or physics though, it’s with our eyeballs. 

We’re just better at detecting some wavelengths of light than others, so in order to convert lumens to watts in an RGB system we need to first get the spectral distribution of the light, separate the red, green, and blue, multiply by the luminous efficacy of each, multiply by the maximum possible efficacy, add them back together, and use that to divide the input number of lumens by in order to get the corrects watts output. 

That's a lot to worry about though, so this addon does it all for you! 

## Keeping it cool (or warm) with Kelvin

Creating believable lights isn't just about the strength - it's also about the color! 

To measure naturally produced light, we use a Kelvin value, which is what color a completely neutral substance (called a blackbody) is when heated to that Kelvin temperature. 

A candle starts at around 1800, incandescent bulbs are usually around 2700, fluorescent light is around 3-4000-ish, direct sun is around 5000 give or take, and a clear sky can be about 6500. By coloring your lights using Kelvin values, they’ll be a bit more believable, especially when you have more than one type of light in your scene that you’ll be comparing them with.

All of the lights in this addon have their color temperatures set in Kelvin based on their real world sources so that you don't have to remember all that. 

## 60+ physically based lights

The lights are organized into four categories - natural, incandescent, LED, and fluorescent. To keep things simple I've placed halogen lights under incandescent and metal halide & high intensity discharge lights under fluorescent. They're not technically the same, but for artistic uses they're close enough. 

Note - since EEVEE doesn't support nodes, IES lights will only show their texture in Cycles

## Simply better defaults, that's all

Although I'm basing these values off of the best information I can find from the real word, the end result is not going to be exactly perfect because I've had to make some assumptions. 

The lumen and Kelvin values listed by light manufacturers are enough to at least get us in the right ballpark, but we don’t have enough information about how they got those numbers in order to exactly match reality. So, I can call these lights physically based or photorealistic, because they are, but I’m not going to claim that they are physically accurate because that’s just not possible with the kind of data that’s readily available. We could actually get more accurate results by using radiant watts, but that's less easy for the user to look up and can be confusing as explained above. 

Secondly, do you have to use real world values to light your scene, even if they could be 100% accurate? NO! If computer graphics isn’t about bending the laws of physics to your whim to make s**t look cool, then I don’t know what is. Reality doesn’t always live up to our ridiculous expectations, which is why film studios and photographers use absurdly bright lights and more visual trickery than a stage magician. However, it’s better to start with something based in reality and break rules of thumb intentionally when you want to be creative, rather than by accident and the other way around. 

### Thanks for your support. Happy lighting!