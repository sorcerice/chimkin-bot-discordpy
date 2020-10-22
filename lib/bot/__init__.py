from asyncio import sleep
from datetime import datetime
from glob import glob

import discord

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed, File, DMChannel
from discord.errors import HTTPException, Forbidden, NotFound
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
								  CommandOnCooldown, BotMissingRole, MissingPermissions)
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import when_mentioned_or, command, has_permissions

from ..db import db

OWNER_IDS = [611941774373683210, 218807000115445760]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument, BotMissingRole, NotFound, HTTPException, MissingPermissions)


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
			self.load_extension(f"{cog}")
			print(f" {cog} cog loaded")

		print("setup complete")

	def run(self, version):
		self.VERSION = version

		print("running setup...")
		self.setup()

		# with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
		# 	self.TOKEN = tf.read()

		self.TOKEN = os.getenv(BOT_TOKEN)

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
			await ctx.send("One or more required arguments are missing, idiot!\nTry using `.help <command name>` (Command name cannot be the alias of the command)")

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
			self.butter = self.get_guild(228966491628765185)
			self.butterch = self.get_channel(642347588107894815)

			self.royals = self.get_guild(568790926017691653)
			self.royalsch = self.get_channel(631021549532479498)
			
			self.sm = self.get_guild(285121209027264512)
			self.smch = self.get_channel(664707489371258881)

			self.test = self.get_guild(727488027391426652)
			self.testch = self.get_channel(734998277828771880)

			await self.butterch.send("Chimkin is now alive! Everyone bow down to the almighty Chimkin!\n<:duckknife:669212549194973204>")
			await self.smch.send("I am online! Rejoice citizens of Shining Moon!")
			await self.royalsch.send("I am now awake and here to service the followers of Zill!")
			await self.testch.send("Chimkin is now online!")

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

			meta = self.get_cog("Meta")
			await meta.set()

			# example for sending files

			# await self.butterch.send(file=File("./data/images/fatcat.jpg"))

		else:
			print("bot reconnected")

	async def on_message(self, message):
		if not message.author.bot:
			if isinstance(message.channel, DMChannel):
				if len(message.content) < 10:
					await message.channel.send("Your message should be atleast 10 characters in length.")

				else:
					member = self.butter.get_member(message.author.id)
					embed = Embed(title=f'''{member.display_name} slid into Chimkin's DMs''',
								  colour=member.colour,
								  timestamp=datetime.utcnow())

				embed.set_thumbnail(url=member.avatar_url)

				fields = [('Member', member.display_name, False),
						  ('Message', message.content, False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				mod = self.get_cog('Mod')
				self.butterBotCh = self.get_channel(714141581308985414)
				await self.butterBotCh.send(embed=embed)
				await message.channel.send("Message relayed to Awie Government")

			else:
				await self.process_commands(message)

bot = Bot()