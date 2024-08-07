import os
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from telethon import TelegramClient, events
    from telethon.tl.functions.channels import JoinChannelRequest
except ImportError:
    install('telethon')
    from telethon import TelegramClient, events
    from telethon.tl.functions.channels import JoinChannelRequest

try:
    import configparser
except ImportError:
    install('configparser')
    import configparser

try:
    from colorama import Fore
except ImportError:
    install('colorama')
    from colorama import Fore

import time
import asyncio

class Forwarder:
    def __init__(self):
        self.config_path = 'config.data'
        self.channels_path = 'channels.txt'
        self.channels_ids_path = 'channels_ids.txt'

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def setup(self):
        self.clear_screen()
        if os.path.exists(self.config_path):
            print(f"{Fore.RED}Configuration already exists!{Fore.RESET}")
            return

        acc = configparser.RawConfigParser()
        acc.add_section('cred')
        api_id = input(f"{Fore.LIGHTWHITE_EX}[+] Api ID: ")
        acc.set('cred', 'id', api_id)
        api_hash = input(f"{Fore.LIGHTWHITE_EX}[+] Api Hash ID: ")
        acc.set('cred', 'hash', api_hash)
        phone = input(f"{Fore.LIGHTGREEN_EX}[+] Phone Number (of account): ")
        acc.set('cred', 'phone', phone)

        with open(self.config_path, 'w') as setup:
            acc.write(setup)
        print(f"{Fore.GREEN}Configuration set up successfully.{Fore.RESET}")

    def start(self):
        self.clear_screen()
        if not os.path.exists(self.config_path):
            print(f"{Fore.RED}Configuration does not exist. Set up your account first!{Fore.RESET}")
            return

        file = configparser.RawConfigParser()
        file.read(self.config_path)
        api_id = file['cred']['id']
        api_hash = file['cred']['hash']
        phone = file['cred']['phone']
        client = TelegramClient(phone, api_id, api_hash)
        client.start()

        ch1 = int(input("Channel ID: "))
        id1 = int(input("Message ID: "))

        async def get_message():
            message = await client.get_messages(ch1, ids=id1)
            return message

        async def get_chat_id(group_link):
            entity = await client.get_entity(group_link)
            return entity.id

        async def write_channel_ids():
            with open(self.channels_path, "r") as f, open(self.channels_ids_path, "w") as w:
                for line in f:
                    chat_id = await get_chat_id(line.strip())
                    print(chat_id)
                    w.write(f"{chat_id}\n")

        async def forward_message():
            while True:
                with open(self.channels_ids_path, "r") as y:
                    for id_chat in y:
                        chat_id = int(id_chat.strip())
                        message = await get_message()
                        try:
                            await client.forward_messages(chat_id, message)
                        except Exception as e:
                            print(f"Error in chat {chat_id}. Message: {e}")
                await asyncio.sleep(120)

        async def main():
            await write_channel_ids()
            await forward_message()

        with client:
            client.loop.run_until_complete(main())

    def join_group(self):
        self.clear_screen()
        if not os.path.exists(self.config_path):
            print(f"{Fore.RED}Configuration does not exist. Set up your account first!{Fore.RESET}")
            return

        configf = configparser.RawConfigParser()
        configf.read(self.config_path)

        api_id = configf['cred']['id']
        api_hash = configf['cred']['hash']
        phone = configf['cred']['phone']
        client = TelegramClient(phone, api_id, api_hash)

        async def join_group(group_link):
            entity = await client.get_entity(group_link)
            await client(JoinChannelRequest(entity))

        async def join_all_groups():
            with open(self.channels_path) as f:
                for link in f:
                    link = link.strip()
                    try:
                        await join_group(link)
                        print(f"{Fore.LIGHTGREEN_EX}Joined Successfully! {link}")
                    except Exception as e:
                        print(f"Failed to join {link}. \nError: {e}")

        with client:
            client.loop.run_until_complete(join_all_groups())

if __name__ == "__main__":

    forwarder = Forwarder()
    forwarder.clear_screen()
    print(f"{Fore.GREEN}―――― @Lawxsz Telegram Tool ――――")
    print(f"\n{Fore.YELLOW}1: Setup Account\n2: Start Forwarding\n3: Join to Groups")
    enter = input("")
    if enter == "1":
        forwarder.setup()
    elif enter == "2":
        forwarder.start()
    elif enter == "3":
        forwarder.join_group()
    else:
        print("ERROR, choose a valid option.")
