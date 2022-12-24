import telebot
import config
from pytube import YouTube, exceptions


# Class containing info about YouTube video
class YTAudio:
    def __init__(self):
        self.streams = None  # Interface to query both adaptive (DASH) and progressive streams
        self.title = None  # Title of the video
        self.description = None  # Video description
        self.duration = None  # Video length
        self.author = None  # Video uploader
        self.views = None  # Current views on the video
        self.thumbnail = None  # Video thumbnail


# Checking if the video is available
def validate_link(yt):
    try:
        yt.check_availability()
        return True
    except exceptions.VideoUnavailable:
        return False


# Getting information about the video
def get_info(yt_link):
    try:
        yt = YouTube(yt_link)
    except exceptions.RegexMatchError:
        return False

    if not validate_link(yt):
        return False
    else:
        yt_streams = yt.streams
        yt_title = yt.title
        yt_author = yt.author
        yt_desc = yt.description
        yt_dur = yt.length
        yt_views = yt.views
        yt_thumb = yt.thumbnail_url
        return yt_streams, yt_title, yt_author, yt_desc, yt_dur, yt_views, yt_thumb


if __name__ == '__main__':
    # Crating the bot with the token given by @BotFather
    bot = telebot.TeleBot(config.TOKEN)


    @bot.message_handler(commands=['start'])
    def welcome(message):
        chat_id = message.chat.id

        bot.send_message(chat_id, "Hi")


    # Handling incoming messages
    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        chat_id = message.chat.id

        link = message.text  # Get user text (should be a yt url)
        audio_info = get_info(link)

        # Validating url
        if not audio_info[0]:
            bot.send_message(chat_id, "Something wrong, I can feel it")
        else:
            bot.send_audio(chat_id, "Let's go!")

# Launch
bot.polling(none_stop=True)
