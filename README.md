# Tweet Instagram Posts Bot

![GitHub all releases](https://img.shields.io/github/downloads/LucEast/tweet-instaposts-bot/total)
![GitHub](https://img.shields.io/github/license/LucEast/tweet-instaposts-bot)

This is the code that runs the account [@LucEast_bot](https://twitter.com/LucEast_bot) on Twitter, tweeting latest Instagram Post 

## Script Setup

- Create an app at the [Twitter Developer site](https://developer.twitter.com/) and create app tokens and keys
- Apply for V1.1 API Access
- Edit [config.cfg](./config.cfg) and put in your Twitter Consumer, Access tokens/keys and the Instagram Profile you want to post updates from
- Change `DRY_RUN` to `yes` if you just want to test the script without actually sending any tweets
- Make sure [state.cfg](./state.cfg) is writable, this is where the last Tweet and its values are stored so to not Tweet repeated messages
- Install the Tweepy library
- Install the Instaloader library
```
# Create venv 
python3 -m venv /path/to/venv

#Run Powershell as an Administrator 
Set-ExecutionPolicy Unrestricted (Optional - Disables needs of Admin privileges)

# Activate venv: Windows
.\path\to\venv\Scripts\Activate.ps1

# Activate venv: Linux / MacOS
source venv/bin/activate

# Install tweepy and instaloader directly
pip3 install tweepy
pip3 install instaloader

# Alternatively, use requirements.txt
pip install -r requirements.txt
```

The script can now simply be called like this:

```
python bot.py
# or
py -3 bot.py
```

## Crontab Setup

Running a cronjob with virtualenv:

```
0 12 * * * cd /home/you/tweet-instaposts-bot/ && /home/you/tweet-instaposts-bot/venv/bin/python /home/you/tweet-instaposts-bot/bot.py
```

## License

All source code and documentation in this repository is licensed under the [MIT license](LICENSE).

![ReadMe_Card](https://github-readme-stats.vercel.app/api/pin/?username=LucEast&repo=tweet-instaposts-bot&title_color=3e83c8&text_color=00cb71&icon_color=299bab&bg_color=171717&hide_border=true)
