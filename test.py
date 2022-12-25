from src.main import validate_link, get_info
from pytube import YouTube

test_url1 = 'https://www.youtube.com/watch?v=NMA_isZYsYQ'  # Video not available in this country
test_url2 = 'you.tube.com/watch?v=NMA_i'  # Not a link
test_url3 = 'https://www.youtube.com/watch?v=NMRhx71bGo4&list=PL8eonCDjyJ7EpHQ8IFYjIAikxkOeAMGKJ&index=1409'


def test_validate_url():
    yt1 = YouTube(test_url1)
    yt2 = YouTube(test_url3)

    answer1 = False
    answer2 = True

    assert validate_link(yt1) == answer1
    assert validate_link(yt2) == answer2


def test_get_info_1():
    answer1 = (False, 'Please send a YT link :-)')
    answer2 = (False, 'Video unavailable 😕')

    assert get_info(test_url2) == answer1
    assert get_info(test_url1) == answer2


def test_get_info_2():
    answer1 = 'Let It Happen'
    answer2 = 'Tame Impala - Topic'
    answer3 = 468
    answer4 = 38093210

    assert get_info(test_url3)[1] == answer1
    assert get_info(test_url3)[2] == answer2
    assert get_info(test_url3)[4] == answer3
    assert get_info(test_url3)[5] >= answer4
