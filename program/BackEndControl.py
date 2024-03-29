import SQLControl

Admin = [325177738921115648, 541246198141681665]
SQLInstance = SQLControl.SQLControl()

#メンバーの追加
def AddMember(name, discord):
    #30人登録されているようなら不可能の通知
    if len(SQLInstance.MemberList) == 30:
        return 'メンバーリストがいっぱいです'

    #すでに登録されていないか判定
    Data = SQLInstance.FindMemberDiscord(discord)
    if not len(Data) == 0:
        return 'すでに登録されています'

    #登録処理
    SQLInstance.AddMember(name, discord)
    return '登録しました'

#メンバーの削除
def RemoveMember(Memberid):
    #未登録の場合は除外できない
    Data = SQLInstance.FindMemberMemberid(Memberid)
    if len(Data) == 0:
        return '除外対象が見つかりませんでした'

    SQLInstance.DeleteMember(Memberid)
    return '除外しました'

#embed用のメンバー一覧
def AllMember():
    idStr = ''
    NameStr = ''
    MentionStr = ''

    for i in range(len(SQLInstance.MemberList)):
        NowData = SQLInstance.MemberList[i]
        
        #進行役なら名前に★
        if NowData[3] == 1:
            NameStr += (NowData[1] + '★\n')
        else:
            NameStr += (NowData[1] + '\n')
        
        idStr += (str(NowData[0]) + '\n')
        MentionStr += ('<@'+str(NowData[2])+'>\n')

    return idStr, NameStr, MentionStr

#進行役への昇格
def UpdateAdmin(MsgDiscord, Memberid):
    #このコマンドを使える人(なぎさん)か
    if not MsgDiscord in Admin:
        return '管理者のみこのコマンドを使えます'

    #対象のメンバーを検索
    if len(SQLInstance.FindMemberMemberid(Memberid)) == 0:
        return '対象メンバーが見つかりませんでした'
    
    #昇格処理
    SQLInstance.UpdateAdmin(Memberid)
    return '指定されたメンバーを進行役にしました'

#凸の予約
def Reservation(msg, discord):
    #投稿されたメッセージにコメントないなら適当にうめる
    if len(msg) == 4:
        msg.append('')

    #BossNoが適切な範囲内か
    if not (0 < int(msg[1]) < 6):
        return '予約対象のボスは数値1~5で指定してください'

    #パーティの判断
    if msg[2] not in ['物理', '魔法', 'ニャル']:
        return '編成を認識できませんでした\n物理・魔法・ニャルのいずれかを入力して下さい'

    #ワンパンかどうかの判断
    if msg[3] == 'ワンパン':
        msg[3] = -1
    else:
        msg[3] = int(msg[3].replace('万', '')) 

    #対象のメンバーを検索
    Data = SQLInstance.FindMemberDiscord(discord)
    if len(Data) == 0:
        return '登録されていないメンバーです'

    #予約処理
    SQLInstance.Reservation(Data[0][0], msg[1], msg[2], msg[3], msg[4])
    return (str(msg[1])+'ボスへの予約を受け付けました')

#本線開始宣言
def StartAtk(discord, BossNo):
    #BossNoが適切な範囲内か
    if not (0 < int(BossNo) < 6):
        return 'ボスは数値1~5で指定してください'

    #対象のメンバーを検索
    MemberData = SQLInstance.FindMemberDiscord(discord)
    if len(MemberData) == 0:
        return '登録されていないメンバーです'

    #残り凸があるのか
    TotsuData = SQLInstance.FindTotsuMemberid(MemberData[0][0])
    CoData = SQLInstance.FindCarryOverMemberid(MemberData[0][0])
    if ((TotsuData[0][1] == 0) and (len(CoData) == 0)):
        return '既に3凸済みです\n持越しも未登録です'

    #すでに本戦済み
    if not TotsuData[0][2] == 0:
        SQLInstance.atk(MemberData[0][0], BossNo)
        return ('現在'+str(TotsuData[0][2])+'ボスと本戦中です\n本戦中の対象を'+str(BossNo)+'に切り替えました')
    
    #凸状態に変更
    SQLInstance.atk(MemberData[0][0], BossNo)
    return '本戦開始を受け付けました'

