import discord
from discord import app_commands
import pyotp
import os

TOKEN = os.getenv("TOKEN")

class TwoFAView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # botão nunca expira

    @discord.ui.button(label="Gerar Código 2FA", style=discord.ButtonStyle.primary, custom_id="gerar_2fa")
    async def gerar(self, interaction: discord.Interaction, button: discord.ui.Button):

        class Modal2FA(discord.ui.Modal, title="Gerar Código 2FA"):

            chave = discord.ui.TextInput(
                label="Cole sua chave 2FA",
                placeholder="Ex: LKKOS4WKTDXJNLS276DPN3KBRY",
                required=True
            )

            async def on_submit(self, interaction: discord.Interaction):

                key = str(self.chave).replace(" ", "").upper()

                try:
                    totp = pyotp.TOTP(key)
                    codigo = totp.now()

                    embed = discord.Embed(
                        title="Código 2FA",
                        description=f"🔐 Código: **{codigo}**",
                        color=0x2b2d31
                    )

                    await interaction.response.send_message(embed=embed, ephemeral=True)

                except:
                    await interaction.response.send_message(
                        "❌ Chave inválida.",
                        ephemeral=True
                    )

        await interaction.response.send_modal(Modal2FA())


class BotClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        self.add_view(TwoFAView())  # registra botão persistente


client = BotClient()

@client.tree.command(name="painel2fa", description="Abrir painel gerador 2FA")
async def painel(interaction: discord.Interaction):

    embed = discord.Embed(
        title="Gerador de Código 2FA",
        description="Clique no botão abaixo para gerar seu código.",
        color=0x2b2d31
    )

    await interaction.response.send_message(embed=embed, view=TwoFAView())


client.run(TOKEN)
