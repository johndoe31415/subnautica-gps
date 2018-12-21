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
with this and implemented a kind of "GPS style" trilateration. Initial
implementation is in 2D only and expects two or three beacons placed on the
water surface (i.e., the Z coordinate is zero).

Then, you can enter two or three distances to any beacons and it will try to
trilaterate your given position.

I plan to add later to also give a bearing when there's a certain point you
want to reach from a given location. Maybe even add true 3d trilateration,
although this is much more complicated.

Anyways, have fun.

## How does it work?
You need to place three beacons at known locations. Your initial liferaft will
always be the center of the universe for trilateration, i.e., placed at (0, 0, 0).
I define "North" to be positive Y values and "East" to be positive X values.
Therefore, in my example, I swam 1km from the liferaft exactly to the north and
placed a "north" beacon there, then swam back and 1km to the west and places a
"west" beacon there. The definitions are changable in the JSON file.

Then, just run it and enter the distances that you're seeing from your current
location. Skip over any you don't want (e.g., close ones that would lead to
numerical instability) by pressing return. After two or three entered values,
you should have a result.

## License
GNU GPL-3.
