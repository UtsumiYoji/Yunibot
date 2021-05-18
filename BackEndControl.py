import SQLControl

SQLInstance = SQLControl.SQLControl()

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
    #現在のメンバー全体を取得
    MemberList = SQLInstance.MemberList()
    DiscordList = MemberList[:, 2]

    #未登録の場合は除外できない
    if not discord in DiscordList:
        return '除外対象が見つかりませんでした'
    
    #削除処理
    index = DiscordList.index(discord)
    SQLInstance.DeleteMember(MemberList[index, 0])

    return '除外しました'

#管理者(予約消去できる人)に変更
def UpdateAdmin(MsgDiscord, UpdateDiscord):
    #このコマンドを使える人(なぎさん)か
    if not MsgDiscord == 541246198141681665:
        return '管理者のみこのコマンドを使えます'

    #現在のメンバー全体を取得
    MemberList = SQLInstance.MemberList()
    DiscordList = MemberList[:, 2]

    #対象のメンバーを検索
    if not UpdateDiscord in DiscordList:
        return '対象メンバーが見つかりませんでした'
    
    #昇格処理
    index = DiscordList.index(UpdateDiscord)
    SQLInstance.UpdateAdmin(index)

    return '指定されたメンバーを進行役にしました'
