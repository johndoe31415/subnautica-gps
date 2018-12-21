# Subnautica GPS System
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

## License
GNU GPL-3.
