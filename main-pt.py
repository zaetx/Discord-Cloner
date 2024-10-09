from os import system
import psutil
import os
from pypresence import Presence
import time
import sys
import discord
import json
import traceback
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.panel import Panel as RichPanel
from rich.progress import Progress
import asyncio
from colorama import Fore, init, Style
import platform
import inquirer
from cloner import Clone

version = '1.4'
console = Console()


def loading(seconds):
    with Progress() as progress:
        task = progress.add_task("", total=seconds)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)


def clearall():
    system('clear')
    print(f"""{Style.BRIGHT}{Fore.RED}

██╗░░░░░░█████╗░░█████╗░██████╗░███████╗██████╗░░██████╗██╗░░██╗░█████╗░██████╗░
██║░░░░░██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝██║░░██║██╔══██╗██╔══██╗
██║░░░░░██║░░██║███████║██║░░██║█████╗░░██║░░██║╚█████╗░███████║██║░░██║██████╔╝
██║░░░░░██║░░██║██╔══██║██║░░██║██╔══╝░░██║░░██║░╚═══██╗██╔══██║██║░░██║██╔═══╝░
███████╗╚█████╔╝██║░░██║██████╔╝███████╗██████╔╝██████╔╝██║░░██║╚█████╔╝██║░░░░░
╚══════╝░╚════╝░╚═╝░░╚═╝╚═════╝░╚══════╝╚═════╝░╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░░░░
{Style.RESET_ALL}{Fore.RESET}""")


def get_user_preferences():
    preferences = {}
    preferences['guild_edit'] = True
    preferences['channels_delete'] = True
    preferences['roles_create'] = True
    preferences['categories_create'] = True
    preferences['channels_create'] = True
    preferences['emojis_create'] = False

    def map_boolean_to_string(value):
        return "Sim" if value else "Não"

    panel_title = "Config BETA"
    panel_content = "\n"
    panel_content += f"- Alterar nome e ícone do servidor: {map_boolean_to_string(preferences.get('guild_edit', False))}\n"
    panel_content += f"- Excluir os canais do servidor de destino: {map_boolean_to_string(preferences.get('channels_delete', False))}\n"
    panel_content += f"- Clonar os cargos: {map_boolean_to_string(preferences.get('roles_create', False))}\n"
    panel_content += f"- Clonar as categorias: {map_boolean_to_string(preferences.get('categories_create', False))}\n"
    panel_content += f"- Clonar os canais: {map_boolean_to_string(preferences.get('channels_create', False))}\n"
    panel_content += f"- Clonar os emojis: {map_boolean_to_string(preferences.get('emojis_create', False))}\n"
    console.print(
        RichPanel(panel_content,
                  title=panel_title,
                  style="bold blue",
                  width=70))

    questions = [
        inquirer.List(
            'reconfigure',
            message='Do you want to reset the default settings?',
            choices=['Yes', 'No'],
            default='No')
    ]

    answers = inquirer.prompt(questions)

    reconfigure = answers['reconfigure']
    if reconfigure == 'No':
        questions = [
            inquirer.Confirm(
                'guild_edit',
                message='Do you want to edit the server icon and name?',
                default=False),
            inquirer.Confirm('channels_delete',
                             message='Deseja deletar os canais?',
                             default=False),
            inquirer.Confirm(
                'roles_create',
                message=
                'Do you want to clone the positions? (IT IS NOT RECOMMENDED TO DISABLE)',
                default=False),
            inquirer.Confirm('categories_create',
                             message='Do you want to clone categories?',
                             default=False),
            inquirer.Confirm('channels_create',
                             message='Do you want to clone channels?',
                             default=False),
            inquirer.Confirm(
                'emojis_create',
                message=
                'Want to clone Emojis?(IT IS RECOMMENDED TO ACTIVATE THIS CLONING SOLO(ALONE) TO AVOID ERRORS)',
                default=False)
        ]

        answers = inquirer.prompt(questions)
        preferences['guild_edit'] = answers['guild_edit']
        preferences['channels_delete'] = answers['channels_delete']
        preferences['roles_create'] = answers['roles_create']
        preferences['categories_create'] = answers['categories_create']
        preferences['channels_create'] = answers['channels_create']
        preferences['emojis_create'] = answers['emojis_create']

    clearall()
    return preferences


versao_python = sys.version.split()[0]


def restart():
    python = sys.executable
    os.execv(python, [python] + sys.argv)


client = discord.Client()
if os == "Windows":
    system("cls")
else:
    print(chr(27) + "[2J")
    clearall()
