from os import curdir, set_inheritable
import sqlite3

class SQLControl:
    #コンストラクタ
    def __init__(self):
        self.con = sqlite3.connect('YuniBot.db', isolation_level=None, check_same_thread=False)
        self.cur = self.con.cursor()
    
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
    
    #メンバーの追加
    def AddMember(self, name, discord):
        self.cur.execute(
            "insert into Member(name, discord) values('"+name+"','"+str(discord)+"')"
        )

        self.cur.execute(
            "insert into TotsuStatus(RemainTotsu) values(3)"
        )
    
    #メンバーに管理者権限を付与
    def UpdateAdmin(self, Memberid):
        self.cur.execute(
            "update Member set admin = 1 where Memberid =" + str(Memberid)
        )
    
    #メンバーの削除
    def DeleteMember(self, Memberid):
        self.cur.execute(
            "delete from Member where Memberid =" + str(Memberid)
        )
        self.cur.execute(
            "delete from TotsuStatus where Memberid =" + str(Memberid)
        )
        self.cur.execute

    #メンバーリストの取得
    def MemberList(self):
        self.cur.execute(
            "select * from Member"
        )
        return self.cur.fetchall()
    
    #本線開始状態への変更
    def atk(self, Memberid, BossNo):
        self.cur.execute(
            "update TotsuStatus set NowTotsu =" + str(BossNo) + "where Memberid =" + str(Memberid)
        )
    
    #本線終了の宣言
    def end(self, Memberid):
        #状態を本線中(1)から変更し，残凸数を減らす
        self.cur.execute(
            "update TotsuStatus set \
                NowTotsu = 0 \
                RemainTotsu = RemainTotsu - 1 \
                where Memberid =" + str(Memberid)
        )
    
    #凸数の修正
    def fix(self, Memberid):
        self.cur.execute(
            "update TotsuStatus set RemainTotsu = RemainTotsu + 1 where Memberid =" + str(Memberid)
        )
    
    #凸数，凸状況の取得
    def TotsuStatus(self):
        self.cur.execute(
            "select * from TotsuStatus"
        )
        return self.cur.fetchall()
    
    #予約の登録
    def Reservation(self, Memberid, BossNo, lap, comment):
        self.cur.execute(
            "insert into Reservation(Memberid, ReservationBossNo, lap, ReservationComment) \
                values("+str(Memberid)+","+str(BossNo)+","+str(lap)+",'"+comment+"')"
        )
    
    #予約の消費(削除)
    def DoneReservation(self, Reservationid):
        self.cur.execute(
            "update Reservation set Done = 1 where Reservationid =" + str(Reservationid)
        )
    
    #未完了予約状況の取得
    def ReservationStatus(self):
        self.cur.execute(
            "select * from Reservation where Done = 0"
        )
        return self.cur.fetchall()
    
    #持ち越しの登録
    def CarryOver(self, Memberid, BossNo, RemainSecond, party, comment):
        self.cur.execute(
            "insert into CarryOver(Memberid, BossNo, RemainSecond, party, comment) \
                values("+str(Memberid)+","+str(BossNo)+","+str(RemainSecond)+",'"+party+"','"+comment+"')"
        )
    
    #持ち越しの完了
    def DoneCarryOver(self, CarryOverid):
        self.cur.execute(
            "update CarryOver set Done = 1 where CarryOverid =" + str(CarryOverid)
        )

    #未完了持ち越し状況の取得
    def CarryOverStatus(self):
        self.cur.execute(
            "select * from CarryOver where Done = 0"
        )
        return self.cur.fetchall()
    
    #周回数の変更
    def LapChange(self, lap):
        self.cur.execute(
            "update Laps set lap = " + str(lap) + " where Lapid = 1"
        )
    
    #周回数の取得
    def LapStatus(self):
        self.cur.execute(
            "select * from Laps"
        )
        return int(self.cur.fetchall()[0][1])
