import os 
import logging.config
from dotenv import load_dotenv

from pythonjsonlogger import jsonlogger
import yaml


with open("logger_config.yml", 'r') as f:        
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)

logger = logging.getLogger('base_logger')


def load_envfile():
    dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        return os.environ
    else:
        raise Exception("Envfile doesn't exist")

def check_envs_exist(env_vars):
    for key in ("DB_NAME", "DB_USER", "DB_PASS", "DB_HOST"):
        if not env_vars.get(key):
            logger.error(f"Variable {key} not defined in env")
            raise Exception("Some value not present in envfile")
    return True

load_envfile()

ACCEPTED_REQUEST = "Спасибо, ваша заявка принята, мы с вами свяжемся в ближайшее время"
ACCEPTED_REQUEST_TO_ADMIN_MESSAGE = "Пользователь с почтой %s подал заявку"
WRONG_EMAIL_MESSAGE = "Похоже, вы ошиблись в адресе %s. Вы уверены, что правильно ввели аадрес своего почтового я щика?"
WITHOUT_EMAIL_MESSAGE = "Похоже, вы забыли добавить в свое сообщение аддрес почтового ящика. Отправьте его, пожал уйста, для регистрации заявки."
NEW_REQUEST = "Новый пользователь %S подал заявку"
SOMETHING_WENT_WRONG = "Похоже, что-то пошло не так, попробуйте, пожалуйста, еще раз"
SOMETHING_WENT_WRONG_WITH_USER = "Похоже, что-то пошло не так с добавление пользователя %s"

 # про форматирование хорошо https://shultais.education/blog/python-f-strings
token = os.environ.get("BOT_TOKEN")
root_address = "https://api.telegram.org/bot"

admin_chat_id = os.environ.get("ADMIN_CHAT_ID")
