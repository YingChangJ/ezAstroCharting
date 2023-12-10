# ezAstroCharting

Easy and quick astro charting with planets and cusps info.

Save an SVG image to the root folder and show it with plt.show.

## example

### using swisseph to get the planets and cusps info

```python
from drawCharts import Charting
import swisseph as swe

# calculate universal time
# swe.set_ephe_path() # set ephe path is very recommended

ut = swe.julday(2024,2,10,0)

# calculate degrees of planets

degrees = []
retro = []
planets = [i for i in range(11)]
for i in planets:
xx, \_ = swe.calc_ut(ut,i)
degrees.append(xx[0])
if xx[3]<0:
retro.append(i)

# calculate cusps

cusps, ascmc = swe.houses(ut,39,116)

Charting(style_index=1).natal(planets,degrees,cusps,ascmc[0],ascmc[1],retro,)
```

![saved svg](./example_pic/pic1.svg)

### what about whole house?

```python
cusps_w, ascmc_w = swe.houses(ut,39,116,b'W')
Charting().natal(planets,degrees,cusps_w,ascmc[0],ascmc[1],retro,)
```

![saved svg](./example_pic/pic2.svg)

## others

1. planets number follows the routine of [swiss ephemeris](https://www.astro.com/swisseph/swephprg.htm), except 11 is the south node.
2. fonts other than Astronomicon.ttf are also good to use. When using no font, Charting(usingFont = False), is a little ugly.
