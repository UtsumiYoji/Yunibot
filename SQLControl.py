import sqlite3

class SQLControl:
    MemberList = []
    TotsuStatus = []
    CarryOver = []
    laps = 0
    ReservationList = []

    #コンストラクタ
    def __init__(self):
        self.con = sqlite3.connect('YuniBot.db', isolation_level=None, check_same_thread=False)
        self.cur = self.con.cursor()

        #メンバーリストを取得
        self.cur.execute(
            "select * from Member"
        )
        SQLControl.MemberList = self.cur.fetchall()

        #凸状況の取得
        self.cur.execute(
            "select * from TotsuStatus"
        )
        SQLControl.TotsuStatus = self.cur.fetchall()

        #周回数状況
        self.cur.execute(
            "select * from Laps"
        )
        SQLControl.laps = int(self.cur.fetchall()[0][1])

        #持越し状況
        self.cur.execute(
            "select * from CarryOver where Done = 0"
        )
        SQLControl.CarryOver = self.cur.fetchall()

        #予約状況
        self.cur.execute(
            "select * from Reservation where Done = 0"
        )
        SQLControl.ReservationList = self.cur.fetchall()
    
    #メンバーリスト，凸状況の更新
    def UpdateMemberList(self):
        self.cur.execute(
            "select * from Member"
        )
        SQLControl.MemberList = self.cur.fetchall()

        self.cur.execute(
            "select * from TotsuStatus"
        )
        SQLControl.TotsuStatus = self.cur.fetchall()

    #デストラクタ
    def __del__(self):
        self.cur.close()
        self.con.close()
    
    #テーブルの作成
    def MakeTable(self):
        #メンバーテーブル
        self.cur.execute(
            "create table Member(\
                Memberid integer primary key autoincrement,\
                name string, \
                discord string,\
                admin integer default 0)"
        )

        #凸数管理テーブル
        self.cur.execute(
            "create table TotsuStatus(\
                Memberid integer primary key autoincrement,\
                RemainTotsu integer,\
                NowTotsu integer default 0)"
        )

        #予約登録テーブル
        self.cur.execute(
            "create table Reservation(\
                Reservationid integer primary key autoincrement,\
                Memberid integer,\
                ReservationBossNo integer,\
                lap integer,\
                ReservationComment string,\
                Done integer default 0)"
        )

        #持ち越し登録テーブル
        self.cur.execute(
            "create table CarryOver(\
                CarryOverid integer primary key autoincrement,\
                Memberid integer,\
                BossNo integer,\
                RemainSecond integer,\
                party string,\
                comment string,\
                Done integer default 0)"
        )

        #周回数テーブル
        self.cur.execute(
            "create table Laps(Lapid integer primary key autoincrement, lap integer)"
        )
        self.cur.execute(
            "insert into Laps(lap) values(1)"
        )

    #v2.1で追加予定のテーブルを作る関数
    def MakeBossHPTable(self):
        #テーブル一覧を取得
        self.cur.execute(
            "select name from sqlite_master where type = 'table'"
        )
        TableList = [table[0] for table in self.cur.fetchall()]
        
        #テーブルがない場合は作成
        if 'BossHP' not in TableList:
            self.cur.execute(
                "create table BossHP(id integer primary key autoincrement, name string, hp integer)"
            )
            for i in range(1, 6):
                self.cur.execute(
                    "insert into BossHP(name, hp) values('ボス"+str(i)+"', 100)"
                )
            print('ボスHPを登録するテーブルが作成されていないため作成しました')

    #ボスの名前を登録する
    def RegBossName(self, BossNo, name):
        self.cur.execute(
            "update BossHP set name = '" + name + "' where id = " + str(BossNo)
        )
    
    #ボスの最大HPを登録する
    def RegBossHP(self, BossNo, BossHP):
        self.cur.execute(
            "update BossHP set hp = " + str(BossHP) + " where id = " + str(BossNo)
        )
    
    #ボスにダメージを与える
    def DamageBoss(self, BossNo, Damage):
        self.cur.execute(
            "update BossHP set hp = hp - " + str(Damage) + " where id = " + str(BossNo)
        )
    
    #ボスのHPを強制的に変更する
    def FixBossHP(self, BossNo, HP):
        self.cur.execute(
            "update BossHP set hp = " + str(HP) + " where id = " + str(BossNo)
        )

    #各ボスの残HP状況を取得
    def ViewBossHP(self):
        self.cur.execute(
            "select * from BossHP"
        )
        return self.cur.fetchall()

    #メンバーの追加
    def AddMember(self, name, discord):
        self.cur.execute(
            "insert into Member(name, discord) values('"+name+"','"+str(discord)+"')"
        )
        self.cur.execute(
            "insert into TotsuStatus(RemainTotsu) values(3)"
        )
        self. UpdateMemberList()
    
    #メンバーに進行権限を付与
    def UpdateAdmin(self, Memberid):
        self.cur.execute(
            "update Member set admin = 1 where Memberid =" + str(Memberid)
        )
        self. UpdateMemberList()
    
    #メンバーの削除
    def DeleteMember(self, Memberid):
        self.cur.execute(
            "delete from Member where Memberid =" + str(Memberid)
        )
        self.cur.execute(
            "delete from TotsuStatus where Memberid =" + str(Memberid)
        )
        self. UpdateMemberList()

    #指定されたdiscordのデータを返してくれる
    def FindMemberDiscord(self, discord):
        self.cur.execute(
            "select * from Member where discord = " + str(discord)
        )
        result = self.cur.fetchall()

        return result
    
    #指定されたMemberidのデータを返してくれる
    def FindMemberMemberid(self, Memberid):
        self.cur.execute(
                "select * from Member where Memberid = " + str(Memberid)
            )
        result = self.cur.fetchall()

        return result

    #本線開始状態への変更
    def atk(self, Memberid, BossNo):
        self.cur.execute(
            "update TotsuStatus set NowTotsu =" + str(BossNo) + " where Memberid =" + str(Memberid)
        )
        self.cur.execute(
            "select * from TotsuStatus"
        )
        SQLControl.TotsuStatus = self.cur.fetchall()

    #指定メンバーの凸状況を取得
    def MemberTotsuStatus(self, Memberid):
        self.cur.execute(
            "select * from TotsuStatus where Memberid = " + str(Memberid)
        )

    #本線終了の宣言
    def end(self, Memberid):
        #状態を本線中(1)から変更する
        self.cur.execute(
            "update TotsuStatus set \
                NowTotsu = 0 \
                where Memberid =" + str(Memberid)
        )
        self.cur.execute(
            "select * from TotsuStatus"
        )
        SQLControl.TotsuStatus = self.cur.fetchall()
    
    #指定メンバーidの凸状況
    def FindTotsuMemberid(self, Memberid):
        self.cur.execute(
            "select * from TotsuStatus where Memberid = " + str(Memberid)
        )
        return self.cur.fetchall()

    #凸数の現象
    def DoneTotsu(self, Memberid):
        self.cur.execute(
            "update TotsuStatus set RemainTotsu = RemainTotsu - 1 \
                where Memberid =" + str(Memberid)
        )
        self.cur.execute(
            "select * from TotsuStatus"
        )
        SQLControl.TotsuStatus = self.cur.fetchall()

    #凸数の修正
    def fix(self, Memberid):
        self.cur.execute(
            "update TotsuStatus set RemainTotsu = RemainTotsu + 1 \
                where Memberid =" + str(Memberid)
        )
        self.cur.execute(
            "select * from TotsuStatus"
        )
        SQLControl.TotsuStatus = self.cur.fetchall()
    
    #予約の登録
    def Reservation(self, Memberid, BossNo, lap, comment):
        self.cur.execute(
            "insert into Reservation(Memberid, ReservationBossNo, lap, ReservationComment) \
                values("+str(Memberid)+","+str(BossNo)+","+str(lap)+",'"+comment+"')"
        )
        self.cur.execute(
            "select * from Reservation where Done = 0"
        )
        SQLControl.ReservationList = self.cur.fetchall()
    
    #指定した予約id&未完了のものを返してくれる
    def FindReservationReservationid(self, Reservationid):
        self.cur.execute(
            "select * from Reservation where Reservationid = " + str(Reservationid) + \
                " and Done = 0"
        )
        return self.cur.fetchall()

    #指定メンバーの予約状況
    def FindReservationMemberid(self, Memberid, BossNo):
        self.cur.execute(
            "select * from Reservation where\
                Memberid = " + str(Memberid) +\
                " and ReservationBossNo =" + str(BossNo) +\
                " and Done = 0"
        )
        return self.cur.fetchall()

    #予約の消費(削除)
    def DoneReservation(self, Reservationid):
        self.cur.execute(
            "update Reservation set Done = 1 where Reservationid =" + str(Reservationid)
        )
        self.cur.execute(
            "select * from Reservation where Done = 0"
        )
        SQLControl.ReservationList = self.cur.fetchall()
    
    #持ち越しの登録
    def AddCarryOver(self, Memberid, BossNo, RemainSecond, party, comment):
        self.cur.execute(
            "insert into CarryOver(Memberid, BossNo, RemainSecond, party, comment) \
                values("+str(Memberid)+","+str(BossNo)+","+str(RemainSecond)+",'"+party+"','"+comment+"')"
        )
        self.cur.execute(
            "select * from CarryOver where Done = 0"
        )
        SQLControl.CarryOver = self.cur.fetchall()
    
    #指定した人の未完了の持越しデータを開始てくれる
    def FindCarryOverMemberid(self, Memberid):
        self.cur.execute(
            "select * from CarryOver where Memberid = " + str(Memberid)\
                + " and Done = 0"
        )
        return self.cur.fetchall()
    
    #指定した持越しidのデータを取得
    def FindCarryOverCoid(self, CarryOverid):
        self.cur.execute(
            "select * from CarryOver where Done = 0 and "\
                + "CarryOverid = " + str(CarryOverid)
        )
        return self.cur.fetchall()

    #持ち越しの完了
    def DoneCarryOver(self, CarryOverid):
        self.cur.execute(
            "update CarryOver set Done = 1 where CarryOverid =" + str(CarryOverid)
        )
        self.cur.execute(
            "select * from CarryOver where Done = 0"
        )
        SQLControl.CarryOver = self.cur.fetchall()
    
    #周回数の変更
    def LapChange(self, lap):
        self.cur.execute(
            "update Laps set lap = " + str(lap) + " where Lapid = 1"
        )
        self.cur.execute(
            "select * from Laps"
        )
        SQLControl.laps = int(self.cur.fetchall()[0][1])
        return SQLControl.laps

    #リセット
    def EndGame(self):
        self.cur.execute(
            "update TotsuStatus set RemainTotsu = 3, NowTotsu = 0"
        )
        self.cur.execute(
            "delete from Reservation"
        )
        self.cur.execute(
            "delete from CarryOver"
        )
        self.__del__()
        self.__init__()

        return

SQLControl().MakeBossHPTable()