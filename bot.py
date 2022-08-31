import os
import discord
from response_handler import ResponseHandler

response_handler = ResponseHandler("inspire")
bot_token = os.getenv("BOT_TOKEN")

class MyClient(discord.Client):            
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        self.channel = self.get_channel(1008853405751590915)


    async def on_message(self, message):
        if message.content == 'ping':
            await message.channel.send('pong')
        
        if message.content == "/date":
            await self.channel.send("Input the desired date in MM/DD/YYYY format")
            msg = await self.wait_for("message")
            date = msg.content.split('/')
            if len(date) != 3: return await self.channel.send("Wrong format. Try again.")

            availability = response_handler.get_specific_date(date)

            if(not availability): return await self.channel.send("Date not available")

            else:
                availabile_parks = []
                for park in availability:
                    availabile_parks.append(park)
                
                if(len(availabile_parks) == 2):
                    return await self.channel.send(f"Both parks available on {'-'.join(date)}")
                else:
                    return await self.channel.send(f"Only {availabile_parks[0]} is available on {'-'.join(date)}")

client = MyClient()
client.run(bot_token)
