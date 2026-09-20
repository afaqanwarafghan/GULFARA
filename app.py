from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gulfara.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>GULFARA</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Montserrat', sans-serif}
.top-bar{background:#7a3e1d;color:white;display:flex;height:32px;align-items:center;overflow:hidden;font-size:12px}
.top-bar div{white-space:nowrap;animation:marq 20s linear infinite}
@keyframes marq{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.header{display:flex;justify-content:space-between;align-items:center;padding:12px 4%;border-bottom:1px solid #eee;position:sticky;top:0;background:white;z-index:99}
.logo{font-weight:700;font-size:26px;letter-spacing:5px;display:flex;gap:8px;align-items:center}
.logo img{height:35px}
.search{flex:1;max-width:450px;margin:0 15px;display:flex;border:1px solid #ddd}
.search input{flex:1;padding:9px;border:0;outline:none}
.search button{background:black;color:white;border:0;padding:0 15px}

/* SLIDER */
.hero{position:relative;height:520px;overflow:hidden;background:#000}
.slide{position:absolute;top:0;left:0;width:100%;height:100%;opacity:0;transition:opacity 1s ease;display:flex;align-items:center}
.slide.active{opacity:1}
.slide img.bg{position:absolute;width:100%;height:100%;object-fit:cover;opacity:0.85}
.slide-content{position:relative;z-index:2;background:rgba(0,0,0,0.85);color:white;padding:30px 35px;margin-left:6%;min-width:300px}
.slide-content h1{font-size:50px;line-height:0.9}
.slide-content h1 span{color:#ff6a00}
.side-label{position:absolute;left:0;top:0;bottom:0;width:32px;background:#7a3e1d;color:white;writing-mode:vertical-rl;display:flex;align-items:center;justify-content:center;font-size:11px;letter-spacing:2px;z-index:3}

.dots{position:absolute;bottom:15px;left:50%;transform:translateX(-50%);display:flex;gap:8px;z-index:5}
.dot{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,0.5);cursor:pointer}
.dot.active{background:white}

.section{padding:40px 4%}
.sec-title{text-align:center;font-size:22px;margin-bottom:25px}
.cat-wrap{display:flex;gap:20px;justify-content:center;flex-wrap:wrap}
.cat{width:110px;text-align:center}
.cat img{width:110px;height:110px;border-radius:50%;object-fit:cover}
.wa{position:fixed;bottom:18px;left:18px;background:#25D366;color:white;padding:10px 16px;border-radius:30px;text-decoration:none;z-index:100}
</style>
</head>
<body>

<div class="top-bar"><div> &nbsp; FREE DELIVERY ACROSS GULF • CASH ON DELIVERY • PREMIUM QUALITY • FREE DELIVERY ACROSS GULF • CASH ON DELIVERY • </div></div>

<div class="header">
<div class="logo"><img src="/static/logo1.png" onerror="this.style.display='none'">GULFARA</div>
<div class="search"><input placeholder="Search..."><button>🔍</button></div>
<div>👤 🛒</div>
</div>

<div class="hero" id="hero">
<div class="side-label">PREMIUM • LUXURY • GULFARA</div>

<div class="slide active">
<img class="bg" src="https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1400">
<div class="slide-content">
<div style="font-size:11px;letter-spacing:3px">GULFARA COLLECTION</div>
<h1>ALL IN ONE<br>COLLECTION<br><span>50%</span><br>OFF</h1>
<div style="margin-top:10px;font-size:12px">WATCHES • PERFUMES • SHOES • CLOTHES</div>
</div>
</div>

<div class="slide">
<img class="bg" src="https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=1400">
<div class="slide-content">
<div style="font-size:11px;letter-spacing:3px">LUXURY WATCHES</div>
<h1>PREMIUM<br>WATCHES<br><span>50%</span><br>OFF</h1>
<div style="margin-top:10px;font-size:12px">CASH ON DELIVERY</div>
</div>
</div>

<div class="slide">
<img class="bg" src="https://images.unsplash.com/photo-1541643600914-78b084683601?w=1400">
<div class="slide-content">
<div style="font-size:11px;letter-spacing:3px">ROYAL PERFUMES</div>
<h1>LUXURY<br>PERFUMES<br><span>50%</span><br>OFF</h1>
<div style="margin-top:10px;font-size:12px">PREMIUM QUALITY</div>
</div>
</div>

<div class="slide">
<img class="bg" src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=1400">
<div class="slide-content">
<div style="font-size:11px;letter-spacing:3px">TRENDING SHOES</div>
<h1>STYLISH<br>SHOES<br><span>50%</span><br>OFF</h1>
<div style="margin-top:10px;font-size:12px">FREE DELIVERY ACROSS GULF</div>
</div>
</div>

<div class="slide">
<img class="bg" src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=1400">
<div class="slide-content">
<div style="font-size:11px;letter-spacing:3px">LUXURY HOME</div>
<h1>MODERN<br>FURNITURE<br><span>50%</span><br>OFF</h1>
<div style="margin-top:10px;font-size:12px">CASH ON DELIVERY</div>
</div>
</div>

<div class="dots" id="dots"></div>
</div>

<div class="section">
<div class="sec-title">SHOP BY CATEGORY</div>
<div class="cat-wrap">
<div class="cat"><img src="https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=200"><p>WATCHES</p></div>
<div class="cat"><img src="https://images.unsplash.com/photo-1541643600914-78b084683601?w=200"><p>PERFUME</p></div>
<div class="cat"><img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=200"><p>SHOES</p></div>
<div class="cat"><img src="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=200"><p>CLOTHES</p></div>
<div class="cat"><img src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=200"><p>HOME</p></div>
</div>
</div>

<a class="wa" href="#">💬 WhatsApp Order</a>

<script>
let slides = document.querySelectorAll('.slide');
let dotsContainer = document.getElementById('dots');
let current = 0;

// create dots
slides.forEach((_,i)=>{
  let d=document.createElement('div');
  d.className='dot'+(i==0?' active':'');
  d.onclick=()=>show(i);
  dotsContainer.appendChild(d);
});
let dots = document.querySelectorAll('.dot');

function show(n){
  slides[current].classList.remove('active');
  dots[current].classList.remove('active');
  current = n;
  if(current>=slides.length) current=0;
  if(current<0) current=slides.length-1;
  slides[current].classList.add('active');
  dots[current].classList.add('active');
}

setInterval(()=>{show(current+1)},3000); // 3 second bad badlega
</script>

</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(TEMPLATE)

with app.app_context(): db.create_all()
if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
