from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
from glob import glob


class cogHandler(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("coghandler")



	@command(name='load', hidden=True)
	@has_permissions(manage_guild=True)
	async def _load(self, ctx, *, cog):
		module = f'lib.cogs.{cog}'
		try:
			self.bot.load_extension(module)
		except commands.ExtensionError as e:
			await ctx.send(f'{e.__class__.__name__}: {e}')
		else:
			await ctx.send(f'\n{cog} loaded')


	@command(name='unload', hidden=True)
	@has_permissions(manage_guild=True)
	async def _unload(self, ctx, *, cog):
		module = f'lib.cogs.{cog}'
		try:
			self.bot.unload_extension(module)
		except commands.ExtensionError as e:
			await ctx.send(f'{e.__class__.__name__}: {e}')
		else:
			await ctx.send(f'\n{cog} unloaded')



def setup(bot):
	bot.add_cog(cogHandler(bot))