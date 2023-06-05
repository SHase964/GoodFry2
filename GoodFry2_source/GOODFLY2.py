# GOOD FLY 2

import pyxel
import random
import time

DISP_X = 256          # スクリーンの縦の長さ
DISP_Y = 256          # スクリーンの横の長さ
PLAYER_X = 0          # プレイヤーのx座標
PLAYER_Y = 0          # プレイヤーのy座標
PLAYER_SHOT_XY = []   # プレイヤーの弾の座標
PLAYER_SHOT_DISP = [] # プレイヤーの弾を表示させるかどうか
ENEMY_SHOT_XY = []    # 敵の弾の座標
ENEMY_SHOT_XY_LENGTH = [] # 敵の弾の幅
ENEMY_SHOT_FLAG = 0   # 敵の弾のフェードアウト用フラグ
ENEMY_NUMBER = 0      # 敵の数
ENEMY_DEAD_XY_FLAG = [] # 敵が死んだときの座標と爆発の段階
SKILL_UP_ITME_FLAG = 0 # スキルアップアイテムのフラグ





class Player:
    def __init__(self, player_x, player_y, player_speed, shot_speed, shot_rapid_time):
        global PLAYER_SHOT_XY
        global PLAYER_SHOT_DISP
        global ENEMY_SHOT_XY

        # プレイヤーのx幅,y幅,弾のx幅,y幅
        self.player_shot_length = [16, 16, 8, 8]
        # プレイヤーの初期座標
        self.player_x = player_x
        self.player_y = player_y
        # プレイヤーのスピード
        self.player_speed = player_speed
        # 弾の座標
        self.shot_xy = []
        # 弾の速さ
        self.shot_speed = shot_speed
        # 弾の連射速度
        self.shot_rapid_time = shot_rapid_time
        # チャタリング防止用の変数
        self.shot_disp = []
        self.shot_i = self.shot_dispi = -1
        self.shot_flag = 1   
        self.out_shot = []
        # 被弾フラグ
        self.dead_flag = 0
        # 爆発の段階
        self.explosion = 5
        # スキルアップアイテム情報
        self.skill_up_item = []
        self.skill_up_texttime = 40
        

        if self.__class__.__name__ == "Player":
            PLAYER_SHOT_XY = self.shot_xy
            PLAYER_SHOT_DISP = self.shot_disp

    # 更新の関数まとめ
    def update(self):
        self.update_player()
        self.update_shot()
        self.update_shot_receive()

    # プレイヤーの座標の更新
    def update_player(self):
        global PLAYER_X
        global PLAYER_Y
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            self.player_x = max(self.player_x - self.player_speed, 0)

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self.player_x = min(self.player_x + self.player_speed, pyxel.width - self.player_shot_length[0])

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
            self.player_y = max(self.player_y - self.player_speed, 0)

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
            self.player_y = min(self.player_y + self.player_speed, pyxel.height - self.player_shot_length[1])
        PLAYER_X = self.player_x
        PLAYER_Y = self.player_y
    
    # プレイヤーが発した弾の座標の更新
    def update_shot(self):
        if pyxel.btn(pyxel.KEY_E):
            self.shot_flag = 1
            self.shot_xy.append([self.player_x+(self.player_shot_length[0]/2-self.player_shot_length[2]/2),\
                self.player_y-self.player_shot_length[3]+4]) 

            if len(self.shot_disp) >= self.shot_rapid_time and self.shot_i == self.shot_dispi\
                and 1 not in self.shot_disp[(self.shot_rapid_time)*-1: ]:
                self.shot_disp.append(1)
            elif self.shot_i != self.shot_dispi:
                self.shot_disp.append(1)
                self.shot_dispi = -1*self.shot_dispi
            else:
                self.shot_disp.append(0)

        elif not pyxel.btn(pyxel.KEY_E) and self.shot_flag == 1: 
            self.shot_flag = 0
            self.shot_i =-1*self.shot_i

        del_index = 0
        for i in range (len(self.shot_xy)):
            #print(len(self.shot_xy))
            index = i-del_index
            self.shot_xy[index][1] -= self.shot_speed
            if self.shot_xy[index][1] <= -self.player_shot_length[3]:
                self.shot_xy.pop(index)
                self.shot_disp.pop(index)
                del_index+=1

    # 被弾したことを検知する関数(当たり判定)
    def update_shot_receive(self):
        global SKILL_UP_ITME_FLAG
        if len(ENEMY_SHOT_XY)!= 0:
            i = 0
            for ag_x, ag_y in ENEMY_SHOT_XY:
                if self.player_x-ENEMY_SHOT_XY_LENGTH[i][0]+4 <= ag_x <= self.player_x+self.player_shot_length[0]-4\
                and self.player_y-ENEMY_SHOT_XY_LENGTH[i][1]+4 <= ag_y <= self.player_y+self.player_shot_length[1]-4 : 
                        # print("out@@@!") 
                        self.dead_flag = 1
                i+=1
        i = 0
        while i < len(self.skill_up_item):
            if self.player_x-8+4 <= self.skill_up_item[i][0] <= self.player_x+self.player_shot_length[0]-4\
                and self.player_y-8+4 <= self.skill_up_item[i][1] <= self.player_y+self.player_shot_length[1]-4 :
                if self.skill_up_item[i][2] == 1:
                    self.player_speed += 0.4
                if self.skill_up_item[i][2] == 2:
                    self.shot_speed += 0.3
                if self.skill_up_item[i][2] == 3:
                    self.shot_rapid_time -= 2
                SKILL_UP_ITME_FLAG = self.skill_up_item[i][2]
                self.skill_up_item.pop(0)

            i += 1


                    


        
            
