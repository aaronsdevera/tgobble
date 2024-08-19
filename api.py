import os
import json
import asyncio

import click
from pyrogram import Client

def load_config():
    files = [x for x in os.listdir() if x.startswith('config')]
    config = files[0] if len(files) == 1 else None
    if not config:
        print('No config file found')
        exit()

    username = None
    api_id = None
    api_hash = None
    phone = None

    with open(config, 'r') as f:
        data = json.load(f)
        username = data['username']
        api_id = data['api_id']
        api_hash = data['api_hash']
        phone = data['phone']

    return username, api_id, api_hash, phone

with open(config, 'r') as f:
    data = json.load(f)
    username = data['username']
    api_id = data['api_id']
    api_hash = data['api_hash']
    phone = data['phone']

app = Client(phone, api_id, api_hash)

async def main():
    async with  as app:
        '''
        async for message in app.get_chat_history(chat_id):
            print(message.text)
        '''
        query = 'BF Repo V3 Files'
        async for result in app.search_global(query, limit=50):
            chat_id = result.chat.id
            title = result.chat.title
            print(f'{chat_id} - {title}')

'''
api_id = 12345
api_hash = "0123456789abcdef0123456789abcdef"


async def main():
    async with Client("my_account", api_id, api_hash) as app:
        await app.send_message("me", "Greetings from **Pyrogram**!")

'''
if __name__ == '__main__':
    asyncio.run(main())
