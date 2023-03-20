import discord
import os
import requests
import discord
from discord.ext import commands

import json


import time
from discord.ext import commands
import colorama
from colorama import Fore
import asyncio





#-----SETUP-----#

prefix = "-"

#use the .env feature to hide your token


with open('config.json', 'r') as f:
    config = json.load(f)
    token = config['TOKEN']


#---------------#

bot = commands.Bot(command_prefix=prefix,
                   help_command=None,
                   case_insensitive=True,
                   self_bot=True)





#---------------------------Ask Proofs after doing +get for Vouches which are to be proven by the User

@bot.command()
async def vouchverify(ctx):
        await ctx.message.delete()
        message = f" To claim those vouches, you gotta prove they're yours. So, make sure to provide legit payment proofs that match the vouch IDs mentioned on the payment app. You got 12 hours to do this. Important points:\n\n> Valid payment proofs required\n> Vouch IDs must match those on the payment app\n> 12-hour deadline\n\nHope that's clear enough!"
        await ctx.send(message)



#-------------------------Staffping Warning(Verbal)


@bot.command()
async def staffping(ctx, channel: discord.TextChannel = None):
    await ctx.message.delete()  # Delete the trigger message

    message = "__**Please Avoid Pinging Staff**__\n\nAvoid pinging or mentioning staff unnecessarily to get a faster response to your ticket. Be patient and follow up politely if needed. Also, avoid reply mentions when responding to staff messages to prevent further delays.\n\nGIF for reference: https://tenor.com/view/mention-stop-dont-ping-ping-discord-gif-19964821"

    if channel is not None:
        await channel.send(message)  # Send the message to the specified channel
    else:
        await ctx.send(message)  # Send the message to the channel where the trigger was used


#------------------------Mention Vouch IDs

@bot.command()
async def mentionvouch(ctx):
        await ctx.message.delete()
        message = f" __**Mention the Vouch IDs Correctly**__ in order to get the reference of all the proofs , otherwise ticket won't be entertained."
        await ctx.send(message)  


#------------------------Vouch import message

@bot.command()
async def vouchimport(ctx, *, message):
    await ctx.message.delete()
    response = f"{message}\n\n> Payment proof ✅\n\n> <@&888763368943534101>"
    await ctx.send(response)


#----------------How The payment proof should look like Tutorial

@bot.command(name='proofinfo')
async def proofinfo(ctx):
    await ctx.message.delete()
    response = """When submitting proofs, it's important to follow certain guidelines to ensure that they are valid and can be processed efficiently. To ensure that your proofs are acceptable, please keep in mind the following:

> ・Proofs must be submitted without any cropping or editing.
> 
> ・Screenshots must be taken from the payment app and should be up-to-date to ensure validity.
> 
> ・If you're using a Windows or Mac computer, please include your window dock and browser dock in the screenshot."""
    await ctx.send(response)



#------------------------12-Hour Wait for Verification

@bot.command()
async def vouch12hr(ctx):
    response = "Thank you for submitting your proofs! We will review them within the next **12 hours**. Once they have been approved, __we'll ping here and admins will do your import of the vouch profile__."
    await ctx.send(response)
    await ctx.message.delete()


  
#---------------------vouch_recovery_ticket_starting

@bot.command()
async def vouchrecovery(ctx, user_id):
    await ctx.message.delete()  # delete the trigger message

    # Respond with two messages
    await ctx.send(f" =add {user_id} ")
    await ctx.send(f"+vouches {user_id}")
    await ctx.send(f"<@{user_id}>")

#------------------------Vouch_recovery_dm 

#This_Can_make_your_account_terminated


@bot.command()
async def recoverydm(ctx, user: discord.User):
    # Send direct message to user
    try:
        await ctx.message.delete()  # delete the trigger message
        channel = await user.create_dm()
        await channel.send(f"A request has been submitted by a new account, which may be you, for a vouch import. Please take a look at the import ticket {ctx.channel.mention} and respond within 12hrs if it wasn't initiated by you.\n\n~Scammeralert Team\nhttps://discord.gg/scammeralert")
        await ctx.send(f"Sent recovery DM to {user.mention}.", delete_after=5)
    except Exception as e:
        error_message = await ctx.send(f"Failed to send recovery DM to {user.mention}: {e}")
        await asyncio.sleep(5)
        await error_message.delete()




#-----------------------How to prove a vouch INfo 
@bot.command()
async def vouchinfo(ctx):
    await ctx.message.delete()
    await ctx.send('**How to Provide Proof of a Vouch**\n\n> To prove a vouch, it is essential to correctly mention the vouch IDs to obtain a reference for verification. Vouch IDs refer to the title of the embedded message for each vouch that was sent. You can either reply to the vouch message or mention the vouch IDs in your response.\n> \n> It is crucial to attach recent and easily accessible proof of the transaction, along with all relevant details. Ensure that the entire transaction details are visible and the window/Mac dock/phone notification (status) bar as well as the navigation bar/browser dock are also visible in the proof. This will make it easier to validate the authenticity of the vouch.')

      
