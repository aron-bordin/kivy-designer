---
layout: post
title:  "Kivy Designer Development"
date:   2015-06-26
---

Hi!

I had some tests on my University last week, so I've done a smaller progress in my development. 

### Events/Properties viewer UI

I did some modifications to Events and Properties UI, and fixed some related bugs. 

* Add custom event is working
* Added a canvas line between properties and event names
* Displaying Info Bubble in the correct position (information about the current event being modified)

# TODO - add screenshot

### Designer Code Input

* Added line number to KvLangArea
* Implemented ListSetting radio

![](https://cloud.githubusercontent.com/assets/4960137/8346063/bf699d74-1acd-11e5-99e1-9c5484200b23.png)

### Designer Tabbed Panel

Implemented a closable and auto sizable TabHeader to Designer Code Input. Now it's possible to close open tabs :)

Implemented "smart" tabs design. Change the tab style to inform if there is something wrong with the source code, if the content has modification, and to say the git status. (Only design, not yet working)

### Bug fixes

I fixed a small bug to Python Console.
Edit Content View was not working with DesignerCodeInput. Working now.


Thats it, thanks for reading :)

Aron Bordin.