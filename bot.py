import os
import discord
from discord.ext import tasks
from response_handler import ResponseHandler
from watcher import Watcher

watcher = Watcher()
response_handler = ResponseHandler("inspire")
bot_token = os.getenv("BOT_TOKEN")

class MyClient(discord.Client):            
    @tasks.loop(minutes=1)
    async def myLoop(self):
        dates = watcher.dates_being_watched
        if dates:
            available_dates = watcher.check_if_available()
            if available_dates:
                for date in available_dates:
                    await self.channel.send(date + " is now available.")
    
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        self.channel = self.get_channel(1008853405751590915)
        self.myLoop.start()

    async def on_message(self, message):
        if message.content == 'ping':
            await message.channel.send('pong')
        
        if message.content == "/date":
            await self.channel.send("Input the desired date (within 90 days of today) in MM/DD/YYYY format")
            msg = await self.wait_for("message")

            date = msg.content.split('/')
            if len(date) != 3: return await self.channel.send("Wrong format. Please Try again.")

            availability = response_handler.get_specific_date(date)

            if not availability: return await self.channel.send("Date Not Available.")

            else:
                availabile_parks = []
                for park in availability:
                    availabile_parks.append(park)
                
                if(len(availabile_parks) == 2):
                    return await self.channel.send(f"Both parks available on {'-'.join(date)}")
                else:
                    return await self.channel.send(f"Only {availabile_parks[0]} is available on {'-'.join(date)}")
        
        if message.content == "/watch":
            await self.channel.send("Input the desired date (within 90 days of today) in MM/DD/YYYY format that you would like to watch.")
            msg = await self.wait_for("message")

            date = msg.content.split('/')

            if len(date) != 3: return await self.channel.send("Wrong format. Please Try again.")

            month = date[0]
            year = date[2]
            day = date[1]

            formatted_date_list = [year, month, day]
            formatted_date = '-'.join(formatted_date_list)
            
            available_dates = response_handler.get_all_available()

            if formatted_date in available_dates:
                return await self.channel.send("It looks like that date is currently available.")
            else:
                await self.channel.send("That date is not available. I will watch it for you!")
                watcher.add_date(formatted_date)
        
        if message.content == "/watch/view":
            dates = watcher.dates_being_watched
            if not dates: return await self.channel.send("No dates are being watched.")

            await self.channel.send('These are the dates being watched: ')

            await self.channel.send(dates)
        
        if message.content == "/watch/remove":
            dates = watcher.dates_being_watched
            if not dates: return await self.channel.send("No dates are being watched.")

            await self.channel.send('These are the dates being watched: ')

            for date in dates:
                await self.channel.send(date)
            
            await self.channel.send("Which date would you like to remove? Enter it as shown above.")

            msg = await self.wait_for("message")
            if msg.content in watcher.dates_being_watched:
                watcher.dates_being_watched.remove(msg.content)
                await self.channel.send("Successfully removed date from watched list.")
            else:
                await self.channel.send("Could not remove date from list. Ensure that date was inputted properly.")


client = MyClient()
client.run(bot_token)