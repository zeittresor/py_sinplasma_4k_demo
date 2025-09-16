import pygame as p,math,colorsys as cs,sys,random as ra,array
p.init();p.mixer.init(44100,-16,2,512)
i=p.display.Info();W,H=i.current_w,i.current_h
s=p.display.set_mode((W,H),p.FULLSCREEN);p.display.set_caption('d')
sn=math.sin;co=math.cos;rr=ra.random;pi=math.pi
C=p.time.Clock();F=60
pL=pR=0;SL=.02;SR=.025;fL=.01;fR=.012;aL=aR=H*.1
mf=.0001;ma=H*.0005;mn=.005;mx=.015;A=H*.05;X=H*.15
S=[(rr()*2-1,rr()*2-1,rr()+.3)for _ in range(80)];sp=.01
Z=[rr()+.3 for _ in range(12)];Hu=[rr() for _ in Z];rp=.008
def cl(h,s,v):r,g,b=cs.hsv_to_rgb(h,s,v);return[int(255*r),int(255*g),int(255*b)]
def iv(c):return(int(.4*(255-c[0])),int(.4*(255-c[1])),int(.4*(255-c[2])))
def mk(fr,d=.8,v=.15):
 sr=44100;n=int(sr*d);b=array.array('h',[0]*(2*n));A=.1;D=.1;S0=.6;R=.2
 AN=int(n*A);DN=int(n*D);SN=int(n*S0);RN=int(n*R)
 if not hasattr(fr,'__iter__'):fr=[fr]
 for f in fr:
  for x in range(n):
   s_=v*32767*sn(2*pi*f*x/sr);l=int(s_*.6);r0=int(s_);b[2*x]+=l;b[2*x+1]+=r0
 for x in range(AN):
  fi=x/AN;b[2*x]=int(b[2*x]*fi);b[2*x+1]=int(b[2*x+1]*fi)
 for x in range(AN,AN+DN):
  xp=(x-AN)/DN;lv=1-(1-.7)*xp;b[2*x]=int(b[2*x]*lv);b[2*x+1]=int(b[2*x+1]*lv)
 for x in range(AN+DN,AN+DN+SN):
  b[2*x]=int(b[2*x]*.7);b[2*x+1]=int(b[2*x+1]*.7)
 for x in range(AN+DN+SN,n):
  xp=(x-(AN+DN+SN))/RN;lv=.7*(1-xp);b[2*x]=int(b[2*x]*lv);b[2*x+1]=int(b[2*x+1]*lv)
 return p.mixer.Sound(buffer=b)
CH=[(261.63,329.63,392),(392,493.88,587.33),(220,261.63,329.63),(349.23,440,523.25)]
CS=[mk(c,.8,.15)for c in CH]
NT=[261.63,293.66,329.63,349.23,392,440,493.88,523.25]
NS=[mk(n,.5,.15)for n in NT]
cF=nF=0
fnt=p.font.Font(None,50)
V=[(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]
E=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
run=1
while run:
 C.tick(F)
 for e in p.event.get():
  if e.type==p.QUIT:run=0
  if e.type==p.KEYDOWN and e.key==p.K_ESCAPE:run=0
 s.fill((0,0,0))
 pL+=SL;pR+=SR
 fL=max(mn,min(mx,fL+mf*sn(pL)*.5));fR=max(mn,min(mx,fR+mf*co(pR)*.5))
 aL=max(A,min(X,aL+ma*co(pL)*.5));aR=max(A,min(X,aR+ma*sn(pR)*.5))
 t=p.time.get_ticks()*1e-3;pv=.3+.7*(sn(t*.2)*.5+.5)
 for y in range(H):
  x1=W*.25+aL*sn(fL*y+pL);x2=W*.75+aR*sn(fR*y+pR)
  if x1>x2:x1,x2=x2,x1
  f=y/H;k=pv+(1-pv)*f*f
  x1=W*.5+(x1-W*.5)*k;x2=W*.5+(x2-W*.5)*k
  d=x2-x1;md=2*(aL+aR)
  hu=((d+md)/(2*md))*360%360
  c0=cl(hu/360,1,1);c1=iv(c0)
  p.draw.line(s,c1,(0,y),(W,y));p.draw.line(s,c0,(int(x1),y),(int(x2),y))
  p.draw.line(s,(0,0,0),(int(x1),y),(int(x1),y),3);p.draw.line(s,(0,0,0),(int(x2),y),(int(x2),y),3)
 cr=co(t*.5);sr=sn(t*.5);p_= .5+.3*sn(t*.3);sx=W*p_;sy=H*p_
 for i in range(len(S)):
  x,y,z=S[i];z-=sp
  if z<=.1:x=rr()*2-1;y=rr()*2-1;z=1
  px=int(W/2+((x*cr-y*sr)/z)*sx);py=int(H/2+((x*sr+y*cr)/z)*sy)
  if 0<=px<W and 0<=py<H:
   s.set_at((px,py),(0,0,0))
  S[i]=(x,y,z)
 for j in range(len(Z)):
  z=Z[j]-rp
  if z<.1:z=1;Hu[j]=rr()
  ox=sn(t*1.3+j)*W*.15*p_;oy=co(t*1.3+j)*H*.15*p_
  rs=(W*(.2+.15*sn(t*.3)))/z
  p.draw.circle(s,cl(Hu[j],1,1),(int(W/2+ox),int(H/2+oy)),int(rs),1)
  Z[j]=z
 ang=t*.5;P=[None]*8
 sx=1+.3*sn(t*.7);sy=1+.3*co(t*.9);sz=1+.3*sn(t*.5)
 for j,v in enumerate(V):
  x,y,z=v;x*=sx;y*=sy;z*=sz
  x1=x*co(ang)-z*sn(ang);z1=x*sn(ang)+z*co(ang)
  y1=y*co(ang)-z1*sn(ang);z2=y*sn(ang)+z1*co(ang)
  k_=200/(z2+3)
  P[j]=(int(W/2+x1*k_),int(H/2+y1*k_))
 for a,b in E:p.draw.line(s,(0,255,255),P[a],P[b],1)
 cF+=1;nF+=1
 if cF>int(F*.8):ra.choice(CS).play();cF=0
 if nF>30 and rr()>.5:ra.choice(NS).play();nF=0
 sz=50+int(10*sn(p.time.get_ticks()*.002))
 txt=fnt.render('github.com/zeittresor',1,(255,255,255))
 txt=p.transform.scale(txt,(txt.get_width()*sz//50,txt.get_height()*sz//50))
 s.blit(txt,(W//2-txt.get_width()//2,H//2-txt.get_height()//2))
 p.display.flip()
p.quit();sys.exit()
