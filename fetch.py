#!/usr/bin/env python

from bs4 import BeautifulSoup

import codecs
import json
import os
import random
import re
import requests
import sys
import time


J = {}
GENRES = []
PANDORA = "http://www.pandora.com"


def get_track_from_artist(artist):
   """Get a random track from an artist"""

   print "=== Looking for a track from " + PANDORA + artist + " ..."

   r = requests.get(PANDORA + artist)
   soup = BeautifulSoup(r.content)

   track = random.choice(soup.findAll("a", class_="track_link"))['href']

   print "=== Found track " + track + " ..."
   time.sleep(1)
   return track


def get_artist_from_genre(genre):
   """Get a random artist from a genre"""

   print "--- Looking for an artist from " + PANDORA + genre + " ..."
   r = requests.get(PANDORA + genre)
   soup = BeautifulSoup(r.content)

   stations = soup.findAll("span", class_="genreArtists")
   artists = random.choice(stations).findAll("a")

   artist = random.choice(artists)['href']
   print "--- Found " + artist + " ..."
   time.sleep(1)
   return artist


def get_genres():
   """Pull genres from Pandora or load from disk"""

   global GENRES

   if os.path.exists("genres.json"):
      f = codecs.open("genres.json", "r", "utf-8")
      GENRES = json.loads(f.read())
      f.close()
   else:
      r = requests.get(PANDORA + "/music/top-stations")
      soup = BeautifulSoup(r.content)

      for link in soup.findAll("a", class_="genreCategory"):
         GENRES.append(link['href'])

      f = codecs.open("genres.json", "w", "utf-8")
      f.write(json.dumps(GENRES))
      f.close()


def save_features():
   """Save features to disk"""

   f = codecs.open("data.json", "w", "utf-8")
   f.write(json.dumps(J))
   f.close()


def load_features():
   """Load or initialize features JSON"""

   global J

   if os.path.exists("data.json"):
      f = codecs.open("data.json", "r", "utf-8")
      J = json.loads(f.read())
      f.close()
   else:
      J = {}
      J['features'] = []


def parse_soup(soup):
   """Parse through soup to find features and get the next url to check"""

   global J

   try:
      features = re.sub(r" +", " ", soup.find("div", class_="song_features").text)
      for line in features.split("\n"):
         line = line.replace("&", "&amp;").strip()
         if line and line.lower() != "features of this track" \
                 and line.lower() != "show more"              \
                 and not line.lower().startswith("these are just a few of the hundreds of attributes cataloged for this"):

            if line not in J['features']:
               J['features'].append(line)
               print "::: " + line

      save_features()

      next = []
      for similar in soup.findAll("div", class_="similar_title"):
         for link in similar.findAll("a"):
            next.append(link['href'])

      next = random.choice(next)

   except:
      print "*** Error getting features"

      f = codecs.open("error.html", "w", "utf-8")
      f.write(soup.prettify())
      f.close()

      print "*** Getting new track after waiting"
      time.sleep(1)
      next = get_track_from_artist(get_artist_from_genre(random.choice(GENRES)))

      save_features()

   print "+++ Next URL " + PANDORA + next + " ..."
   time.sleep(1)
   return next


def get_soup(url):
   """Get soup from a URL"""

   print "+++ Getting soup for " + PANDORA + url + " ..."

   r = requests.get(PANDORA + url)
   soup = BeautifulSoup(r.content)

   time.sleep(1)
   return soup


def main():
   """Main entry point"""

   load_features()

   get_genres()


   for i in range(10):
      print "----------------------------------------------------------------------------------"
      print "Genre " + str(i + 1)
      print "----------------------------------------------------------------------------------"
      track = get_track_from_artist(get_artist_from_genre(random.choice(GENRES)))

      for j in range(50):
         print "----------------------------------------------------------------------------------"
         print "Track " + str(j + 1)
         print "----------------------------------------------------------------------------------"
         track = parse_soup(get_soup(track))
         time.sleep(1)

   save_features()


if __name__ == "__main__":
   sys.exit(main())
