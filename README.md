# TWKid-bet-system

# Introduction
This website is made for our AOE3 clan 台灣囝(TW_Kids) tournament, provide a place that our clan members can bet and have fun. I write it based on flask and simple html. This is not a well maintained project, it's just a simple prectice.

# How to run
Before you start it, make sure you change the url in 'main.py', it should be `127.0.0.1` by default.  
  
Starting the projrct
```
python main.py
```
Although if you got a correct form of 'data.txt', you can simply update you database by 
```
python sqliteControl.py
```

# How to use
The website provide some basic function for running a gambling platform. As a manager, you can open new games with 2 choices, stop people to bet on it and draw the result. Also you can create new account and sent money directly to him.
As a player, you can bet and watch you bet history, there will be some surprise messages when you do something wrong. 
