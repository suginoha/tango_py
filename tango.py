import pygame
import random

#たんごpy
#構想　pygameを使って表示　

#英語
#知っているか　1 はい　2 いいえ

#日本語
#あっていたか　1 はい　2 いいえ

# 評価 1 1 clear
# 評価 1 2 miss
# 評価 2 - unknown

#結果をlogに残していく


def read_japan():
    ret = []
    with open("./japan.txt") as f:#データ読み込み
        for l in f:
            if len(l) > 0:ret += [i for i in l[:-1].split("、") if i !=""]
    print(len(ret))
    return ret


def read_english():
    ret = []
    with open("./english.txt") as f:#データ読み込み
        for l in f:
            if len(l) > 0:ret += [i for i in l[:-1].split(",") if i !=""]
    print(len(ret))
    return ret


def write(x, y, size, word):
    font = pygame.font.SysFont("notosansmonocjkjp", size) #Ubuntu 18.04の標準日本語フォント
    text = font.render(word, True, (0,0,0))
    screen.blit(text, [x,y])


def next_question():
    global question_no, answer, tango, q_count

    e, j, result = tango[question_no]
    if answer == [1,1]:result += ["clear"]
    elif answer == [1,2]:result += ["miss"]
    else:result += ["unknown"]

    answer = []
    question_no += 1
    if question_no >= q_count:
        return False
    return True


def log_add(text):
    with open("./tango.log", mode='a') as f:
        f.write("\n"+text)


def main():
    global question_no, answer, tango, status

    for j,e in zip(read_japan(), read_english()):
        tango += [(e, j, [])]

    random.shuffle(tango)

    for i in tango:
        print(i)

    next_sw = True

    while next_sw:
        screen.fill((250,250,250))
        write(100, 100, 60, tango[question_no][status])
        if status==0:
            write(100, 300, 30, "1: 知っている   2: 知らない")
        if status==1:
            if answer[0]==1:
                write(100, 300, 30, "1: あっていた   2: いいえ")
            else:
                write(100, 300, 30, "1 or 2: 次へ")
        pygame.display.update()
        pygame.time.wait(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_1, pygame.K_KP1]:
                    answer += [1]
                    status += 1
                    if status == 2:
                        next_sw = next_question()
                        status = 0
                    #print(1)
                if event.key in [pygame.K_2, pygame.K_KP2]:
                    answer += [2]
                    status += 1
                    if status == 2:
                        next_sw = next_question()
                        status = 0
                    #print(2)
    log_add("### result ###")
    for i in range(q_count):
        e, j, a = tango[i]
        log_add(f"{e} {j} {a[0]}")


pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("たんごpy")

status = 0 #0:出題 1:解答
question_no = 0 #現在の問題
answer = []
tango = []
q_count = 20 #一回の出題数

main()
