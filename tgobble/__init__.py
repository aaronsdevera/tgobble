from tgobble.const import DEFAULT_USER_AGENT
from tgobble.utils import generate_timestamp, generate_datetime_timestamp, generate_uuid
import os
import json
from pyrogram import Client

class TGobble:
    """TGobble base class"""
    user_agent: str = DEFAULT_USER_AGENT

    socks5: str = None

    pretty: bool = False

    config: str = None

    username: str = None
    api_id: str = None
    api_hash: str = None
    phone: str = None

    app: Client = None

    def __init__(self, socks5: str = None, user_agent: str = None, pretty: bool = False, config: str = None):
        if socks5:
            self.socks5 = socks5
        if user_agent:
            self.user_agent = user_agent
        if pretty:
            self.pretty = pretty
        
        self.load_config(config=config)

        self.app = self.create_client()

        pass
    
    def set_socks(self, socks5: str = None):
        '''Set socks5 proxy'''
        if socks5:
           self.socks5 = socks5 

    def set_user_agent(self, user_agent: str = None):
        '''Set user agent'''
        if user_agent:
            self.user_agent = user_agent 

    def find_config(self):
        '''Find config file'''
        files = [x for x in os.listdir() if x.startswith('config')]
        config = files[0] if len(files) == 1 else None
        if not config:
            print('No config file found')
            exit()
        return config

    def load_config(self, config: str = None):
        '''Load config file'''
        found_config = config if config else self.find_config()

        with open(found_config, 'r') as f:
            data = json.load(f)
            self.username = data['username'] if 'username' in data else None
            self.api_id = data['api_id'] if 'api_id' in data else None
            self.api_hash = data['api_hash'] if 'api_hash' in data else None
            self.phone = data['phone'] if 'phone' in data else None

        return
    
    def get_config(self):
        '''Get config data'''
        return {
            'username': self.username,
            'api_id': self.api_id,
            'api_hash': self.api_hash,
            'phone': self.phone
        }
    
    def create_client(self):
        '''Create Pyrogram client'''
        self.app = Client(
            self.username if self.username else self.phone,
            api_id=self.api_id,
            api_hash=self.api_hash,
            phone_number=self.phone,
            proxy=self.socks5
        )
        return self.app
    
    def client(self):
        '''Return Pyrogram client'''
        return self.app
    
    def search_joined_chats(self, query: str, limit: int = 100):
        '''Search chats'''
        results = []
        with self.app:
            for result in self.app.search_global(query, limit=limit):
                chat_dict = json.loads(str(result)).get('chat')
                if chat_dict not in results:
                    results.append(chat_dict)
            return {
                'timestamp': generate_datetime_timestamp(generate_timestamp()),
                'uuid': generate_uuid(),
                'action': 'search_joined_chats',
                'query': query,
                'results': results
            }
        
    def search_received_messages(self, query: str, limit: int = 100):
        '''Search messages'''
        results = []
        with self.app:
            for result in self.app.search_global(query, limit=limit):
                results.append(json.loads(str(result)))
            return {
                'timestamp': generate_datetime_timestamp(generate_timestamp()),
                'uuid': generate_uuid(),
                'action': 'search_received_messages',
                'query': query,
                'results': results
            }
        
    def get_chat_from_url(self, query: str):
        '''attempt to resolve chat id from a url'''
        results = []
        with self.app:
            chat_dict = json.loads(str(self.app.get_chat(query)))
            if chat_dict not in results:
                results.append(chat_dict)
            return {
                'timestamp': generate_datetime_timestamp(generate_timestamp()),
                'uuid': generate_uuid(),
                'action': 'get_chat_from_url',
                'query': query,
                'results': results
            }
        
    def get_messages_by_id(self, chat_id: int, limit: int = 100):
        '''Get messages by chat id'''
        results = []
        with self.app:
            for result in self.app.get_chat_history(chat_id, limit=limit):
                results.append(json.loads(str(result)))
            return {
                'timestamp': generate_datetime_timestamp(generate_timestamp()),
                'uuid': generate_uuid(),
                'action': 'get_messages_by_id',
                'chat_id': chat_id,
                'results': results
            }
        
    def get_message_from_url(self, url: str):
        '''Get message by url'''
        
        message_id = int(url.split('/')[-1])
        chat_identifier = url.split('/')[-2]
        chat_info = self.get_chat_from_url(chat_identifier)

        if not len(chat_info['results']) == 1:
            raise Exception(f'Multiple chat results found when searching: {url}')

        with self.app:

            chat_id = chat_info['results'][0]['id']
            
            chat_dict = json.loads(str(self.app.get_messages(chat_id=chat_id, message_ids=message_id)))

            return {
                'timestamp': generate_datetime_timestamp(generate_timestamp()),
                'uuid': generate_uuid(),
                'action': 'get_message_from_url',
                'query': url,
                'results': [chat_dict]
            }
        
    def get_file_by_id(self, file_id: str):
        '''Download file by file id'''
        with self.app:
            file = self.app.download_media(file_id, in_memory=True)
            return file