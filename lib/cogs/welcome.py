from discord import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command

from ..db import db


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member):
        if member.guild.name == "Butter":
            db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
            await self.bot.get_channel(598539329320648897).send(f'''Hello {member.mention}, welcome to **{member.guild.name}**<:peepoblush:633637992090697739>!\n\nFeel free to check out the <#600949560386256907> so you don't get lost!\nIf you're from SMRO, please role yourself at <#686074623506382891>''')

            await member.add_roles(*(member.guild.get_role(id_) for id_ in [(633887205806440499)]))
        else:
            pass

    @Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.name == "Butter":
            db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
            await self.bot.get_channel(598539329320648897).send(f"**{member.display_name}** has left **{member.guild.name}** <:pepemeltdown:609067100417294339>\n\nIt was nice having you around <:peepoblush:633637992090697739>")
        else:
            pass


def setup(bot):
    bot.add_cog(Welcome(bot))
