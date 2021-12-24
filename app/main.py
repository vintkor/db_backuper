"""
Backup PostgreSQL database to AWS S3.
"""

import datetime
import os
import boto3


AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")


class Dumper:

    def __init__(self):
        self.DB_CONTAINER_NAME = os.getenv('DB_CONTAINER_NAME')
        self.DB_USER_NAME = os.getenv('DB_USER_NAME')
        self.POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
        self.POSTGRES_DB = os.getenv('POSTGRES_DB')
        self.filename = self._get_now_datetime_str()

    @staticmethod
    def say_hello():
        print('👋 Hi! This tool will dump PostgreSQL database, compress and encode it, and then send to AWS S3.\n')

    @staticmethod
    def _get_now_datetime_str():
        now = datetime.datetime.now()
        name_template = 'dump_{}.sql'

        return name_template.format(now.strftime('%Y-%m-%d__%H-%M-%S'))

    def dump_database(self):
        print("📦 Preparing database backup started")
        command = f'docker exec -i {self.DB_CONTAINER_NAME} /bin/bash -c ' \
                  f'"PGPASSWORD={self.POSTGRES_PASSWORD} ' \
                  f'pg_dump --username {self.DB_USER_NAME} {self.POSTGRES_DB}" > {self.filename}'

        dump_db_operation_status = os.WEXITSTATUS(os.system(command))

        if dump_db_operation_status != 0:
            exit(f"\U00002757 Dump database command exits with status {dump_db_operation_status}.")

        print("\U0001F510 DB dumped")

    def load_to_s3(self):
        client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        with open(self.filename, 'rb') as data:
            client.upload_fileobj(data, AWS_S3_BUCKET_NAME, self.filename)

        print("\U0001f680 Uploaded")

    def remove_temp_files(self):
        os.remove(self.filename)
        print("\U0001F44D That's all!")


if __name__ == "__main__":
    dumper = Dumper()
    dumper.say_hello()
    dumper.dump_database()
    dumper.load_to_s3()
    dumper.remove_temp_files()
