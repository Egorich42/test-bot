import re 
from dotenv import load_dotenv
from settings import logger

def extract_email_from_str(message:str):
    match = re.search(r'[\w\.-]+@[\w\.-]+', message)
    if match:
        result = match.group(0)
        return result
    else:
        logger.error(f"Email in message {message} was not founded")
        return False 

def check_email(email:str):  
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(email_regex,email)):  
        logger.info(f"Email {email} is valid")
        return True  
    else: 
        logger.error(f"Email {email} is invalid")
        return False