class Enemy_1(Player):
    def __init__(self,lenghs, player_x, player_y, player_speed, shot_speed, shot_ins_time, enemy_liner_type):
        super().__init__(player_x, player_y, player_speed, shot_speed, 0)
        self.player_shot_length = lenghs # [敵の縦，敵の横，弾の縦，弾の横]
        self.shot_global = []
        self.shot_flag = 0
        self.shot_ins_time = shot_ins_time
        self.enemy_liner_type = enemy_liner_type
        self.score_plus = 0 # 弾が当たった時，スコア加算されたかのフラグ
        self.pre_shot_time = time.time()
        self.next_shot_sec = random.uniform(self.shot_ins_time, 2.0)


    def update_player(self):
        self.player_y += self.player_speed*0.5 # 敵のｙ方向の速さ

        
    def update_shot(self):
        global ENEMY_SHOT_XY
        global ENEMY_SHOT_XY_LENGTH
        # 弾の生成
        if self.dead_flag != 1:
            if self.pre_shot_time + self.next_shot_sec - time.time() <= 0.1\
                and self.player_y <= DISP_Y-self.player_shot_length[1]:    
                self.shot_xy.append([self.player_x+(self.player_shot_length[0]/2-self.player_shot_length[2]/2),\
                    self.player_y+self.player_shot_length[1]-4])
                ENEMY_SHOT_XY.append(self.shot_xy[-1])
                self.shot_global.append(len(ENEMY_SHOT_XY)-1)
                ENEMY_SHOT_XY_LENGTH.append(self.player_shot_length[2:4])
                # print(ENEMY_SHOT_XY_LENGTH[0][0])
                self.pre_shot_time = time.time()
                self.next_shot_sec = random.uniform(self.shot_ins_time, 2.0) 
    
    # ---敵-弾だけ進む-- # 
    def progress_shot(self):
    
        global ENEMY_SHOT_FLAG
        del_index = 0

        for i in range (len(self.shot_xy)):
            index = i-del_index
            self.shot_xy[index][1] -= self.shot_speed

            ENEMY_SHOT_XY[self.shot_global[index]] = self.shot_xy[index]
            if self.shot_xy[index][1] > DISP_Y and self.shot_global[index] == 0:
                self.shot_xy.pop(0)
                self.shot_global.pop(0)
                ENEMY_SHOT_FLAG+=1
                ENEMY_SHOT_XY.pop(0)
                del_index+=1
                self.shot_global = list(map(lambda x:x-1, self.shot_global))

                

    def update_shot_receive(self):
        global ENEMY_DEAD_XY_FLAG
        if len(PLAYER_SHOT_XY)!= 0:
            i = 0
            while i < len(PLAYER_SHOT_XY):
                if self.player_x-8 <= PLAYER_SHOT_XY[i][0] <= self.player_x+self.player_shot_length[0] \
                and self.player_y +self.player_shot_length[1]-2 >= PLAYER_SHOT_XY[i][1] and self.player_y <= PLAYER_SHOT_XY[i][1]+8\
                and PLAYER_SHOT_DISP[i] == 1 and self.dead_flag != 1: 
                    # print("out!!!!!!!!!") 
                    self.dead_flag = 1
                    if self.enemy_liner_type != 6:
                        ENEMY_DEAD_XY_FLAG.append([self.player_x, self.player_y, 5, 3]) # 爆発の処理
                    else :
                        ENEMY_DEAD_XY_FLAG.append([self.player_x, self.player_y, 6, 3]) # 爆発の処理

                    PLAYER_SHOT_XY.pop(i)   # プレイヤーの弾を削除
                    PLAYER_SHOT_DISP.pop(i) 
                i += 1

