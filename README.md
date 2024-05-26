## Stock Market Email Update

This script calls on 3 different APIs to make this magic happen, I
will be running it on python anywhere as a free task.

This was a project from a class so for me the goal of completing it
on my own was kind of enough I doubt I will update this although 
since I will be running the script in python anywhere for a while 
I may tweak it and try to make the News Story function a bit more 
effective.

What this script does:

- Checks the price of a stock using this endpoint https://www.alphavantage.co/
- The project actually called to only return news on a significant movement but I did not like that so we just
return news regardless while also building a string that notifies the user of the price. If the price does not move more than five percent over 
the past 24 hours it informs the user it was stable, but still searches for stories and pulls back 3.
- If There are not 3 returned stories the script returns as many as it can.
- Finally it takes all this information and generates an email and sends it out to the user or target email address.

## What is to come

Probably nothing, like I said I may smooth the edges out more ... add error handling for API issues but that is about it
this was just a fun project I did and wanted to share.