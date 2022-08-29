from pyrogram import Client,filters
class StopBot:
    @Client.on_message(filters.command('stop'))
    async def stop_bot(client: Client, message):
        client.stop()