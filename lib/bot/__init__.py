from asyncio import sleep
from datetime import datetime
from glob import glob

import discord

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed, File, DMChannel
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
								  CommandOnCooldown, BotMissingRole)
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import when_mentioned_or, command, has_permissions

from ..db import db

OWNER_IDS = [611941774373683210, 218807000115445760]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument, BotMissingRole)


def get_prefix(bot, message):
	prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
	return when_mentioned_or(prefix)(bot, message)


class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f" {cog} cog ready")

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
	def __init__(self):
		self.ready = False
		self.cogs_ready = Ready()

		self.scheduler = AsyncIOScheduler()

		db.autosave(self.scheduler)
		super().__init__(command_prefix=get_prefix, owner_ids=OWNER_IDS)

	def setup(self):
		for cog in COGS:
			self.load_extension(f"lib.cogs.{cog}")
			print(f" {cog} cog loaded")

		print("setup complete")

	def run(self, version):
		self.VERSION = version

		print("running setup...")
		self.setup()

		with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print("running bot...")
		super().run(self.TOKEN, reconnect=True)

	async def process_commands(self, message):
		ctx = await self.get_context(message, cls=Context)

		if ctx.command is not None and ctx.guild is not None:
			if self.ready:
				await self.invoke(ctx)

			else:
				await ctx.send("Can you like wait for me to come online? <:pepehiss:413283219040108554>")

	async def on_connect(self):
		print("bot connected")

	async def on_disconnect(self):
		print("bot disconnected")

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("Sora's code fucked up")

		else:
			await self.testch.send("An error occured")

		raise

	async def on_command_error(self, ctx, exc):
		if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
			pass

		elif isinstance(exc, MissingRequiredArgument):
			await ctx.send("One or more required arguments are missing, idiot!")

		elif isinstance(exc, CommandOnCooldown):
			await ctx.send(f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f} secs, fuckface.")

		elif hasattr(exc, "original"):
			if isinstance(exc.original, HTTPException):
				await ctx.send("Ugh. What did you break, stupid!")

			elif isinstance(exc.original, Forbidden):
				await ctx.send("I do not have permission to do that, blame the damned server owner.")

			else:
				raise exc.original

		else:
			raise exc


	async def on_ready(self):
		if not self.ready:
			self.guild = self.get_guild(228966491628765185)
			self.testch = self.get_channel(714141581308985414)
			self.smch = self.get_channel(642347588107894815)
			self.scheduler.start()

			# await self.smch.send("Chimkin is now alive! Everyone bow down to the almighty Chimkin!\n<:duckknife:669212549194973204>")

			# embed = Embed(title="Nyes, it is I, teh mighty Chimkin", description="This isn't even my final form",
			# 			  colour=0xFF0000, timestamp=datetime.utcnow())
			# fields = [("Name", "Value", True),
			# 		   ("Another field", "This field is next to the other one.", True),
			# 		   ("A non-inline field", "This field will appear on it's own row.", False)]
			# 
			# for name, value, inline in fields:
			# 	 embed.add_field(name=name, value=value, inline=inline)
			# 	 embed.set_author(name="Butter", icon_url=self.guild.icon_url)
			# 	 embed.set_footer(text="This is a footer")
			# 	 embed.set_thumbnail(url=self.guild.icon_url)
			# 	 embed.set_image(url=self.guild.icon_url)
			# await channel.send(embed=embed)
			
			while not self.cogs_ready.all_ready():
				await sleep(0.5)

			self.ready = True
			print(" bot ready")

			# example for sending files

			# await channel.send(file=File("./data/images/fatcat.jpg"))

		else:
			print("bot reconnected")

	async def on_message(self, message):
		if not message.author.bot:
			if isinstance(message.channel, DMChannel):
				if len(message.content) < 50:
					await message.channel.send("Your message should be atleast 50 characters in length.")

				else:
					member = self.guild.get_member(message.author.id)
					embed = Embed(title=f'''{member.display_name} slid into Chimkin's DMs''',
								  colour=member.colour,
								  timestamp=datetime.utcnow())

				embed.set_thumbnail(url=member.avatar_url)

				fields = [('Member', member.display_name, False),
						  ('Message', message.content, False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				mod = self.get_cog('Mod')
				await mod.log_channel.send(embed=embed)
				await message.channel.send("Message relayed to Awie Government")

			else:
				await self.process_commands(message)

bot = Bot()