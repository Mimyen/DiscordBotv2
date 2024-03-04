
# Function that increments saved log_id
def changeid() -> int:
    with open("DiscordBot/Bot/Config/log_id", "r+") as file:
        bid : int = int(file.read())

        file.truncate()
        file.seek(0)

        file.write(f"{bid + 1}")
        return bid

# Its just for style points, becuase you use it as log.id()
def id() -> int:
    return changeid()