import re


def main():
    with open("restaurant.txt", "r") as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            find = re.findall(r"<[\w,' ]*>", line)
            name = find[0]
            dietary = find[1]
            alcohol = find[2]
            wheelchair = find[3]
            wifi = find[4]
            print "name: %s, dietary: %s, alcohol: %s, wheel: %s, wifi: %s" % (name, dietary, alcohol, wheelchair, wifi)


if __name__ == '__main__':
    main()