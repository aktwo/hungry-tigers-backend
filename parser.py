from textblob import TextBlob
import re
import json
import urllib2
import string

def get_buildings():
  building_file = open("Buildings", "r")
  building_dict = {}
  for line in building_file:
    line = line.rstrip('\n')
    words = line.split(':')
    if len(words[0].split(" ")) > 1:
      certainty = False
    else:
      certainty = True
    building_dict[words[0]] = {"name": words[1], "certainty": certainty}
  return building_dict

def building_search(words, building_dict):
  scores = {}
  search_string = ""
  i = 0
  for word in words:
    search_string = r"\b" + word + r"\b"
    pattern = re.compile(search_string, flags=re.IGNORECASE)
    for building in building_dict:

      search_name = building
      proper_name = building_dict[building]['name']
      certain = building_dict[building]['certainty']

      if pattern.search(search_name):
        if certain:
          return proper_name
        else:
          if proper_name not in scores:
            try:
              int(word)
              scores[proper_name] = 1
            except:
              scores[proper_name] = 2
          else:
            try:
              int(word)
              scores[proper_name] += 1
            except:
              scores[proper_name] += 2
  try:
    return sorted(scores.items(), key=lambda a:a[1], reverse=True)[0][0]
  except:
    return None

def process_input(string, building_dict):
  string = re.sub(r'[^\x00-\x7F]+','', string) # remove non-ascii characters
  blob = TextBlob(string)
  blob = TextBlob(blob.stripped)
  words = [x for (x,y) in blob.tags if not (y == "DT" or y == "IN" or y == "CC" or y == "TO")]
  building = building_search(words, building_dict)
  if building:
    (lat, lng) = get_geocode(building)
    return [building, lat, lng]
  else:
    return None

def get_geocode(building):
  url1 = 'http://maps.googleapis.com/maps/api/geocode/json?address='
  url2 = '%20Princeton,%20New%20Jersey%2008544%20USA&sensor=false'
  reformat = string.replace(building, ' ', '%20')
  url = url1 + reformat + url2

  map_json = urllib2.urlopen(url)
  data = json.load(map_json)
  lat = data['results'][0]['geometry']['location']['lat']
  lng = data['results'][0]['geometry']['location']['lng']
  return (lat, lng)

# buildings = get_buildings()

# while(True):
#   prompt = raw_input("Enter query: ")
#   print process_input(prompt, buildings)
