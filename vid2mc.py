#objective: create a 60fps original resolution recreation of "Bad Apple" in Minecraft in any way
import math,cv2
from PIL import Image
from copy import deepcopy
from typing import Dict,List
videoFile='./crop/out00.mp4'
mcfunctionFile='./datapacks/data/apple/functions/place.mcfunction'

mcfunctionContent=[
    'execute at @e[tag=topleft] run summon armor_stand ~ ~-6 ~-200 {{Tags:["cb"]}}',
    "execute at @e[tag=cb] run setblock ~ ~-1 ~ barrier replace"
]
cmdPreset:Dict[str,str|List[str]]={
    "cmd":'\n'.join([
        "execute at @e[tag=cb] run setblock ~-{x} ~{y} ~{z} command_block replace",
        "data modify block  ~-{x} ~{y} ~-{z} Command set value 'execute at @e[tag=topleft] run fill ~-{x1} ~2 ~-{z1} ~-{x2} ~2 ~-{z2} {block}'",
        "execute at @e[tag=cb] run setblock ~-{x} ~{y2} ~{z} redstone_wire replace"]),
    "next":'\n'.join([
        "execute at @e[tag=cb] run setblock ~-{x1} ~{y1} ~ repeater[facing={facing}] replace",
        "execute at @e[tag=cb] run setblock ~-{x2} ~{y2} ~ barrier replace",
        "execute @e[tag=cb] run setblock ~-{x2} ~{y1} ~ redstone_wire replace"]),
    #thay x,z mỗi lần dùng
    "moveLayer":[
        "execute at @e[tag=cb] run setblock ~-{x} ~{y} ~-{z} redstone_wire[{we}=up,south=side] replace\nexecute at @e[tag=cb] run setblock ~-{x} ~{y2} ~-{z} barrier replace",
        "execute at @e[tag=cb] run setblock ~-{x} ~{y} ~-{z} redstone_wire[south=up,{we}=side] replace\nexecute at @e[tag=cb] run setblock ~-{x} ~{y2} ~-{z} barrier replace",
        "execute at @e[tag=cb] run setblock ~-{x} ~{y} ~-{z} redstone_wire[{we}=up,south=side] replace\nexecute at @e[tag=cb] run setblock ~-{x} ~{y2} ~-{z} barrier replace",
        "execute at @e[tag=cb] run setblock ~-{x} ~{y} ~-{z} redstone_wire[north=up,{we}=side] replace\nexecute at @e[tag=cb] run setblock ~-{x} ~{y2} ~-{z} barrier replace",
    ]
}
x,y,z=0,0,0
direction=0#right, 1 for left
def fill_scale(array,pos,color):
    "pxArray, pixel pos, color (0,1)"
    maxWidth,maxHeight=len(array),len(array[0])
    maxMatchW=0
    maxMatchH=0
    xoff,yoff=1,0
    skippo=[]
    for h in range(pos[1],maxHeight):
        if array[pos[0]][h+yoff]==color:
            xoff=0
            for w in range(pos[0],maxWidth):
                if array[w+xoff][h+yoff]==color:
                    skippo.append((w+xoff,h+yoff))
                    maxMatchW+=1
                elif xoff-1<maxMatchW:
                    maxMatchW=xoff-1
                else:
                    break
                xoff+=1
            yoff+=1
        else:
            maxMatchH=yoff
    return (pos[0],maxMatchW),(pos[1],maxMatchH),skippo


print('Read file: {}'.format(videoFile))
cap = cv2.VideoCapture(videoFile) # says we capture an image from a webcam
width  = math.floor(cap.get(3))
height = math.floor(cap.get(4))
blocks=['white_wool,black_wool']
last_pxArray=[]
while(cap.isOpened()):
    ret,cv2_im = cap.read()
    if ret :
        converted = cv2.cvtColor(cv2_im,cv2.COLOR_BGR2RGB)

        im = Image.fromarray(converted)
        pxArray=[]
        #please help me
        for w in range(im.width):
            lay=[]
            for h in range(im.height):
                color=0#white
                if im.getpixel((w,h)) > 128*3: color=1#black
                lay.append(color)
            pxArray.append(lay)
        skip=[]
        x+=1
        mcfunctionContent.append(cmdPreset["next"].format(x1=x,x2=x+1,y1=y,y2=y+1,facing='east' if direction==0 else 'west'))
        for w,pw in enumerate(pxArray):
            for h,ph in enumerate(pw):
                if ph != last_pxArray[w][h] and (w,h) not in skip:
                    d1,d2,skipext=fill_scale(pxArray,(w,h),ph)
                    mcfunctionContent.append(cmdPreset["cmd"].format(x=x,y=y,y2=y+1,z=z+2,x1=d1[0],z1=d1[0],x2=d2[0],z2=d2[0]),block=blocks[color])
                    skip.extend(skipext)
