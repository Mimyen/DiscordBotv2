# General
ICON_URL = "https://cdn.discordapp.com/attachments/1194995669988016218/1200539924085080064/image.png?ex=65c68cee&is=65b417ee&hm=d7dfe03ab65a1acc704c18182bbe2a5ed7a44caddd45394c5488c29c0adc2319&"

# Help Extension
COMMAND_HELP_NAME = "help"
COMMAND_HELP_DESCRIPTION = "Get information about any command"
COMMAND_HELP_IGNORED_COMMANDS = [
            "connect",
            "disconnect",
            "test3",
            "getgid",
            "help",
            "test4"
]

# Music Extension
MUSIC_PATH = "Temp/music/"

LINKEXCEPTION = "Provided link doesn't match requirements"

LISTENER_ONMOVE_DISCONNECT = "Bot disconnected from voice channel"

COMMAND_CONNECT_NAME = "connect"
COMMAND_CONNECT_DESCRIPTION = "Connects to voice channel that user is connected to"
COMMAND_CONNECT_CONNECTED = "Connected to your voice channel"
COMMAND_CONNECT_ERROR = "Either you I'm already connected to voice channel or you aren't in one!"

COMMAND_DISCONNECT_NAME = "disconnect"
COMMAND_DISCONNECT_DESCRIPTION = "Disconnects bot from voice channel in your guild"
COMMAND_DISCONNECT_DISCONNECTED = "Disconnected from voice channel"
COMMAND_DISCONNECT_NO_VC = "No voice channel to disconnect from"

COMMAND_PLAY_NAME = "play"
COMMAND_PLAY_DESCRIPTION = "Adds song to playlist, if nothing is currently playing makes bot play that song"
COMMAND_PLAY_QUERY = "Song to play, either link or youtube-search"
COMMAND_PLAY_ERROR = "You aren't connected to any voice channel"
COMMAND_PLAY_PLAYING = "Playing now"
COMMAND_PLAY_ADDED = "Added to playlist"

COMMAND_PLAYLIST_NAME = "playlist"
COMMAND_PLAYLIST_DESCRIPTION = "Outputs current playlist"
COMMAND_PLAYLIST_CURRENT = "Current playlist"
COMMAND_PLAYLIST_EMPTY = "Playlist is empty"

COMMAND_SKIP_NAME = "skip"
COMMAND_SKIP_DESCRIPTION = "Skips current songs"
COMMAND_SKIP_SKIPPED = "Skipped song"
COMMAND_SKIP_NOTRACK = "No track is currently playing!"

COMMAND_CURRENTSONG_NAME = "currentsong"
COMMAND_CURRENTSONG_DESCRIPTION = "Replies with song that is currently playing"
COMMAND_CURRENTSONG_CURRENT = "Current song"
COMMAND_CURRENTSONG_NOSONG = "No song is currently playing"

COMMAND_PAUSE_NAME = "pause"
COMMAND_PAUSE_DESCRIPTION = "Pauses the bot"
COMMAND_PAUSE_PAUSE = "Playing has been paused"
COMMAND_PAUSE_ERROR = "Bot isn't playing"

COMMAND_RESUME_NAME = "resume"
COMMAND_RESUME_DESCRIPTION = "Resumes the bot"
COMMAND_RESUME_RESUME = "Playing has been resumed"
COMMAND_RESUME_ERROR = "Playing isn't paused"

COMMAND_CLEAR_NAME = "clear"
COMMAND_CLEAR_DESCRIPTION = "Clears the playlist"
COMMAND_CLEAR_CLEAR = "Playlist has been cleared"
COMMAND_CLEAR_ERROR = "Playlist is empty"

COMMAND_STOP_NAME = "stop"
COMMAND_STOP_DESCRIPTION = "Stop the bot"
COMMAND_STOP_STOP = "Playing has been stopped"
COMMAND_STOP_ERROR = "Bot is not playing"

COMMAND_REMOVE_NAME = "remove"
COMMAND_REMOVE_DESCRIPTION = "Removes given track from playlist (by number from /playlist)"
COMMAND_REMOVE_ID = "Id of the song"
COMMAND_REMOVE_REMOVED = "Removed track from playlist:"
COMMAND_REMOVE_ERROR = "No track with such id"

