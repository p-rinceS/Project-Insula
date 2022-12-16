import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from os import getenv
from itertools import cycle
import requests, random
load_dotenv()

intents = discord.Intents.all()
# intents.members = True

bot = commands.Bot(command_prefix = ';', intents=intents, case_insensitive = True)
@bot.command()
async def ping(ctx):
    await ctx.reply('pong')

@bot.command()
async def dog(ctx):
    r_Dog = requests.get('https://dog.ceo/api/breeds/image/random')
    data = r_Dog.json()
    link = data['message']
    dog_embed = discord.Embed(title ='')
    dog_embed.set_image(url=link)
    await ctx.channel.send(embed=dog_embed)

@bot.command()
async def cat(ctx):
    r_Cat = requests.get('https://api.thecatapi.com/v1/images/search')
    data = r_Cat.json()
    cat_Emb = discord.Embed(title = '')
    cat_img_link = data[0]['url']
    cat_Emb.set_image(url = cat_img_link)
    await ctx.channel.send(embed=cat_Emb)

@bot.event
async def on_ready():
    print('Alive and ready!')
    status_change.start()

status = cycle(['Prince', 'Prefix: \";\"', 'Null'])

@tasks.loop(seconds=5)
async def status_change():
    await bot.change_presence(activity=discord.Game(next(status)))


bot.run(getenv('TOKEN'))