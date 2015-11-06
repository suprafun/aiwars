# Overview #

The _core game classes_ maintain a game's state and it's gameplay rules. They are used both server- and client-side. Game state synchronization happens via so-called _situation updates_, a set of serializable classes. Every server-side player action generates a situation update, which clients can then apply to keep their local game state up-to-date.

![http://docs.google.com/drawings/pub?id=1S_x2am8-XfxjzrGoMEKQh2iPstiQXi2PKkOZh9BXGxM&w=641&h=466&n=n.png](http://docs.google.com/drawings/pub?id=1S_x2am8-XfxjzrGoMEKQh2iPstiQXi2PKkOZh9BXGxM&w=641&h=466&n=n.png)

![http://docs.google.com/drawings/pub?id=1P0739j3veQr_BCqIA2nZSj4KoKgwrHZOQWiXgZ1vtfI&w=672&h=177&n=n.png](http://docs.google.com/drawings/pub?id=1P0739j3veQr_BCqIA2nZSj4KoKgwrHZOQWiXgZ1vtfI&w=672&h=177&n=n.png)


# Server-side usage #

The server may call the player action functions directly. These functions return a situation update object, which can be sent to clients. A server usually only calls player action functions in reaction to a client command message.

These situation updates can be filtered by the game class for specific players: player clients should only know what they can see. This is particularly important when fog-of-war is enabled, but even when it is disabled there may still be hidden units.


# Client-side usage #

Clients should not call player action functions directly. Instead, the server will send them situation updates, which they should apply to their game object. The game object will update the local game state accordingly. For player clients, the local game state is often a subset of the real game state: