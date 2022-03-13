from map_requests import get_maps


def make_maps(start, end):
    dataset = {}
    with open("path.txt", "r") as f:
        s = f.readline()
    for year in range(start, end):
        dataset[year] = s + str(year) + ".txt"
    get_maps(dataset)


if __name__ == "__main__":
    make_maps(1946, 2023)

