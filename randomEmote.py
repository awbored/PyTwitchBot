from unittest import skip
import numpy as np
import requests
from bs4 import BeautifulSoup as bs


def random_emote(cnt=1):

    # Getting emotes from site and assigning to emotes array
    url = 'https://www.twitchemotes.com/'
    emotes = []
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    allEmotes = soup.findAll('a', class_='emote-name')

    motes = soup.select('img')
    for mote in motes:
        mote = mote.get('data-regex')
        if mote is None:
            continue
        emotes.append(mote)

    # Limits number to 50, for Twitch chat text limitations
    if cnt > 50:
        cnt = 50

    rndEmote = np.random.choice(emotes, cnt)
    rndEmote = rndEmote.tolist()
    rndEmote = " ".join(rndEmote)

    return(rndEmote)