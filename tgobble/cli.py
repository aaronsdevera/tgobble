import os
import json
import random

import click

from tgobble.utils import from_base64
from tgobble import TGobble

####################################################################################################
# CREATE A TGOBBLE INSTANCE
####################################################################################################

####################################################################################################
# CLI ENTRY POINT
####################################################################################################
@click.group()
def cli():
    """tgobble: starter repo for CLI tools"""
    pass


####################################################################################################
# UTIL COMMANDS
####################################################################################################
@cli.group()
def utils():
    """Utilities, tools, and config commands."""
    pass

@utils.group()
def config():
    """Configuration commands."""
    pass

@config.command()
@click.option('--pretty', is_flag=True, help='Pretty print the output.')
def get( pretty ):
    """Display the current configuration."""
    results = TGobble().get_config()
    if pretty:
        click.echo( json.dumps( results, indent=4 ) )
    else:
        click.echo( json.dumps( results ) )

@config.command()
@click.argument('filepath')
@click.option('--pretty', is_flag=True, help='Pretty print the output.')
def load( filepath, pretty):
    """Load a new configuration file."""
    TGobble().load_config( filepath )
    results = TGobble().get_config()
    if pretty:
        click.echo( json.dumps( results, indent=4 ) )
    else:
        click.echo( json.dumps( results ) )

####################################################################################################
# SEARCH COMMANDS
####################################################################################################
@cli.group()
def search():
    """Search commands."""
    pass

@search.command()
@click.argument('query')
@click.option('--limit', '-l', default=100, help='Limit the number of results.')
@click.option('--pretty', is_flag=True, help='Pretty print the output.')
def chats( query, limit, pretty ):
    """Search utility for identifying chat info."""
    results =  TGobble().search_joined_chats(query, limit)
    if pretty:
        click.echo( json.dumps( results, indent=4 ) )
    else:
        click.echo( json.dumps( results ) )

@search.command()
@click.argument('query')
@click.option('--limit', '-l', default=100, help='Limit the number of results.')
@click.option('--pretty', is_flag=True, help='Pretty print the output.')
def messages( query, limit, pretty ):
    """Search utility for identifying chat info."""
    results =  TGobble().search_received_messages(query, limit)
    if pretty:
        click.echo( json.dumps( results, indent=4 ) )
    else:
        click.echo( json.dumps( results ) )

####################################################################################################
# SEARCH COMMANDS
####################################################################################################
@cli.group()
def search():
    """Search commands."""
    pass

@search.command()
@click.argument('query')
@click.option('--pretty', is_flag=True, help='Pretty print the output.')
def chats( query, pretty ):
    """Search utility for identifying chat info."""
    results =  TGobble().search_joined_chats(query)
    if pretty:
        click.echo( json.dumps( results, indent=4 ) )
    else:
        click.echo( json.dumps( results ) )

@search.command()
@click.argument('query')
@click.option('--pretty', is_flag=True, help='Pretty print the output.')
def messages( query, pretty ):
    """Search utility for messages."""
    results =  TGobble().search_received_messages(query)
    if pretty:
        click.echo( json.dumps( results, indent=4 ) )
    else:
        click.echo( json.dumps( results ) )

@search.command(name='url')
@click.argument('url')
@click.option('--pretty', is_flag=True, help='Pretty print the output.')
def search_url( url, pretty ):
    """Search url to identify chat info."""
    results =  TGobble().get_chat_from_url(url)
    if pretty:
        click.echo( json.dumps( results, indent=4 ) )
    else:
        click.echo( json.dumps( results ) )

####################################################################################################
# NOM COMMANDS
####################################################################################################
@cli.group()
def nom():
    """Message extraction commands. Omnomnom."""
    pass

@nom.command()
@click.argument('chat_id')
@click.option('--limit', '-l', default=100, help='Limit the number of results.')
@click.option('--pretty', is_flag=True, help='Pretty print the output.')
def chat( chat_id, limit, pretty ):
    """Dump messages by chat_id"""
    results =  TGobble().get_messages_by_id( chat_id if chat_id.startswith('-') else f'-{chat_id}', limit )
    if pretty:
        click.echo( json.dumps( results, indent=4 ) )
    else:
        click.echo( json.dumps( results ) )

@nom.command(name='url')
@click.argument('url')
@click.option('--limit', '-l', default=100, help='Limit the number of results.')
@click.option('--pretty', is_flag=True, help='Pretty print the output.')
def nom_url( url, limit, pretty ):
    """Dump messages by url. Use format "https://t.me/channelusername/1337"
    """
    results =  TGobble().get_message_from_url( url )
    if pretty:
        click.echo( json.dumps( results, indent=4 ) )
    else:
        click.echo( json.dumps( results ) )

@nom.command(name='photos')
@click.argument('url_or_file_id')
@click.option('--output', '-o', default='./', help='Output directory.')
def nom_photos( url_or_file_id, output ):
    """Dump media by message url or file id. Use format "https://t.me/channelusername/1337"
    """
    results =  TGobble().get_message_from_url( url_or_file_id )
    if len(results['results']) == 1:
        result = results['results'][0]
        media = result['photo']
        if media:
            click.echo( f"Downloading: {media['file_id']}")
            f = TGobble().get_file_by_id( media['file_id'])
            file_bytes = bytes(f.getbuffer())
            filename = f.name
            filepath = os.path.join( output, filename )
            open(filepath, 'wb').write( file_bytes )
            click.echo( f"Downloaded to: {filepath}")

@nom.command(name='file')
@click.argument('url_or_file_id')
@click.option('--output', '-o', default='./', help='Output directory.')
def nom_file( url_or_file_id, output ):
    """Dump media by message url or file id. Use format "https://t.me/channelusername/1337"
    """
    file_id = None
    if '/' in url_or_file_id:
        results =  TGobble().get_message_from_url( url_or_file_id )
        if len(results['results']) == 1:
            result = results['results'][0]
            print(result)
            media = result['']
            if media:
                media['file_id']
    else:
        file_id = url_or_file_id

    click.echo( f"Downloading: {file_id}")
    f = TGobble().get_file_by_id( file_id )
    file_bytes = bytes(f.getbuffer())
    filename = f.name
    filepath = os.path.join( output, filename )
    open(filepath, 'wb').write( file_bytes )
    click.echo( f"Downloaded to: {filepath}")