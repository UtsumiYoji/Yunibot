#discord_botで必要なモジュール
import discord
import asyncio
from discord.ext import tasks, commands

#自作関数
from file_box import excel
from file_box import clanbattle
from file_box import status
import rule

client = discord.Client()

#予約確認板の更新
async def reservation():
    #チャンネルidの設定
    channel = client.get_channel(761666813573857290)

    #予約メッセージの投稿
    res = status.reserve()
    embed = discord.Embed(title='予約状況')
    embed.add_field(name='1ボス：'+str(res[0][0])+'人', value=res[0][1], inline=False)
    embed.add_field(name='2ボス：'+str(res[1][0])+'人', value=res[1][1], inline=False)
    embed.add_field(name='3ボス：'+str(res[2][0])+'人', value=res[2][1], inline=False)
    embed.add_field(name='4ボス：'+str(res[3][0])+'人', value=res[3][1], inline=False)
    embed.add_field(name='5ボス：'+str(res[4][0])+'人', value=res[4][1], inline=False)
    await channel.send(embed=embed)

#残凸の確認
async def remainig():
    #チャンネルidの設定
    channel = client.get_channel(761666636897452103)

    #残凸メッセージの投稿
    res = status.remaing()
    embed = discord.Embed(title='凸進捗状況')
    embed.add_field(name='現在：'+res[1]+'ボス', value=res[0])
    await channel.send(embed=embed)

#ループ処理
async def loop():
    while True:
        result = status.endgame()
        if not result is False:
            channel = client.get_channel(766858675976667176)
            await channel.send(result)
            channel = client.get_channel(764803209066971156)
            await channel.send('クラバトの日付が変わりました！\n前日に行った予約状況等は全て初期化されています')

        await asyncio.sleep(55)

#起動時
@client.event
async def on_ready():
    print('Login')
    await loop()

#メッセージ受信時
@client.event
async def on_message(msg):
    #botからのメッセージは無視
    if msg.author.bot:
        return

    #ルールの出力
    if msg.content == '.outrule':
        result = rule.rule()
        await msg.channel.send(embed=result[0])
        await msg.channel.send(embed=result[1])

    #メンバーの登録
    if msg.content.startswith('.add'):
        result = excel.add_member(msg.content.split())
        await msg.channel.send(result)
    
    #メンバーの除外
    if msg.content.startswith('.remove'):
        result = excel.remove_member(msg.content.split())
        await msg.channel.send(result)
    
    #メンバー一覧の表示
    if msg.content.startswith('.allmember'):
        result = excel.all_member()
        embed = discord.Embed(title='登録されているメンバー一覧')
        embed.add_field(name='名前', value=result[0])
        embed.add_field(name='ID', value=result[1])
        embed.add_field(name='メンション', value=result[2])
        await msg.channel.send(embed=embed)
    
    #凸予約
    if msg.content.startswith('.set'):
        result = clanbattle.setin(msg.content.split(), msg.author.id)
        await msg.channel.send(result)
        await reservation()
    
    #凸予約の取り消し
    if msg.content.startswith('.del'):
        result = clanbattle.delete(msg.content.split(), msg.author.id)
        await msg.channel.send(result)
        await reservation()

    #持越しの登録
    if msg.content.startswith('.co'):
        result = clanbattle.carry_over(msg.content.split(), msg.author.id)
        await msg.channel.send(result)
        await remainig()

    #凸宣言,持越し宣言
    if msg.content.startswith('.atk'):
        result = clanbattle.atk(msg.author.id)
        if result[1] == 0:
            await msg.add_reaction('✔️')

        if result[1] == 1:
            await msg.add_reaction('⭕')
        
        if result[1] == 2:
            await msg.add_reaction('❌')
        
        await msg.channel.send(result[0])
        await reservation()
        await remainig()

    #凸の修正
    if msg.content.startswith('.fix'):
        result = clanbattle.fix(msg.author.id)
        await msg.channel.send(result)
        await remainig()

    #ボスの切り替え
    if msg.content == '.bc':
        result = clanbattle.boss_change()
        channel = client.get_channel(764803209066971156)
        await channel.send(result)
    
    #ボスの強制切り替え
    if msg.content.startswith('.bc set'):
        result = clanbattle.boss_set(int(msg.content.split()[2]))
        channel = client.get_channel(764803209066971156)
        await channel.send(result)

client.run('NzU2NTM3NDE3NzY2NDA0MTM4.X2TSYA.Y_sySloffreMQYoIzJLZ9ibBnDw')