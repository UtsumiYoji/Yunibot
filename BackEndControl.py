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
def Reservation(BossNo, lap, comment, discord):
    #BossNoが適切な範囲内か
    if not (0 < int(BossNo) < 6):
        return '予約対象のボスは数値1~5で指定してください'
    
    #周回数的に予約できる範囲か
    if int(lap) < SQLInstance.laps:
        return '何週目の指定が不適切です'

    #対象のメンバーを検索
    Data = SQLInstance.FindMemberDiscord(discord)
    if len(Data) == 0:
        return '登録されていないメンバーです'

    #予約処理
    SQLInstance.Reservation(Data[0][0], BossNo, lap, comment)
    return (str(lap)+'週目'+str(BossNo)+'ボスへの予約を受け付けました')

#本線開始宣言
def StartAtk(discord, BossNo):
    #BossNoが適切な範囲内か
    if not (0 < int(BossNo) < 6):
        return 'ボスは数値1~5で指定してください'

    #対象のメンバーを検索
    MemberData = SQLInstance.FindMemberDiscord(discord)
    if len(MemberData) == 0:
        return '登録されていないメンバーです'

    #既に本戦中じゃないか，残り凸があるのか
    TotsuData = SQLInstance.FindTotsuMemberid(MemberData[0][0])
    CoData = SQLInstance.FindCarryOverMemberid(MemberData[0][0])
    if ((TotsuData[0][1] == 0) and (len(CoData) == 0)):
        return '既に3凸済みで、持越しも登録されていません'
    if not TotsuData[0][2] == 0:
        SQLInstance.atk(MemberData[0][0], BossNo)
        return ('現在'+str(TotsuData[0][2])+'ボスと本戦中です\n本戦中の対象を'+str(BossNo)+'に切り替えました')
    
    #凸状態に変更
    SQLInstance.atk(MemberData[0][0], BossNo)
    return '本戦開始を受け付けました'

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
    damege = msg[1].replace('万', '')
    if damege == '〆':
        damege = '〆'
    elif damege.isdecimal():
        damege = int(damege)
        #現在の
    else:
        return '〆または与えたダメージを入力してください'

    #持越しかどうか判定
    CoData = SQLInstance.FindCarryOverMemberid(MemberData[0][0])
    if not len(CoData) == 0:
        SQLInstance.DoneCarryOver(CoData[0][0])
        SQLInstance.end(MemberData[0][0])
        return '持越しの完了として処理しました'

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
def CarryOver(BossNo, RemainSecond, party, comment, discord):
    #BossNoが適切な範囲内か
    if not (0 < int(BossNo) < 6):
        return '予約対象のボスは数値1~5で指定してください'
    
    #残り秒数が適切か
    if not (20 < int(RemainSecond) < 91):
        return '持越し秒数は21~90秒の間で入力して下さい'

    #パーティが適切か
    if party not in ['物理', '魔法', 'ニャル']:
        return '編成を認識できませんでした\n物理・魔法・ニャルのいずれかを入力して下さい'

    #対象のメンバーを検索
    MemberData = SQLInstance.FindMemberDiscord(discord)
    if len(MemberData) == 0:
        return '登録されていないメンバーです'

    #持越しが登録されていないか判定
    CoData = SQLInstance.FindCarryOverMemberid(MemberData[0][0])
    if not len(CoData) == 0:
        #登録されていたら完了したことにしてしまう
        SQLInstance.DoneCarryOver(CoData[0][0])
    
    #持越しの登録
    SQLInstance.AddCarryOver(\
        MemberData[0][0], int(BossNo), int(RemainSecond), party, comment)    
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
