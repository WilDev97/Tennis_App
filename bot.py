"""
Created on Thu Jul 13 20:16:44 2023

@author: Wilbur Williams
"""
import discord
import responses

chat_history = {}  # Dictionary to store chat history for each user

async def send_message(message, user_message, is_private):
    try:
        user_id = str(message.author.id)
        if user_id not in chat_history:
            chat_history[user_id] = {"messages": [], "last_bot_message": None, "state": "giving_recommendations"}

        response = responses.get_response(user_message)
        # Add mention to the response
        response = f'{message.author.mention}, {response}'
        embed = discord.Embed(
           description=response,
           color=discord.Color.yellow()
         
       )
        # embed.set_image(url="https://raw.githubusercontent.com/WilDev97/Ganjapp-Public/main/ganjapp_image_emb.jpg")

        await message.author.send(embed=embed) if is_private else await message.channel.send(embed=embed)

        # Store the user message and bot response in chat history
        chat_history[user_id]["messages"].append((user_message, response))
        chat_history[user_id]["last_bot_message"] = response

    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = 'MTEyOTIwNDU0MzE4NDQ0OTU0Nw.Gs-ita.n4UqDyNNCYMV9NA532uXsGGx1tS69vjAsrnOpc'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event #Fills bot status bar
    async def on_ready():
        await client.change_presence(activity=discord.Game(name = "Tennis Expert!"))
        print(f'{client.user} is now running!')
        
    @client.event #Gives users commands on arrival
    async def on_member_join(member):
        await member.send("Welcome to Serve Savant AI. Ask me anything tennis!")
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        if message.content.lower().startswith('prompt'):
        # Your code for initiating a new prompt goes here
            response = "Gimme a new question de man!"
            await message.channel.send(response)
            return

        # elif message.content.startswith('help'):
        #     embed2 = discord.Embed(title="Bot Commands", description="These are the commands available for GanjApp:", color=discord.Color.gold())
        #     embed2.add_field(name="help", value="Displays help message!", inline=False)
        #     embed2.add_field(name="prompt", value="New Prompt!", inline=False)
        #     await message.channel.send(embed = embed2)
        #     return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
            
        # # Print the chat history for the user
        # user_id = str(message.author.id)
        # recent_user_chats = chat_history[user_id][-3:]  # Get the last three user messages
        # for user_message in recent_user_chats:
        #     print(f"User: {user_message}")

    client.run(TOKEN)

