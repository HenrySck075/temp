#objective: create a 30fps original resolution recreation of "Bad Apple" in Minecraft in any way
#execute store result score @p dash run data get entity @e[tag=topleft] Pos
try:
    import math,cv2
    from PIL import Image
    from copy import deepcopy
    from typing import Dict,List
    print("compiling, press ctrl-c to save")
    videoFile='./crop/out00.mp4'
    mcfunctionFile='./datapacks/data/apple/functions/place.mcfunction'
    animFrameDir='./datapacks/data/appleanim/functions/frame{}.mcfunction'
    mcfunctionContent=[
        'scoreboard objectives add frames dummy',#frame counter
        'execute at @e[tag=topleft] align xyz run setblock ~160 ~-2 ~160 repeating_command_block',
        "execute at @e[tag=topleft] align xyz run data modify block ~160 ~-2 ~160 Command set value 'scoreboard players add frame frames 1'",
        'execute at @e[tag=topleft] align xyz run data modify block ~160 ~-2 ~160 auto set value false']

    direcName=['west','north','east','south']
    x,z=160,160
    direction=0#directName
    def fill_scale(array,pos,color):
        "pxArray, pixel pos, color (0,1)"
        maxWidth,maxHeight=len(array),len(array[0])
        maxMatchW=0
        maxMatchH=0
        xoff,yoff=1,0
        skippo=[]
        for h in range(pos[1],maxHeight):
            try:
                if array[pos[0]+1][h]!=color and xoff==1: break
                if array[pos[0]][h]==color:
                    xoff=0
                    maxMatchW=0
                    for w in range(pos[0],maxWidth):
                        if array[w][h]==color:
                            skippo.append((w,h))
                            maxMatchW+=1
                        elif w-1<maxMatchW:
                            maxMatchW=w-1
                        else:
                            break
                        xoff+=1
                    yoff+=1
                else:
                    maxMatchH=yoff
            except IndexError:break
        return maxMatchW,maxMatchH,skippo

    cap = cv2.VideoCapture(videoFile)
    width  = math.floor(cap.get(3))
    height = math.floor(cap.get(4))
    blocks=['white_wool','gray_wool','black_wool']
    last_pxArray=[[0]*90]*120
    repeatedFrames=1
    frames=1
    updatedFrames=1
    while(cap.isOpened()):
        if z<-160:direction=1;z+=1
        if z> 160:direction=3;z-=1
        if x<-160:direction=2;x+=1
        if x> 160:direction=0;x-=1
        ret,cv2_im = cap.read()
        if ret:
            if (frames-1)%2==0:
                converted = cv2.cvtColor(cv2_im,cv2.COLOR_BGR2RGB)
                im = Image.fromarray(converted)
                pxArray:List[List[int]]=[]
                #please help me
                for w in range(im.width):
                    lay=[]
                    for h in range(im.height):
                        c=sum(im.getpixel((w,h)))
                        if c>(60*3) and c<(190*3): color=1#gray
                        elif c<(190*3):color=2#black
                        else:color=0#white
                        lay.append(color)
                    pxArray.append(lay)
                skip=[]
                animFrame=[]
                for w,pw in enumerate(pxArray):
                    for h,ph in enumerate(pw):
                        if (ph != last_pxArray[w][h]) and (w,h) not in skip:
                            repeatedFrames=1
                            d1,d2,skipext=fill_scale(pxArray,(w,h),ph)
                            animFrame.append(f'execute at @e[tag=topleft] align xyz run fill ~-{w} ~2 ~-{h} ~-{d1} ~2 ~-{d2} {blocks[ph]}')
                            skip.extend(skipext)
                if last_pxArray==pxArray:repeatedFrames+=1
                last_pxArray=deepcopy(pxArray)
                if animFrame!=[]:
                    with open(animFrameDir.format(updatedFrames),'w') as w:
                        w.write('\n'.join(animFrame))
                    match direction:
                        case 0: x-=1
                        case 1: z-=1
                        case 2: x+=1
                        case 3: z+=1
                    print(x,z)
                    mcfunctionContent.append("\nexecute at @e[tag=topleft] align xyz run setblock ~{0} ~-2 ~{1} chain_command_block\nexecute at @e[tag=topleft] align xyz run data modify block ~{0} ~-2 ~{1} Command set value 'execute if score frame frames matches {3} run function appleanim:frame{2}'".format(x,z,updatedFrames,frames-repeatedFrames))
                    updatedFrames+=1
            frames+=1
        else:break
    raise KeyboardInterrupt("Program Completed")
except KeyboardInterrupt:
    with open(mcfunctionFile,'w') as w:
        w.write('\n'.join(mcfunctionContent))
