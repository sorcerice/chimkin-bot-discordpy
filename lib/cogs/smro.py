from datetime import datetime, timedelta
from re import search

from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions


class SMRO(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_links = [756197003482103900,
                              756197026806366379, 756197090643935463]
        self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.smro_log = self.bot.get_channel(462769611604099072)
            self.bot.cogs_ready.ready_up("smro")

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if message.channel.id in self.allowed_links:
                if search(self.url_regex, message.content):
                    print(f'A message was allowed in {message.channel.name}')
                else:
                    await message.delete()
                    await message.channel.send('Not chit chat in this channel!\nOnly post links with captions in a single message!', delete_after=10)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot and after.guild.id == 285121209027264512:
            if before.content != after.content:
                embed = Embed(title=f"Message Edited!",
                              description=f"Edited by **{after.author.display_name}** in {after.channel.name}",
                                          colour=0x11806a,  # Dark Teal
                              timestam=datetime.utcnow())
                fields = [("Before", before.content, False),
                          ("After", after.content, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                await self.smro_log.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot and message.guild.id == 285121209027264512:
            embed = Embed(title=f"Message Deleted!",
                          description=f"Deleted by **{message.author.display_name}** in **{message.channel.name}**",
                                      colour=0xe74c3c,  # Red
                          timestam=datetime.utcnow())
            fields = [("Deleted Content", message.content, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await self.smro_log.send(embed=embed)

    @Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed = Embed(title="Discord Tag Name Changed!",
                          colour=0xe67e22,  # Orange
                          timestamp=datetime.utcnow())

            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await self.smro_log.send(embed=embed)

        if before.discriminator != after.discriminator:
            embed = Embed(title="Discord Tag# Changed!",
                          description=f"**{after.display_name}'s** discord tag changed",
                                      colour=0xa84300,  # Dark Orange
                          timestamp=datetime.utcnow())

            fields = [("Before", before.discriminator, False),
                      ("After", after.discriminator, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await self.smro_log.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = Embed(title=f"Nickname Changed!",
                          colour=0x2ecc71,  # Green
                          timestamp=datetime.utcnow())

            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.smro_log.send(embed=embed)

        elif before.roles != after.roles:
            embed = Embed(title=f"Role Updated!",
                          description=f"**{after.display_name}'s** role was updated",
                                      colour=0x206694,  # Dark Blue
                          timestamp=datetime.utcnow())

            fields = [("Before", ",".join([r.mention for r in before.roles]), False),
                      ("After", ",".join([r.mention for r in after.roles]), False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.smro_log.send(embed=embed)


def setup(bot):
    bot.add_cog(SMRO(bot))
