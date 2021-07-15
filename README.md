# IQOption Trading Bot 

## Warning: 

  The bots were coded using an API from IQ Option platform. Based on my experience, this is an extremely bad broker with very high spread and low fps. As this platform was most accessible from where I live, I decided to use it to test my trading strategies. The documentation of the APIs were also limited and lackluster. So I would recommend staying away from this API and use other reputable exchanges. That being said, we will strictly discuss the strategies used and tested, instead of the installing and running applications.  

## Introduction 

This spring of 2021 was my first gap semester and I found a new interest: investing and trading. As a coder, I wanted to automate my trading experience as well as improving my strategies using bots. This is a great way to remove emotions out of my decisions and induce a disciplinary framework for my trading strategy. An effective and consistent system would ultimately become a good source of passing income. 

## Strategies: 

1. Momentum catch: 

  The bot will detect momentum shift in a specific time frame and place order following that momentum. 
  
  For examplem, if Bitcoin shows 3 green consecutive 5m candles, then the bot will put a call order. A sell order will be placed in the opposite scenarios. 
  
  Pros: good for a bear trend or bull trend 
  
  Cons: bad during a sideway or crab market 
  
  Please check btc5m.py, btc1m.py, stock1m.py for references.


2. dca bot: 

  The bot will continue to buy as the price drops to dollar cost average the call order spanning through out a dip. Then it will sell all positions once the price recovers to a certain point.
  
  Pros: works very well during volatile sideway movements 
  
  Cons: works very poorly during trendy market(bear or bull) 
  

## results: 

- The momentum bots' success rate were about 50%, there are still many tweaking that needs to be done and implementation of different indicators for better decision making. 

- The dca bot works really well at first, with a success rate of almost 100%. However, during the Bitcoin May crash, it fails miserably due to the price not recovering. If u run this bot for years then it would still work as Bitcoin recovers later in a Bull market. But as trading is all about short term movements, this method renders failure in an event of a big bear crash. 

## Google cloud implementaion 

- The bots were tested 24/7 using Google Cloud Computing Machines 

- Tools include: 

1. python3 
2. dependencies
3. tmux to run the script 24/7, please refer to tmux documentation for usage 
4. vim as the virtual IDE. 


## Conclusion 

As I will be migrating my trading bot development to different platform and a different API, This serves as a small introduction only. Hence, I did not discuss too much into the coding aspect. Please look at my code yourself or ask me any questions if you wanna learn more about any specific lines or functions. 

Trading bot algorithms are extremely hard to build and test. I will be working on during my passive time in college to find the most optimized strategy. During this period I will be uploading a more thorough documentation and testings as well as a better code representation. 
