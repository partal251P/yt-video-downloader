from pytube import YouTube
import mergesort


def searching_in_streams( response, format):
    """
    Will take a list with all the objects and will sort them
    :param response: str()
    :param format: str()
    :return: list(), list()
    """
    temp_list = {}
    if format == 2:
        stream = YouTube(response).streams.filter(file_extension="mp4")
    elif format == 1:
        stream = YouTube(response).streams.filter(only_audio=True)

    for element in stream:  # Creation of the dict with the quality : id
        if format == 1 and element.abr:
            temp_list[element.abr] = element.itag
        elif format == 2 and element.resolution:
            temp_list[element.resolution] = element.itag

    if format == 1:  # Will use the function fusion to sort the different ints (quality)
        a = [i[:-4] for i in temp_list.keys()]
        sorted_audio = [i + "kbps" for i in mergesort.fusion(a)]
        return temp_list, sorted_audio
    else:
        a = [i[:-1] for i in temp_list.keys()]
        sorted_audio = [i + "p" for i in mergesort.fusion(a)]
        return temp_list, sorted_audio


def quality_check(response, format):
    """
    Sort the different quality available for the video in question by using the mergesort
    :param response: str()
    :param format: str()
    :return: list(), list()
    """
    if format == 2:
        sorted_resolutions = searching_in_streams(response, format)
        return sorted_resolutions

    elif format == 1:
        sorted_audio = searching_in_streams(response, format)
        return sorted_audio