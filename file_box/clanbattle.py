import openpyxl

def setin(msg, userid):
    #1~5の域を出た数値だったら怒る
    if not (0 < int(msg[1]) < 6):
        r_msg = '予約対象のボスは数値1~5で指定してください'
        return r_msg

    wb = openpyxl.open('./datasheet.xlsx')
    sh = wb['メンバーリスト']

    for i in range(30):
        if sh.cell(row=2+i, column=2).value == str(userid):
            #空いてる予約場所にいれていく
            if sh.cell(row=2+i, column=3).value == None:
                sh.cell(row=2+i, column=3).value = int(msg[1])

            elif sh.cell(row=2+i, column=4).value == None:
                sh.cell(row=2+i, column=4).value = int(msg[1])

            elif sh.cell(row=2+i, column=5).value == None:
                sh.cell(row=2+i, column=5).value = int(msg[1])
            else:
                r_msg = '3枠予約済みです．予約の取り消し後に再実行してください．'
                return r_msg

            #予約の完了
            wb.save('./datasheet.xlsx')
            r_msg = str(msg[1]) + 'ボスへの予約を受け付けました'
            return r_msg
    
    #メンバーが見つからない場合
    r_msg = '登録されていないメンバーです．リーダーに連絡してください．'
    return r_msg

def delete(msg, userid):
    #1~5の域を出た数値だったら怒る
    if not (0 < int(msg[1]) < 6):
        r_msg = '予約対象のボスは数値1~5で指定してください'
        return r_msg

    wb = openpyxl.open('./datasheet.xlsx')
    sh = wb['メンバーリスト']

    for i in range(30):
        if sh.cell(row=2+i, column=2).value == str(userid):
            #一致する予約場所を消す
            if sh.cell(row=2+i, column=3).value == int(msg[1]):
                sh.cell(row=2+i, column=3).value = None

            elif sh.cell(row=2+i, column=4).value == int(msg[1]):
                sh.cell(row=2+i, column=4).value = None

            elif sh.cell(row=2+i, column=5).value == int(msg[1]):
                sh.cell(row=2+i, column=5).value = None
            else:
                r_msg = str(msg[1]) + 'ボスへの予約が見つかりませんでした'
                return r_msg

            #予約の完了
            wb.save('./datasheet.xlsx')
            r_msg = str(msg[1]) + 'ボスへの予約を取り消しました'
            return r_msg
    
    #メンバーが見つからない場合
    r_msg = '登録されていないメンバーです．リーダーに連絡してください．'
    return r_msg

def carry_over(msg, userid):
    if not (int(msg[1]) < 6):
        r_msg = '持越しのボスは数値1~5で指定してください\n持越しの消化を宣言するときは0にして下さい'
        return r_msg
    
    wb = openpyxl.open('./datasheet.xlsx')
    sh = wb['メンバーリスト']

    for i in range(30):
        #idが一致する人の所に持ち越しを登録
        if sh.cell(row=2+i, column=2).value == str(userid):
            if int(msg[1]) == 0:
                sh.cell(row=2+i, column=7).value = None
                r_msg = '持越しを保持していない状態として登録しました'
            else:
                sh.cell(row=2+i, column=7).value = int(msg[1])
                r_msg = str(msg[1]) + 'ボスへ持越し登録を行いました．\n対象のボスが来たら通知します．'

            #予約の完了
            wb.save('./datasheet.xlsx')
            return r_msg

    #メンバーが見つからない場合
    r_msg = '登録されていないメンバーです．リーダーに連絡してください．'
    return r_msg

