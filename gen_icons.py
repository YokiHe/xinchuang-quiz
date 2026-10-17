#!/usr/bin/env python3
# 生成 PWA 图标：蓝色圆角方块 + 白色“信”。输出 icon-512.png / icon-192.png / apple-touch-icon.png
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SIZE = 512
SS = 4  # 超采样抗锯齿
BIG = SIZE * SS

def make(size_output, maskable=False):
    img = Image.new('RGBA', (BIG, BIG), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # 渐变背景条带（上深下浅蓝）
    top, bot = (36, 79, 190), (59, 139, 245)
    for y in range(BIG):
        r = y / BIG
        c = tuple(int(top[i] + (bot[i] - top[i]) * r) for i in range(3)) + (255,)
        d.line([(0, y), (BIG, y)], fill=c)
    # maskable 版本图形内缩（safe zone 80%），普通版本圆角
    if maskable:
        d.rectangle([0, 0, BIG, BIG], fill=None)
        inset = int(BIG * 0.13)
    else:
        inset = 0
        radius = BIG // 5
        d.rounded_rectangle([0, 0, BIG, BIG], radius=radius, fill=(47, 111, 214, 255))
    # 白色“信”
    font = ImageFont.truetype('/System/Library/Fonts/Hiragino Sans GB.ttc', int(BIG * 0.56), index=0)
    t = '信'
    bb = d.textbbox((0, 0), t, font=font)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((BIG - w) / 2 - bb[0], (BIG - h) / 2 - bb[1] - BIG * 0.01), t, font=font, fill=(255, 255, 255, 255))
    img = img.resize((size_output, size_output), Image.LANCZOS)
    if maskable:
        # 透明角裁成圆角（普通尺寸下）
        m = Image.new('L', (size_output, size_output), 0)
        dm = ImageDraw.Draw(m)
        dm.rounded_rectangle([0, 0, size_output, size_output], radius=size_output // 5, fill=255)
        img.putalpha(m)
    return img

make(512).save(os.path.join(HERE, 'icon-512.png'))
make(192).save(os.path.join(HERE, 'icon-192.png'))
make(180).save(os.path.join(HERE, 'apple-touch-icon.png'))
print('icons OK:', os.listdir(HERE))
