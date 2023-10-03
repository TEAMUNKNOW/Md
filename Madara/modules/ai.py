import requests
import httpx
from pyrogram import filters, Client, idle
from pyrogram.types import Message
from Madara import pgram as app


# Dictionary to store the conversation history for each user
conversation_history = {}

@app.on_message(filters.command("chat"))
async def gpt(_: Client, message: Message):
    txt = await message.reply("💬")

    if len(message.command) < 2:
        return await txt.edit("Please provide a message too.")

    query = message.text.split(maxsplit=1)[1]

    # Retrieve conversation history for this user
    chat_id = message.chat.id
    if chat_id in conversation_history:
        dialog_messages = conversation_history[chat_id]
    else:
        dialog_messages = []

    url = "https://api.safone.me/chatgpt"
    payload = {
        "message": query,
        "chat_mode": "assistant",
        "dialog_messages": dialog_messages,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        try:
            response = await client.post(
                url, json=payload, headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            results = response.json()

            # Check if the API response contains the 'message' key
            if "message" in results:
                bot_response = results["message"]

                # Update conversation history with the latest message
                dialog_messages.append({"bot": bot_response, "user": query})
                conversation_history[chat_id] = dialog_messages

                await txt.edit(bot_response)
            else:
                await txt.edit("**An error occurred. No response received from the API.**")
        except httpx.HTTPError as e:
            await txt.edit(f"**An HTTP error occurred: {str(e)}**")
        except Exception as e:
            await txt.edit(f"**An error occurred: {str(e)}**")


# Bing code

API_URL = "https://sugoi-api.vercel.app/search"

@app.on_message(filters.command("bing"))
async def bing_search(client: Client, message: Message):
    try:
        if len(message.command) == 1:
            await message.reply_text("Please provide a keyword to search.")
            return

        keyword = " ".join(
            message.command[1:]
        )  # Assuming the keyword is passed as arguments
        params = {"keyword": keyword}
        response = requests.get(API_URL, params=params)

        if response.status_code == 200:
            results = response.json()
            if not results:
                await message.reply_text("No results found.")
            else:
                message_text = ""
                for result in results[:7]:
                    title = result.get("title", "")
                    link = result.get("link", "")
                    message_text += f"{title}\n{link}\n\n"
                await message.reply_text(message_text.strip())
        else:
            await message.reply_text("Sorry, something went wrong with the search.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

BASE_URL = 'https://api.safone.me'

def ask_bard(question):
    endpoint = f"{BASE_URL}/bard"
    headers = {'Content-Type': 'application/json'}
    body = {'message': question}
    
    try:
        response = requests.post(endpoint, json=body, headers=headers)
        response_data = response.json()
        
        if response.ok:
            choices = response_data.get('choices', [])
            if choices:
                return choices[0]['content'][0]
            else:
                return "Error: No response content found."
        else:
            print(f"Error: {response.status_code}, {response_data}")
            return f"Error: {response.text}"
    except requests.RequestException as e:
        return f"Error occurred: {e}"

# Command handler for the /ask command
@app.on_message(filters.command("bard", prefixes="/"))
async def ask_command_handler(client: Client, message: Message):
    question = " ".join(message.command[1:])
    if question:      
        response_content = ask_bard(question)
        await message.reply(response_content)
    else:
        await message.reply("Please provide a question after the /ask command.")



__help__= """
AI-Powered Chatbot.

*Available commands:*

 ➛ /chat - Chat with me. Usage: /chat hey
 ➛ /bing <keyword>
For example: /bing cats
 ➛ /bard - Chat with me. Usage: /bard who are you
"""

__mod_name__ = "ᗩI ᑕᕼᗩT"   
__command_list__ = [
    "chat",
    "bing",
    "bard",
      ]
