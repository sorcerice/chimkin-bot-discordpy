from random import randint

from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
from PIL import Image, ImageDraw, ImageFilter

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
			 aliases=['hsig'],
			 description='Get a picture of your SMRO char',
			 brief='Get a picture of your SMRO char')
	async def get_helsig(self, ctx, *, charName: str):
		linkName = charName.replace(' ', '%20')
		URL = f'http://51.161.117.101/char/index.php/characterhel/{linkName}'

		bg=Image.open('data/images/sigbg')

		embed = Embed(title='Shining Moon - Helheim',
					  description=f'Sprite for {charName}')

		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		embed.set_thumbnail(url='https://www.shining-moon.com/hel/themes/default/img/logo.gif')
		embed.set_image(url=URL)
		embed.set_footer(text='Nice char you got there', icon_url=ctx.guild.icon_url)

		await ctx.send(embed=embed)

	@command(name='nsig',
			 aliases=['nsig'],
			 description='Get a picture of your SMRO char',
			 brief='Get a picture of your SMRO char')
	async def get_nifsig(self, ctx, *, charName: str):
		linkName = charName.replace(' ', '%20')
		URL = f'http://51.161.117.101/char/index.php/characternif/{linkName}'

		embed = Embed(title='Shining Moon - Helheim',
					  description=f'Sprite for {charName}')

		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		embed.set_thumbnail(url='https://www.shining-moon.com/hel/themes/default/img/logo.gif')
		embed.set_image(url=URL)
		embed.set_footer(text='Nice char you got there', icon_url=ctx.guild.icon_url)

		await ctx.send(embed=embed)


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("sigs")

def setup(bot):
	bot.add_cog(Sigs(bot))