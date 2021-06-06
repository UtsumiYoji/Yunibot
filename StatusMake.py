import SQLControl
import datetime
SQLInstance = SQLControl.SQLControl()

def StatusMake():
    #残凸数のデータ
    RemainTotsu3 = ''
    RemainTotsu2 = ''
    RemainTotsu1 = ''
    RemainTotsu0 = ''
    RemainMain = 0
    RemainOver = 0

    #残凸ループ処理
    for i in range(len(SQLInstance.MemberList)):
        #持越し情報を記録
        CoData = SQLInstance.FindCarryOverMemberid(SQLInstance.MemberList[i][0])

        if SQLInstance.TotsuStatus[i][1] == 3:
            RemainMain += 3
            #本戦中かどうか判断
            if not SQLInstance.TotsuStatus[i][2] == 0:
                RemainTotsu3 += str(SQLInstance.TotsuStatus[i][2]) + '⚔️'

            RemainTotsu3 += (SQLInstance.MemberList[i][1] + '@3')
            if not len(CoData) == 0:
                RemainOver += 1
                RemainTotsu3 += ('co' + str(CoData[0][2]))
            RemainTotsu3 += '\n'

        elif SQLInstance.TotsuStatus[i][1] == 2:
            RemainMain += 2
            #本戦中かどうか判断
            if not SQLInstance.TotsuStatus[i][2] == 0:
                RemainTotsu2 += str(SQLInstance.TotsuStatus[i][2]) + '⚔️'

            RemainTotsu2 += (SQLInstance.MemberList[i][1] + '@2')
            if not len(CoData) == 0:
                RemainOver += 1
                RemainTotsu2 += ('co' + str(CoData[0][2]))
            RemainTotsu2 += '\n'

        elif SQLInstance.TotsuStatus[i][1] == 1:
            RemainMain += 1
            #本戦中かどうか判断
            if not SQLInstance.TotsuStatus[i][2] == 0:
                RemainTotsu1 += str(SQLInstance.TotsuStatus[i][2]) + '⚔️'

            RemainTotsu1 += (SQLInstance.MemberList[i][1] + '@1')
            if not len(CoData) == 0:
                RemainOver += 1
                RemainTotsu1 += ('co' + str(CoData[0][2]))
            RemainTotsu1 += '\n'

        else:
            if not len(CoData) == 0:
                #本戦中かどうか判断
                if SQLInstance.TotsuStatus[i][2] == 0:
                    RemainTotsu0 += str(SQLInstance.TotsuStatus[i][2]) + '⚔️'
                
                RemainOver += 1
                RemainTotsu0 += (SQLInstance.MemberList[i][1] + '0')
                RemainTotsu0 += ('co' + str(CoData[0][2])) 
                RemainTotsu0 += '\n'
    
    #凸情報を繋げる
    RemainTotsu = RemainTotsu3 + RemainTotsu2 + RemainTotsu1 + RemainTotsu0 +\
        '全体で' + str(RemainMain) + '凸残っています' + \
        '\n持越しが' + str(RemainOver) + '件残っています'
    del RemainTotsu3, RemainTotsu2, RemainTotsu1, RemainTotsu0

    #予約ループ処理
    ReservationMsg = ''
    if len(SQLInstance.ReservationList) == 0:
        ReservationMsg = '予約なし'

    else:
        for i in range(len(SQLInstance.ReservationList)):
            #メンバー名の取得
            MemberName = SQLInstance.FindMemberMemberid(SQLInstance.ReservationList[i][1])[0][1]

            ReservationMsg += '('+str(SQLInstance.ReservationList[i][0])+')' +\
                                str(MemberName) + ' '+\
                                str(SQLInstance.ReservationList[i][3]) + '周目' +\
                                str(SQLInstance.ReservationList[i][2]) + 'ボス' +\
                                ':'+str(SQLInstance.ReservationList[i][4]) + '\n'

    #持越しループ処理
    CarryOverMsg = ''
    if len(SQLInstance.CarryOver) == 0:
        CarryOverMsg = '持越し記録なし'

    else:
        for i in range(len(SQLInstance.CarryOver)):
            #メンバー名の取得
            MemberName = SQLInstance.FindMemberMemberid(SQLInstance.CarryOver[i][1])[0][1]

            CarryOverMsg += '('+str(SQLInstance.CarryOver[i][0])+')' +\
                            str(MemberName) + ' '+\
                            str(SQLInstance.CarryOver[i][2]) + 'ボス ' +\
                            str(SQLInstance.CarryOver[i][3]) + '秒 '+\
                            str(SQLInstance.CarryOver[i][4]) +\
                            ':'+str(SQLInstance.CarryOver[i][5]) + '\n'

    #段階処理，周数処理
    lap = SQLInstance.laps
    if lap < 4:
        LapMsg = str(lap)+'周目 1段階目'
    elif lap < 11:
        LapMsg = str(lap)+'周目 2段階目'
    elif lap < 31:
        LapMsg = str(lap)+'周目 3段階目'
    elif lap < 41:
        LapMsg = str(lap)+'周目 4段階目'
    else:
        LapMsg = str(lap)+'周目 5段階目'

    #終わり，返す
    return RemainTotsu, ReservationMsg, CarryOverMsg, LapMsg, RemainMain

def EndGame():
    #現在時刻を取得
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    now = now.strftime('%H:%M')

    #切り替わり時間か
    if not (now == '04:59'):
        return False
    
    #凸漏れ通知のためのメッセージ
    StatusData = StatusMake()

    #凸数，予約のリセット
    SQLInstance.EndGame()

    #メッセージを投稿するかどうか
    if StatusData[4] < 45:
        return StatusData[0]