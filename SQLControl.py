from os import curdir
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
                name string, discord string,\
                admin integer default 0)"
        )

        #凸数管理テーブル
        self.cur.execute(
            "create table TotsuStatus(\
                Memberid integer,\
                RemainTotsu integer default 3,\
                NowTotsu integer default 0,\
                )"
        )
        #30人分登録
        for i in range(30):
            self.cur.execute(
                "insert into TotsuStatus(Memberid) values("+str(i+1)+")"
            )

        #予約登録テーブル
        self.cur.execute(
            "create table Reservation(\
                Reservationid integer primary key autoincrement,\
                Memberid integer,\
                ReservationBossNo integer,\
                lap integer,\
                ReservationComment string,\
                Done integer default 0,\
                )"
        )

        #持ち越し登録テーブル
        self.cur.execute(
            "create table CarryOver(\
                Memberid integer,\
                BossNo integer,\
                RemainSecond integer,\
                party string,\
                comment string,\
                Done integer default 0,\
            )"
        )
    
    #メンバーの追加
    def AddMember(self, name, discord):
        self.cur.execute(
            "insert into Member(name, discord) values('"+name+"','"+discord+"')"
        )
        #インクリメント値のリセット
        self.cur.execute(
            "delete from sqlite_sequence where name='Member'"
        )
    
    #メンバーに管理者権限を付与
    def UpdateAdmin(self, discord):
        self.cur.execute(
            "update Member set admin = 1 where discord =" + str(discord)
        )
    
    #メンバーの削除
    def DeleteMember(self, discord):
        self.cur.execute(
            "delete from Member where discord =" + str(discord)
        )

    #メンバーリストの取得
    def MemberList(self):
        self.cur.execute(
            "select * form Member"
        )
        return self.cur.fetchall()
    
    #本線開始状態への変更
    def atk(self, Memberid):
        self.cur.execute(
            "update TotsuStatus set NowTotsu = 1 where Memberid =" + str(id)
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
                value("+str(Memberid)+","+str(BossNo)+","+str(lap)+",'"+comment+"')"
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
    
    #未完了持ち越し状況の取得
    def ReservationStatus(self):
        self.cur.execute(
            "select * from CarryOver where Done = 0"
        )
        return self.cur.fetchall()