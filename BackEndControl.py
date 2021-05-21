import SQLControl

SQLInstance = SQLControl.SQLControl()

#discordidからメンバーが登録されているか判定する
def JudgmentDiscord(discord):
    MemberList = SQLInstance.MemberList()
    DiscordList = MemberList[:, 2]

    if discord in DiscordList:
        return True
    else:
        return False

#discordidからMemberidが登録されているか判定する
def FindMemberid(discord):
    MemberList = SQLInstance.MemberList()
    DiscordList = MemberList[:, 2]

    index = DiscordList.index(discord)
    return MemberList[index, 0]

#メンバーの追加
def AddMember(name, discord):
    #現在のメンバー全体を取得
    MemberList = SQLInstance.MemberList()

    #30人登録されているようなら不可能の通知
    if len(MemberList) == 30:
        return 'メンバーリストがいっぱいです'

    #すでに登録されていないか判定
    if discord in MemberList[:, 2]:
        return 'すでに登録されています'

    #登録処理
    SQLInstance.AddMember(name, discord)
    return '登録しました'

#メンバーの削除
def RemoveMember(discord):
    #未登録の場合は除外できない
    if not JudgmentDiscord(discord):
        return '除外対象が見つかりませんでした'
    
    #削除処理
    Memberid = FindMemberid(discord)
    SQLInstance.DeleteMember(Memberid)

    return '除外しました'

#管理者(予約消去できる人)に変更
def UpdateAdmin(MsgDiscord, UpdateDiscord):
    #このコマンドを使える人(なぎさん)か
    if not MsgDiscord == 541246198141681665:
        return '管理者のみこのコマンドを使えます'

    #対象のメンバーを検索
    if not JudgmentDiscord(UpdateDiscord):
        return '対象メンバーが見つかりませんでした'
    
    #昇格処理
    Memberid = FindMemberid(UpdateDiscord)
    SQLInstance.UpdateAdmin(Memberid)

    return '指定されたメンバーを進行役にしました'

#凸の予約
def Reservation(BossNo, lap, comment, discord):
    #BossNoが適切な範囲内か
    if not (0 < BossNo < 6):
        return '予約対象のボスは数値1~5で指定してください'
    
    #周回数的に予約できる範囲か
    if lap < SQLInstance.LapStatus():
        return '何週目の指定が不適切です'

    #対象のメンバーを検索
    if not JudgmentDiscord(discord):
        return '登録されていないメンバーです'

    #予約処理
    Memberid = FindMemberid(discord)
    SQLInstance.Reservation(Memberid, BossNo, lap, comment)

    return (str(lap)+'週目'+str(BossNo)+'ボスへの予約を受け付けました')

#本線開始宣言
def StartAtk(discord, BossNo):
    #対象のメンバーを検索
    if not JudgmentDiscord(discord):
        return '登録されていないメンバーです'
    