#持越し戦終了
def EndCo(discord, msg):
    #対象のメンバーを検索
    MemberData = SQLInstance.FindMemberDiscord(discord)
    if len(MemberData) == 0:
        return '登録されていないメンバーです'

    #既に本戦開始宣言をしているのか
    TotsuData = SQLInstance.FindTotsuMemberid(MemberData[0][0])
    if TotsuData[0][2] == 0:
        return '本戦開始宣言が行われていません'

    #ダメージの認識
    damage = msg[1].replace('万', '')
    if (damage == '〆') or (damage == '-1'):
        #死亡は-1
        SQLInstance.FixBossHP(TotsuData[0][2], -1)
    else:
        damage = int(damage)
        #書き込まれたダメージ数が残HPと比較して正しいか
        if damage > SQLInstance.SelectBossHP(TotsuData[0][2]):
            return 'ダメージ数がボスの残HPを超えています\nボスを討伐した場合は .end 〆 と入力してください'
        
        #ダメージをデータベースに反映
        SQLInstance.DamageBoss(TotsuData[0][2], damage)
    
    #凸完了処理
    CoData = SQLInstance.FindCarryOverMemberid(MemberData[0][0])
    SQLInstance.end(MemberData[0][0])
    SQLInstance.DoneCarryOver(CoData[0][0])

    return '持越しの消化として処理しました'

#本戦終了宣言(持越し消化宣言)
def EndAtk(discord, msg):
    #対象のメンバーを検索
    MemberData = SQLInstance.FindMemberDiscord(discord)
    if len(MemberData) == 0:
        return '登録されていないメンバーです'

    #既に本戦開始宣言をしているのか
    TotsuData = SQLInstance.FindTotsuMemberid(MemberData[0][0])
    if TotsuData[0][2] == 0:
        return '本戦開始宣言が行われていません'
    
    #ダメージの認識
    damage = msg[1].replace('万', '')
    if (damage == '〆') or (damage == '-1'):
        #死亡は-1
        SQLInstance.FixBossHP(TotsuData[0][2], -1)
    else:
        damage = int(damage)
        #書き込まれたダメージ数が残HPと比較して正しいか
        if damage > SQLInstance.SelectBossHP(TotsuData[0][2]):
            return 'ダメージ数がボスの残HPを超えています\nボスを討伐した場合は .end 〆 と入力してください'
        
        #ダメージをデータベースに反映
        SQLInstance.DamageBoss(TotsuData[0][2], damage)

    #凸完了処理
    SQLInstance.end(MemberData[0][0])
    SQLInstance.DoneTotsu(MemberData[0][0])

    #予約済みの凸なのか
    ReservationData = SQLInstance.FindReservationMemberid(MemberData[0][0], TotsuData[0][2])
    if not len(ReservationData) == 0:
        SQLInstance.DoneReservation(ReservationData[0][0])
        return '予約の消化として処理しました'
    
    #予約なし凸
    return '本戦終了を受け付けました'

#凸数の修正
def fix(discord):
    #対象のメンバーを検索
    MemberData = SQLInstance.FindMemberDiscord(discord)
    if len(MemberData) == 0:
        return '登録されていないメンバーです'
    
    #修正可能か
    TotsuData = SQLInstance.FindTotsuMemberid(MemberData[0][0])
    if TotsuData[0][1] == 3:
        return '1凸も記録されていません\n修正処理は行いませんでした'
    
    #修正処理
    SQLInstance.fix(MemberData[0][0])
    return '凸数を一つ増やしました'

#予約の取り消し
def DelReservation(discord, Reservationid):
    #登録されている予約か判定
    Data = SQLInstance.FindReservationReservationid(Reservationid)
    if len(Data) == 0:
        return '予約が見つかりません'

    #メンバーの情報を取得
    MemberData = SQLInstance.FindMemberDiscord(discord)
    if len(MemberData) == 0:
        return '登録されていないメンバーです'
    
    #予約者と一緒or管理者だったら予約削除
    if ((MemberData[0][3] == 1) or (Data[0][1] == MemberData[0][0])):
        SQLInstance.DoneReservation(Reservationid)
        return '指定された予約を削除しました'

    #削除できないよ…
    return '予約の削除は進行役または本人のみが行えます'

