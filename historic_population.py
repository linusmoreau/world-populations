import json


NUMBER = 0
PERCENTAGE = 1
STRING = 2


def print_debug(*args):
    if debugging:
        print(*args)


def load_leaders():
    with open("country_leaders.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(file, ints):
    keys = []
    entries = []
    with open(file, 'r', encoding='utf-8') as f:
        line = f.readline().strip()
        keys.extend(line.split(','))
        for line in f:
            values = []
            ingroup = False
            value = ''
            for c in line.strip():
                if c == '"':
                    ingroup = not ingroup
                elif not ingroup and c == ',':
                    if len(values) in ints:
                        value = to_int(value)
                    values.append(value)
                    value = ''
                else:
                    value += c
            if len(values) in ints:
                value = to_int(value)
            values.append(value)
            entries.append(values)
    return keys, entries


def to_int(s):
    s = s.replace(',', '')
    if len(s) == 0:
        return None
    else:
        return int(s)


def load_populations():
    data = load_csv("mpd2020.csv", [2, 3, 4])
    return data


def populate(data, cols):
    for c in cols:
        prev = None
        subs = None
        previ = 0
        subsi = 0
        for i, entry in enumerate(data):
            if i >= subsi:
                subs = None
            if entry[c] is not None:
                prev = entry[c]
                previ = i
            else:
                if subs is None and subsi is not None:
                    for j in range(i, len(data)):
                        if data[j][c] is not None:
                            subsi = j
                            subs = data[j][c]
                            break
                    else:
                        subsi = None
                if prev is None and subs is None:
                    entry[c] = None
                elif prev is None:
                    entry[c] = subs
                elif subs is None:
                    entry[c] = prev
                else:
                    entry[c] = int(prev + (i - previ) / (subsi - previ) * (subs - prev))
    return data


def organize(keys, entries, header, header2, content):
    data = {}
    for entry in entries:
        if entry[header] not in data:
            data[entry[header]] = {}
        e = {}
        for i in content:
            e[keys[i]] = entry[i]
        data[entry[header]][entry[header2]] = e
    return data


def build_name_map(src, dst):
    name_map = {
        "Bolivia": "Bolivia (Plurinational State of)",
        "Cape Verde": "Cabo Verde",
        "Congo": "D.R. of the Congo",
        "Congo-Brazzaville": "Congo",
        "Czechia": "Czech Republic",
        "Iran": "Iran (Islamic Republic of)",
        "Ivory Coast": "Côte d'Ivoire",
        "Korea, North": "D.P.R. of Korea",
        "Korea, South": "Republic of Korea",
        "Lao": "Lao People's DR",
        "Macedonia": "TFYR of Macedonia",
        "Moldova": "Republic of Moldova",
        "Palestine": "State of Palestine",
        "Russia": "Russian Federation",
        "Soviet Union": "Former USSR",
        "Sudan": "Sudan (Former)",
        "Syria": "Syrian Arab Republic",
        "Taiwan": "Taiwan, Province of China",
        "Tanzania": "U.R. of Tanzania",
        "Venezuela": "Venezuela (Bolivarian Republic of)",
        "Vietnam": "Viet Nam",
        "Yugoslavia": "Former Yugoslavia"
    }
    for name in src:
        if name not in name_map:
            if name in dst:
                name_map[name] = name
            else:
                print_debug("Name not found:", name)
    return name_map


def get_population(data, name, year):
    try:
        forname = data[name]
        try:
            forname[year]['pop']
        except KeyError:
            pass
    except KeyError:
        print_debug("Name not found:", name)


def build_table(data, leaders, name_map, year):
    table = {}
    cols = ["Ideology", "Population (1000s)", "Population (%)", "GDP (billions)", "GDP (%)", "GDP per capita",
            "GDP Growth (pc)"]
    col_type = {"Ideology": STRING, "Population (1000s)": NUMBER, "Population (%)": PERCENTAGE,
                "GDP (billions)": NUMBER, "GDP (%)": PERCENTAGE, "GDP per capita": NUMBER,
                "GDP Growth (pc)": PERCENTAGE}
    for col in cols:
        table[col] = {}

    pop_totals = {}
    gdp_totals = {}
    next_pop_totals = {}
    next_gdp_totals = {}
    for country, ideologies in leaders.items():
        found = False
        if country not in name_map or name_map[country] not in data:
            continue
        for ideology, periods in ideologies.items():
            for period in periods:
                start = period[0]
                if period[1] is None:
                    end = base + 1
                else:
                    end = period[1]
                if year in range(start, end):
                    info = data[name_map[country]]
                    try:
                        pop = info[year]['pop']
                        gdp = info[year]['gdppc'] * pop / 1e6
                    except KeyError:
                        found = True
                        break
                    pop_totals.setdefault(ideology, 0)
                    pop_totals[ideology] += pop
                    gdp_totals.setdefault(ideology, 0)
                    gdp_totals[ideology] += gdp
                    try:
                        next_pop = info[year + 1]['pop']
                        next_gdp = info[year + 1]['gdppc'] * next_pop / 1e6
                    except KeyError:
                        next_pop = pop
                        next_gdp = gdp
                    next_pop_totals.setdefault(ideology, 0)
                    next_pop_totals[ideology] += next_pop
                    next_gdp_totals.setdefault(ideology, 0)
                    next_gdp_totals[ideology] += next_gdp
                    found = True
                    break
            if found:
                break

    pop_proportions = {}
    pop_total = 0
    gdp_proportions = {}
    gdp_total = 0
    next_pop_total = 0
    next_gdp_total = 0
    for ideology in pop_totals:
        pop_total += pop_totals[ideology]
        gdp_total += gdp_totals[ideology]
        next_pop_total += next_pop_totals[ideology]
        next_gdp_total += next_gdp_totals[ideology]
    for ideology in pop_totals:
        pop_proportions[ideology] = pop_totals[ideology] / pop_total
        gdp_proportions[ideology] = gdp_totals[ideology] / gdp_total

    for ideology in pop_totals:
        table["Ideology"][ideology] = ideology
        table["Population (1000s)"][ideology] = pop_totals[ideology]
        table["Population (%)"][ideology] = pop_totals[ideology] / pop_total
        table["GDP (billions)"][ideology] = gdp_totals[ideology]
        table["GDP (%)"][ideology] = gdp_totals[ideology] / gdp_total
        table["GDP per capita"][ideology] = gdp_totals[ideology] / pop_totals[ideology] * 1e6
        table["GDP Growth (pc)"][ideology] = ((next_gdp_totals[ideology] / next_pop_totals[ideology]) /
                                              (gdp_totals[ideology] / pop_totals[ideology]) - 1)
    return table, cols, col_type


def display_number(num: float, size):
    display_string(str(int(num) + (num - int(num) >= 0.5)), size)


def display_percentage(perc: float, size):
    display_string(str(round(perc * 100, 1)), size)


def display_string(s, size):
    if len(s) >= size:
        s = s[:size-1]
    print(s.rjust(size), end="")


def display_element(e, col_type, size):
    if col_type == NUMBER:
        display_number(e, size)
    elif col_type == PERCENTAGE:
        display_percentage(e, size)
    else:
        display_string(e, size)


def display_table(table, cols, col_type, title, size=24, sortby=1):
    print("-" * size * len(cols))
    print(title.rjust(size))
    for header in cols:
        display_element(header, "string", size)
    print()
    order = sorted(list(table[cols[0]].keys()), key=lambda n: table[cols[sortby]][n], reverse=True)
    for row in order:
        for col in cols:
            display_element(table[col][row], col_type[col], size)
        print()


def average_gdp_pc_growth(tables):
    totals = {}
    pop_totals = {}

    for table in tables.values():
        for ideology in table["Ideology"]:
            pop = table["Population (1000s)"][ideology]
            totals.setdefault(ideology, 0)
            totals[ideology] += pop * table["GDP Growth (pc)"][ideology]
            pop_totals.setdefault(ideology, 0)
            pop_totals[ideology] += pop

    averages = {}
    for ideology in totals:
        averages[ideology] = totals[ideology] / pop_totals[ideology]
    return averages


def display_gdp_pc_growth(data):
    order = sorted(list(data.keys()), key=lambda n: data[n], reverse=True)
    display_string("Ideology", 24)
    display_string("GDP Growth (pc)", 24)
    print()
    for ideology in order:
        display_string(ideology, 24)
        display_percentage(data[ideology], 24)
        print()


if __name__ == '__main__':
    base = 2022
    debugging = False
    leaders = load_leaders()
    keys, entries = load_populations()
    entries = populate(entries, range(3, 5))
    data = organize(keys, entries, 1, 2, range(3, 5))
    name_map = build_name_map(leaders, data)
    tables = {}
    for year in range(1946, 2019):
        table, cols, col_type = build_table(data, leaders, name_map, year)
        # display_table(table, cols, col_type, str(year))
        tables[year] = table
    display_gdp_pc_growth(average_gdp_pc_growth(tables))

