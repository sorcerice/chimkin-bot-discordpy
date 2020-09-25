from asyncio import sleep

from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions

class AutoMod(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.butterMarket = self.bot.get_channel(650206780047097867)

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("automod")

	@Cog.listener()
	async def on_message(self, message):
		if not message.author.bot:
			if message.channel.id == 650206780047097867:
				if message.content.startswith(('B>', 'T>', 'S>', 'PC>', 's>', 't>', 'b>', 'pc>')):
					await message.add_reaction('👍')
					await sleep(30)
					await message.clear_reactions()
				else:
					await message.delete()
					await message.channel.send(f'Message needs to start with `B>`, `S>`, `T>` or `PC>`\nDiscuss trades elsewhere so trades don\'t get lost in chat!', delete_after=10)



def setup(bot):
	bot.add_cog(AutoMod(bot))