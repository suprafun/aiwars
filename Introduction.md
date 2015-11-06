# Introduction #

AI Wars is loosely based on the Advance Wars series. The core rules are the same: building units, tile-based movement, transporting, supplying, hiding, close-range attacking and retaliating, long-range fire, fog-of-war. However, terrain, unit and building types can easily be customized. This allows for very specific gameplay.

For example, it's possible to create a collect-all-properties game, with only a weaponless 'collector' unit that can capture buildings, a 'property' building that can be captured in one turn, and various terrain types that make movement more or less difficult. A custom level that gives every player it's own fenced-off level segment can then turn the game into a sort of traveling-salesman algorithm competition.


# Overview #

The core of this project is the game logic. A set of classes that can be used to quickly set up a working game.

Besides that, code for a default server, AI client and observer client is provided, so the project is immediately usable: start the server, start an observer client and a couple of AI clients and watch how the AI clients battle each other.