import tkinter
import tkinter.font
import random
import time
import winsound

import LJH
import SYC
import SYH

from Scene import *

WIDTH = 1280
HEIGHT = 720

GAMES = [LJH.FlappyBird, LJH.Shooting, LJH.Maze, LJH.Rhythm, SYC.Jump, SYC.AirHockey, SYC.Moskito, SYH.Classification, SYH.Race, SYH.AvoidDDong]

# 게임 중 타이머 업데이트, 게임오버 확인 후 처리를 한다
def process_game():
    global score, life, switch_time

    update_timer_bar()

    if game.is_gameover:
        switch_time = time.time()

        if game.is_clear:
            score += 1
            print("success", score, life)
        else:
            life -= 1
            print("fail", score, life)

        if life >= 0:
            blind.update_info(game, life, score)
            root.after(1, process_switching, set_random_game)
        else:
            blind.update_info(None)
            root.after(1, process_switching, set_result_screen)

    else:
        root.after(1, process_game)

# 화면 전환 중 실행되며 가림막이 움직이는 것을 처리한다
def process_switching(set_func):
    global pre_time

    dt = time.time() - switch_time

    if dt >= SWITCH_TIME / 2 and pre_time < SWITCH_TIME / 2:
        set_func()

    blind.update(dt)
    
    pre_time = dt

    if dt >= SWITCH_TIME:
        if life >= 0:
            root.after(1, process_game)
        game.start()
    else:
        root.after(1, process_switching, set_func)

# 타이머를 업데이트한다
def update_timer_bar():
    global timer_bar_front

    tm = 0

    if game.is_countdown:
        tm = max(game.max_time - game.play_time, 0)
    else:
        tm = min(game.play_time, game.max_time)

    screen.itemconfig(timer_text, text=f"{int(tm)}s")
    
    screen.delete(timer_bar_front)
    timer_bar_front = screen.create_rectangle(0, 0, WIDTH * tm / game.max_time, 30, fill="green2")

    screen.tag_raise(timer_bar_back)
    screen.tag_raise(timer_bar_front)
    screen.tag_raise(timer_text)

# 스크린을 초기화한다
def reset_screen():
    global screen, blind, timer_bar_back, timer_bar_front, timer_text

    screen.pack_forget()
    screen = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
    screen.focus_set()
    screen.pack()

    blind = Blind(screen, game, life, score)

# 게임 플레이용으로 스크린을 초기화한다
def reset_game_screen():
    global screen, timer_bar_back, timer_bar_front, timer_text

    reset_screen()

    timer_bar_back = screen.create_rectangle(0, 0, WIDTH, 30, fill="light gray")
    timer_bar_front = screen.create_rectangle(0, 0, WIDTH, 30, fill="green")
    timer_text = screen.create_text(0, 0, text="0", font=timer_font)
    screen.moveto(timer_text, WIDTH / 2 - 10, -4)

# 시작화면을 준비한다
def set_start_screen():
    global game

    reset_screen()

    game = Start(screen, start, root.destroy, switch_bgm, is_playing_bgm)

    blind.update_info(None)

# 결과화면을 준비한다
def set_result_screen():
    global game

    reset_screen()

    game = Result(screen, back, score, time.time() - start_time)

    blind.update_info(None)

# 게임을 랜덤으로 골라 게임화면을 준비한다
def set_random_game():
    global game

    reset_game_screen()

    Game = random.choice(GAMES)

    game = Game(screen)

    update_timer_bar()

# 게임을 시작한다
def start():
    global game, score, life, start_time, switch_time, pre_time

    score = 0
    life = 3
    start_time = time.time()
    switch_time = time.time()
    pre_time = 0

    game = None

    blind.update_info(game)

    process_switching(set_random_game)

# 시작화면으로 돌아간다
def back():
    global switch_time

    switch_time = time.time()
    process_switching(set_start_screen)

# 배경음악을 온오프한다
def switch_bgm():
    global is_playing_bgm
    if is_playing_bgm:
        is_playing_bgm = False
        winsound.PlaySound(None, winsound.SND_FILENAME)
    else:
        is_playing_bgm = True
        winsound.PlaySound("resource/bgm.wav", winsound.SND_ASYNC | winsound.SND_LOOP | winsound.SND_FILENAME)

root = tkinter.Tk()

root.title("Relay Minigame")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

# 프로그램 아이콘 설정
root.iconbitmap("resource/aing.ico")

# 타이머에서 사용할 폰트
timer_font = tkinter.font.Font(family="Consolas", size=25, weight="bold")

# 시작화면, 게임화면, 결과화면이 그려질 캔버스
screen = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)

# 게임 플레이 정보가 저장될 변수
game = None

# 점수와 목숨
score : int = 0
life : int = -1

# 시간 계산용 변수들
start_time = 0
switch_time = 0
pre_time = 0

# 가림막
blind = None

# 배경음악 재생 정보
is_playing_bgm = False
switch_bgm()

# 시작화면 준비 후 시작
set_start_screen()
game.start()

root.mainloop()