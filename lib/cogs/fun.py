from datetime import datetime
from random import choice, randint
from typing import Optional
from glob import glob
import re
from io import BytesIO
import os
from dotenv import load_dotenv

from libneko import pag
from aiohttp import request
from discord import Member, Embed
from discord import File
from discord.ext import commands, tasks
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown, bot_has_role, BotMissingRole

from bs4 import BeautifulSoup

andreID = 468021052128231434


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blacklistedAutoReplyChannels = [
            756197003482103900, 756197026806366379, 756197090643935463, 836575998782734356]

    @command(name="8ball",
             aliases=["predict", "foresee", "noodleme"],
             brief="Ask Chimkin yes or no questions",
             description="Ask Chimkin yes or no questions",
             help='Ask Chimkin yes or no questions',
             usage=' Will Chimkin ever be happy?')
    @bot_has_role(286937446611156992)
    async def _8ball(self, ctx, *, question):
        responses = ['Awie council says yes.',
                     'Council of eggs says yes.',
                     'Yes, if you slap Lunch.',
                     'Yes, if you roast Lunch.',
                     'Yes, if you spank Lunch.',
                     'Donate 1000 MC to Amber and it will happen.',
                     'Spank, slap and roast Lunch 4x and it should pass.',
                     'If you wingman for Ry, it is certain.',
                     'Yes, and you will also get an MVP card today',
                     'Awies smile on you.',
                     "Foresight failed. Lunch's fat ass blocked the view.",
                     "An awie lost one of it's 9 lives, try again later.",
                     "Nick doesn't want you to ask that.",
                     'Ashe scummed your 8ball, try again later.',
                     'Failed. Liz wants it to be a secret.',
                     "The Awie Council has made a decision, it's no",
                     'Eggsassins will prevent it.',
                     'No, and you are never getting an MVP card.',
                     'It is highly unlikely because Lunch said so.',
                     'Nope, because Lunch is still a homophobe.',
                     "Roam's big PP blocked the view"]
        await ctx.send(f'{choice(responses)}')

    @command(name="dice",
             aliases=["roll", "rngesus"],
             brief="Rolls a dice and sums the output (useful if we ever want to play D&D)",
             description=f'Rolls a dice and sums the output',
             help='Type the number of rolls followed by \'d\' followed by the number of sides on the dice',
             usage=' 3d6\n3 is the number of rolls\n6 is the number of sides on the dice')
    # @cooldown(5, 30, BucketType.user)
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split("d"))

        if dice <= 25:
            rolls = [randint(1, value) for i in range(dice)]

            await ctx.send(" + ".join([str(r) for r in rolls]) + f"= {sum(rolls)}")

        else:
            await ctx.send("You fucking nuts? Try a lower number, idiot!")

    @command(name="slap",
             brief="Makes you slap someone",
             description="Makes you slap someone",
             help='Makes you slap someone',
             usage='@Lunch cuz why not')
    @bot_has_role(286937446611156992)
    @cooldown(5, 10, BucketType.user)
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("Umm, who are you even trying to slap, idiot?")

    @command(name="say",
             aliases=["echo", "repeat"],
             brief="Chimkin repeats anything you want to say",
             description="Chimkin repeats anything you want to say",
             help='Chimkin repeats anything you want to say')
    @bot_has_role(286937446611156992)
    @cooldown(5, 60, BucketType.user)
    async def echo_message(self, ctx, *, message):
        if message == "Sora's code fucked up":
            await ctx.send("NO U <:peepogiggle:633637995865571328>")
        elif message == "An error occured":
            await ctx.send("How about no?")
        elif message.startswith("/tts"):
            await ctx.send("LOL NO")
        else:
            await ctx.message.delete()
            await ctx.send(message)

    @command(name="fact",
             aliases=["animal"],
             brief='''Has random facts and images of cats, dogs, pandas, foxes, birds and koalas''',
             description='''Has random facts and images of cats, dogs, pandas, foxes, birds and koalas''',
             help='Gives a random fact and image of dog, cat, panda, fox, birb, koala, kangaroo, racoon, red_panda',
             usage=' cat')
    @cooldown(5, 20, BucketType.user)
    async def animal_fact(self, ctx, animal: str):
        fact_url = f"https://some-random-api.ml/animal/{animal}"

        async with request("GET", fact_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()

                embed = Embed(title=f"{animal.title()} fact",
                              description=data["fact"],
                              colour=ctx.author.colour)
                embed.set_image(url=data["image"])
                await ctx.send(embed=embed)

            else:
                await ctx.send(f'''No facts are available for that animal.
								\nKnown animals: dog, cat, panda, fox, birb, koala, kangaroo, racoon, red_panda''')

    @command(name='roast',
             brief='Roast someone',
             description='Roast someone',
             help='Roast someone')
    @bot_has_role(286937446611156992)
    # @cooldown(1, 20, BucketType.user)
    async def roast_command(self, ctx):
        URL = f'https://evilinsult.com/generate_insult.php?lang=en&type=text'

        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.read()

                soup = BeautifulSoup(data.decode('utf-8'), 'lxml')

                insult = soup.find('body').text

                await ctx.send(insult)

            else:
                await ctx.send(f'API returned a {response.status} status.')

    @command(name='meme',
             brief='Shows a random meme Sora stole from somewhere',
             description='Shows a random meme Sora stole from somewhere',
             help='Shows a random meme Sora stole from somewhere')
    @bot_has_role(286937446611156992)
    # @cooldown(3, 30, BucketType.guild)
    async def pull_meme(self, ctx):
        img = choice(glob('./data/smemes/*.jpg'))
        await ctx.send(file=File(img))

    @command(name='bless',
             aliases=['compliment'],
             description='Chimken compliments the person you mention',
             help='Chimken compliments the person you mention',
             usage='`.bless @melonbun`')
    @cooldown(1, 20, BucketType.guild)
    async def bless_command(self, ctx, member: Member):
        responses = [f'{member.mention} is an awesome friend.',
                     f'{member.mention} is a gift to those around them.',
                     f'{member.mention} is a smart cookie.',
                     f'{member.mention}, you are awesome.',
                     f'''{ctx.author.display_name} likes {member.mention}'s style.''',
                     f'{ctx.author.display_name} appreciates {member.mention}.',
                     f'{member.mention} is the most perfect {member.mention} there is.',
                     f'{ctx.author.display_name} is grateful to have known {member.mention}.',
                     f'{member.mention} deserves a hug right now.',
                     f'{member.mention} should be proud of themselves.',
                     f'{member.mention} has a great sense of humour.',
                     f'On a scale of 1 to 10, {member.mention} is an 11.',
                     f'{member.mention} is like a ray of sunshine on a really dreary day.',
                     f'{member.mention} is making a difference.',
                     f'{member.mention} brings out the best in other people.']

        await ctx.send(f'{choice(responses)}')

    @command(name='awie',
             description='Gives you an Awie fact and a bonus random Awie picture.',
             brief='Gives you an Awie fact and a bonus random Awie picture.',
             help='Gives you an Awie fact and a bonus random Awie picture')
    async def awie_facts(self, ctx):
        fact_url = f"https://some-random-api.ml/facts/cat"
        image_url = f"https://some-random-api.ml/img/cat"

        async with request("GET", image_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image_link = data["link"]
            else:
                image_link = None
        async with request("GET", fact_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()

                catFact = data['fact']
                pattern = re.compile('cat', re.IGNORECASE)
                awieFact = pattern.sub(f'awie', catFact)

                embed = Embed(title=f"Awie fact",
                              description=awieFact,
                              colour=ctx.author.colour)
                if image_link is not None:
                    embed.set_image(url=image_link)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"API returned a {response.status} status.")

    @command(name="choose",
             aliases=["decide"],
             description="Need help choosing between things? Ask Chimkin!",
             brief="Need help choosing between things? Ask Chimkin!",
             help='Need help choosing between things? Ask Chimkin!',
             usage=' cat, ashe, chimkin, sora')
    async def choose_command(self, ctx, *, options: str):
        randomOption = options.split(', ')

        await ctx.send(f"Chimkin chooses :{choice(randomOption)}")

    @command(name="chat",
             aliases=["c"],
             description="Chat with Chimkin",
             brief="Chat with Chimkin",
             help='Chat with Chimkin',
             usage='How are you today chimkin?')
    async def chat_command(self, ctx, *, message: str):
        APIKEY = os.getenv('SRA_KEY')
        spaceReplacedMessage = message.replace(" ", "%20")
        replyLink = f"https://some-random-api.ml/chatbot/?key={APIKEY}&message={spaceReplacedMessage}"

        async with request("GET", replyLink, headers={}) as response:
            if response.status == 200:
                data = await response.json()

                try:
                    reply = data["response"]
                    await ctx.send(reply)
                except KeyError:
                    await ctx.send('Something went wrong.\nTry not to use formatted text.\nThank you!')
            else:
                await ctx.send(f"{ctx.author.mention}, I'm sorry.\nI think I might be broken for a while.")

    @command(name="lyrics",
             description="Gets lyrics if you give a song title and artist",
             brief="Gives lyrics if you give a song title and artist",
             help='Gives lyrics if you give a song title and artist',
             usage=' More K/DA\nThere is a 1 in 100 chance that the lyrics get uwufied')
    async def get_lyrics(self, ctx, *, query: str):
        spaceReplacedQuery = query.replace(" ", "%20")
        if randint(0, 100) == 100:
            owoCheck = True
        else:
            owoCheck = False

        lyricsLink = f"https://some-random-api.ml/lyrics/?title={spaceReplacedQuery}&cancer={owoCheck}"

        async with request("GET", lyricsLink, headers={}) as response:
            if response.status == 200:
                data = await response.json()

                thumbnail = data["thumbnail"]["genius"]
                link = data["links"]["genius"]

                author = data["author"]
                title = data["title"]

                @pag.embed_generator(max_chars=2048)
                def cooler_embed(paginator, page, page_index):
                    embed = Embed(title=f"{author} - {title}",
                                  description=page,
                                  url=link,
                                  colour=ctx.author.colour)
                    embed.set_thumbnail(url=thumbnail)
                    embed.set_author(name=ctx.author.display_name,
                                     icon_url=ctx.author.avatar_url)
                    embed.set_footer(
                        text="Such lyrics! Such Moods!", icon_url=ctx.guild.icon_url)
                    return embed

                nav = pag.EmbedNavigatorFactory(
                    factory=cooler_embed, max_lines=20)
                nav += data['lyrics']

                nav.start(ctx)

            else:
                await ctx.send(f"{ctx.author.mention}, something went wrong!")

# fake nitro commands
    @command(name='cjam',
             aliases=['catjam'],
             description='CAT JAM!!!!!',
             brief='CJAM!!!!!',
             help='CJAM!!!!!')
    async def send_cjam(self, ctx):
        URL = 'https://cdn.discordapp.com/attachments/674592975270969344/758992722677465138/catJAM.gif'
        async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
            if resp.status == 200:
                img = BytesIO(await resp.read())
                await ctx.send(content=f'Request by {ctx.author.display_name}', file=File(img, 'catJAM.gif'))

    @command(name='xd',
             aliases=['exdee'],
             description='EXDEEE',
             brief='EXDEEE',
             help='EXDEEE')
    async def send_cxd(self, ctx):
        URL = 'https://media.discordapp.net/attachments/313985990765182986/737457432669716480/XD.gif'
        async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
            if resp.status == 200:
                img = BytesIO(await resp.read())
                await ctx.send(content=f'Request by {ctx.author.display_name}', file=File(img, 'XD.gif'))

    @command(name='djam',
             aliases=['dogjam'],
             description='DOG JAM!!!',
             brief='DOG JAM!!!',
             help='DOG JAM!!!')
    async def send_djam(self, ctx):
        URL = 'https://cdn.discordapp.com/attachments/642347588107894815/759352440851136532/1596771065419.gif'
        async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
            if resp.status == 200:
                img = BytesIO(await resp.read())
                await ctx.send(content=f'Request by {ctx.author.display_name}', file=File(img, 'XD.gif'))

    @command(name='rjam',
             aliases=['ratjam'],
             description='RAT JAM!!!',
             brief='RAT JAM!!!',
             help='RAT JAM!!!')
    async def send_rjam(self, ctx):
        URL = 'https://cdn.betterttv.net/emote/5f43037db2efd65d77e8a88f/3x'
        async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
            if resp.status == 200:
                img = BytesIO(await resp.read())
                await ctx.send(content=f'Request by {ctx.author.display_name}', file=File(img, 'ratJAM.gif'))

    @command(name='gjam',
             aliases=['ogjam', 'gandalfjam'],
             description='OG GANDALF!!!',
             brief='GANDALF!!!',
             help='GANDALF!!!')
    async def send_gjam(self, ctx):
        URL = 'https://cdn.betterttv.net/emote/5fc63c950adab74618587f93/3x'
        async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
            if resp.status == 200:
                img = BytesIO(await resp.read())
                await ctx.send(content=f'Request by {ctx.author.display_name}', file=File(img, 'gandalfJAM.gif'))

    @command(name='pepejam',
             aliases=['pjam'],
             description='OG GANDALF!!!',
             brief='GANDALF!!!',
             help='GANDALF!!!')
    async def send_pepejam(self, ctx):
        URL = 'https://cdn.betterttv.net/emote/5b77ac3af7bddc567b1d5fb2/3x'
        async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
            if resp.status == 200:
                img = BytesIO(await resp.read())
                await ctx.send(content=f'Request by {ctx.author.display_name}', file=File(img, 'pepeJAM.gif'))

    @command(name='popcat',
             aliases=['pcat'],
             description='OG GANDALF!!!',
             brief='GANDALF!!!',
             help='GANDALF!!!')
    async def send_popcat(self, ctx):
        URL = 'https://cdn.betterttv.net/emote/5fa8f232eca18f6455c2b2e1/3x'
        async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
            if resp.status == 200:
                img = BytesIO(await resp.read())
                await ctx.send(content=f'Request by {ctx.author.display_name}', file=File(img, 'popcat.gif'))

    @command(name='bongocat',
             aliases=['bcat'],
             description='BONGO CAT!!!',
             brief='BONGO CAT!!!',
             help='BONGO CAT!!!')
    async def send_bongocat(self, ctx):
        URL = 'https://cdn.betterttv.net/emote/5ba6d5ba6ee0c23989d52b10/3x'
        async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
            if resp.status == 200:
                img = BytesIO(await resp.read())
                await ctx.send(content=f'Request by {ctx.author.display_name}', file=File(img, 'bongocat.gif'))

    @command(name='petpet',
             aliases=['pet'],
             description='Pet person',
             brief='Tag a person to pet them or pet yourself!',
             help='.petpet @Lunch')
    async def petpet_command(self, ctx, member: Member):
        APIKEY = os.getenv('SRA_KEY')
        memberAvatarUrl = member.avatar_url_as(format='png')
        URL = f"https://some-random-api.ml/premium/petpet?avatar={memberAvatarUrl}&key={APIKEY}"

        async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
            if resp.status == 200:
                img = BytesIO(await resp.read())
                await ctx.send(file=File(img, f'{member.display_name}_petpet.gif'))
            else:
                await ctx.send(f'Error Code: {resp.status}')

    @petpet_command.error
    async def petpet_command_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("You need to mention someone to pet!")

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if len(message.content) != 0:
                messageConverter = message.content.split()[0].lower()
                messageLower = message.content.lower()
            else:
                return
            try:
                if message.channel.guild.id == 285121209027264512:  # smro guild id
                    if not message.channel.guild.id in self.blacklistedAutoReplyChannels:
                        joinTime = message.author.joined_at
                        currentTime = datetime.now()
                        memberAge = currentTime - joinTime

                        greetingTags = ['hi', 'henyo', 'hello', 'hey']
                        helpTags = ['help', 'new', 'where', 'please']

                        if memberAge.days < 7 and any(tags in messageLower for tags in greetingTags) and any(tags in messageLower for tags in helpTags):
                            await message.channel.send(f'Heya {message.author.mention}! \nForum Guides Section: https://www.shining-moon.com/ipb/index.php?/forum/45-guides/ \nHelheim Guide Section: https://www.shining-moon.com/ipb/index.php?/forum/82-helheim/ \nNiflheim Guide Section: https://www.shining-moon.com/ipb/index.php?/forum/58-niflheim/ \n\nFor build, equipment or any other guides check out the forum! \nNote: To access a major chunk of the forum you need a separate forum ID.', delete_after=60)
            except AttributeError:
                print('A new SMRO member messaged in my DMs')

            if messageConverter == 'bye':
                await message.channel.send(f'Bye {message.author.mention}~~~')
            if messageConverter == 'revolution':
                await message.channel.send(content='RISE UP BROTHERS!!', file=File('./data/images/deuxvultchimkin.png'))

            if len(message.content) != 12:
                bestClassTags = ['best', 'class', 'start']
                fourthJobTags = ['4th', 'job', 'when']
                himmelCardTags = ['himmelmez', 'card', 'where', 'get']
                tempCircTags = ['temporal', 'circlet', 'when']
                resetEnchantTags = ['how', 'to', 'reset', 'enchant', 'of']
                homunAITags = ['homunculus', 'ai', 'not', 'working']

                if all(tags in messageLower for tags in bestClassTags):
                    await message.channel.send('Start with rebel! Easiest class to gear, level and fast zeny farm \n Guides: *make sure you have a forum ID to view these guides* \nNiflheim: https://www.shining-moon.com/ipb/index.php?/topic/8113-budget-rebel-for-farm/', delete_after=20)

                if all(tags in messageLower for tags in fourthJobTags):
                    await message.channel.send('It\'s currently in development on the test server. Lunar is working through some kinks. But there is no fixed ETA on it yet.', delete_after=10)

                if all(tags in messageLower for tags in himmelCardTags):
                    await message.channel.send('Currently only obtainable from ECA <:SMeca:668824453588844554>\n Later available from Old Glast Heim Challenge Mode instance when it will be implemented (No ETA)', delete_after=10)

                if all(tags in messageLower for tags in tempCircTags):
                    await message.channel.send('Available from Old Glast Heim Challenge Mode instance when it will be implemented (No ETA)', delete_after=10)

                if all(tags in messageLower for tags in resetEnchantTags):
                    await message.channel.send('Most enchants that use the Lapine Box UI for enchants can be reset by using the same item again \nFor more details about enchanting check here: https://www.shining-moon.com/helheim/index.php/Lapine_Enchanting', delete_after=10)

                if all(tags in messageLower for tags in homunAITags):
                    await message.channel.send('Homunculus AI was disabled in a kRO patch by kRO itself and thus we do not have it since we are on that patch. Homunculus AI returned in a later patch which is going to be the next update to SMRO.', delete_after=180)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