class Enemy_2(Enemy_1):
    def update_player(self):
        if self.player_y < PLAYER_Y:    
            if self.player_x < PLAYER_X:
                self.player_x = self.player_x + self.player_speed
            
            if self.player_x > PLAYER_X:
                self.player_x = self.player_x - self.player_speed

            if self.player_x == PLAYER_X:
                pass

        self.player_y += self.player_speed*0.5 # 敵のｙ方向の速さ

class Enemy_3(Enemy_1):
    def __init__(self,lenghs, player_x, player_y, player_speed, shot_speed, shot_ins_time, enemy_liner_type):
        super().__init__(lenghs, player_x, player_y, player_speed, shot_speed, shot_ins_time, enemy_liner_type)
        self.pre_move_time = time.time()
        self.next_move_sec = random.uniform(2.0, 4.0) 
        self.move_lr = random.choice([1, -1])
        self.aim_player_xy = []
    
    def update_player(self):
        if self.pre_move_time + self.next_move_sec - time.time() <= 0:
            self.move_lr *= -1
            self.pre_move_time = time.time()
            self.next_move_sec = random.uniform(2.0, 4.0)  
        if self.player_x <= 0:
            self.move_lr = 1
        if self.player_x + self.player_shot_length[0] >= DISP_X:
            self.move_lr = -1
        

        if self.move_lr == 1:
            self.player_x = self.player_x + self.player_speed
        elif self.move_lr == -1:
            self.player_x = self.player_x - self.player_speed
        
        self.player_y += self.player_speed*0.5 # 敵のｙ方向の速


class Enemy_4(Enemy_3):
    def __init__(self,lenghs, player_x, player_y, player_speed, shot_speed, shot_ins_time, enemy_liner_type):
        super().__init__(lenghs, player_x, player_y, player_speed, shot_speed, shot_ins_time, enemy_liner_type)
        self.player_x_now = []
            
    def update_shot(self):
        global ENEMY_SHOT_XY
        global ENEMY_SHOT_XY_LENGTH
        # 弾の生成
        if self.dead_flag != 1:
            if self.pre_shot_time + self.next_shot_sec - time.time() <= 0.1\
                and self.player_y <= DISP_Y-self.player_shot_length[1]:    
                self.shot_xy.append([self.player_x+(self.player_shot_length[0]/2-self.player_shot_length[2]/2),\
                    self.player_y+self.player_shot_length[1]-4])
                ENEMY_SHOT_XY.append(self.shot_xy[-1])
                self.shot_global.append(len(ENEMY_SHOT_XY)-1)
                ENEMY_SHOT_XY_LENGTH.append(self.player_shot_length[2:4])
                self.pre_shot_time = time.time()
                self.next_shot_sec = random.uniform(self.shot_ins_time, 2.0) 
                self.player_x_now.append(PLAYER_X) 

    # ---敵-弾だけ進む-- # 
    def progress_shot(self):

        global ENEMY_SHOT_FLAG
        del_index = 0

        for i in range (len(self.shot_xy)):
            index = i-del_index
            if self.player_x_now[index]+4 > self.shot_xy[index][0]:
                if self.player_x_now[index]+4 - self.shot_xy[index][0] > abs(self.shot_speed):
                    self.shot_xy[index][0] -= self.shot_speed*0.7
                else :
                    self.shot_xy[index][0] = self.player_x_now[index]+4
            elif self.player_x_now[index]+4 < self.shot_xy[index][0]:
                if  self.shot_xy[index][0] - self.player_x_now[index]+4 > abs(self.shot_speed):
                    self.shot_xy[index][0] += self.shot_speed*0.7
                else :
                    self.shot_xy[index][0] =self.player_x_now+4
            elif self.player_x_now[index]+4 == self.shot_xy[index][0]:
                pass

            self.shot_xy[index][1] -= self.shot_speed
            

            ENEMY_SHOT_XY[self.shot_global[index]] = self.shot_xy[index]
            if self.shot_xy[index][1] > DISP_Y and self.shot_global[index] == 0:
                self.shot_xy.pop(0)
                self.shot_global.pop(0)
                self.player_x_now.pop(0)
                ENEMY_SHOT_FLAG+=1
                ENEMY_SHOT_XY.pop(0)
                del_index+=1
                self.shot_global = list(map(lambda x:x-1, self.shot_global))


    


