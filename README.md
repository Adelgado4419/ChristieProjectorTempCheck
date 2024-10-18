#Hey there!

Welcome to my little project that tracks the temperature of 32 projectors we’ve got set up at our venue—specifically, the Christie DWU1100-GS.

#A Bit of Backstory

This all kicked off because we were running into issues where the projectors were overheating, and I wanted a way to check all of the current temps of the projectors withouth logging into the UI of each one every time. I started looking into the projector and noticed an API document which showed it had a way to query the temp data. 

So i figured why not, and started down the path of figuring out how to write my first python program with Socket.


#How It Works

Here’s the lowdown:

I’ve got a list of IP addresses for the projectors, and I loop through them using the socket library. I kick things off with “data_received = 0” because the data i receive back from the projector spits out 23 lines of info and after some trial and error with a program called Hercules, I discovered that the juicy info I needed was on the 21st line. So, I tweaked my code to count responses and only grab that line, i convert the data to to a string, i then read the string and use reGex to extract the Celcius temp, which i then convert to Fahrenheit, write it to the database, close the socket, and then start a timer for 5 minutes to start the whole process again. 

Please feel free to use any bit of this code, good luck!
