import os
import json
import re
import requests

with open("../rawdata/playArea.json", "r") as json_file:
    config = json.load(json_file)

for c in range(config['colFrom'], config['colTo'] + 1):
	for r in range(config['rowFrom'], config['rowTo'] +1):
		url = "https://mt0.sea.cf.wyrimaps.wyri.haxim.us/v/13/wow_battle_for_azeroth/7/{}/{}.jpg".format(c,r)
		filename = "../rawdata/map_{}_{}.jpg".format(c,r)
		response = requests.get(url)
		with open(filename, "wb") as file:
			file.write(response.content)

rawdata_dir = "../rawdata"
image_files = [f for f in os.listdir(rawdata_dir) if f.endswith(".jpg")]

def calculate_coordinates(image_name, base_x=96, base_y=60):
    match = re.match(r"map_(\d+)_(\d+)\.jpg", image_name)
    if match:
        x = int(match.group(1)) - base_x
        y = int(match.group(2)) - base_y
        return x * 256, y * 256
    return 0, 0

svg_code = f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="{config['viewBox']}" width="{config['width']}" height="{config['height']}">
"""

# Přidání obrázků
for img in image_files:
    x, y = calculate_coordinates(img)
    svg_code += f'    <image href="./rawdata/{img}" width="256" height="256" x="{x}" y="{y}"/>\n'

svg_code += """
    <defs>
        <mask id="playMask">
            <rect width="200%" height="200%" x="-100%" y="-100%" fill="white" />
            <polygon 
                id="playArea"
                points="
"""
for point in config["polygon"]:
    svg_code += f"                {point[0]},{point[1]}\n"
svg_code += """
                "/>
        </mask>
    </defs>
    <rect width="200%" height="200%" x="-100%" y="-100%" fill="#FF000055" mask="url(#playMask)">
        <title>Zákaz vstupu</title>
    </rect>
    <use href="#playArea" fill="#00FF0022">
        <title>Herní zóna</title>
    </use>
</svg>
"""

# Uložení do souboru
with open("../herní-zóna.svg", "w", encoding="utf-8") as file:
    file.write(svg_code)  # Zapíše nový obsah

print("SVG soubor byl úspěšně vygenerován.")
