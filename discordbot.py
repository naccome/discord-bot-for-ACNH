import discord
import re
import gspread

TOKEN = 'YOUR DISCORD BOT TOKEN'

client = discord.Client();

@client.event
async def on_ready():
	print('I have logged in')

@client.event
async def on_message(message):
	if message.author.bot:
		return

	if message.content == 'Hello':
		await message.channel.send('Hello')

@client.event
async def on_message(message):
	if re.match('カブ*', message.content):
		price = re.sub("\\D", "", message.content)
		await message.channel.send('Your stock price is ' + price)
		gspread.updateSheet(price)

client.run(TOKEN)

