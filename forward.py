from telethon import TelegramClient, events
import time
import os
import configparser
from colorama import Fore




class Forwarder:
    def setup():
        if os.path.exists("config.data"):
            acc = configparser.RawConfigParser()
            
            acc.add_section('cred')
            api_id = input(f"{Fore.LIGHTWHITE_EX}[+] Api ID : ")
           
            acc.set('cred', 'id', api_id)
            api_hash = input(f"{Fore.LIGHTWHITE_EX}[+] Api Hash ID : ")
           
            acc.set('cred', 'hash', api_hash)
            phone = input(f"{Fore.LIGHTGREEN_EX}[+] Phone Number (of acc) : ")
           
            acc.set('cred', 'phone', phone)
            setup = open('config.data', 'w')
           
            acc.write(setup)
            setup.close()   
            
    def start():
        file = configparser.RawConfigParser()
        file.read('config.data')
        api_id = file['cred']['id']
        api_hash = file['cred']['hash']
        phone = file['cred']['phone']
        client = TelegramClient(phone, api_id, api_hash)        
        client.start()
        async def get_message():
            message = await client.get_messages(-1001632822487, ids=83)
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
forwarder = Forwarder
enter = input("¿You want to SETUP a account? 1: \n¿You want to Start the Forwarder? 2: ")
if enter == "1":
    forwarder.setup()
elif enter == "2":
    forwarder.start()
else:
    print("ERROR, choice a valid option bro!")
