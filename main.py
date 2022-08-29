import asyncio
from lib.data.db_start import init, initServer
from loader import app
import uvloop
from pyrogram.methods.utilities.idle import idle
async def main():

    uvloop.install()
    initServer()
    await init()
    await app.start()
    await idle()
    
 
if __name__ == '__main__':
    loop= asyncio.get_event_loop()
    loop.run_until_complete(main())
