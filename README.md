# Subnautica GPS System
[![Build Status](https://travis-ci.org/johndoe31415/subnautica-gps.svg?branch=master)](https://travis-ci.org/johndoe31415/subnautica-gps)

Subnautica is an *amazing* [game by Unknown Worlds
Entertainment](https://unknownworlds.com/subnautica/). It is incredible, picked
it up over the christmas holidays and was immediately addicted. It's an open
world exploration/survival game in which you can place "beacons" at certain
point in the map. From any given position of your character, you can get the
precise distance to all of your beacons.

However, you cannot easily trilaterate yourself and record that position
without placing another beacon. So, the engineer I am, I wanted to experiment
with this and implemented a kind of "GPS style" trilateration. This is what
this is: It uses a relatively simple giant step/baby step type algorithm for 3D
trilateration which should be numerically rather stable.

Anyways, have fun.

## How does it work?
You need to place three beacons at known locations. Your initial liferaft will
always be the center of the universe for trilateration, i.e., placed at (0, 0, 0).
I define "North" to be positive Y values and "East" to be positive X values.
Therefore, in my example, I swam 1km from the liferaft exactly to the north and
placed a "north" beacon there, then swam back and 1km to the west and places a
"west" beacon there. The definitions are changable in the JSON file.

The more beacons you have, the better the approximation. With the current
version, the raw data is saved, which means that if the algorithm improves
later on you can simply recalculate positions.

## How do I run it?
Pretty easy. Want to know where you are?

```
$ ./sngps where
Depth: 595
Distance to Liferaft: 1397
Distance to NAV N 1k: 1050
Distance to NAV W 1k: 1103
Distance to NAV S 1k:
Position: -864 / 920 depth 595 (error 9)
Location name: Alien Portal
```
Here, you can see I gave the program only the distances to the origin and the
N/W beacons. Any error value lower than 20 means that all results are pretty
much in agreement with each other. When you see a large error value here, it
likely means you've mixed up some beacons.

So, cool, now it saved "Alien Portal" in the locations.json file. But how do I
find it again? Easy enough:

```
$ ./sngps goto
Current position: .
Target          : Alien Portal
How far    [1.0]:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Position          : 0 / 0 depth 0
Target            : -864 / 920 depth 595
Distance to target: 1395
Bearing           : 317°
Direction         : NW +2° (+0.2 ticks)
Depth difference  : 595
```

Here, we enter as the current position "." (which is the shortcut for Liferaft,
the origin) and as a target our previously located portal. Then it also asks,
how far in the line we want to go. Usually we want to go all the way there (1.0
or simply return), but sometimes you might want the *exact* position between
two bases and you can simply enter "0.5" here.

Then it tells you that you want to go from (0, 0, 0) to (-864, 920, 595). The
distance is 1395 meters and your azimuth (bearing) is 317°. This is 2 degrees
more than NW. It even gives you the Subnautica compass "ticks" (each of which
is 7.5°), so N + 1tick means the compass tick that is one to the right of
North.

So after you've cataloged everything, you might want to have a map of it? Sure:

```
$ ./sngps plot
```

And with some Gnuplot magic you get a nice map of everything:

[![Map of the plotted terrain](https://TODO)]

## License
GNU GPL-3.