# Pawel Extension
COMMAND_ILE_NAME = "ile"
COMMAND_ILE_DESCRIPTION = "Ile kodu napisał dzisiaj Paweł?"
COMMAND_ILE_P1 = "Paweł napisał dzisiaj "
COMMAND_ILE_P2 = " linijek kodu. 🖊️"

COMMAND_MILOSC_NAME = "milosc"
COMMAND_MILOSC_DESCRIPTION = "Sprawdź czy te osoby się kochają ❤️"
COMMAND_MILOSC_IMIE1 = "Imie pierwszej osoby"
COMMAND_MILOSC_IMIE2 = "Imie drugiej osoby"
COMMAND_MILOSC_ODPOWIEDZI = [
    "kochają się",
    "nie kochają się",
    "są zakochani, takiej miłosci to ty kolego w życiu nie widzialeś"
]

COMMAND_PAWELNADZIS_NAME = "pawelnadzis"
COMMAND_PAWELNADZIS_DESCRIPTION = "Zobacz jakiego Pawła dziś mamy!"
COMMAND_PAWELNADZIS_TEKST = "Paweł na dziś: "
COMMAND_PAWELNADZIS_PAWLY = [
    "Paweł kox 💪",
    "Paweł beta 😒",
    "Paweł programista 🤓",
    "Paweł pizda 🍑",
    "Paweł sterydziarz 💉",
    "Paweł autysta 🤓",
    "Paweł romantyk 😍",
    "Paweł siłacz 💪",
    "Paweł incel 🤓",
    "Paweł koder 🤓",
]

# Sync Extension
COMMAND_SYNC_SYNCHRONIZING = "Synchronizing bot commands"

# General TTO Paths
BOARD_ASSETS_PATH = "Bin/TTO/"
BOARD_SAVE_PATH = "Temp/Boards/"

# TicTacToe Extension
COMMAND_CREATEGAME_NAME = "createttt"
COMMAND_CREATEGAME_DESCRIPTION = "Creates a game of TicTacToe"
COMMAND_CREATEGAME_PLAYERSTARTS = "Choose who starts"
COMMAND_CREATEGAME_DIFFICULTY = "Choose the difficulty of a bot"

# TicTacToePVP Extension
COMMAND_CREATEGAMEPVP_NAME = "createpvp"
COMMAND_CREATEGAMEPVP_DESCRIPTION = "Creates a game of TicTacToe between two players"
COMMAND_CREATEGAMEPVP_PLAYERONE = "Mention player who starts"
COMMAND_CREATEGAMEPVP_PLAYERTWO = "Mention second player"

# AI Extension
GPT_DEFAULT_SETTINGS = "Behave like gpt 3.5, answer in language that you are asked in"

COMMAND_GPTASK_NAME = "gptask"
COMMAND_GPTASK_DESCRIPTION = "Ask ai a question"
COMMAND_GPTASK_QUERY = "Insert your question here"

# Stock Market Extension
CRYPTO_PATH = "Temp/cryptocurrency/"


# ManagerApp Extension
MANAGER_IP = '127.0.0.1'
MANAGER_PORT = 2223

MANAGER_PASSWORD = "pawel&ola=dobrePolacz3nie"

MANAGER_RESPONSE = "response"
MANAGER_RESPONSE_ERROR = "Error"
MANAGER_RESPONSE_TOKEN = "Token"
MANAGER_RESPONSE_CORRECT = "Correct input"
MANAGER_RESPONSE_AUTHORIZED = "Authorized"
MANAGER_RESPONSE_ALREADY_AUTHORIZED = "Already authorized"
MANAGER_RESPONSE_OUTPUT = "output"
MANAGER_RESPONSE_MESSAGE = "message"
MANAGER_RESPONSE_NO_ACCEESS = "No access"
MANAGER_RESPONSE_INCORRECT_CALL = "Incorrect socket call"
MANAGER_RESPONSE_INVALID_JSON = "Invalid JSON"
MANAGER_RESPONSE_INCORRECT_PASSWORD = "Password is incorrect"
MANAGER_RESPONSE_INCORRECT_AUTH_DATA = "Incorrect authorization data"
MANAGER_RESPONSE_NO_ACCESS = "No access"
MANAGER_RESPONSE_INCORRECT_GUILD_ID = "Incorrect guild_id"
MANAGER_RESPONSE_SEND_MESSAGE_SENT = "Message sent"
MANAGER_RESPONSE_SEND_MESSAGE_ERROR = "Incorrect send_message data"
