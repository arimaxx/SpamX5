from asyncio import sleep
from. import TheSpamX
from pyrogram import Client, filters
from pyrogram.types import Message

spam_chats = []

def add_command_help(module_name: str, commands: list) -> None:
    if module_name in CMD_HELP.keys():
        command_dict = CMD_HELP[module_name]
    else:
        command_dict = {}

    for command in commands:
        command_dict[command[0]] = command[1]

    CMD_HELP[module_name] = command_dict

def get_arg(message: Message) -> str:
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

### Pyrogram Event Handlers

@Client.on_message(filters.command("tagall", ".") & filters.me)
async def mentionall(client: Client, message: Message):
    chat_id = message.chat.id
    reply_message = message.reply_to_message
    args = get_arg(message)
    if not reply_message and not args:
        return await message.edit("**Send me a message or reply to a message!**")
    await message.delete()
    spam_chats.append(chat_id)
    user_count = 0
    user_text = ""
    async for user in client.get_chat_members(chat_id):
        if chat_id not in spam_chats:
            break
        user_count += 1
        user_text += f"[{user.user.first_name}](tg://user?id={user.user.id}), "
        if user_count == 5:
            if args:
                text = f"{args}\n\n{user_text}"
                await client.send_message(chat_id, text)
            elif reply_message:
                await reply_message.reply(user_text)
            await sleep(2)
            user_count = 0
            user_text = ""
    try:
        spam_chats.remove(chat_id)
    except ValueError:
        pass

@Client.on_message(filters.command("cancel", ".") & filters.me)
async def cancel_spam(client: Client, message: Message):
    if message.chat.id not in spam_chats:
        return await message.edit("**It seems there is no tagall here.**")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except ValueError:
            pass
        return await message.edit("**Cancelled.**")

### Command Help

add_command_help(
    "tagall",
    [
        ["tagall [text/reply ke chat]", "Tag all the members one by one"],
        ["cancel", "to stop.tagall"],
    ],
)
