import json
import asyncssh

import discord
from discord.ext import commands
from discord import app_commands

CONFIG_FILE = 'config.json'

class Config:
    def __init__(self, config_path) -> None:
        with open(config_path) as f:
            config_json = json.load(f)
        self.ip = config_json['ip']
        self.key = asyncssh.read_private_key(config_json['key_path'])
        self.username = config_json['username']
        self.port = config_json['port']


class Instance_Commands:
    def __init__(self, name:str, clean:str) -> None:
        self.name = name
        self.clean_command = clean

    async def clean(self, client:asyncssh.SSHClientConnection):
        return await client.run(self.clean_command, check=False)

class Server_Commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.config = Config(CONFIG_FILE)
        self.sms = Instance_Commands('verde', 'sudo smsclean')
        self.dev = Instance_Commands('roxo', 'sudo devclean')
        self.non = Instance_Commands('non', 'echo hello')

    async def get_client(self) -> asyncssh.SSHClientConnection:
        return await asyncssh.connect(host=self.config.ip, username=self.config.username, port=self.config.port, client_keys=[self.config.key])
    
    def get_instance_from_str(self, instance_str: discord.app_commands.Choice[str]) -> Instance_Commands:
        match instance_str.value:
            case 'sms':
                return self.sms
            case 'dev':
                return self.dev
            case _:
                return self.non

    @app_commands.command(name='clean', description='limpar banco de dados')
    @app_commands.describe(instancia='A instância do dolibarr')
    @app_commands.choices(instancia=[
        app_commands.Choice(name='verde(SMS)', value='sms'),
        app_commands.Choice(name='roxo(develop)', value='dev')])
    async def clean_server(self, interaction: discord.Interaction, instancia: discord.app_commands.Choice[str]) -> None:
        instance = self.get_instance_from_str(instancia)
        client = await self.get_client()
        result = await instance.clean(client)
        response = f"**instancia: {instance.name}**\n"
        if result.exit_status != 0:
            response += f"**stderr:**\n{result.stderr}"
        response += f"**stdout:**\n{result.stdout}"
        client.close()
        await interaction.response.send_message(response, ephemeral=True)

    @commands.command()
    async def sync(self, ctx):
        async with ctx.typing():
            fmt = await self.bot.tree.sync()
            await ctx.send(f'synced {len(fmt)} commands :)')


async def setup(bot):
    await bot.add_cog(Server_Commands(bot))
