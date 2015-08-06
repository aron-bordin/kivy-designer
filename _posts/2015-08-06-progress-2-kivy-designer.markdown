---
layout: post
title:  "Progress Report 2"
date:   2015-08-06
---


Hi!

I have advanced in my proposal and extra items, and as we are getting closer to the end of the project, let's see how it's going, and my next steps until the end.

### Usual Python/Garden modules on Buildozer spec editor

When writing your application, it's usual to forgot or don't even know the name of a package dependency. So I have added a list of usual Python and Garden modules to the Buildozer Spec Editor.

### Action Item description

By default, Kivy action button doesn't support a description to each item. So I created a custom one, the in the future, will be used to display action shortcuts.

![](https://cloud.githubusercontent.com/assets/4960137/8922073/9df4bc22-34b4-11e5-83d4-3bdd0153801c.png)
 
### New Status Bar

I created a new Status bar to Kivy Designer. The old statusbar was able to display only a item once, and was not working with small screens. 

With the new one, we have three different regions to display information.

![](https://cloud.githubusercontent.com/assets/4960137/8887424/c6b8f966-3257-11e5-89fa-4127e3eb5d56.png)
![](https://cloud.githubusercontent.com/assets/4960137/8887423/c6b6f2e2-3257-11e5-9763-553a0090712e.png)
![](https://cloud.githubusercontent.com/assets/4960137/8887425/c6b94c72-3257-11e5-8b19-d903c005cddd.png)
![](https://cloud.githubusercontent.com/assets/4960137/8887426/c6b9d7e6-3257-11e5-982b-4351edfcb4bf.png)

### Kivy Designer Tools

I added some tools to help with the project development:

#### Export .png
A helper so create a .png image from the application UI or from the selected widget on Playground

#### Check pep8
A simple shortcut to run a pep8 checker in the project under development.

#### Create Setup.py
A UI tool to help you to create a setup.py to your application.

#### Create .gitignore
Creates a simple .gitignore to kivy designer projects

### Kivy Modules

I added support to some Kivy modules with KD. When running your project, you can select and use the following modules:

* touchring
* monitor
* screen - where you can set and emulate different screen sizes and dimensions
* inspector
* webdebugger

### Git/Github integration

Using [GitPython](http://gitpython.readthedocs.org/en/stable/), Kivy Designer now supports git repositories.

You can start a new repo, commit, add files, pull/push data remotely, check diffs and switch/create branches :)

### Find

A simple tool to find text or regex in source code.


### Bug fixes

I had pushed a list of bug fixes related with [kivy console](https://github.com/kivy/kivy-designer/pull/102), [project loader](https://github.com/kivy/kivy-designer/pull/101) and a [problem with small screens and acitongroup](https://github.com/kivy/kivy-designer/pull/100)