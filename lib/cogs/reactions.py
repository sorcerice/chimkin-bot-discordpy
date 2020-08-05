from discord.ext.commands import Cog

roles = {
	"⭐": 685137322727047189,	# Casual
	"🌙": 646817958537986063,	# Adventure
}

class Reactions(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.reaction_message = await self.bot.get_channel(714141581308985414).fetch_message(740458093615382538)
			self.bot.cogs_ready.ready_up("reactions")


	@Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if self.bot.ready and payload.message_id == self.reaction_message.id:
			role = self.bot.guild.get_role(roles[payload.emoji.name])
			await payload.member.add_roles(role, reason="SMRO Role Reaction")

	@Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		if self.bot.ready and payload.message_id == self.reaction_message.id:
			member = self.bot.guild.get_member(payload.user_id)
			role = self.bot.guild.get_role(roles[payload.emoji.name])
			await member.remove_roles(role, reason="SMRO Role Reaction Removed")


def setup(bot):
	bot.add_cog(Reactions(bot))