import configparser
import instaloader
import sys
import tweepy
from datetime import datetime


"""
Set up config values and constants
"""
L = instaloader.Instaloader(download_comments=False, max_connection_attempts=9, post_metadata_txt_pattern=None,
                            save_metadata=False, download_video_thumbnails=False, download_geotags=False, filename_pattern="{shortcode}")

config_file = configparser.ConfigParser()
config_file.read("config.cfg")
DRY_RUN = config_file.getboolean("TWITTER", "DRY_RUN")
CONSUMER_KEY = config_file.get("TWITTER", "CONSUMER_KEY")
CONSUMER_SECRET = config_file.get("TWITTER", "CONSUMER_SECRET")
ACCESS_KEY = config_file.get("TWITTER", "ACCESS_KEY")
ACCESS_SECRET = config_file.get("TWITTER", "ACCESS_SECRET")
# Instagram username and password for future features.
# INSTA_USER = config_file.get("INSTAGRAM", "INSTA_USER")
# INSTA_PASSWORD = config_file.get("INSTAGRAM", "INSTA_PASSWORD")
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)


CONFIG_FILENAME = "state.cfg"


PROFILE = config_file.get("INSTAGRAM", "PROFILE")


config = configparser.ConfigParser()
config.read(CONFIG_FILENAME)


def load_profile(name):
    """
    Downloads the content from the data source
    """
    print("Profile: ", name)
    user = instaloader.Profile.from_username(L.context, name)
    print("Profile loaded:")
    return user


def check_if_should_download(profile):
    for post in profile.get_posts():
        download = L.download_post(post, PROFILE)
        if download == True:
            return post
        print("Values have not changed: Do not download")


def download_post(post):
    video = post.is_video
    i = 1
    files = []
    if video == True:
        post_file = post.owner_username+"/"+post.shortcode+".mp4"
        files.append(post_file)
        return files
    if post.mediacount > 4:
        while i <= 4:
            post_file = post.owner_username+"/" + \
                post.shortcode+"_{}.jpg".format(i)
            files.append(post_file)
            i += 1
        return files
    if post.mediacount > 1:
        while i <= post.mediacount:
            post_file = post.owner_username+"/" + \
                post.shortcode+"_{}.jpg".format(i)
            files.append(post_file)
            i += 1
        return files
    else:
        post_file = post.owner_username+"/"+post.shortcode+".jpg"
        files.append(post_file)
        return files


def send_tweet(tweet, pics):
    """
    Sends tweet using the tweepy library
    """
    if DRY_RUN:
        print("[DRY RUN] Not actually sending tweet")
        return

    twitter_API = tweepy.API(auth)
    print(pics)
    media_ids = []
    print("Tweeting with handle @{}".format(twitter_API.verify_credentials().screen_name))
    for pic in pics:
        res = twitter_API.media_upload(pic)
        media_ids.append(res.media_id)
    # media_ids = [twitter_API.media_upload(i).media_id_str for i in pics]
    twitter_API.update_status(status=tweet, media_ids=media_ids)


def check_if_should_tweet(post):
    """
    Performs several tests to check if a tweet should be sent or not:
    - Current data's date must be newer than the one saved in the state configuration
    - Any of the percentage values must have changed and be higher as well
    """
    print("Checking old / new values")
    tweet_date = datetime.strptime(
        config.get("LAST_TWEET", "date"), "%Y-%m-%d")
    insta_date = post.date_local.date()
    print("date: {} / {}".format(config.get("LAST_TWEET", "date"), post.date_local.date()))

    if tweet_date.date() < insta_date:
        last_post = datetime.strptime(config.get(
            "LAST_TWEET", "last_downloaded_post"), "%Y-%m-%d")
        new_post = post.date_local.date()
        print("Downloaded: {} / New: {}".format(last_post, new_post))
        if last_post.date() < new_post:
            return True
        print("Values have not changed: Do not tweet")
        return False
    else:
        print("Date is same or older: Do not tweet")
        return False


def save_state(post):
    """
    Saves the date and percentages from the current CSV data to a state configuration file
    """
    config.set("LAST_TWEET", "date", post.date_local.strftime("%Y-%m-%d"))
    config.set("LAST_TWEET", "last_downloaded_post",
               post.date_local.strftime("%Y-%m-%d"))

    if DRY_RUN:
        print("")
        print("[DRY RUN] Not updating the state configuration")
        print("")
        config.write(sys.stdout)
        return

    with open(CONFIG_FILENAME, "w") as configfile:
        config.write(configfile)
        print("Saved state configuration")


def generate_message(post):
    """
    Concatenates the three progress bars into the final tweet message text
    """
    if post.caption is None:
        msg = "https://www.instagram.com/p/{}".format(post.shortcode)
        return msg
    if len(post.caption) > 280:
        tweet = post.caption[:225]
        msg = "{}...\n\nhttps://www.instagram.com/p/{}".format(
            tweet, post.shortcode)
    else:
        msg = post.caption
    return msg


def run_all():
    load = load_profile(PROFILE)
    if not load:
        print("No matching profile found")
        raise
    post = check_if_should_download(load)
    if post:
        print("Downloading...")
        post_file = download_post(post)
        should_send = check_if_should_tweet(post)
        print("")
        print("Send tweet?", should_send)
        if should_send:
            print("Sending tweet:")
            print("")
            msg = generate_message(post)
            print(msg)
            print("")
            send_tweet(msg, post_file)
        save_state(post)


try:
    run_all()
except:
    raise
