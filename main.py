import requests, json
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.refresher import Refresher

refresher = Refresher()
events = refresher.update_events()
print(events.shape)
players = refresher.update_players()
print(players.shape)
