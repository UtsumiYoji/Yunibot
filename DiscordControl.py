import discord

client = discord.Client()

#

@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Game(name='Running on Ver.2.0.0.0')
    )

@client.event
async def on_message(msg):
    #メンバーの登録
    if msg.content.startwith('.add'):
        pass

    #メンバーのadminへの昇格
    if msg.content.startwith('.admin'):
        pass

    #メンバーの除外
    if msg.content.startwith('.remove'):
        pass

    #メンバー一覧
    if msg.content == '.allmember':
        pass

    #凸予約
    if msg.content.startswith('.set'):
        pass

    #凸予約の取り消し
    if msg.content.startswith('.del'):
        pass

    #持越しの登録
    if msg.content.startswith('.co'):
        pass

    #本線開始宣言
    if msg.content.startswith('.atk'):
        pass

    #本線終了
    if msg.content.startswith('.end'):
        pass

    #凸の修正
    if msg.content.startswith('.fix'):
        pass

    #周数の切り替え
    if msg.content == 'lc':
        pass

    #周数の強制切替
    if msg.content.startswith('.lc set'):
        pass