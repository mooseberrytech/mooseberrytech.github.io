title: Learn from Your Bugs and Move On
date: 2024-12-10
author: Adriana Vasiu
category: ways-of-working

I can talk openly about making mistakes and introducing bugs. 
Because any issue I created in software was done unwillingly and unknowingly.

Show me a software engineer that hasn't created any bug and I will show you a liar!

In the past, I used to stay up at night and beat myself up because on the day I discovered that I introduced a bug somewhere,
and it made it into production. Or I made a mistake, and it was costly.
Next day I would go back to work, being mentally exhausted and going at it again, writing more code, 
fixing more issues and probably introducing the occasional issues as well. 

These days I work with teams to prevent those issues from happening and minimise the impact that any issue causes into production.
Testing, any sort of automation, observability and a lot of other practices help with that.
Software Delivery Lifecycle is a passion of mine.

Over the years, the way I deal with failure and the way I react when I discover I made a mistake in my job has changed dramatically, 
and it pushed me forward. Hopefully talking openly about my own journey will help some of you to get there faster than I did. 
Because I did take my time with this!

This is what I used to do when I discovered an issue I introduced in code: 

- I was so stressed about it that I couldn't properly focus on finding a fast and correct solution. 
  I put so much pressure on myself in those moments that for a brief time being rational just flew out of the window. 
- I took it very personally. How could I dare introduce a bug? 
  Why did I not think about this? 
  Now when I think about it, this sort of attitude was pretty absurd, and not rational. 
  Who am I to think that I cannot make mistakes? 
  If you want to skip the part when you are doing something wrong then most likely you need to skip the work all-together, 
  because accept it, you will make mistakes! 
- I was ashamed and I beat myself up over anything, no matter how small. Not very productive. 

And this is where I am now with my thinking:

- Unwillingly and unknowingly a logic error or something contextual will come into play, and things will go slightly sideways sometimes. 
  Accept it, own up to it, take responsibility. 
  Speak up when you discover it and make sure that everyone in the team is fully aware so that a fix can be worked on and all focus is on remediation.
- When an issue is discovered, especially in production, after you have fixed it, spend appropriate time to understand how the issue happened.
  Why it hasn't been caught up in time? Take this opportunity to improve testing in this area.
  Make sure that everyone working on that area of the code has much better chances of not introducing another issue. 
- Especially if the issue is long run, think about how it could have been caught sooner. 
  What sort of monitoring and observability do you need to put in place? 
  Make the alerting more granular and aggressive if needs be.
- Fully analyse the impact and communicate clearly with the business on what happened and how the team can prevent this from happening again. 
- If the issue occurred because of an assumption that was made, especially if the assumption was not documented, 
  take this opportunity to document that assumption and validate it with the business stakeholders. 
  Any assumption should be properly reflected in tests, tests are your living documentation. 
  Name your tests so explicitly so that any new team member can understand the business logic from tests alone.
- When you fix an issue pay extra attention that no regression is introduced, that can happen especially in the rush of things. 
  Make sure that you don't modify existing tests unless they are actually wrong or if they make the wrong assumption. 
  Add new tests to cover what you just fixed.


One of the most important things that I learned over the years, and it applies not only to software, is to accept
that we do make mistakes, especially when we deal with challenging situations, when we learn, when we grow, when we try!

So what can we do about it? We can try and fix much more than we ever break! 