class App:
    def __init__(self):
        global PLAYER_X
        global PLAYER_Y
        pyxel.init(DISP_X, DISP_Y,scale=3, caption="GOOD FLY 2")
        pyxel.load("my_resource.pyxres")
        
        # ******自由に設定できる******* #
        # 初期位置x, y, 動きの速さ(値が大きいほど早い)，弾の速さ(値が大きいほど早い)，連射速度(値が大きいほど遅い)
        self.player = Player(120, 220, 3, 2, 20)
        self.enemy_ins_time_min = 0.3            # 敵を次に生成する時間の最小値 
        self.enemy_ins_time_max = 2.0            # 敵を次に生成する時間の最大値 
        # 　　******ここまで****** 　　#
        
        self.player_speed = self.player.player_speed
        self.get_score = 0
        self.score_value = [10, 15,20, 25, 30, 25]
        self.shot_type = []
        self.enemy = []
        self.next_enemy_ins = 200
        self.next_skill_up_ins = 150        
        self.pre_time = 0
        self.next_sec = 0
        self.pre_time_cloud = time.time()
        self.next_sec_cloud = random.uniform(1, 3)
        PLAYER_X = self.player.player_x
        PLAYER_Y = self.player.player_y
        self.gamemode = 0
        self.back_ground_mode = 0
        self.cloud = []
        self.star = []
        for i in range(0, 11):
            self.cloud.append([random.randint(-48, DISP_X), random.randint(-48, DISP_Y), random.randint(1, 4)])
        
        star_type = list(range(1, 4))
        w = [0.9, 0.05, 0.05]
        for i in range(0, 20):    
            next_star_type = random.choices(star_type, k = 1, weights=w)
            self.star.append([random.randint(-8, DISP_X), random.randint(-8, DISP_Y), next_star_type[0]])

        pyxel.run(self.draw, self.updata)

    # ---敵のインスタンス--- # 
    def enemy_instance(self):
        global ENEMY_NUMBER
        enemy_type = list(range(1, 7))
        w = [0.15, 0.15, 0.2, 0.2, 0.1, 0.2] # 生成確率
        next_enemy_type = random.choices(enemy_type, k = 1, weights=w)

        # Enemy_n([敵の縦，敵の横，弾の縦，弾の横]，生成場所_x，生成場所_y，進む速さ，弾の速さ，弾の生成時間の下限(sec)，（敵の種類）)
        if next_enemy_type[0] == 1:
            self.enemy.append(Enemy_1([16, 16, 8, 8],random.randint(-8, DISP_X-8), -8, 1, -2, 1, 1) )
            self.shot_type.append(1)
        elif next_enemy_type[0] == 2:
            self.enemy.append(Enemy_2([16, 16, 8, 8],random.randint(-8, DISP_X-8), -8, 1, -2, 1, 2) )
            self.shot_type.append(1)
        elif next_enemy_type[0] == 3:
            self.enemy.append(Enemy_3([16, 16, 8, 8],random.randint(-8, DISP_X-8), -8, 1, -2, 1, 3) )
            self.shot_type.append(1)
        elif next_enemy_type[0] == 4:
            self.enemy.append(Enemy_4([16, 16, 8, 8],random.randint(-8, DISP_X-8), -8, 1, -2, 1, 4) )
            self.shot_type.append(2)
        elif next_enemy_type[0] == 5:
            self.enemy.append(Enemy_1([16, 16, 5, 10],random.randint(-8, DISP_X-8), -8, 5, -6, 0.2, 5) )
            self.shot_type.append(3)
        elif next_enemy_type[0] == 6:
            self.enemy.append(Enemy_1([32,24 , 8, 12],random.randint(-8, DISP_X-8), -8, 0.5, -3, 1, 6) )
            self.shot_type.append(4)

                
        ENEMY_NUMBER += 1

    # ---敵の弾のインデックス更新--- #
    def enemy_shot_index(self, a):
        for i in range(ENEMY_NUMBER):
            if i != a:
                self.enemy[i].shot_global = list(map(lambda x:x-ENEMY_SHOT_FLAG, self.enemy[i].shot_global))

    # ---初期化--- #
    def initiarize(self):
        global PLAYER_SHOT_XY, PLAYER_SHOT_DISP, ENEMY_SHOT_XY, ENEMY_SHOT_FLAG, ENEMY_NUMBER, ENEMY_DEAD_XY_FLAG, PLAYER_X, PLAYER_Y, SKILL_UP_ITME_FLAG
        
        PLAYER_SHOT_XY = []   # プレイヤーの弾の座標
        PLAYER_SHOT_DISP = [] # プレイヤーの弾を表示させるかどうか
        ENEMY_SHOT_XY = []    # 敵の弾の座標
        ENEMY_SHOT_FLAG = 0   # 敵の弾のフェードアウト用フラグ
        ENEMY_NUMBER = 0      # 敵の数
        ENEMY_DEAD_XY_FLAG = [] # 敵が死んだときの座標と爆発の段階
        SKILL_UP_ITME_FLAG = 0

        self.player = Player(120, 220, 3, 2, 20)
        self.enemy = []
        self.shot_type = []
        self.next_enemy_ins = 200
        self.next_skill_up_ins = 150
        self.pre_time = time.time()
        self.next_sec = random.uniform(self.enemy_ins_time_min, self.enemy_ins_time_max) 
        PLAYER_X = self.player.player_x
        PLAYER_Y = self.player.player_y
        self.pre_time_cloud = time.time()
        if self.back_ground_mode == 0 or self.back_ground_mode == 1:
            self.next_sec_cloud = random.uniform(0.2, 2.0) 
        elif self.back_ground_mode == 2 :
            self.next_sec_cloud = random.uniform(0, 0.2) 


        self.get_score = 0


    # ---プレイヤー，敵の更新--- #
    def updata(self):
        global ENEMY_NUMBER
        global ENEMY_SHOT_FLAG
        global ENEMY_SHOT_XY_LENGTH

        
        # ゲーム終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        
        # タイトル画面
        if self.gamemode == 0:
            self.pre_time = time.time()
            self.next_sec = random.uniform(self.enemy_ins_time_min, self.enemy_ins_time_max)  
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.gamemode = 1
            if pyxel.btnp(pyxel.KEY_TAB):
                self.back_ground_mode = (self.back_ground_mode + 1) % 3


        
        # ゲーム中
        elif self.gamemode == 1:
        
            # スペースを押している間はゆっくり動く
            if pyxel.btn(pyxel.KEY_SPACE):
                self.player.player_speed = 1
            else :
                self.player.player_speed = self.player_speed  


            # -敵-生成
            if self.pre_time + self.next_sec - time.time() <= 0:
                self.pre_time = time.time()
                self.next_sec = random.uniform(self.enemy_ins_time_min, self.enemy_ins_time_max)  
                self.enemy_instance()
        
            # -プレイヤー-更新
            self.player.update()
            i = 0
            
            # -敵-被弾してなかったら更新
            while i < ENEMY_NUMBER:
                if self.enemy[i].dead_flag != 1:
                    self.enemy[i].update()
                elif self.enemy[i].score_plus == 0 :
                    type = str(self.enemy[i].__class__.__name__)
                    t = int(type[-1])-1
                    if t == 5:
                        t = self.enemy[i].enemy_liner_type
                    #print(self.get_score[t])
                    self.get_score += self.score_value[t]
                    self.enemy[i].score_plus = 1
                self.enemy[i].progress_shot() # 弾だけ進む
                # -敵-弾がフェードアウトしたらすべての弾のインデックスを更新
                if ENEMY_SHOT_FLAG > 0:
                    self.enemy_shot_index(a = i)
                    ENEMY_SHOT_XY_LENGTH.pop(0)
                    ENEMY_SHOT_FLAG = 0
                i+=1
            
            # 敵が0じゃなかったら
            if len(self.enemy)!=0 :
                # -敵-弾が放たれず，かつフェードアウトしたら，削除（打たれても実態はあり）
                if len(self.enemy[0].shot_global) == 0 and self.enemy[0].player_y > DISP_Y+30:
                    self.enemy.pop(0)
                    self.shot_type.pop(0)
                    ENEMY_NUMBER -= 1

            # スコアによる敵の排出率の増加
            if self.get_score >= self.next_enemy_ins:
                if self.enemy_ins_time_min -0.1 > 0:
                    self.enemy_ins_time_min -= 0.1
                if self.enemy_ins_time_min -0.1 > 1: 
                    self.enemy_ins_time_max -= 0.1
                
                self.next_enemy_ins += 200

            # スキルアップアイテムの生成及び削除
            if self.get_score >= self.next_skill_up_ins:
                r = random.randint(1, 3)
                if r == 1 and self.player.player_speed <= 6 \
                or r == 2 and self.player.shot_speed <= 5 \
                or r == 3 and self.player.shot_rapid_time >= 5:
                    self.player.skill_up_item.append([random.randint(0, DISP_X-8), -8, r])
                self.next_skill_up_ins += 150
            
            i = 0 
            while i < len(self.player.skill_up_item):
                self.player.skill_up_item[i][1] += 2
                if self.player.skill_up_item[i][1] >= DISP_Y+8:
                    self.player.skill_up_item.pop(0)
                    i -= 1
                i += 1

        # 雲の生成
        if self.gamemode == 0 or self.gamemode == 1:
            if self.back_ground_mode == 0 or self.back_ground_mode == 1:
                if self.pre_time_cloud + self.next_sec_cloud - time.time() <= 0:
                    self.pre_time_cloud = time.time()
                    self.next_sec_cloud = random.uniform(0.2, 2)  
                    self.cloud.append([random.randint(-48, DISP_X), -48, random.randint(1, 4)])
                j = 0
                while j < len(self.cloud):
                    if self.cloud[j][1] > DISP_Y+48:
                        self.cloud.pop(j)
                        j -= 1
                    self.cloud[j][1] += 1
                    j += 1
        
        # 星の生成
            if self.back_ground_mode == 2:
                star_type = list(range(1, 4))
                w = [0.9, 0.05, 0.05]
            
                if self.pre_time_cloud + self.next_sec_cloud - time.time() <= 0:
                    self.pre_time_cloud = time.time()
                    self.next_sec_cloud = random.uniform(0, 0.2)     
                    next_star_type = random.choices(star_type, k = 1, weights=w)
                    self.star.append([random.randint(-8, DISP_X), -8, next_star_type[0]])
        
                j = 0
                while j < len(self.star):
                    if self.star[j][1] > DISP_Y+8:
                        self.star.pop(j)
                        j -= 1
                    self.star[j][1] += 5
                    j += 1

        # ゲームオーバー            
        elif self.gamemode == 2:
            self.pre_time = time.time()
            self.next_sec = random.uniform(0.1, 2.0)
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.initiarize()
                self.gamemode = 1
            if pyxel.btnp(pyxel.KEY_ENTER):
                self.initiarize()
                self.gamemode = 0
                
        
        # -プレイヤー-被弾したらゲームオーバー #
        if self.player.dead_flag == 1:
            self.gamemode = 2 
                        
        



    def draw(self):
        if self.back_ground_mode == 0:
            pyxel.cls(6)
        if self.back_ground_mode == 1:
            pyxel.cls(9)
        if self.back_ground_mode == 2:
            pyxel.cls(0)
            
        global ENEMY_DEAD_XY_FLAG
        global SKILL_UP_ITME_FLAG   

        # 雲を描写
        if self.back_ground_mode == 0 or self.back_ground_mode == 1:
            for i in range(len(self.cloud)):
                if self.cloud[i][2] == 1:
                    pyxel.blt(self.cloud[i][0], self.cloud[i][1], 2, 0, 0, 64, 40, 0) 
                if self.cloud[i][2] == 2:
                    pyxel.blt(self.cloud[i][0], self.cloud[i][1], 2, 0, 40, 40, 32, 0) 
                if self.cloud[i][2] == 3:
                    pyxel.blt(self.cloud[i][0], self.cloud[i][1], 2,32, 64, 32, 32, 0) 
                if self.cloud[i][2] == 4:
                    pyxel.blt(self.cloud[i][0], self.cloud[i][1], 2,0, 96, 48, 32, 0) 
        # 星を描写
        elif self.back_ground_mode == 2:
            for i in range(len(self.star)):
                if self.star[i][2] == 1:
                    pyxel.blt(self.star[i][0], self.star[i][1], 2, 0, 72, 8, 8, 0) 
                if self.star[i][2] == 2:
                    pyxel.blt(self.star[i][0], self.star[i][1], 2, 8, 72, 8, 8, 0) 
                if self.star[i][2] == 3:
                    pyxel.blt(self.star[i][0], self.star[i][1], 2, 0, 80, 8, 8, 0) 
    
    

        if self.gamemode == 0:
            pyxel.blt(50, 50, 1, 0, 0, 32, 32, 0)
            pyxel.blt(83, 50, 1, 32, 0, 32, 32, 0)
            pyxel.blt(116, 50, 1, 32, 0, 32, 32, 0)
            pyxel.blt(149, 50, 1, 0, 32, 32, 32, 0)
            pyxel.blt(70, 84, 1, 32, 32, 32, 32, 0)
            pyxel.blt(101, 84, 1, 32, 64, 32, 32, 0)
            pyxel.blt(125, 84, 1, 0, 96, 32, 32, 0)
            pyxel.blt(167, 82, 1, 32, 96, 32, 32, 0)
            color = 0
            if self.back_ground_mode == 2: 
                color = 7
            pyxel.text(100, 200, "Press Space Key", color)

    


        # 弾を描写  
        for i in range(len(self.player.shot_xy)):
            if self.player.shot_disp[i] == 1:
                pyxel.blt(self.player.shot_xy[i][0], self.player.shot_xy[i][1], 0, 16, 0, self.player.player_shot_length[2], self.player.player_shot_length[3], 1)

        # 戦闘機を描写
        pyxel.blt(self.player.player_x, self.player.player_y, 0, 0, 0, self.player.player_shot_length[0], self.player.player_shot_length[1], 1,)
        
        for i in range(len(self.enemy)):
            for j in range(len(self.enemy[i].shot_xy)):
                if self.shot_type[i] == 1:
                    pyxel.blt(self.enemy[i].shot_xy[j][0], self.enemy[i].shot_xy[j][1], 0, 24, 0, self.enemy[i].player_shot_length[2], self.enemy[i].player_shot_length[3], 1)
                if self.shot_type[i] == 2:
                    pyxel.blt(self.enemy[i].shot_xy[j][0], self.enemy[i].shot_xy[j][1], 0, 16, 9, self.enemy[i].player_shot_length[2], self.enemy[i].player_shot_length[3], 1)
                if self.shot_type[i] == 3:
                    pyxel.blt(self.enemy[i].shot_xy[j][0], self.enemy[i].shot_xy[j][1], 0, 23, 13, self.enemy[i].player_shot_length[2], self.enemy[i].player_shot_length[3], 1)
                if self.shot_type[i] == 4:
                    pyxel.blt(self.enemy[i].shot_xy[j][0], self.enemy[i].shot_xy[j][1], 0, 20, 27, self.enemy[i].player_shot_length[2], self.enemy[i].player_shot_length[3], 1)
        

        # 敵を描写
        for i in range(len(self.enemy)):
            if self.enemy[i].dead_flag != 1:
                if  self.enemy[i].enemy_liner_type == 1:
                    pyxel.blt(self.enemy[i].player_x, self.enemy[i].player_y, 0, 0, 32, self.enemy[i].player_shot_length[0], self.enemy[i].player_shot_length[1], 1,)
                elif self.enemy[i].enemy_liner_type == 2:
                    pyxel.blt(self.enemy[i].player_x, self.enemy[i].player_y, 0, 0, 16, self.enemy[i].player_shot_length[0], self.enemy[i].player_shot_length[1], 1,)
                elif self.enemy[i].enemy_liner_type == 3:
                    pyxel.blt(self.enemy[i].player_x, self.enemy[i].player_y, 0, 0, 48, self.enemy[i].player_shot_length[0], self.enemy[i].player_shot_length[1], 1,)
                elif self.enemy[i].enemy_liner_type == 4:
                    pyxel.blt(self.enemy[i].player_x, self.enemy[i].player_y, 0, 0, 64, self.enemy[i].player_shot_length[0], self.enemy[i].player_shot_length[1], 4,)
                elif self.enemy[i].enemy_liner_type == 5:
                    pyxel.blt(self.enemy[i].player_x, self.enemy[i].player_y, 0, 0, 80, self.enemy[i].player_shot_length[0], self.enemy[i].player_shot_length[1], 4,)
                elif self.enemy[i].enemy_liner_type == 6:
                    pyxel.blt(self.enemy[i].player_x, self.enemy[i].player_y, 0, 0, 96, self.enemy[i].player_shot_length[0], self.enemy[i].player_shot_length[1], 4,)
                        
                    
        # 敵の爆破の描写
        i = 0
        while i < len(ENEMY_DEAD_XY_FLAG) :
           
            if ENEMY_DEAD_XY_FLAG[i][2] > 0:
                if ENEMY_DEAD_XY_FLAG[i][2] == 6:    
                    pyxel.blt(ENEMY_DEAD_XY_FLAG[i][0]+4, ENEMY_DEAD_XY_FLAG[i][1]+4, 0, 32, 96, 24, 24, 1) 
                else :
                    pyxel.blt(ENEMY_DEAD_XY_FLAG[i][0]+8, ENEMY_DEAD_XY_FLAG[i][1]+8, 0, 32, (5-ENEMY_DEAD_XY_FLAG[i][2])*16, 16, 16, 1) 
                ENEMY_DEAD_XY_FLAG[i][3] -= 1
                if ENEMY_DEAD_XY_FLAG[i][3] == 0:
                    ENEMY_DEAD_XY_FLAG[i][2] -= 1
                    ENEMY_DEAD_XY_FLAG[i][3] = 3
                
            if ENEMY_DEAD_XY_FLAG[i][2] == 0:
                ENEMY_DEAD_XY_FLAG.pop(0)
                i-=1
            i+=1
        
        # スキルアップアイテムの描写
        for i in range(len(self.player.skill_up_item)):
            if self.player.skill_up_item[i][2] == 1:
                pyxel.blt(self.player.skill_up_item[i][0], self.player.skill_up_item[i][1], 0, 48, 0, 8, 8, )
            if self.player.skill_up_item[i][2] == 2:
                pyxel.blt(self.player.skill_up_item[i][0], self.player.skill_up_item[i][1], 0, 56, 0, 8, 8, )
            if self.player.skill_up_item[i][2] == 3:
                pyxel.blt(self.player.skill_up_item[i][0], self.player.skill_up_item[i][1], 0, 48, 8, 8, 8, )    
        
        # スキルアップアイテムを得た描写
        if SKILL_UP_ITME_FLAG > 0:
            if SKILL_UP_ITME_FLAG == 1:
                pyxel.text(10, 10, "Player Speed UP!!!!", 2)
            if SKILL_UP_ITME_FLAG == 2:
                pyxel.text(10, 10, "Shot Speed UP!!!!", 3)
            if SKILL_UP_ITME_FLAG == 3:
                pyxel.text(10, 10, "Shot Rapid Speed UP!!!!", 1)
            if self.player.skill_up_texttime == 0:
                self.player.skill_up_texttime = 40
                SKILL_UP_ITME_FLAG = 0
            self.player.skill_up_texttime-=1
                
            
        # スコアの描写
        if self.gamemode != 0:
            color = 0
            if self.back_ground_mode == 2: 
                color = 7
            pyxel.text(210, 10, "Score:{}".format(self.get_score), color)

        # プレイヤーの爆破     
        if self.gamemode == 2 :
            pyxel.blt(PLAYER_X, PLAYER_Y, 0, 32, 0, 16, 16, 1) 
            pyxel.blt(63, 50, 1, 96, 0, 32, 32, 0)
            pyxel.blt(96, 50, 1, 64, 32, 32, 32, 0)
            pyxel.blt(129, 50, 1, 96, 32, 32, 32, 0)
            pyxel.blt(161, 50, 1, 64, 64, 32, 32, 0)
            pyxel.blt(63, 84, 1, 64, 0, 32, 32, 0)
            pyxel.blt(96, 84, 1, 96, 64, 32, 32, 0)
            pyxel.blt(129, 84, 1, 64, 64, 32, 32, 0)
            pyxel.blt(161, 84, 1, 0, 64, 32, 32, 0)
            color = 0
            if self.back_ground_mode == 2: 
                color = 7
            pyxel.text(105, 150, "Your Score : ", color)
            pyxel.text(155, 150, str(self.get_score), 8)
            pyxel.text(89, 180, "Home : Press Enter Key", color)
            pyxel.text(85, 190, "Retry : Press Space Key", color)
            pyxel.text(89, 200, "quit : Press \"q\" Key", color)



App()

