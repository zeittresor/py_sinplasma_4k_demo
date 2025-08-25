import pygame,math,colorsys,sys,random,array
pygame.init();pygame.mixer.init(44100,-16,2,512)
i=pygame.display.Info();w,h=i.current_w,i.current_h
sn=math.sin;co=math.cos;rr=random.random;pi=math.pi
sc=pygame.display.set_mode((w,h),pygame.FULLSCREEN)
pygame.display.set_caption("demo")
C=pygame.time.Clock();F=60
pL=pR=0;sL=.02;sR=.025;fL=.01;fR=.012;aL=aR=h*.1
mf=.0001;ma=h*.0005;mn=.005;mx=.015;A=h*.05;X=h*.15
st=[(rr()*2-1,rr()*2-1,rr()+.3)for _ in range(80)];sp=.01
rz=[rr()+.3 for _ in range(12)];hr=[rr() for _ in rz];rp=.008
def c_(H,S,V):r=colorsys.hsv_to_rgb(H,S,V);return[int(255*x)for x in r]
def inv(c):return tuple(int(.4*(255-x))for x in c)
def m(fr,d=.8,v=.15):
 sr=44100;n=int(sr*d);b=array.array("h",[0]*(2*n));A_=.1;D=.1;S=.6;R=.2
 AN=int(n*A_);DN=int(n*D);SN=int(n*S);RN=int(n*R)
 if not hasattr(fr,'__iter__'):fr=[fr]
 for f_ in fr:
  for x in range(n):
   s=v*32767*sn(2*pi*f_*x/sr);l=int(s*.6);r=int(s)
   b[2*x]+=l;b[2*x+1]+=r
 for x in range(AN):
  fI=x/AN;b[2*x]=int(b[2*x]*fI);b[2*x+1]=int(b[2*x+1]*fI)
 for x in range(AN,AN+DN):
  xp=(x-AN)/DN;lv=1-(1-.7)*xp
  b[2*x]=int(b[2*x]*lv);b[2*x+1]=int(b[2*x+1]*lv)
 for x in range(AN+DN,AN+DN+SN):
  b[2*x]=int(b[2*x]*.7);b[2*x+1]=int(b[2*x+1]*.7)
 for x in range(AN+DN+SN,n):
  xp=(x-(AN+DN+SN))/RN;lv=.7*(1-xp)
  b[2*x]=int(b[2*x]*lv);b[2*x+1]=int(b[2*x+1]*lv)
 return pygame.mixer.Sound(buffer=b)
ch=[(261.63,329.63,392),(392,493.88,587.33),(220,261.63,329.63),(349.23,440,523.25)]
cs=[m(x,.8,.15)for x in ch]
nt=[261.63,293.66,329.63,349.23,392,440,493.88,523.25]
ns=[m(x,.5,.15)for x in nt]
ci=cf=nf=0
fnt=pygame.font.Font(None,50)
r=1
while r:
 C.tick(F)
 for e in pygame.event.get():
  if e.type==pygame.QUIT:r=0
  if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE:r=0
 sc.fill((0,0,0))
 pL+=sL;pR+=sR
 fL+=mf*sn(pL)*.5;fL=max(mn,min(fL,mx))
 fR+=mf*co(pR)*.5;fR=max(mn,min(fR,mx))
 aL+=ma*co(pL)*.5;aL=max(A,min(aL,X))
 aR+=ma*sn(pR)*.5;aR=max(A,min(aR,X))
 t=pygame.time.get_ticks()*1e-3;pv=.3+.7*(sn(t*.2)*.5+.5)
 for y in range(h):
  x1=w*.25+aL*sn(fL*y+pL)
  x2=w*.75+aR*sn(fR*y+pR)
  if x1>x2:x1,x2=x2,x1
  f=y/h;k=pv+(1-pv)*f*f
  x1=w*.5+(x1-w*.5)*k;x2=w*.5+(x2-w*.5)*k
  d=x2-x1;md=2*(aL+aR)
  hu=(d+md)/(2*md)*360%360
  c0=c_(hu/360,1,1);c1=inv(c0)
  pygame.draw.line(sc,c1,(0,y),(w,y))
  pygame.draw.line(sc,c0,(int(x1),y),(int(x2),y))
  pygame.draw.line(sc,(0,0,0),(int(x1),y),(int(x1),y),3)
  pygame.draw.line(sc,(0,0,0),(int(x2),y),(int(x2),y),3)
 cr=co(t*.5);sr=sn(t*.5);p=.5+.3*sn(t*.3);sx=w*p;sy=h*p
 for i in range(len(st)):
  x,y,z=st[i];z-=sp
  if z<=.1:x=rr()*2-1;y=rr()*2-1;z=1
  px=int(w/2+((x*cr-y*sr)/z)*sx);py=int(h/2+((x*sr+y*cr)/z)*sy)
  if 0<=px<w and 0<=py<h:
   br=int(max(0,1-z)*255);sc.set_at((px,py),(br,br,br))
  st[i]=(x,y,z)
 for j in range(len(rz)):
  z=rz[j]-rp
  if z<.1:z=1;hr[j]=rr()
  ox=sn(t*1.3+j)*w*.15*p;oy=co(t*1.3+j)*h*.15*p
  rs=(w*(.2+.15*sn(t*.3)))/z
  pygame.draw.circle(sc,c_(hr[j],1,1),(int(w/2+ox),int(h/2+oy)),int(rs),1)
  rz[j]=z
 cf+=1
 if cf>int(F*.8):
  random.choice(cs).play();cf=0
 nf+=1
 if nf>30 and rr()>.5:
  random.choice(ns).play();nf=0
 sz=50+int(10*sn(pygame.time.get_ticks()*.002))
 t=fnt.render("github.com/zeittresor",1,(255,255,255))
 t=pygame.transform.scale(t,(t.get_width()*sz//50,t.get_height()*sz//50))
 sc.blit(t,(w//2-t.get_width()//2,h//2-t.get_height()//2))
 pygame.display.flip()
pygame.quit();sys.exit()
