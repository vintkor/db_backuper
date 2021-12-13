"""
Backup PostgreSQL database to Yandex Object Storage, that has S3 compatible API.
"""

import datetime
import os

import boto3


# S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
# BACKUP_KEY_PUB_FILE = os.getenv("BACKUP_KEY_PUB_FILE")
# TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Moscow")


class Dumper:

    def __init__(self):
        self.DB_CONTAINER_NAME = os.getenv('DB_CONTAINER_NAME')
        self.DB_USER_NAME = os.getenv('DB_USER_NAME')
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
        command = f'docker exec -t {self.DB_CONTAINER_NAME} pg_dumpall -c -U {self.DB_USER_NAME} > {self.filename}'
        dump_db_operation_status = os.WEXITSTATUS(os.system(command))

        if dump_db_operation_status != 0:
            exit(f"\U00002757 Dump database command exits with status {dump_db_operation_status}.")

        print("\U0001F510 DB dumped, archieved and encoded")

    def remove_temp_files(self):
        os.remove(self.filename)
        print("\U0001F44D That's all!")

# def get_s3_instance():
#     session = boto3.session.Session()
#     return session.client(
#         service_name='s3',
#         endpoint_url='https://storage.yandexcloud.net'
#     )
#
#
# def upload_dump_to_s3():
#     print("\U0001F4C2 Starting upload to Object Storage")
#     get_s3_instance().upload_file(
#         Filename=DB_FILENAME,
#         Bucket=S3_BUCKET_NAME,
#         Key=f'db-{get_now_datetime_str()}.sql.gz.enc'
#     )
#     print("\U0001f680 Uploaded")
#


if __name__ == "__main__":
    dumper = Dumper()
    dumper.say_hello()
    dumper.dump_database()
    dumper.remove_temp_files()
