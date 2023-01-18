import os
import random, discord
from discord.ext import commands, tasks
from itertools import cycle
import csv
# import openai




intents = discord.Intents.all()
intents.members = True
client = commands.Bot(
command_prefix = ".", 
intents=intents, 
case_insensitive=True)

# lets authorize openai api key

# openai.api_key = (os.environ['OPEN_AI_KEY'])
# openai.Model.list()
token = ""

# id = '805896949932359722' Server ID


# Bot is activated and Ready
@client.event
async def on_ready():
  print("Bot is activated properly")
  status_change.start()

status = cycle(['UIC', '.grades'])
Trusted = [135932078486192128]

@tasks.loop(seconds = 10)
async def status_change():


  await client.change_presence(activity=discord.Game(next(status)))

for guild in client.guilds:
  print(guild)
  print(guild.id)


@client.event
async def on_message(m):
  name = m.author.display_name
  if name == None:
    name = m.author

  m_log = discord.Embed(title=name, color=10181046,description='') 
  m_log.add_field(name='Content:', value= m.content, inline = False)
  m_log.add_field(name='Server:', value= str(m.guild), inline = False)
  m_log.add_field(name='Channel:', value= str(m.channel), inline = False)
  m_log.add_field(name='Time:', value= str(m.created_at), inline = False)

  



  # print(m)

  if m.author.id == 893525520833216543:  
      return

  await client.get_channel(954146629617872916).send(embed = m_log)
  await client.process_commands(m)


@client.command(name= 'connect',aliases = ['join', 'play'], pass_context = True)
async def connect(ctx):
  if ctx.author.voice is None:
    await ctx.reply('You\'re not in a Voice Channel.')
  voice_channel = ctx.author.voice.channel
  if ctx.voice_client is None:
    await voice_channel.connect()
  else:
    await ctx.voice_client.move_to(voice_channel)


@client.command(name = 'disconnect', aliases = ['leave'])
async def disconnect(ctx):
  await ctx.voice_client.disconnect()






@client.command(name="coinflip", aliases=["cf", "headsortails"], pass_context = True)
 # COIN FLIP COMMAND START---------------------------------
async def coinflip(ctx):
  heads_or_tails = ['<:tails:903489344185172009>','<:heads:903489327361818654> ']
  await ctx.channel.trigger_typing()
  await ctx.channel.send(random.choice(heads_or_tails))

#----
# @client.command(name="ai", aliases=['answer'], pass_context=True)
# async def open(ctx, *args):
#   prompts = ' '.join(args)
  
#   response = openai.Completion.create(
#   engine="text-davinci-003",
#   prompt= prompts,
#   temperature = 0.4,
#   max_tokens = 64
# )
#   await ctx.message.reply(response['choices'][0]['text'])

#----
  
# @client.command(name="image", aliases=['givemeimage'], pass_context=True)
# async def open(ctx, *args):
#   prompts = ' '.join(args)
#   response = openai.Image.create(
#   prompt= prompts,
#   n=1,
#   size="1024x1024"
# )
  # await ctx.message.reply(response['data'][0]['url'])

@client.command(name="avatar", aliases=['av'], pass_context=True)
async def avatar(ctx, member : discord.Member = None):
    avEmbed = discord.Embed(title = 'Avatar', color = 2763306)
    if member == None:
      member = ctx.author
    link = member.avatar_url
    avEmbed.set_author(name = ctx.author, icon_url = link)
    avEmbed.set_image(url = link)
    await ctx.channel.send(embed = avEmbed)





@client.command(name="purge", aliases= ['delete'])
    #check user role
async def purge(ctx, number=1):

  if ctx.author.id in Trusted:
    access = True
  else:
    access = False

  if access == True:
    print("Access Granted:", number, "messages purged successfully.")
    await ctx.channel.purge(limit = int(number)+1)
  else:
    print("Access Denied: No approved role.")



@client.command(name="ping", aliases=["latency"], pass_context=True)
async def ping(ctx):
    await ctx.channel.send('``Latency: ' + str(round(client.latency*1000)) + 'ms``')



@client.command(name = "gradeDist", aliases=['gradedistribution', 'grades', 'grade'])
async def gradeDist(ctx, semester='' ,subject='', courseNum = ''):
  
    checks = False
    if (semester != '' and subject != '' and courseNum != ''):
      checks = True
      # semester argument not case sensitive
      semester = semester.upper()
      try:
        f = open(semester+'.csv')
        f.close()
      except FileNotFoundError:
        await ctx.channel.send("Semester not in directory.")
    else:
      await ctx.channel.send("Your arguments were not recognized, say .help for more assistance.")
    if (checks == True):
      # subject argument not case sensitive
      subject = subject.upper()
      csvfile = open(semester+".csv")
      csvreader = csv.reader(csvfile)
      rows = []
      for row in csvreader:
        rows.append(row)
        
      for i in rows:
        if i[0] == subject and i[1] == courseNum:
          passrate = ((int(i[5]) + int(i[6]) + int(i[7]))/int(i[22]))*100
          #colors in order: very red, red, orange, yellow, yellow green, green
          colors = [0xAB1515,0xFF5C5C, 0xF19941, 0xEBDF22, 0xA4F871, 0x45A30B]
          if (passrate >= 0 and passrate <= 49):
            pass_likelihood = colors[0]
          elif(passrate >= 50 and passrate <= 59):
            pass_likelihood = colors[1]
          elif(passrate >= 60 and passrate <= 69):
            pass_likelihood = colors[2]
          elif(passrate >= 70 and passrate <= 79):
            pass_likelihood = colors[3]
          elif(passrate >= 80 and passrate <= 89):
            pass_likelihood = colors[4]
          elif(passrate >= 90 and passrate <= 100):
            pass_likelihood = colors[5]
            #----------------------
          GradeEmbed = discord.Embed(title="UIC Grade Distribution", description='',color=pass_likelihood)
          GradeEmbed.add_field(name = "_____", value = "**Semester:** "+ semester +"\n**Course: **" + i[2] + "\n**Professor: **" + i[21] + "\n\n**A:** " + i[5] +"\n**B:** " + i[6] + "\n**C:** " + i[7] + "\n**D:** " + i[8] + "\n**F:** " + i[9] + "\n**Pass Rate:** "+f'{passrate:.2f}%' +"\n**Dropped:** " + i[20])
          GradeEmbed.set_author(name = ctx.author, icon_url = ctx.author.display_avatar)
          
          GradeEmbed.set_footer(text = "Students: " + i[22])
          await ctx.author.send(embed = GradeEmbed)

@client.command(aliases=["shut","shutdown","quit","stop_that","stahp", "kill"])
async def killswitch(ctx):
   if ctx.author.id in Trusted:
    killPerm = True
   else:
    killPerm = False

   if killPerm == True:
    print("UIClassmate is being shut down by: " + str(ctx.author))
    await ctx.send("Attention: UIClassmate is now offline.")
    await client.close()
   else:
    print("Kill request denied. User: " + str(ctx.author))
    
      



# KEEPS THE BOT ALIVE FUNCTION CALL

#RUNS BOT WITH SECRET TOKEN

# client.run(os.environ['TOKEN']) 
client.run(token) 
