from map_requests import get_maps


def make_maps():
    dataset = {}
    for year in range(1946, 2022):
        with open("leaders_ideologies/" + str(year) + ".txt", "r") as f:
            dataset[year] = f.readline()
    get_maps(dataset)


if __name__ == "__main__":
    make_maps()

