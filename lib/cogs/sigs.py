from random import randint
from io import BytesIO
from array import array

from discord import Embed, File
from discord.ext.commands import Cog
from discord.ext.commands import command

from PIL import Image, ImageDraw, ImageFont, ImageOps
from aiohttp import request

class Sigs(Cog):
	def __init__(self, bot):
		self.bot = bot


	@command(name='novasig',
			 aliases=['poop'],
			 description='Gives a dirty signature of your stinky noba character.',
			 brief='Gives a dirty signature of your stinky noba character.')
	async def get_poop(self, ctx, *, charName: str):
		bgNum = randint(0,11)
		posNum = randint(0,15)
		linkName = charName.replace(' ', '%20')
		URL = f'https://novaragnarok.com/ROChargenPHP/newsig/{linkName}/{bgNum}/{posNum}'

		await ctx.send(URL)

	@command(name='hsig',
			 aliases=['helsig'],
			 description='Get a picture of your Shining Moon(Helheim) char',
			 brief='Get a picture of your Shining Moon(Helheim) char')
	async def get_helsig(self, ctx, *, charName: str):
		bgchoice = randint(1,51)
		bg = Image.open(f'./data/images/sigbg/{bgchoice}.png')

		posNum = randint(0,5)

		linkName = charName.replace(' ', '%20')
		spriteURL = f'http://51.161.117.101/char/index.php/characterhel/{linkName}/{posNum}/7'

		async with request("GET", spriteURL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
			if response.status == 200:
				sprBytes = await response.read()
			else:
				await ctx.send(f'Beep Boop\n{response.status} status')

		sprite = Image.open(BytesIO(sprBytes))

		bg_copy = bg.copy()
		bg_copy.paste(sprite, (0, 0), sprite.convert('RGBA'))
		draw = ImageDraw.Draw(bg_copy)

		fontCharName = ImageFont.truetype(font=BytesIO(open('./data/fonts/Kyrou_9_Regular_Bold.ttf', "rb").read()), size=8)
		fontRealmName = ImageFont.truetype(font=BytesIO(open('./data/fonts/Kyrou_9_Regular.ttf', "rb").read()), size=6)

		(x, y) = (130, 155)
		CHARNAME = f'{charName}'
		color = 'rgb(255, 255, 255)'
		draw.text((x, y), CHARNAME, fill=color, font=fontCharName)

		(x, y) = (130, 170)
		REALMNAME = 'HELHEIM'
		color = 'rgb(255, 255, 255)'
		draw.text((x, y), REALMNAME, fill=color, font=fontRealmName)

		arr = BytesIO()
		bg_copy.save(arr, format='PNG')
		arr.seek(0)
		file = File(arr, f'''{charName}'s sig - Helheim.png''')

		await ctx.send(file=file)

	@command(name='nsig',
			 aliases=['nifsig'],
			 description='Get a picture of your Shining Moon(Helheim) char',
			 brief='Get a picture of your Shining Moon(Helheim) char')
	async def get_nifsig(self, ctx, *, charName: str):
		bgchoice = randint(1,51)
		bg = Image.open(f'./data/images/sigbg/{bgchoice}.png')

		posNum = randint(0,5)

		linkName = charName.replace(' ', '%20')
		spriteURL = f'http://51.161.117.101/char/index.php/characternif/{linkName}/{posNum}/7'

		async with request("GET", spriteURL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
			if response.status == 200:
				sprBytes = await response.read()
			else:
				await ctx.send(f'Beep Boop\n{response.status} status')

		sprite = Image.open(BytesIO(sprBytes))

		bg_copy = bg.copy()
		bg_copy.paste(sprite, (0, 0), sprite.convert('RGBA'))
		draw = ImageDraw.Draw(bg_copy)

		fontCharName = ImageFont.truetype(font=BytesIO(open('./data/fonts/Kyrou_9_Regular_Bold.ttf', "rb").read()), size=8)
		fontRealmName = ImageFont.truetype(font=BytesIO(open('./data/fonts/Kyrou_9_Regular.ttf', "rb").read()), size=6)

		(x, y) = (130, 155)
		CHARNAME = f'{charName}'
		color = 'rgb(255, 255, 255)'
		draw.text((x, y), CHARNAME, fill=color, font=fontCharName)

		(x, y) = (130, 170)
		REALMNAME = 'NIFLHEIM'
		color = 'rgb(255, 255, 255)'
		draw.text((x, y), REALMNAME, fill=color, font=fontRealmName)

		arr = BytesIO()
		bg_copy.save(arr, format='PNG')
		arr.seek(0)
		file = File(arr, f'''{charName}'s sig - Helheim.png''')

		await ctx.send(file=file)

	@command(name="navatar",
			 aliases=["niftar"],
			 description="Creates avatar for Niflheim character",
			 brief="Creates avatar for Niflheim character")
	async def get_nif_avatar(self, ctx, *, charName: str):
		linkName = charName.replace(' ', '%20')
		URL = f"http://51.161.117.101/char/index.php/avatar/{linkName}"
		await ctx.send(URL)


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("sigs")

def setup(bot):
	bot.add_cog(Sigs(bot))