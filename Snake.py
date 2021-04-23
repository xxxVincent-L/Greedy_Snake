# 这是一个pygame的最小开发框架
import pygame
import sys
import random
from pygame.locals import *
import pygame

pygame.init()  # 初试化pygame

white_colour = pygame.Color(255, 255, 255)  # 白色
black_colour = pygame.Color(0, 0, 0)  # 黑色
red_colour = pygame.Color(255, 0, 0)  # 红色
green_colour = pygame.Color(0, 255, 0)  # 绿色
yellow_colour = pygame.Color(150, 160, 0)  # 黄色
blue_colour = pygame.Color(0, 0, 255)  # 蓝色
game_surface = pygame.display.set_mode((600, 400))  # 设置pygame游戏框大小
pygame.display.set_caption("贪吃蛇")  # 设置游戏标题
# 初始化游戏界面内使用的字体
font = pygame.font.SysFont("SIMYOU.TTF", 40)

# 添加背景音乐
file = r'F:/Pycharm/Snakes/bgm.wav'  # 音乐的路径
pygame.mixer.init()  # 初始化
track = pygame.mixer.music.load(file)  # 加载音乐文件
pygame.mixer.music.play()  # 开始播放音乐流


# 给自动运行的蛇改变方向
def head_direction(key, direction):
    if key == 27:
        sys.exit()
    elif key == 119 and direction != "Down":
        direction = "Up"
        return direction
    elif key == 97 and direction != "Right":
        direction = "Left"
        return direction
    elif key == 100 and direction != "Left":
        direction = "Right"
        return direction
    elif key == 115 and direction != "Up":
        direction = "Down"
        return direction


# 控制蛇的行走、实现蛇的自动行走
def new_head_position(head_position, direction):
    if direction == "Up":
        head_position[1] -= 20
    elif direction == "Down":
        head_position[1] += 20
    elif direction == "Left":
        head_position[0] -= 20
    elif direction == "Right":
        head_position[0] += 20
    return head_position


# 得分显示
def drawScore(score):
    # 设置分数的显示颜色
    Surf = font.render('Score:%s' % (score), True, green_colour)
    # 设置分数的位置
    Rect = Surf.get_rect()
    Rect.midtop = (300, 200)
    # 绑定以上设置到句柄
    game_surface.blit(Surf, Rect)


def main():
    head_position = [100, 100]  # 蛇的初始位置
    food_position = [200, 100]  # 食物的位置
    bomb_position = []  # 炸弹的位置
    bad_food_position = []  # 坏食物的位置
    snake_position = [[100, 100]]  # 蛇身的整个位置
    empty_position = []  # 空出的位置
    score = 0  # 分数的初始化
    for i in range(30):
        for j in range(20):
            empty_position.append([i * 20, j * 20])
    if head_position in empty_position:  # 把蛇头的位置从空位中排除
        empty_position.remove(head_position)

    direction = "Right"  # 蛇的初始朝向
    EVENT_TIME = pygame.USEREVENT + 1  # 设置时延
    speed_time = 400
    pygame.time.set_timer(EVENT_TIME, speed_time)
    # 炸弹与坏食物的位置设定
    bomb_position = random.choice(empty_position)
    empty_position.remove(bomb_position)
    bad_food_position = random.choice(empty_position)
    empty_position.remove(bad_food_position)
    while True:

        game_surface.fill(black_colour)  # 背景填充为黑色
        for i in range(len(snake_position)):  # 用循环来画整个蛇
            pygame.draw.rect(game_surface, white_colour,
                             Rect(snake_position[i][0], snake_position[i][1], 20, 20))  # 在[100, 100]处画20*20的矩形
        pygame.draw.rect(game_surface, red_colour,
                         Rect(food_position[0], food_position[1], 20, 20))  # 画出食物的位置
        pygame.draw.rect(game_surface, yellow_colour,
                         Rect(bomb_position[0], bomb_position[1], 20, 20))  # 画出炸弹的位置
        pygame.draw.rect(game_surface, blue_colour,
                         Rect(bad_food_position[0], bad_food_position[1], 20, 20))  # 画出不好的食物的位置
        drawScore(score)  # 画出分数

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 如果是退出键则退出游戏
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == 32:
                    speed_time = (speed_time - 100) % 400
                    pygame.time.set_timer(EVENT_TIME, speed_time)
                else:
                    direction = head_direction(event.key, direction)


            elif event.type == EVENT_TIME:
                head_position = new_head_position(head_position, direction)  # 蛇的位置不断变化
                snake_position.insert(0, [head_position[0], head_position[1]])  # 蛇头永远在列表最开始，蛇尾在列表最尾

                if head_position in empty_position:  # 排除蛇头的位置
                    empty_position.remove(head_position)

                if food_position == head_position:  # 蛇吃到食物，食物用随机数刷新，分数+1
                    food_position = random.choice(empty_position)
                    score += 1
                elif bad_food_position == head_position:  # 蛇迟到坏食物，坏食物用随机数刷新，分数-1
                    bad_food_position = random.choice(empty_position)
                    score -= 1
                elif bomb_position == head_position:  # 蛇碰到炸弹，直接结束
                    sys.exit()

                else:
                    empty_position.append(snake_position.pop())  # 每次移动，去除蛇尾，回归成空位置

            """
            # 添加按键移动功能w,a,s,d移动，坐标原点为左上角
            elif event.type == pygame.KEYDOWN:  # 获取按键的键值
                print("您的按键键值是：", event.key)
            """

            """

            # 增加死亡判断功能
            """
        if head_position[0] < 0 or head_position[0] > 600 \
                or head_position[1] < 0 or head_position[1] > 400:
            sys.exit()

        for i in snake_position[1:]:  # 当蛇头碰到蛇身时，直接退出游戏（利用一个切片
            if head_position[0] == i[0] and \
                    head_position[1] == i[1]:
                sys.exit()

        pygame.display.update()


main()

