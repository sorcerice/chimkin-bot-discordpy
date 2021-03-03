from discord import Embed
from datetime import datetime
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.errors import HTTPException


class Log(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.guild = (228966491628765185)
            self.log_channel = self.bot.get_channel(739388066048770118)
            self.bot.cogs_ready.ready_up("log")

    @Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed = Embed(title="Username Change",
                          colour=after.colour,
                          timestamp=datetime.utcnow())

            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        if before.discriminator != after.discriminator:
            embed = Embed(title="Tag Change",
                          description=f"**{after.display_name}'s** discord tag changed",
                          colour=after.colour,
                          timestamp=datetime.utcnow())

            fields = [("Before", before.discriminator, False),
                      ("After", after.discriminator, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        if before.avatar_url != after.avatar_url:
            embed = Embed(title="Avatar Change",
                          description=f"**{after.display_name}'s** new image is below, old to the right",
                          colour=after.colour,
                          timestamp=datetime.utcnow())

            embed.set_thumbnail(url=before.avatar_url)
            embed.set_image(url=after.avatar_url)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = Embed(title=f"Nickname Change **({after.guild.name})**",
                          colour=after.colour,
                          timestamp=datetime.utcnow())

            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        elif before.roles != after.roles:
            embed = Embed(title=f"Role updates **({after.guild.name})**",
                          description=f"**{after.display_name}'s** role was updated",
                          colour=after.colour,
                          timestamp=datetime.utcnow())

            fields = [("Before", ",".join([r.mention for r in before.roles]), False),
                      ("After", ",".join([r.mention for r in after.roles]), False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            if before.content != after.content:
                try:
                    embed = Embed(title=f"Message Edit **({after.guild.name})**",
                                  description=f"Edit by **{after.author.display_name}** in **#{after.channel.name}**",
                                  colour=after.author.colour,
                                  timestamp=datetime.utcnow())

                    fields = [("Before", before.content, False),
                              ("After", after.content, False)]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    await self.log_channel.send(embed=embed)
                except HTTPException as exc:
                    self.log_channel.send(
                        'A message that exceeded/did not meet discord embed restrictions was edited')

    @Cog.listener()
    async def on_message_delete(self, message):
        try:
            if not message.author.bot:
                embed = Embed(title=f"Message Deletions **({message.guild.name})**",
                              description=f"Deleted by **{message.author.display_name}** in **#{message.channel.name}**",
                              colour=message.author.colour,
                              timestamp=datetime.utcnow())

                if len(message.content) != 0:
                    fields = [("Content", message.content, False)]
                elif len(message.attachments) != 0:
                    attachments = message.attachments
                    for attachment in attachments:
                        proxyUrl = attachment.proxy_url
                    fields = [('Content', proxyUrl, False)]
                else:
                    fields = [
                        ('Content', 'Deleted message couldn\'t be logged')]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                    await self.log_channel.send(embed=embed)
        except ValueError:
            await self.log_channel.send(f'Value Error.\n Message deleted by {message.author.display_name}')


def setup(bot):
    bot.add_cog(Log(bot))
