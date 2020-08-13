from datetime import datetime, timedelta
from random import choice

from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions

from ..db import db


# Reference of number emotes
# 0⃣ 1️⃣ 2⃣ 3⃣ 4⃣ 5⃣ 6⃣ 7⃣ 8⃣ 9⃣ 🔟

numbers = ('1️⃣', '2⃣', '3⃣', '4⃣', '5⃣',
			'6⃣', '7⃣', '8⃣', '9⃣', '🔟')


class Reactions(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.polls = []
		self.giveaways = []

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.roles = {
				"⭐": self.bot.guild.get_role(685137322727047189),	# Casual
				"🌙": self.bot.guild.get_role(646817958537986063),	# Adventure
			}
			self.reaction_message = await self.bot.get_channel(714141581308985414).fetch_message(740458093615382538)
			self.starboard_channel = self.bot.get_channel(714141581308985414)
			self.bot.cogs_ready.ready_up("reactions")


	@command(name='createpoll',
			 aliases=['mkpoll'],
			 description='Usage: .mkpoll <time limit in seconds> "<Poll Question - quotes are needed>" <option1-10>.',
			 brief='Usage: .mkpoll <time limit in seconds> "<Poll Question - quotes are needed>" <option1-10>.')
	# @has_permissions(manage_guild=True)
	async def create_poll(self, ctx, hours: int, question: str, *options):
		if len(options) > 10:
			await ctx.send('You can only have a maximum of 10 options.')

		else:
			embed = Embed(title='Poll',
						  description=question,
						  colour=ctx.author.colour,
						  timestamp=datetime.utcnow())

			fields=[('Options', '\n'.join([f'{numbers[idx]} {option}' for idx, option in enumerate(options)]), False),
					('Instructions', 'React to cast a vote!', False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			message = await ctx.send(embed=embed)

			for emoji in numbers[:len(options)]:
				await message.add_reaction(emoji)

			self.polls.append((message.channel.id, message.id))

			self.bot.scheduler.add_job(self.complete_poll, "date", run_date=datetime.now()+timedelta(seconds=hours),
									   args=[message.channel.id, message.id])



	@command(name='giveaway',
			 desciption='Usage: .giveaway <time limit in seconds for> <Title of giveaway>')
	# @has_permissions(manage_guild=True)
	async def create_giveaway(self, ctx, mins: int, *, description: str):
		embed = Embed(title='Giveaway',
					  description=description,
					  colour=ctx.author.colour,
					  timestamp=datetime.utcnow())

		fields=[('End time', f'{datetime.utcnow()+timedelta(seconds=mins*60)} UTC', False)]
		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		message = await ctx.send(embed=embed)
		await message.add_reaction('✅')

		self.giveaways.append((message.channel.id, message.id))

		self.bot.scheduler.add_job(self.complete_giveaway, "date", run_date=datetime.now()+timedelta(seconds=mins),
								   args=[message.channel.id, message.id])



	async def complete_poll(self, channel_id, message_id):
		message = await self.bot.get_channel(channel_id).fetch_message(message_id)

		most_voted = max(message.reactions, key=lambda r: r.count)

		await message.channel.send(f'''Henyo Awie Nation!<:cathmm:669212551439187999>
									\nNyes, results are in and option **{most_voted.emoji}** was the most popular with **{most_voted.count-1}** votes <:detectivepeepo:713457722221396072>
									\nTook me ages to count the votes <:tiredcat:707960228960010270>''')
		self.polls.remove((message.channel.id, message.id))



	async def complete_giveaway(self, channel_id, message_id):
		message = await self.bot.get_channel(channel_id).fetch_message(message_id)

		if len((entrants := [u for u in await message.reactions[0].users().flatten() if not u.bot])) > 0:
			winner = choice(entrants)
			await message.channel.send(f'🥳 Congratulations 🎉**{winner.mention}**🎉 - you won the giveaway!🥳')
			self.giveaways.remove((message.channel.id, message.id))

		else:
			await message.channel.send(f'Giveaway ended - No one entered.... <:peeposad:633637989611864074>')
			self.giveaways.remove((message.channel.id, message.id))



	@Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if self.bot.ready and payload.message_id == self.reaction_message.id:
			current_roles = filter(lambda r: r in self.roles.values(), payload.member.roles)
			await payload.member.remove_roles(*current_roles, reason="SMRO Role Reaction")
			await payload.member.add_roles(self.roles[payload.emoji.name], reason='SMRO Role Reaction')
			await self.reaction_message.remove_reaction(payload.emoji, payload.member)

		# elif payload.emoji.name == "<:kekw:675005062938099722>":
		# 	message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

		# 	if not message.author.bot and payload.member.id != message.author.id:
		# 		msg_id, stars = db.record("SELECT StarMessageID, Stars FROM starboard WHERE RootMessageID = ?",
		# 								  message.id) or (None, 0)

		# 		embed = Embed(title="Kek'd message",
		# 					  colour=message.author.colour,
		# 					  timestamp=datetime.utcnow())

		# 		fields = [("Author", message.author.mention, False),
		# 				  ("Content", message.content or "See attachment", False),
		# 				  ("Stars", stars+1, False)]

		# 		for name, value, inline in fields:
		# 			embed.add_field(name=name, value=value, inline=inline)

		# 		if len(message.attachments):
		# 			embed.set_image(url=message.attachments[0].url)

		# 		if not stars:
		# 			star_message = await self.starboard_channel.send(embed=embed)
		# 			db.execute("INSERT INTO starboard (RootMessageID, StarMessageID) VALUES (?, ?)",
		# 					   message.id, star_message.id)

		# 		else:
		# 			star_message = await self.starboard_channel.fetch_message(msg_id)
		# 			await star_message.edit(embed=embed)
		# 			db.execute("UPDATE starboard SET Stars = Stars + 1 WHERE RootMessageID = ?", message.id)

		elif payload.message_id in (poll[1] for poll in self.polls):
			message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

			for reaction in message.reactions:
				if (not payload.member.bot 
					and payload.member in await reaction.users().flatten()
					and reaction.emoji != payload.emoji.name):
					await message.remove_reaction(reaction.emoji, payload.member)


def setup(bot):
	bot.add_cog(Reactions(bot))