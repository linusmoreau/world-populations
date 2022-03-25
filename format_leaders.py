import json
import os

countries = {}
names = {}
all_names = []
colours = {
    "National-Conservatism": "#084081",
    "Liberalism": "#ffff33",
    "Liberal-Conservatism": "#3690c0",
    "Social-Democracy": "#fb9a99",
    "Socialism": "#e41a1c",
    "Communism": "#7f0000",
    "Military Rule": "#525252",
    "Monarchism": "#762a83",
    "Colonialism": "#f4a460"
}
empires = {"Protectorate", "French", "British", "Spanish", "Portuguese", "Belgian", "Italian", "Dutch"}


def load():
    global countries, names, all_names
    with open("country_leaders.json", "r") as f:
        countries = json.load(f)
    with open("names.json", "r") as f:
        names = json.load(f)
    with open("all_names.json", "r") as f:
        all_names = json.load(f)


def write(year, data):
    if not os.path.isdir("leaders_ideologies"):
        os.mkdir("leaders_ideologies")
    with open("leaders_ideologies/" + str(year) + ".txt", "w") as f:
        json.dump(data, f)


def add_names():
    if "Colonies" not in names:
        names["Colonies"] = []
    for name in all_names:
        for empire in empires:
            if empire in name and "Occupied" not in name and name not in names["Colonies"] and \
                    name != "French_Guiana_1946_2016":
                names["Colonies"].append(name)
    for country in countries.keys():
        if country not in names:
            names[country] = list(
                filter(lambda n: country.replace(' ', '_') in n and n not in names["Colonies"],
                       all_names))
    with open("names.json", "w") as f:
        json.dump(names, f)


def generate(year):
    def add_to_tags(tag):
        parts = tag.split('_')
        start = int(parts[-2])
        end = int(parts[-1])
        if year >= start and (end is None or year <= end or end == 2016):
            tags.append(tag)

    data = {
        "title": str(year),
        "hidden": [],
        "background": "#1a1a1a",
        "borders": "#000000",
        "legendFont": "Roboto",
        "legendFontColor": "#ffffff",
        "legendBgColor": "#00000000",
        "areBordersShown": True,
        "defaultColor": "#d1dbdd",
        "labelsColor": "#6a0707",
        "strokeWidth": "medium",
        "areLabelsShown": False,
        "legendPosition": "custom",
        "legendX": "64.14",
        "legendY": "192.50",
        "legendSize": "custom",
        "legendScale": 0.7,
        "legendStatus": "show",
        "scalingPatterns": True,
        "legendRowsSameColor": True
    }
    groups = {}
    for ideology, colour in colours.items():
        tags = []
        for name in names:
            for tag in names[name]:
                if ideology == "Colonialism" and name == "Colonies":
                    add_to_tags(tag)
                if ideology == "Military Rule" and name == "Occupied":
                    add_to_tags(tag)
                try:
                    for period in countries[name][ideology]:
                        start = period[0]
                        end = period[1]
                        if year >= start and (end is None or year < end):
                            add_to_tags(tag)
                except KeyError:
                    pass
        if ideology == "Colonialism" and len(tags) == 0:
            tags.append(names["Colonies"][0])
        groups[colour] = {"label": ideology, "paths": tags}
    data["groups"] = groups
    return data


if __name__ == "__main__":
    load()
    add_names()
    for year in range(1946, 2023):
        write(year, generate(year))
