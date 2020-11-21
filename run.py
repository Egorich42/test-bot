import bot
from bot import message_manager,settings

if __name__ == "__main__":
    message_manager.run_pooling(7, settings.token)