#持越しの登録
def CarryOver(msg, discord):
    #コメントの有無確認
    if len(msg) == 5:
        msg.append('')

    #BossNoが適切な範囲内か
    if not (0 < int(msg[1]) < 6):
        return '予約対象のボスは数値1~5で指定してください'
    
    #残り秒数が適切か
    if not (20 < int(msg[2]) < 91):
        return '持越し秒数は21~90秒の間で入力して下さい'

    #パーティが適切か
    if msg[3] not in ['物理', '魔法', 'ニャル']:
        return '編成を認識できませんでした\n物理・魔法・ニャルのいずれかを入力して下さい'

    #ダメージの判定
    if msg[4] == 'ワンパン':
        damage = -1
    else:
        damage = int(msg[4].replace('万', ''))

    #対象のメンバーを検索
    MemberData = SQLInstance.FindMemberDiscord(discord)
    if len(MemberData) == 0:
        return '登録されていないメンバーです'

    #持越しが3件以上登録されていないか判定
    CoData = SQLInstance.FindCarryOverMemberid(MemberData[0][0])
    if len(CoData) == 3:
        return '既に3件の持越し登録がされています\n.delco で既存の登録を削除してください'
    
    #持越しの登録
    SQLInstance.AddCarryOver(\
        MemberData[0][0], int(msg[1]), int(msg[2]), msg[3], damage, msg[5])    
    return '持越しを登録しました'

#持越しの削除
def DelCarryOver(discord, CarryOverid):
    #登録されている予約か判定
    CoData = SQLInstance.FindCarryOverCoid(CarryOverid)
    if len(CoData) == 0:
        return '予約が見つかりません'
    
    #メンバーの情報を取得
    MemberData = SQLInstance.FindMemberDiscord(discord)
    if len(MemberData) == 0:
        return '登録されていないメンバーです'

    #予約者と一緒or進行役だった持越し削除
    if ((MemberData[0][3] == 1) or (CoData[0][1] == MemberData[0][0])):
        SQLInstance.DoneCarryOver(CarryOverid)
        return '指定された持越しを削除しました'
    
    #削除できないよ…
    return '持越し状態の削除は進行役または本人のみが行えます'

#ボスの名前の設定
def RegBossName(msg):
    #ボスのNoが適切か
    BossNo = int(msg[2])
    if not 0 < BossNo < 6:
        return 'ボスは数値1~5で指定してください'

    SQLInstance.RegBossName(BossNo, msg[3])
    return '名前を登録しました'

#ボスのHPの設定
def RegBossHP(msg):
    #ボスのNoが適切か
    BossNo = int(msg[2])
    if not 0 < BossNo < 6:
        return 'ボスは数値1~5で指定してください'

    SQLInstance.RegBossHP(BossNo, int(msg[3]))
    return '最大HPを登録しました'

#ボスHPの強制変更
def FixBossHP(msg):
    #ボスのNoが適切か
    BossNo = int(msg[2])
    if not 0 < BossNo < 6:
        return 'ボスは数値1~5で指定してください'
    
    #与えられたHP数が適切か
    NewHP = int(msg[3].replace('万', ''))
    if SQLInstance.SelectBossMaxHP(BossNo) < NewHP:
        return 'ボスの最大HPを超える値を設定しようとしています'
    
    SQLInstance.FixBossHP(BossNo, NewHP)

    #応答メッセージの作成
    if NewHP == -1:
        return (str(BossNo)+'ボスを討伐済みに設定しました')
    else:
        return (str(BossNo)+'ボスのHPを'+str(NewHP)+'万に設定しました')

#周数の増加
def LapChange():
    #現在の周数を取得
    NowLap = int(SQLInstance.laps)

    #データベース操作
    SQLInstance.LapChange(NowLap+1)
    SQLInstance.ResetBossHP()

    #予約者一覧のdiscordidを取得
    DiscordData = list(set(SQLInstance.ReservationDiscordId()))
    
    #予約なしなら終わり
    if len(DiscordData) == 0:
        return (str(NowLap+1) + '周目に到達しました')

    #メンションできる形式にして繋げる
    result = str(NowLap+1) + '周目に到達しました\n**予約者一覧**'
    for i in range(len(DiscordData)):
        result += ('\n<@' + str(DiscordData[i]) + '>')
    
    return result
