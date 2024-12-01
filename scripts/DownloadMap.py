import requests

col_from = 96
col_to = 97
row_from = 59
row_to = 61

for c in range(col_from, col_to + 1):
	for r in range(row_from, row_to +1):
		url = "https://mt0.sea.cf.wyrimaps.wyri.haxim.us/v/13/wow_battle_for_azeroth/7/{}/{}.jpg".format(c,r)
		filename = "../rawdata/map_{}_{}.jpg".format(c,r)
		response = requests.get(url)
		with open(filename, "wb") as file:
			file.write(response.content)