import asyncio
import aiohttp
import time
import aircv as ac
import pygame
import sys

# ![](https://s3.bmp.ovh/imgs/2023/01/16/76a5232788c38b1f.gif)

# 异步执行
loop = asyncio.get_event_loop()
# loop.run_until_complete(save_board_segon())


# pg start
"""pg初始化"""
pygame.init()
showw = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Segon-LSPaintboard")
showw.fill((255, 255, 255))
pygame.display.update()

"""文字"""

basicFont = pygame.font.Font("PingFang.ttf", 40)
async def textt1(text):
    pygame.draw.rect(showw, (255, 255, 255), (0, 0, 1000, 70))
    text = basicFont.render(text, 1, (0, 255, 0))
    showw.blit(text, (10, 10))
    pygame.display.update()

async def textt2(text):
    pygame.draw.rect(showw, (255, 255, 255), (0, 700, 1000, 70))
    text = basicFont.render(text, 1, (0, 255, 0))
    showw.blit(text, (10, 710))
    pygame.display.update()

loop.run_until_complete(textt1("正常"))
# pg end


board_url = "https://segonoj.site/paintboard/board"


lastret = ""


async def get_board_segon():
    # if(1):
    try:
        cnt=0
        async with aiohttp.ClientSession() as session:
            async with session.get(board_url) as resp:
                ret = await resp.text()
                if (ret == lastret):
                    return 0
                lastret = ret
                ret = ret.split('\n')
                for y in range(0, 999):
                    for x in range(0, 599):
                        now = ret[y][x*6:x*6+6]
                        if(showw.get_at((y, x))!=(int(now[0:2], 16), int(
                            now[2:4], 16), int(now[4:6], 16))):
                                pygame.draw.rect(showw, (int(now[0:2], 16), int(
                                    now[2:4], 16), int(now[4:6], 16)), (y+70, x, 1, 1))
                        else:
                            cnt+=1
                # image.show()
                textt2(str(cnt/0.2)+"px/s")
                return cnt/0.2
    except Exception as e:
        print("Error at get_board_segon()\n> "+str(e))
        await textt1(str(e))
        return -1


async def save_board_segon():
    try:
        pygame.image.save(showw,'0.png')
    except Exception as e:
        print("Error at save_board_segon()\n> ", str(e))
        await textt1(str(e))





async def matchImg(imgsrc, imgobj, confidencevalue=0.5):  # imgsrc=原始图像，imgobj=待查找的图片
    try:
        await save_board_segon()
        imsrc = ac.imread(imgsrc)
        imobj = ac.imread(imgobj)
        # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}
        match_result = ac.find_all_template(imsrc, imobj, confidencevalue)
        # print(match_result)
        # print(match_result[0]['rectangle'][0])
        for i in range(0, len(match_result)):
            findd = match_result[i]['rectangle']
            for j in range(findd[0][0], findd[2][0]):
                pygame.draw.rect(showw,(255, 0, 0), (j, findd[3][1]+70, 1, 1))
                pygame.draw.rect(showw,(255, 0, 0), (j, findd[0][1]+70, 1, 1))

            for j in range(findd[0][1], findd[3][1]):
                pygame.draw.rect(showw,(255, 0, 0), (findd[0][0], j+70, 1, 1))
                pygame.draw.rect(showw,(255, 0, 0), (findd[2][0], j+70, 1, 1))
    except Exception as e:
        print("Error at matchImg()\n> "+str(e))
        await textt1(str(e))

imagepath = ["1.png"]


async def wmatchImg():
    for imm in imagepath:
        await matchImg("0.png", imm)


# loop.run_until_complete(wmatchImg())

# pg start
while 1:
    loop.run_until_complete(get_board_segon())
    time.sleep(0.2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
# pg end
