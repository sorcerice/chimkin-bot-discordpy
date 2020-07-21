from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed, File
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

PREFIX = "."
OWNER_IDS = [611941774373683210]


class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.scheduler = AsyncIOScheduler()

		super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

	def run(self, version):
		self.VERSION = version

		with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print("running bot...")
		super().run(self.TOKEN, reconnect=True)

	async def on_connect(self):
		print("bot connected")

	async def on_disconnect(self):
		print("bot disconnected")

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("You fucked up")

		else:
			channel = self.get_channel(734998277828771880)
			await channel.send("An error occured")

		raise

	async def on_command_error(self, ctx, exc):
		if isinstance(exc, CommandNotFound):
			pass

		else:
			raise exc.original

	async def on_ready(self):
		if not self.ready:
			self.ready = True
			self.guild = self.get_guild(727488027391426652)
			print("bot ready")

			channel = self.get_channel(734998277828771880)
			await channel.send("Chimkin has been activated!")

			# Embed example

			embed = Embed(title="Nyes, it is I, teh mighty Chimkin", description="This isn't even my final form",
						 colour=0xFF0000, timestamp=datetime.utcnow())
			fields = [("Name", "Value", True),
					  ("Another field", "This field is next to the other one.", True),
					  ("A non-inline field", "This field will appear on it's own row.", False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
				embed.set_author(name="Butter", icon_url=self.guild.icon_url)
				embed.set_footer(text="This is a footer")
				embed.set_thumbnail(url=self.guild.icon_url)
				embed.set_image(url=self.guild.icon_url)
			await channel.send(embed=embed)

			# example for sending files

			await channel.send(file=File("./data/images/fatcat.jpg"))

		else:
			print("bot reconnected")

	async def on_message(self, message):
		pass

bot = Bot()