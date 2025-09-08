from src.refresher import Refresher

refresher = Refresher()
events = refresher.update_events()
print(events.shape)
players = refresher.update_players()
print(players.shape)
