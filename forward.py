from telethon import TelegramClient, events
import time

api_id = 123
api_hash = 'apihash'
client = TelegramClient('messi', api_id, api_hash)
client.start()


async def get_message():
                                        # ID OF GROUP   
    message = await client.get_messages(-1001632822487, ids="" # ID OF MESSAGE TO FORWARD, COPY THE LINK AND COPY THE ID (LASTEST NUMBERS))
    return message


async def get_chat_id(group_link):
    entity = await client.get_entity(group_link)
    chat_id = entity.id
    return chat_id


with open("channels.txt", "r") as f:
    lines = f.readlines()
    with open("channels_ids.txt", "w") as w:
        for i in lines:
            chat_id = client.loop.run_until_complete(get_chat_id(i.strip()))
            print(chat_id)
            w.write(str(chat_id) + "\n")


async def forward_message():
    while True:
        with open("channels_ids.txt", "r") as y:
            lines = y.readlines()
            for id_chat in lines:
                chat_id = int(id_chat.strip())
                message = await get_message() 
                try:
                    await client.forward_messages(chat_id, message)
                except Exception as e:
                    print(f"Error in the chat {chat_id}. Message: {e}")
            time.sleep(120)


with client:
    client.loop.run_until_complete(forward_message())
