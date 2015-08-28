---
layout: post
title:  "Kivy Designer - Python Mobile made easy :)"
date:   2015-08-27
---


Hi!

This is the final report of Kivy Designer development, and the end of GSoC :( 

In this post I'll show you an overview of my original proposal, and compare with the final result.

## Expectations

Right now, major part of toolchains for Python Mobile still under development, and to new developers, it usually sounds confusing. 

My goal with this project was to evolve Kivy Designer and makes it an IDE that organizes and help us to develop Python/Kivy applications targeting multiple platforms.

## Project Overview

I've made some small modifications to the original proposal. In my proposal, Kivy Designer should be integrated with Hanga. But due to some problems on Hanga, this part of the project was not developed. 

I've made some important improvements to the Kivy Designer. I think that the main feature is the Builder. The Builder helps you to target the same project/source code to multiple platforms. So you can easily develop your app on your computer, and then deploy in on your mobile device :)
Now the Builder supports Buildozer and the default Python interpreter to run on your computer; but it's ready to be integrated with new tools.

Some enhancements were made to help with the development itself. An important one is the Jedi integration. Now, Kivy Designer provides auto completion to Python source codes :) And custom themes to CodeInput :)

It's integrated with Kivy Modules, that helps your your see the app running in different screen sizes, dimensions, orientations, etc; debug it; and more.

And, sure, what is a project without a good control? Kivy Designer is now integrated with Git. You can easily uses git features inside Designer, work with remote repos, branches, etc.

## Progress Overview

I was able to complete my proposal and even add some extra features to the project; but this summer was not enough to release a complete and powerful IDE. We have a lot of new features, however, it stills a WIP. 
Unfortunately I had a different calendar at University this year. So I have been studying during the whole GSoC(today, August 27, is my last day with classes. I did my last test some hours ago, and starting my University vacations now :P ). 

So I was not able to focus a lot of time on GSoC :(

I just feel that, with a better time, I should be delivering an even powerful project. But ...

## Is it the end ?

GSoC was an amazing and unique experience for me. 

I had been walking around in the beginning of the year trying to find open source projects that I could help. And then, I read about GSoC.

I see GSoC as a bridge that helped me to connect and learn/study about a project/company. So, now I'm completely able to keep contributing with them, make my project even better, and have a good connection with the open source community.

Now I can say you that I'm really experienced with Kivy Designer, and I've a good understanding/experience with Kivy itself, so, let's keep playing :) 