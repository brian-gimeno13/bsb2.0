""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get

from helpers import checks


class Choice(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Heads", style=discord.ButtonStyle.blurple)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.value = "heads"
        self.stop()

    @discord.ui.button(label="Tails", style=discord.ButtonStyle.blurple)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "tails"
        self.stop()


class Location(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="BWM", description="Broadway Mall, Hicksville."
            ),
            discord.SelectOption(
                label="CRG", description="Crystal Run Galleria, Middletown."
            ),
            discord.SelectOption(
                label="Visitor", description="For our out of town friends!️"
            ),
        ]
        super().__init__(
            placeholder="Round1 Location...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        choices = {
            "bwm": 0,
            "crg": 1,
            "visitor": 2
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        result_embed = discord.Embed(color=0x9C84EF)
        result_embed.set_author(
            name=interaction.user.name, icon_url=interaction.user.avatar.url
        )

        if user_choice_index == 0:
            role = get(interaction.guild.roles, id=1124389027139813406)
            await interaction.user.add_roles(role)
            result_embed.description = "Thanks for joining BWM, " + interaction.user.name + "!"
            result_embed.colour = 0xECF542
        elif user_choice_index == 1:
            role = get(interaction.guild.roles, id=1124390274798473279)
            await interaction.user.add_roles(role)
            result_embed.description = "Thanks for joining CRG, " + interaction.user.name + "!"
            result_embed.colour = 0x42F5D1
        else:
            role = get(interaction.guild.roles, id=1124390314677915658)
            await interaction.user.add_roles(role)
            result_embed.description = "Thanks for stopping in, " + interaction.user.name + "!"
            result_embed.colour = 0x424BF5
        await interaction.response.edit_message(
            embed=result_embed, content=None, view=None
        )


class LocationView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Location())


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="randomfact", description="Get a random fact.")
    @checks.not_blacklisted()
    async def randomfact(self, context: Context) -> None:
        """
        Get a random fact.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://uselessfacts.jsph.pl/random.json?language=en"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="coinflip", description="Make a coin flip, but give your bet before."
    )
    @checks.not_blacklisted()
    async def coinflip(self, context: Context) -> None:
        """
        Make a coin flip, but give your bet before.

        :param context: The hybrid command context.
        """
        buttons = Choice()
        embed = discord.Embed(description="What is your bet?", color=0x9C84EF)
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["heads", "tails"])
        if buttons.value == result:
            embed = discord.Embed(
                description=f"Correct! You guessed `{buttons.value}` and I flipped the coin to `{result}`.",
                color=0x9C84EF,
            )
        else:
            embed = discord.Embed(
                description=f"Woops! You guessed `{buttons.value}` and I flipped the coin to `{result}`, better luck next time!",
                color=0xE02B2B,
            )
        await message.edit(embed=embed, view=None, content=None)

    @commands.hybrid_command(
        name="location", description="Gain a role for your go-to Round1 location.", ephemeral=True
    )
    @checks.not_blacklisted()
    async def location(self, context: Context) -> None:
        """
        Play the rock paper scissors game against the bot.

        :param context: The hybrid command context.
        """
        view = LocationView()
        await context.send("Please make your choice", view=view)


async def setup(bot):
    await bot.add_cog(Fun(bot))
