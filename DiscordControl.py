import discord
import asyncio
import StatusMake
import BackEndControl

client = discord.Client()

StatusChannel = 
ReaderChannel = 
CommandChannel = 

#予約状況を表示してくれる
async def ReloadStatus():
    channel = client.get_channel(StatusChannel)
    await channel.purge(limit=None)

    StatusData = StatusMake.StatusMake()
    embed = discord.Embed(title=StatusData[3])
    embed.add_field(name='残凸状況', value=StatusData[0], inline=False)
    embed.add_field(name='予約状況', value=StatusData[1], inline=False)
    embed.add_field(name='持越し状況', value=StatusData[2], inline=False)
    await channel.send(embed=embed)

#クラバトの日付変更を監視するループ
async def loop():
    while True:
        StatusData = StatusMake.EndGame()
        if not StatusData is False:
            #凸漏れ通知
            channel = client.get_channel(ReaderChannel)
            embed = discord.Embed(title='凸漏れ通知', description=StatusData, color=0xff0000)
            await channel.send(embed=embed)

            #日付変更通知
            channel = client.get_channel(CommandChannel)
            await channel.send('クラバトの日付が変わりました！\n前日に行った予約状況等は全て初期化されています')
            await ReloadStatus()
    
        await asyncio.sleep(55)

@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Game(name='Running on Ver.2.0.0.0')
    )
    await loop()

@client.event
async def on_message(msg):
    #メンバーの登録
    if msg.content.startswith('.add'):
        Smsg = msg.content.split()
        Rmsg = BackEndControl.AddMember(Smsg[1], Smsg[2])
        await msg.channel.send(Rmsg)

    #メンバーのadminへの昇格
    elif msg.content.startswith('.admin'):
        Smsg = msg.content.split()
        Rmsg = BackEndControl.UpdateAdmin(msg.author.id, Smsg[1])
        await msg.channel.send(Rmsg)

    #メンバーの除外
    elif msg.content.startswith('.remove'):
        Smsg = msg.content.split()
        Rmsg = BackEndControl.RemoveMember(Smsg[1])
        await msg.channel.send(Rmsg)

    #メンバー一覧
    elif msg.content == '.allmember':
        Rmsg = BackEndControl.AllMember()
        embed = discord.Embed(title='メンバー一覧')
        embed.add_field(name='id', value=Rmsg[0])
        embed.add_field(name='名前', value=Rmsg[1])
        embed.add_field(name='メンション', value=Rmsg[2])
        await msg.channel.send(embed=embed)

    #凸予約
    elif msg.content.startswith('.set'):
        Smsg = msg.content.split()
        Rmsg = BackEndControl.Reservation(Smsg[1], Smsg[2], Smsg[3], msg.author.id)
        await msg.channel.send(Rmsg)
        await ReloadStatus()

    #持越しの削除
    elif msg.content.startswith('.delco'):
        Smsg = msg.content.split()
        Rmsg = BackEndControl.DelCarryOver(msg.author.id, Smsg[1])
        await msg.channel.send(Rmsg)
        await ReloadStatus()

    #凸予約の取り消し
    elif msg.content.startswith('.del'):
        Smsg = msg.content.split()
        Rmsg = BackEndControl.DelReservation(msg.author.id, Smsg[1])
        await msg.channel.send(Rmsg)
        await ReloadStatus()

    #持越しの登録
    elif msg.content.startswith('.co'):
        Smsg = msg.content.split()
        Rmsg = BackEndControl.CarryOver(Smsg[1], Smsg[2], Smsg[3], Smsg[4], msg.author.id)
        await msg.channel.send(Rmsg)
        await ReloadStatus()
    
    #本線開始宣言
    elif msg.content.startswith('.atk'):
        Smsg = msg.content.split()
        Rmsg = BackEndControl.StartAtk(msg.author.id, Smsg[1])
        await msg.channel.send(Rmsg)
        await ReloadStatus()

    #本線終了
    elif msg.content.startswith('.end'):
        Rmsg = BackEndControl.EndAtk(msg.author.id)
        await msg.channel.send(Rmsg)
        await ReloadStatus()

    #凸の修正
    elif msg.content.startswith('.fix'):
        Rmsg = BackEndControl.fix(msg.author.id)
        await msg.channel.send(Rmsg)
        await ReloadStatus()

    #周数の切り替え
    elif msg.content == '.lc':
        NowLap = int(BackEndControl.SQLInstance.laps)
        Rmsg = BackEndControl.SQLInstance.LapChange(NowLap+1)
        await msg.channel.send(str(Rmsg)+'周目に到達しました！')

    #周数の強制切替
    elif msg.content.startswith('.lc set'):
        Smsg = msg.content.split()
        Rmsg = BackEndControl.SQLInstance.LapChange(int(Smsg[2]))
        await msg.channel.send('現在の周数を'+str(Rmsg)+'周目に設定しました')

client.run('')