import atexit
import time
import re
import urllib3
import requests

import spotipy.exceptions
from apscheduler.schedulers.background import BackgroundScheduler

from config.constants import SCOPE, ERROR_LOG_FILE, LOG_FILE, ACCOUNT_NAME
from operation.db_wrapper import DBWrapper
from operation.evaluator import Evaluator
from operation.song_collector import SongCollector
from operation.sptfy_wrapper import SptfyWrapper
from util.logging import Logger

lg = Logger(LOG_FILE, ERROR_LOG_FILE)
sp = SptfyWrapper(lg, SCOPE, './config/account.env')
db = DBWrapper(lg)
cl = SongCollector(sp, db, lg, 10)
ev = Evaluator(sp, db, lg)
tmp = 0


def eval_all(recursive_count=0):
    try:
        ev.evaluate_all('all', 30)
    except TimeoutError:
        lg.log("RUN Timeout when evaluating", 1)
        time.sleep(30)
        if recursive_count < 3:
            recursive_count += 1
            eval_all(recursive_count)


def eval_period():
    ev.evaluate_period('favs4', 28, 25)
    ev.evaluate_period('favs2', 14, 20)


def run_collector():
    try:
        cl.run()
    except spotipy.exceptions.SpotifyException as ex:
        lg.log("COLL Spotify Exception: " + ex.msg, 1)
    except requests.exceptions.RetryError:
        lg.log("COLL Request Exception: RetryError", 1)
    except urllib3.exceptions.MaxRetryError as ex:
        lg.log("COLL urllib Exception: " + ex.reason, 1)


def check_playlist_names():
    its = [item['name'] for item in sp.get_playlists(ACCOUNT_NAME)]
    for name in its:
        if name[0] != "/":
            return
        if not re.search("/(.*:.*/?)*", name):
            return
        params = name.split("/")
        param_kwargs = {'pl_name': name,'genres':[], 'limit': 30, 'days':28}
        for param in params:
            inps = param.split(":")
            if inps[0] == "g":
                param_kwargs["genres"] += inps[1].split("_")
            if inps[0] == "l":
                param_kwargs["limit"] = int(inps[1])
            if inps[0] == "d":
                param_kwargs['days'] = int(inps[1])
        if len(param_kwargs['genres']) > 0:
            ev.evaluate(**param_kwargs)
        else:
            param_kwargs.pop("genres")
            ev.evaluate(**param_kwargs)


lg.log("RUN Checking database...", 0)
songs = db.execute_select("select * from songs;")
song = str(songs[0]).encode('utf-8') if len(songs) > 0 else "Empty"
lg.log(f"RUN {len(songs)} entries: "+str(song), 0)
lg.log("RUN Check successful.", 0)

sched = BackgroundScheduler(daemon=True)
sched.add_job(eval_all, 'cron', hour='2', minute='30')
sched.add_job(eval_period, 'cron', hour='3', minute='30')
sched.add_job(run_collector, 'interval', seconds=10)
sched.start()

atexit.register(lambda: sched.shutdown())
eval_period()
while True:
    pass
