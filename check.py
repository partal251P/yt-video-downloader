def check_link(link):
    while True:
        if not len(link) in [43, 76]:
            link = input("Error, you entered a invalid link "
                         "(you maybe entered a link to a playlist insteed of a single video). "
                         "Enter the correct link:\n>>")
        else:
            break
    return link


def check_format(format):
    while True:
        if format not in ["1", "2"]:
            format = input("You entered a wrong format, try again. Entered the correct format you want "
                           "to download: \n(1) Mp3\n(2) Mp4\n>>")
        else:
            break
    return format

def check_choice(choice):
    while True:
        if choice not in ["1", "2"]:
            choice = input("You entered a wrong input, try again. Do you want to download:\n"
                       "(1) Playlist\n"
                       "(2) Single video\n>>")
        else:
            break
    return choice