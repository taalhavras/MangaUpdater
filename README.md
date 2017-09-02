# MangaUpdater
This will scrape specific subreddits for new manga chapters and send updates to the user via email.

# Why would you make this?
Because I like reading manga and I dislike having to constantly check different places to see if new chapters are up yet. Since I already check my email every two minutes this will save me (and hopefully you) some time! 

# Praw
This project uses PRAW, the python reddit API wrapper. To get set up with praw read [this](https://praw.readthedocs.io/en/latest/getting_started/quick_start.html). In addition to installing PRAW you will need to obtain a reddit client secret and client id, which the link shows you how to do. Once you have those values, just paste them into the script and you should be good to go!

# Yagmail
I used yagmail (https://github.com/kootenpv/yagmail) to handle sending emails. You must set up yagmail using keyring and a .yagmail file to use this code, see the yagmail readme for details. If you really don't want to do this you could have your email and password stored in the code but I personally found that unattractive. 

# So how can I choose what manga to scan for?
Create a file called 'manga\_names.txt' in this directory and put the titles of the series you want updates on in it. Each new title should go on a new line and capitalization doesn't matter. In some cases you may not be able to use the full manga name. For example, Kaguya Sama Wa Kokurasetai is also refered to as Kaguya wants to be confessed to. Instead of including both titles you should just use Kaguya, which works fine. In the future support might be added for aliasing multiple names so they refer to the same manga.

# Filtering emails
This is totally optional, but since I use gmail I thought it would be nice to filter all emails this script sent me and label them accordingly. You can do this by filtering for emails with the subject line "CHAPTER:" that are sent by the gmail account to itself.

