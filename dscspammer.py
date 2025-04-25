import asyncio
import aiohttp
import discord
from discord.ext import commands
import platform
import os

BLUE = '\033[94m'
GREEN = '\033[92m'
RESET = '\033[0m'

spamming = True

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_header():
    print(f"""{BLUE}██████╗░░██████╗░█████╗░░██████╗██████╗░░█████╗░███╗░░░███╗███╗░░░███╗███████╗██████╗░{RESET}  
{GREEN}██╔══██╗██╔════╝██╔══██╗██╔════╝██╔══██╗██╔══██╗████╗░████║████╗░████║██╔════╝██╔══██╗{RESET}  
{BLUE}██║░░██║╚█████╗░██║░░╚═╝╚█████╗░██████╔╝███████║██╔████╔██║██╔████╔██║█████╗░░██████╔╝{RESET}  
{GREEN}██║░░██║░╚═══██╗██║░░██╗░╚═══██╗██╔═══╝░██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝░░██╔══██╗{RESET}  
{BLUE}██████╔╝██████╔╝╚█████╔╝██████╔╝██║░░░░░██║░░██║██║░╚═╝░██║██║░╚═╝░██║███████╗██║░░██║{RESET}  
{GREEN}╚═════╝░╚═════╝░░╚════╝░╚═════╝░╚═╝░░░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝{RESET}  
{BLUE}░█████╗░██████╗░████████╗██████╗░{RESET} 
{GREEN}██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗{RESET} 
{BLUE}██║░░╚═╝██████╔╝░░░██║░░░██████╔╝{RESET} 
{GREEN}██║░░██╗██╔══██╗░░░██║░░░██╔══██╗{RESET} 
{BLUE}╚█████╔╝██║░░██║░░░██║░░░██║░░██║{RESET} 
{GREEN}░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝{RESET}""")

async def webhook_spammer(webhook_url, message):
    async with aiohttp.ClientSession() as session:
        while spamming:
            try:
                async with session.post(webhook_url, json={"content": message}) as response:
                    print(f"[Webhook] Sent: {response.status}")
            except Exception as e:
                print(f"[Webhook] Error: {e}")

async def bot_spammer(bot, message):
    await bot.wait_until_ready()
    while spamming:
        for guild in bot.guilds:
            for channel in guild.text_channels:
                try:
                    await channel.send(message)
                    print(f"[Bot] Sent to #{channel.name}")
                except Exception as e:
                    print(f"[Bot] Error in #{channel.name}: {e}")

async def input_listener(bot):
    global spamming
    while True:
        user_input = await asyncio.to_thread(input, "")
        if user_input.strip().lower() == "stop":
            spamming = False
            print("[!] Spamming stopped by user.")
            try:
                await bot.close()
            except:
                pass
            break

async def main():
    clear_screen()

    print_header()

    print("\nSelect the spamming method:")
    print("1. Webhook Spammer")
    print("2. Bot Spammer")
    selection = input("Enter 1 or 2: ").strip()

    spam_message = input("Enter your spam message: ").strip()

    if selection == "1":  
        webhook_url = input("Enter your webhook URL: ").strip()
        if not webhook_url:
            print("[!] No webhook URL provided, exiting.")
            return
        print(f"[*] Webhook URL selected. Starting webhook spamming...")
        await webhook_spammer(webhook_url, spam_message)
    elif selection == "2":  
        token = input("Enter your bot token: ").strip()
        intents = discord.Intents.default()
        intents.messages = True
        intents.guilds = True

        bot = commands.Bot(command_prefix="!", intents=intents)

        @bot.event
        async def on_ready():
            print(f"[*] Bot is online as {bot.user}")
            print(f"[*] Starting bot spamming...")
            asyncio.create_task(bot_spammer(bot, spam_message))
            print(f"[*] Starting input listener...")
            asyncio.create_task(input_listener(bot))

        try:
            await bot.start(token)
        except Exception as e:
            print(f"[!] Bot failed to start: {e}")
    else:
        print("[!] Invalid selection. Exiting.")

if __name__ == "__main__":
    asyncio.run(main())
