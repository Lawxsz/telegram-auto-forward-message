from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
import os
import configparser
from colorama import Fore
import time

class Forwarder:
    def setup(self):
        os.system("cls")
        if os.path.exists("config.data"):
            print(f"{Fore.RED}Configuration already exists!{Fore.RESET}")
            return

        acc = configparser.RawConfigParser()
        acc.add_section('cred')
        api_id = input(f"{Fore.LIGHTWHITE_EX}[+] Api ID : ")
        acc.set('cred', 'id', api_id)
        api_hash = input(f"{Fore.LIGHTWHITE_EX}[+] Api Hash ID : ")
        acc.set('cred', 'hash', api_hash)
        phone = input(f"{Fore.LIGHTGREEN_EX}[+] Phone Number (of account) : ")
        acc.set('cred', 'phone', phone)

        with open('config.data', 'w') as setup:
            acc.write(setup)
        print(f"{Fore.GREEN}Configuration set up successfully.{Fore.RESET}")

    def start(self):
        os.system("cls")
        if not os.path.exists("config.data"):
            print(f"{Fore.RED}Configuration does not exist. Set up your account first!{Fore.RESET}")
            return

        file = configparser.RawConfigParser()
        file.read('config.data')
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
                            print(f"Error in chat {chat_id}. Message: {e}")
                    time.sleep(120)

        with client:
            client.loop.run_until_complete(forward_message())

    def join_group(self):
        os.system("cls")
        if not os.path.exists("config.data"):
            print(f"{Fore.RED}Configuration does not exist. Set up your account first!{Fore.RESET}")
            return

        configf = configparser.RawConfigParser()
        configf.read('config.data')

        api_id = configf['cred']['id']
        api_hash = configf['cred']['hash']
        phone = configf['cred']['phone']
        client = TelegramClient(phone, api_id, api_hash)

        async def join_group(group_link):
            entity = await client.get_entity(group_link)
            await client(JoinChannelRequest(entity))

        with client:
            with open('channels.txt') as f:
                group_links = f.readlines()
                for link in group_links:
                    link = link.strip()
                    try:
                        client.loop.run_until_complete(join_group(link))
                        print(f"{Fore.LIGHTGREEN_EX}Joined Successfully! {link}")
                    except Exception as e:
                        print(f"Failed to join {link}. \nError: {e}")

if __name__ == "__main__":
    forwarder = Forwarder()
    os.system("cls")
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