#-----------------------Reminder For a Channel Check within 12hour (Using Either Carl, Flantic or any bot which has ? as prefix and uses ?rm as trigger for taking the command for reminder)
      
  
@bot.command()
async def remindchannel(ctx):
  
    await ctx.send(f'?rm {ctx.channel.mention} {ctx.channel} 12hr')
    await ctx.message.delete()  # Delete the command trigger message



#--------------------------------Vouch For MM , Exch & Selling

#MM
@bot.command()
async def vouchmm(ctx, *, message):
    await ctx.send(f'`+rep {ctx.author.mention} MM | {message}`')
    await ctx.message.delete()

#Selling
@bot.command()
async def vouchsold(ctx, *, message):
    invite_link = "https://discord.gg/BdkryGCQgs"
    await ctx.send(f'`+rep {ctx.author.mention} Sold | {message}`')
    await ctx.send(invite_link)
    await ctx.message.delete()
  
#Exch
@bot.command()
async def vouchexch(ctx, *, message):
    await ctx.send(f'`+rep {ctx.author.mention} Exchange | {message}`')
    await ctx.message.delete()
  
#----------------------------------------Transaction Details (Crypto)

  
@bot.command()
async def check(ctx, arg, args):
    url = f'https://api.blockcypher.com/v1/{arg}/main/txs/{args}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        confirmations = data['confirmations']
        preference = data['preference']
        try:
            confirmed = data['confirmed'].replace('T', ' ').replace('Z', '')
        except:
            confirmed = 'Not confirmed'
        try:
            received = data['received'].replace('T', ' ').replace('Z', '')
        except:
            received = 'Not received'
        double_spend = data['double_spend']

        # Extract receiver and sender addresses
        for output in data['outputs']:
            if 'addresses' in output.keys():
                if output['addresses'][0] != data['inputs'][0]['addresses'][0]:
                    receiver_address = output['addresses'][0]
                    sender_address = data['inputs'][0]['addresses'][0]
                    break
        
        # Get price of transaction
        output_values = [output['value'] for output in data['outputs']]
        price = sum(output_values) / 10 ** 8 # divide by 10^8 to convert from satoshis to the base unit of the cryptocurrency
        await ctx.reply(f'Sender Address: {sender_address}\nReceiver Address: {receiver_address}\nConfirmations: {confirmations}\nPreference: {preference}\nConfirmed: {confirmed}\nReceived: {received}\nDouble Spend: {double_spend}\nCrypto  Transacted: {price} {arg.upper()}')
    else:
        await ctx.reply('Invalid Transaction ID')

    
  
#-------------------------------Basic Maths Calculation (Such as +,-,* or /)

      
@bot.command()
async def calc(ctx, *, expression):
    try:
        result = eval(expression)
        await ctx.message.delete()
        await ctx.send(f"{expression} = {result}")
    except:
        await ctx.send('Invalid expression')




#------------------------------Universal Bot Commands

#1
@bot.command()
async def mplay(ctx, *, message):
    channel = bot.get_channel(1083636551092797510)
    await channel.send(f'+play {message}')
    await ctx.message.delete()  # Deletes the message sent by the user

@bot.command()
async def mvc(ctx):
    await ctx.send('<#1083637097254096936>')
    await ctx.message.delete()     

@bot.command()
async def mskip(ctx):
    channel = bot.get_channel(1083636551092797510)
    await channel.send('+skip')
    await ctx.message.delete()

@bot.command()
async def mvolume(ctx, message):
    channel = bot.get_channel(1083636551092797510)
    await channel.send(f'+volume {message}')
    await ctx.message.delete()

#2



@bot.command()
async def hplay(ctx, *, message):
    channel = bot.get_channel(985557881749393458)
    await channel.send(f'+play {message}')
    await ctx.message.delete()  # Deletes the message sent by the user

@bot.command()
async def hvc(ctx):
    await ctx.send('<#981267051513520148>')
    await ctx.message.delete()     

@bot.command()
async def hskip(ctx):
    channel = bot.get_channel(985557881749393458)
    await channel.send('+skip')
    await ctx.message.delete()

@bot.command()
async def hvolume(ctx, message):
    channel = bot.get_channel(985557881749393458)
    await channel.send(f'+volume {message}')
    await ctx.message.delete()  


#--------------------------Token Info Command
#under Build




bot.run(token, bot=False)
