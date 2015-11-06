# Overview #

The building blocks of AI Wars are units, buildings and terrain.

Buildings provide income for the player, and some buildings can be used to build and repair certain unit types. Buildings can be captured by certain units. Buildings can't be destroyed.

The primary use of units is to attack enemy units and to capture neutral or enemy buildings. Some units can move further than others, depending on the terrain. Moving costs fuel and some unit types use fuel even when stationary. Units can fire at other units, using either their primary weapon (which uses ammunition) or their secondary weapon, depending on which one is most effective against the target. Some units can fire across several tiles, others need to stand next to their target. Most units can retaliate after being attacked. Some units can transport and supply others, or capture properties. Some units can hide themselves.

Terrain affects unit movement and sometimes provides a cover bonus, which reduces damage dealt to a unit. Some terrain types can also hide units if the fog-of-war rule is applied.


Almost all of these characteristics can be modified per unit type.

# Rules #

At the start of each turn, a player first receives income from the buildings he owns. Then, repairs are conducted: any damaged unit that's standing on a friendly building that can repair that unit type gains a few hitpoints. Repair cost depends on the price and maximum hitpoints of the unit: a full repair would cost the same as building a new unit. Then these units and any other units that are standing next to a supplying unit are fully supplied with fuel and ammunition.

Then, any units that use fuel per turn use that amount of fuel, and if they're out of fuel, they either can't move, or are destroyed instantly, depending on their characteristics.


From this point on, a player can issue commands. He can [issue 3](https://code.google.com/p/aiwars/issues/detail?id=3) command types:

**Building units**
  * build units - if he has the required funds, and an unoccupied building that can build the desired unit type
  * destroy units - friendly units can be destroyed at any time, without refunds

**Moving units**
  * move units - if they're not out of fuel, or blocked by enemy units or terrain, or currently being transported by another unit
  * combine units - if the target unit is damaged and of the same type as the moving unit
  * load units - if the target unit can transport the moving unit, and if still has room

**Performing actions**
  * supply units - if the unit can supply others, and if there are friendly units nearby
  * unload units - if the unit is currently being transported by another, and if the destination point is not occupied
  * attack units - if the target unit is within range of the attacking unit, and if the attacking unit can actually damage the target
  * capture buildings - if the unit is on top of the building and the building is not owned by the player
  * hide units - hides or unhides the unit


When a players turn has ended, he can no longer issue commands until his next turn starts.

# Notes #

When a unit is destroyed, all the units that it was transporting are destroyed with it.

A unit will only use it's primary weapon if it has ammunition and if it can deal more damage with it than with it's secondary weapon.

Damage dealt is deterministic:
```
damage = floor((attacker.strength * attacker.hitpoints) * (10 - defender.terrain.cover) / 1000)
```
So, for example, a unit that has 5 hitpoints, and that deals 80 damage against it's target, will normally deal 4 damage against it's target. If the target has a cover bonus of 2 or more, it will only receive 3 damage, and a cover bonus of at least 4 would further reduce that to 2.

Units can detect hidden units only within a certain radius - typically a radius of 1. That means they must stand next to a hidden unit before they can spot it. Buildings can't spot hidden units unless they're standing directly on top of the building.

When a unit is trapped - that is, a previously unseen enemy unit is blocking it's path - it can not perform any other actions during that turn.

# Advance Wars #

For those who are familiar with Advance Wars, specifically Advance Wars: Black Hole Rising, it may be useful to know where AI Wars differs. Here is a brief summary of all the differences, in as far as I am familiar with AW:BHR.

In AI Wars:
  * CO effects, CO powers and weather effects are not supported
  * damage is deterministic, damage dealt is never randomized
  * there are no missile silos, Black Hole special weapons and volcano outbursts
  * there is no support for buildings with hitpoints in general, such as the Black Hole special weapons and pipe seams
    * such buildings can however be simulated by unmovable units
    * their weapon functions could be simulated as well, if I implement different target range patterns (currently units are limited to a diamond-shape target zone)
  * the default database contains some minor differences: the Neotank is called Heavy tank, and pipelines and pipe seams are replaced by an Impassable terrain type

Advance Wars: Dual Strike contains some new units and buildings. Some of these can be recreated in AI Wars, some can't:
  * Megatank: can be implemented
  * Pipe runner: can be implemented
  * Stealth bomber: can be implemented
  * Carrier: can be implemented
  * Oozium: unit absorbing is not supported
  * Figher: can be implemented
  * Black bomb: applying damage to multiple tiles is not supported, nor can units self-destruct upon attack
  * Black boat: repairing units with other units is not supported, not automatically supplying surrounding units at the start of a turn is not supported
  * Com tower: firepower increase based on number of com towers is not supported

Advance Wars: Days of Ruin contains new units and the behavior of some units has changed. Some of this can be recreated in AI Wars, some of it can't:
  * Bike: can be implemented
  * Flare: launching flares is not supported
  * Rig: constructing temporary airports or seaports is not supported
  * Anti-tank: can be implemented
  * War tank: can be implemented
  * Duster: can be implemented
  * Sea plane: can be implemented
  * Gun boat: can be implemented
  * Battleship: can be implemented
  * Carrier: launching units and constructing units from other units is not supported
  * Temporary airfield: can be implemented
  * Temporary port: can be implemented