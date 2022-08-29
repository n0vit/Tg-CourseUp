
from re import I
from time import sleep
import motor.motor_asyncio
from beanie import init_beanie
import subprocess
from .data_model import CourseModel


def initServer():
    process_id = subprocess.run('pgrep mongod', shell=True, stdout=subprocess.PIPE)
    print(process_id.stdout.decode())
    if len(process_id.stdout.decode()) !=0:
        subprocess.run("sudo kill {}".format(process_id.stdout.decode()), shell=True, input="Nov15".encode())
        sleep(2)
    subprocess.run("sudo /opt/homebrew/bin/mongod --config /opt/homebrew/etc/mongod.conf  --logpath /Users/nikolai/mongo.log --fork", shell=True, input="Nov15".encode())





async def init():
        # Beanie uses Motor under the hood 
    client = motor.motor_asyncio.AsyncIOMotorClient()
    print(client.server_info())
    await init_beanie(database=client.db_Course, document_models=[CourseModel])
     
