"""Render the Variant speech-bubble sign-off image.
usage: python3 variant_bubble.py "QUOTE TEXT" out.jpg
Base art: base.png (sticker collage, Variant figure, empty bubble)."""
import sys, os
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))
FONT='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
BOX=(1095,135,2098,474)   # usable text area inside the bubble (base is 2416x1216)
def wrap(d,words,f,maxw):
    lines,cur=[], ''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
def render(quote,out,width=1200):
    im=Image.open(os.path.join(HERE,'base.png')).convert('RGBA')
    d=ImageDraw.Draw(im); words=quote.upper().split()
    x0,y0,x1,y1=BOX; bw,bh=x1-x0,y1-y0
    for size in range(120,40,-2):
        f=ImageFont.truetype(FONT,size); lines=wrap(d,words,f,bw)
        lh=int(size*1.12); th=lh*len(lines)
        if th<=bh and all(d.textlength(l,font=f)<=bw for l in lines): break
    y=y0+(bh-th)//2
    for l in lines:
        d.text(((x0+x1)/2,y+lh/2),l,font=f,fill=(17,17,17,255),anchor='mm'); y+=lh
    bg=Image.new('RGB',im.size,(255,255,255)); bg.paste(im,mask=im.split()[3])
    bg=bg.resize((width,round(width*im.height/im.width)),Image.LANCZOS)
    bg.save(out,quality=86,optimize=True,progressive=True)
    print(out,size,'px',len(lines),'lines',os.path.getsize(out)//1024,'KB')
if __name__=='__main__': render(sys.argv[1],sys.argv[2])
