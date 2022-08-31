import datetime
import discord
from response_handler import ResponseHandler


response_handler = ResponseHandler("inspire")


class MyClient(discord.Client):            
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        self.channel = self.get_channel(1008853405751590915)


    async def on_message(self, message):
        if message.content == 'ping':
            await message.channel.send('pong')
        
        if message.content == '/dates/all':
            dates = response_handler.get_all_available()
            if dates: 
                for date in dates:
                    await self.channel.send(date)
        
        if message.content == f"/date":
            await self.channel.send("Input the desired date in MM/DD/YYYY format")
            msg = await self.wait_for("message")
            date = msg.content.split('/')
            if len(date) != 3: return await self.channel.send("Wrong format. Try again.")

            availability = response_handler.get_specific_date(date)

            if(not availability): return self.channel.send("Date not available")

            else:
                availabile_parks = []
                for park in availability:
                    availabile_parks.append(park)
                
                if(len(availabile_parks) == 2):
                    return await self.channel.send(f"Both parks available on {'-'.join(date)}")
                else:
                    return await self.channel.send(f"Only {availabile_parks[0]} is available on {'-'.join(date)}")

            """
            results = []
            for date in dates['calendar-availabilities']:
                if(date['availability'] != 'cms-key-no-availability'):
                    resObj = {}
                    resObj['date'] = date['date']
                    resObj['parks'] = []
                    for park in date['facilities']:
                        if park['available'] == True:
                            resObj['parks'].append(park['facilityName'])
                    results.append(resObj)


            for result in results:
                date = result['date']
                parks = result['parks']

                if(len(parks) == 2):
                    await message.channel.send(f"On {date} both parks available")
                else:
                    park = parks[0]
                    if park == 'DLR_CA': await message.channel.send(f"On {date} only California Adventure is available")
                    else: await message.channel.send(f"On {date} only Disneyland Park is available")
            """

client = MyClient()
client.run('MTAwODg1MjU2MTU2NDAwODUzOQ.GgOpz5.WUgST4w6H4d_Qn4HbOqRazbwmDILcD9ho0gGZw')
