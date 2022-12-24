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
        err_msg = "Please send a YT link :-)"
        return False, err_msg

    if not validate_link(yt):
        err_msg = "Video unavailable 😕"
        return False, err_msg
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

    # For multiuser support, chats will contain chat ids, as well as current audio info
    chats = {}
    # For displaying the appropriate error
    error_msg = None

    # Handling /start command
    @bot.message_handler(commands=['start'])
    def welcome(message):
        chat_id = message.chat.id  # Get chat id

        yt_audio = YTAudio()
        chats[chat_id] = yt_audio
        # Welcome message
        bot.send_message(chat_id,
                         "Welcome, {0.first_name}!\n"
                         "I am a bot for converting YouTube videos to downloadable audio."
                         "\n\nPlease send a link to a YT video to start :-)"""
                         "\n\n<b>Available commands:</b>"
                         "\n/start - initialize the bot"
                         "\n/help - to see available commands"
                         "\n/info - to get info about the last video".format(message.from_user, bot.get_me()),
                         parse_mode='html')

    # Handling /help command
    @bot.message_handler(commands=['help'])
    def command_help(message):
        chat_id = message.chat.id  # Get chat id
        # Help message
        bot.send_message(chat_id, "<b>Available commands:</b>"
                                  "\n/start - initialize the bot"
                                  "\n/help - to see available commands"
                                  "\n/info - to get info about the last video",
                         parse_mode='html')

    # Handling incoming messages
    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        chat_id = message.chat.id

        link = message.text  # Get user text (should be a yt url)
        audio_info = get_info(link)

        # Validating url
        if not audio_info[0]:
            bot.send_message(chat_id, audio_info[1])
        else:
            try:
                bot.send_audio(chat_id, "Let's go!")
            except telebot.apihelper.ApiTelegramException:
                bot.send_message(chat_id, "Audio of such size cannot be sent through telegram 🤓")
            except Exception:
                bot.send_message(chat_id, "Something went wrong 🤔")

# Launch
bot.polling(none_stop=True)