while True:
    token = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Enter your token to proceed{Style.RESET_ALL}{Fore.RESET}\n >'
    )
    guild_s = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Enter the ID of the server you want to replicate{Style.RESET_ALL}{Fore.RESET}\n >'
    )
    guild = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Enter the target server ID to paste the copied server{Style.RESET_ALL}{Fore.RESET}\n>'
    )
    clearall()
    print(f'{Style.BRIGHT}{Fore.GREEN}The values ​​entered are:')
    token_length = len(token)
    hidden_token = "*" * token_length
    print(
        f'{Style.BRIGHT}{Fore.GREEN}Your token: {Fore.YELLOW}{hidden_token}{Style.RESET_ALL}{Fore.RESET}'
    )
    print(
        f'{Style.BRIGHT}{Fore.GREEN}ID from the Server to replicate: {Fore.YELLOW}{guild_s}{Style.RESET_ALL}{Fore.RESET}'
    )
    print(
        f'{Style.BRIGHT}{Fore.GREEN}ID of the Server you want to paste the copied server: {Fore.YELLOW}{guild}{Style.RESET_ALL}{Fore.RESET}'
    )
    confirm = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Are the values ​​correct? {Fore.YELLOW}(Y/N){Style.RESET_ALL}{Fore.RESET}\n >'
    )
    if confirm.upper() == 'Y':
        if not guild_s.isnumeric():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}O ID of the server to replicate must contain only numbers.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if not guild.isnumeric():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}O ID from the destination server must contain only numbers.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if not token.strip() or not guild_s.strip() or not guild.strip():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}One or more fields are blank.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if len(token.strip()) < 3 or len(guild_s.strip()) < 3 or len(
                guild.strip()) < 3:
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}One or more fields are less than 3 characters long.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        break
    elif confirm.upper() == 'N':
        clearall()
    else:
        clearall()
        print(
            f'{Style.BRIGHT}{Fore.RED}Opção inválida. Por favor, insira Y ou N.{Style.RESET_ALL}{Fore.RESET}'
        )
input_guild_id = guild_s
output_guild_id = guild
token = token
clearall()


@client.event
async def on_ready():
    try:
        start_time = time.time()
        table = Table(title="Versions", style="bold magenta", width=85)
        table.add_column("Componente", width=35)
        table.add_column("Versions", style="cyan", width=35)
        table.add_row("Cloner", version)
        table.add_row("Discord.py", discord.__version__)
        table.add_row("Python", versao_python)
        console.print(RichPanel(table))
        console.print(
            RichPanel(f" Successful authentication on {client.user.name}",
                      style="bold blue",
                      width=69))
        print(f"\n")
        loading(5)
        clearall()
        guild_from = client.get_guild(int(input_guild_id))
        guild_to = client.get_guild(int(output_guild_id))
        preferences = get_user_preferences()

        if not any(preferences.values()):
            preferences = {k: True for k in preferences}

        if preferences['guild_edit']:
            await Clone.guild_edit(guild_to, guild_from)
        if preferences['channels_delete']:
            await Clone.channels_delete(guild_to)
        if preferences['roles_create']:
            await Clone.roles_create(guild_to, guild_from)
        if preferences['categories_create']:
            await Clone.categories_create(guild_to, guild_from)
        if preferences['channels_create']:
            await Clone.channels_create(guild_to, guild_from)
        if preferences['emojis_create']:
            await Clone.emojis_create(guild_to, guild_from)

        end_time = time.time()
        duration = end_time - start_time
        duration_str = time.strftime("%M:%S", time.gmtime(duration))
        print("\n\n")
        print(
            f"{Style.BRIGHT}{Fore.BLUE} O server was successfully cloned in {Fore.YELLOW}{duration_str}{Style.RESET_ALL}"
        )
        print(
            f"{Style.BRIGHT}{Fore.BLUE} Visit our Discord server: {Fore.YELLOW}https://discord.gg/loadedshop{Style.RESET_ALL}"
        )
        print(
            f"{Style.BRIGHT}{Fore.BLUE}Finalizing the process and closing the account session {Fore.YELLOW}{client.user}"
        )
        await asyncio.sleep(30)
        await client.close()  #fecha o codigo

    except discord.LoginFailure:
        print(
            "Unable to authenticate to account. Please verify that the token is correct."
        )
    except discord.Forbidden:
        print(
            "Cloning could not be performed due to insufficient permissions."
        )
    except discord.NotFound:
        print(
            "Could not find some of the copy elements(canais, categorias, etc.)."
        )
    except discord.HTTPException:
        print(
            "There was an error communicating with the Discord API. In 20 seconds, the code will continue from where it left off.."
        )
        loading(20)

        await Clone.emojis_create(guild_to, guild_from)
    except asyncio.TimeoutError:
        print(f"Ocorreu um erro: TimeOut")
    except Exception as e:

        print(Fore.RED + " Ocorreu um erro:", e)
        print("\n")
        traceback.print_exc()
        panel_text = (
            f"1. Incorrect server ID\n"
            f"2.You are not on the entered server\n"
            f"3. Server entered does not exist\n"
            f"Still not resolved? Contact the developer at [link=https://discord.gg/loadedshop]https://discord.gg/loadedshop[/link]"
        )
        console.print(
            RichPanel(panel_text,
                      title="Possible causes and solutions",
                      style="bold blue",
                      width=70))
        print(
            Fore.YELLOW +
            "\The code will reset in 20 seconds. If you don't want to wait, refresh the page and start over."
        )
        print(Style.RESET_ALL)
        loading(20)
        restart()
        print(Fore.RED + "Restarting...")


try:
    client.run(token)
except discord.LoginFailure:
    print(Fore.RED + "The token entered is invalid")
    print(
        Fore.YELLOW +
        "\n\The code will reset in 10 seconds. If you don't want to wait, refresh the page and start over."
    )
    print(Style.RESET_ALL)
    loading(10)
    restart()
    clearall()
    print(Fore.RED + "Restarting...")
