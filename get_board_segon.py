import asyncio
from PIL import Image
import aiohttp
import time
import aircv as ac

# ![](https://s3.bmp.ovh/imgs/2023/01/16/76a5232788c38b1f.gif)

board_url = "https://segonoj.site/paintboard/board"
loop = asyncio.get_event_loop()


async def get_board_segon():
    #if(1):
    try:
        image = Image.new('RGB', (1000, 600), (0, 0, 0))
        async with aiohttp.ClientSession() as session:
            async with session.get(board_url) as resp:
                ret = await resp.text()
                ret = ret.split('\n')
                for y in range(0, 999):
                    for x in range(0, 599):
                        now = ret[y][x*6:x*6+6]
                        image.putpixel((y, x), (int(now[0:2], 16), int(
                            now[2:4], 16), int(now[4:6], 16)))
                image.show()
                return image
    except:
        print("Error at get_board_segon()")
        return None


async def save_board_segon():
    try:
        ret = await get_board_segon()
        ret.save(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) +
                 str(time.time() % 1)[1:]+".png")
        ret.save("0.png")
    except:
        print("Error at save_board_segon()")


#ret = loop.run_until_complete(save_board_segon())


async def matchImg(imgsrc, imgobj, confidencevalue=0.5):  # imgsrc=原始图像，imgobj=待查找的图片
    try:
        image = Image.open('0.png')
        imsrc = ac.imread(imgsrc)
        imobj = ac.imread(imgobj)
        # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}
        match_result = ac.find_all_template(imsrc, imobj, confidencevalue)
        # print(match_result)
        # print(match_result[0]['rectangle'][0])
        for i in range(0, len(match_result)):
            findd = match_result[i]['rectangle']
            for j in range(findd[0][0], findd[2][0]):
                for k in range(findd[0][1], findd[3][1]):
                    image.putpixel((j, findd[0][1]), (255, 0, 0))
                    image.putpixel((j, findd[3][1]), (255, 0, 0))

            for j in range(findd[0][1], findd[3][1]):
                image.putpixel((findd[0][0], j), (255, 0, 0))
                image.putpixel((findd[2][0], j), (255, 0, 0))
        image.show()
        # image.save("2.png")
        image.save("0.png")
        return image
    except:
        print("Error at matchImg())")

imagepath = ["1.png"]


async def wmatchImg():
    for imm in imagepath:
        await matchImg("0.png", imm)


loop.run_until_complete(wmatchImg())