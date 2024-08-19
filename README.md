# tgobble
Gobbling up Telegram attachments

## installing

If you have [`poetry`](https://python-poetry.org/) you can do enter the repo and run `poetry install` and you can just use `poetry run tgobble` from the command line.

Otherwise you can do a build like `poetry build` and install the resulting `.whl` binary.

## example config file

You can get the `api_id` and the `api_hash` by going to [my.telegram.org](https://my.telegram.org), authenticating, and creating "a new app" from the options on the webpage.

```
{
    "phone": "+<phone>",
    "api_id": "<id>>",
    "api_hash": "<hash>"
}
```

## easy mode usage

Assuming you know the telegram url where the attachment is at:

```
tgobble nom photos 'https://t.me/TheDarkWebInformer/2444'
```

This will download the attachments to a file. Use `-o/--output` to direct the file to filepath output.

If you know the file ID, its even quicker:

```
tgobble nom file BQACAgIAAx0CXLUsCAACj_Bmwq5WuCfhdicrjEHdncl7kMqVagACH0sAAkffiEnLgzooQU_bOB4E
```

## how to find the file id

There are some tools built into `tgobble` to help you find the `file_id`

**searching for a chat**
```
tgobble search chats 'BF V3 Files'
```

from the output you will want to find the chat `id.

**dumping messages from a chat**

```
tgobble nom chat 1001555377160 --pretty --limit 100
```

Now that you have the ID, you can dump the chat with the `nom` command. Use `-l/--limit` to specify the maximum number of messages and `-p/--pretty` to pretty print.

**getting the files from a specific message**

after dumping the messages, hopefully you find the one you wanted. Get the file ID, and throw it in:

```
tgobble nom file BQACAgIAAx0CXLUsCAACj_Bmwq5WuCfhdicrjEHdncl7kMqVagACH0sAAkffiEnLgzooQU_bOB4E
```