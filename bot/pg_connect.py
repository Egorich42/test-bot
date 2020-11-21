import os 
import psycopg2
import settings
from settings import logger

# Про энвфалый https://habr.com/ru/post/472674/
# про работу с Постгрей https://khashtamov.com/ru/postgresql-python-psycopg2/

class WorkWithPostgres:
    env_vars = settings.load_envfile() 
    settings.check_envs_exist(env_vars)

    def conn_to_db(self):
        try: 
            conn = psycopg2.connect(dbname=self.env_vars["DB_NAME"], 
                                    user=self.env_vars["DB_USER"],
                                    password=self.env_vars["DB_PASS"],
                                    host=self.env_vars["DB_HOST"],
                                    connect_timeout=30
                                    )
            return conn
        except Exception as e: #TIMEOUT
            logger.error(e)
            raise Exception(e)

    def write_new_student(self, telegram:str, email:str):
        conn = self.conn_to_db()
        cursor = conn.cursor()
        if cursor:
            # email add validation
            insert_student_command = "INSERT INTO students (telegram, email) VALUES (%s, %s)"
            try:

                logger.info(f"Trying execute command {insert_student_command} ")
                cursor.execute(insert_student_command, (telegram, email))
                conn.commit()
                logger.info(f"Command {insert_student_command} was executed succesfully")
                cursor.execute(insert_student_command, (telegram, email))
                cursor.close()
                logger.info("Cursor closed ")
                conn.close()
                logger.info("Connection closed")
                return True
            except Exception as e:
                logger.error(e)
                raise Exception(e)
        else:
            logger.error("Something wrong with Postgres - cursor is None")
            raise Exception("Something wrong with Postgres - cursor is None")
    

# new = WorkWithPostgres()
# - get message
# - check message on email
# new.write_new_student("Egorich42", "pochta@il")

# CHECK_ENVFILE, TIMEOT, NO ACCESS, WRONG_DB, unique_vaues 

# сделвть email unique полем

