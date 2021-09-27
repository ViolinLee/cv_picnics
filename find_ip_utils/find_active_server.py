import platform 
import sys 
import os 
import time 
import _thread
import argparse
from urllib import request
from lxml.html import parse
from bs4 import BeautifulSoup
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument('prefix', type=str)
args = parser.parse_args()
 

def post_ip(target_url):
  try:
    response = request.urlopen(target_url, timeout=7)
    html = response.read()
    soup = BeautifulSoup(html, 'lxml')
    title = soup.title
    
    if "Flask Show Image" in title:
      print(target_url)
  except:
    pass


if __name__ == '__main__':
  print("Scanning...")
  prefix = args.prefix + '.'
  for i in tqdm(reversed(range(0, 256))):
    target_url = 'http://' + prefix + str(i) + ':8000/api/vis'
    _thread.start_new_thread(post_ip, (target_url,))
    time.sleep(0.5)
