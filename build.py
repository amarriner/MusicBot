#!/usr/bin/env python

from pattern.en import conjugate, PARTICIPLE

import json
import random
import sys


# List of song attributes
f = open("data.json")
j = json.loads(f.read())
f.close()

print "Total Features: " + str(len(j['features']))

# List of verbs, animals and elements
# Band name is present participle verb + animal/element
f = open("corpora/data/words/verbs.json")
verbs = json.loads(f.read())['verbs']
f.close()

f = open("corpora/data/animals/common.json")
animals = json.loads(f.read())['animals']
f.close()

f = open("corpora/data/science/elements.json")
for e in json.loads(f.read())['elements']:
   animals.append(e['name'])
f.close()

# List of foods and nouns
# Track name is food + noun
f = open("corpora/data/foods/fruits.json")
foods = json.loads(f.read())['fruits']
f.close()

f = open("corpora/data/foods/vegetables.json")
foods = foods + json.loads(f.read())['vegetables']
f.close()

f = open("corpora/data/foods/pizzaToppings.json")
foods = foods + json.loads(f.read())['pizzaToppings']
f.close()

f = open("corpora/data/words/nouns.json")
nouns = json.loads(f.read())['nouns']
f.close()


def clean_feature(f):
   """Strips unwated characters and makes feature ready for tweeting"""

   if f.startswith("a "):
      f = f[2:]

   if f.startswith("an "):
      f = f[3:]

   return str(f)


def build_tweet():
   """Build tweet per template"""

   verb = conjugate(random.choice(verbs)['present'], tense=PARTICIPLE, parse=True).title()
   animal = random.choice(animals).title()
   food = random.choice(foods).title()
   noun = random.choice(nouns).title()

   band = food + " " + noun
   track = verb + " " + animal

   feature1 = clean_feature(random.choice(j['features']))
   feature2 = clean_feature(random.choice(j['features']))
   feature3 = random.choice(j['features'])

   s = "I like the " + feature1 + " and " + feature2 + " with " + \
          feature3 + " in " + band + "'s " + '"' + track + '"'

   return s


def main():
   """Main entry point"""

   s = ""
   while len(s) > 140 or not s:

      s = build_tweet()
      print "Length: " + str(len(s))
      print s
      print "--------------------------------------------------------------------------"


if __name__ == "__main__":
   sys.exit(main())