def atk(userid):
    wb = openpyxl.open('./datasheet.xlsx')
    sh = wb['メンバーリスト']

    for i in range(30):
        #idが一致する人の所の残凸を減らす，予約，持越し登録されてたら削除
        if sh.cell(row=2+i, column=2).value == str(userid):
            #持越し
            if sh.cell(row=2+i, column=7).value == sh['J1'].value:
                sh.cell(row=2+i, column=7).value = None
                wb.save('./datasheet.xlsx')

                r_msg = '持越しの消費として処理しました'
                return r_msg, 0
            
            #3凸済み
            if sh.cell(row=2+i, column=6).value == 0:
                r_msg = '未消化の凸を確認できませんでした．\nタスキル等により修正が必要な場合は.fixをお使いください'
                return r_msg ,2
            
            #予約と一致して凸
            if sh.cell(row=2+i, column=3).value == sh['J1'].value:
                sh.cell(row=2+i, column=3).value = None
                sh.cell(row=2+i, column=6).value -= 1

            elif sh.cell(row=2+i, column=4).value == sh['J1'].value:
                sh.cell(row=2+i, column=4).value = None
                sh.cell(row=2+i, column=6).value -= 1

            elif sh.cell(row=2+i, column=5).value == sh['J1'].value:
                sh.cell(row=2+i, column=5).value = None
                sh.cell(row=2+i, column=6).value -= 1
            
            else:
                sh.cell(row=2+i, column=6).value -= 1
            
            wb.save('./datasheet.xlsx')
            r_msg = '残り' + str(sh.cell(row=2+i, column=6).value) + '凸です'
            return r_msg, 1
        
    #メンバーが見つからない場合
    r_msg = '登録されていないメンバーです．リーダーに連絡してください．'
    return r_msg, 2

def fix(userid):
    wb = openpyxl.open('./datasheet.xlsx')
    sh = wb['メンバーリスト']

    for i in range(30):
        #idが一致する人の所の残凸を増やす
        if sh.cell(row=2+i, column=2).value == str(userid):
            #修正の必要がない場合
            if sh.cell(row=2+i, column=6).value == 3:
                r_msg = '1凸も記録されていません．\n修正処理は行いませんでした．'
                return r_msg

            #増やす処理
            sh.cell(row=2+i, column=6).value += 1
            wb.save('./datasheet.xlsx')
            r_msg = '修正処理を行いました．残り' + str(sh.cell(row=2+i, column=6).value) + '凸です．'
            return r_msg
        
    #メンバーが見つからない場合
    r_msg = '登録されていないメンバーです．リーダーに連絡してください．'
    return r_msg

def boss_change():
    wb = openpyxl.open('./datasheet.xlsx')
    sh = wb['メンバーリスト']

    #ボスの変更処理
    sh['J1'].value += 1
    if sh['J1'].value == 6:
        sh['J1'].value = 1
    wb.save('./datasheet.xlsx')
    
    msg = str(sh['J1'].value) + "ボスが来ました！\n予約者\n"
    #予約者の確認
    for i in range(30):
        #予約をリスト化
        for reserve_list_cell in sh['C'+str(i+2)+':E'+str(i+2)]:
            reserve_list = []
            for j in range(len(reserve_list_cell)):
                reserve_list.append(reserve_list_cell[j].value)

        #予約リストの中に含まれていたら…
        if sh['J1'].value in reserve_list:
            msg += '<@'+str(sh.cell(row=2+i, column=2).value)+'> '
    
    #持越し登録者の確認
    msg += '\n持越し登録者\n'
    for i in range(30):
        if sh.cell(row=i+2, column=7).value == sh['J1'].value:
            msg += '<@'+str(sh.cell(row=2+i, column=2).value)+'> '
    
    return msg

def boss_set(num):
    #受け取った値が正常か
    if not (0<num<6):
        r_msg = 'ボスの値は1~6を指定してください．'
    
    else:
        wb = openpyxl.open('./datasheet.xlsx')
        sh = wb['メンバーリスト']

        #ボスの値を変更
        sh['J9'].value = num
        wb.save('./datasheet.xlsx')

        r_msg = '現在のボスを' + str(num) + 'に変更しました'

    return r_msg
    