import datetime
import openpyxl

#残り予約の確認
def reserve():
    wb = openpyxl.open('./datasheet.xlsx', data_only=True)
    sh = wb['メンバーリスト']

    #総数，型の宣言
    one = [0, '→']
    two = [0, '→']
    thr = [0, '→']
    fou = [0, '→']
    fiv = [0, '→']

    #予約に番号が入っていたら追加
    for i in range(30):
        #範囲の値を取得
        for reserve_list_cell in sh['C'+str(i+2)+':E'+str(i+2)]:
            reserve_list = []
            for j in range(len(reserve_list_cell)):
                reserve_list.append(reserve_list_cell[j].value)
        
        if 1 in reserve_list:
            one[0] += 1
            one[1] += str(sh.cell(row=2+i, column=1).value) + ', '
        
        if 2 in reserve_list:
            two[0] += 1
            two[1] += str(sh.cell(row=2+i, column=1).value) + ', '
        
        if 3 in reserve_list:
            thr[0] += 1
            thr[1] += str(sh.cell(row=2+i, column=1).value) + ', '
        
        if 4 in reserve_list:
            fou[0] += 1
            fou[1] += str(sh.cell(row=2+i, column=1).value) + ', '
        
        if 5 in reserve_list:
            fiv[0] += 1
            fiv[1] += str(sh.cell(row=2+i, column=1).value) + ', '
    
    return one, two, thr, fou, fiv

def remaing():
    wb = openpyxl.open('./datasheet.xlsx')
    sh = wb['メンバーリスト']

    #残凸数の確認
    msg = ''
    rem = 0
    cao = 0
    for i in range(30):
        if sh.cell(row=i+2, column=6).value == 3:
            msg += str(sh.cell(row=i+2, column=1).value) + '@3'
            rem += 3
        
            if not sh.cell(row=i+2, column=7).value is None:
                msg += '+co' + str(sh.cell(row=i+2, column=7).value)
                cao += 1
            msg += '\n'

    for i in range(30):
        if sh.cell(row=i+2, column=6).value == 2:
            s_msg += str(sh.cell(row=i+2, column=1).value) + '@2'
            rem += 2

            if not sh.cell(row=i+2, column=7).value is None:
                msg += '+co' + str(sh.cell(row=i+2, column=7).value)
                cao += 1
            msg += '\n'
    
    for i in range(30):
        if sh.cell(row=i+2, column=6).value == 1:
            f_msg += str(sh.cell(row=i+2, column=1).value) + '@1'
            rem +- 1
        
            if not sh.cell(row=i+2, column=7).value is None:
                msg += '+co' + str(sh.cell(row=i+2, column=7).value)
                cao += 1
            msg += '\n'
    
    for i in range(30):
        if sh.cell(row=i+2, column=6).value == 0:
            f_msg += str(sh.cell(row=i+2, column=1).value) + '@0'
        
            if not sh.cell(row=i+2, column=7).value is None:
                msg += '+co' + str(sh.cell(row=i+2, column=7).value)
                cao += 1
            msg += '\n'
    
    msg += '\n全体で' + str(rem) + '凸残っています'
    msg += '\n持越しが' + str(cao) + '件残っています'
    return msg, str(sh['J1'].value)

def endgame():
    #現在時刻をHH:MM形式で取得，55秒おき
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    now = now.strftime('%H:%M')

    #もしクローズできる時間じゃないなら帰る
    if not (now=='04:59'):
        return False

    #クローズ処理可能な時間ならExcelを開く
    wb = openpyxl.open('./datasheet.xlsx')
    sh = wb['メンバーリスト']

    #合計45凸以上記録されていたらクラバト中と認識
    remain_sum = 0
    for i in range(30):
        remain_sum += sh.cell(row=i+2, column=6).value
    
    if remain_sum > 45:
        wb.close()
        return False
    
    #各種数値をリセット
    for i in range(30):
        sh.cell(row=i+2, column=3).value = None
        sh.cell(row=i+2, column=4).value = None
        sh.cell(row=i+2, column=5).value = None
        sh.cell(row=i+2, column=6).value = 3
        sh.cell(row=i+2, column=7).value = None

    #保存，返す
    wb.save('./datasheet.xlsx')
    r_msg = '本日の凸漏れ数は'+str(remain_sum)+'件です'

    return r_msg
    