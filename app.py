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
<title>GULFARA | Premium Gulf Collection</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Montserrat', sans-serif}
.top-announce{background:#7a3e1d;color:#fff;display:flex;height:34px;align-items:center;font-size:12px;letter-spacing:1px;overflow:hidden}
.top-announce div{white-space:nowrap;animation:marq 22s linear infinite}
@keyframes marq{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.header{display:flex;align-items:center;justify-content:space-between;padding:12px 4%;border-bottom:1px solid #eee;position:sticky;top:0;background:white;z-index:99}
.logo{font-weight:700;font-size:26px;letter-spacing:5px;display:flex;align-items:center;gap:10px}
.logo img{height:38px}
.search-box{flex:1;max-width:480px;margin:0 18px;display:flex;border:1px solid #ddd}
.search-box input{flex:1;padding:10px;border:0;outline:none}
.search-box button{background:black;color:white;border:0;padding:0 18px}
.hero{position:relative;height:520px;background:#f2f2f2}
.hero img{width:100%;height:100%;object-fit:cover}
.hero-overlay{position:absolute;left:6%;top:20%;background:rgba(0,0,0,0.85);color:white;padding:30px 34px}
.hero-overlay h1{font-size:52px;line-height:0.9}
.hero-overlay h1 span{color:#ff6a00}
.side-label{position:absolute;left:0;top:0;bottom:0;width:32px;background:#7a3e1d;color:white;writing-mode:vertical-rl;display:flex;align-items:center;justify-content:center;font-size:11px;letter-spacing:2px}
.section{padding:45px 4%}
.sec-title{text-align:center;font-size:22px;font-weight:500;margin-bottom:28px;letter-spacing:1px}
.cat-wrap{display:flex;gap:22px;justify-content:center;flex-wrap:wrap}
.cat{width:110px;text-align:center}
.cat img{width:110px;height:110px;border-radius:50%;object-fit:cover;border:1px solid #eee}
.cat p{font-size:12px;margin-top:8px}
.grid-4{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(min-width:900px){.grid-4{grid-template-columns:repeat(4,1fr)}}
.card{border:1px solid #eee}
.card-img{height:210px;background:#f9f9f9;position:relative;display:flex;align-items:center;justify-content:center}
.card-img img{max-width:90%;max-height:90%}
.badge{position:absolute;top:8px;left:8px;background:#e53935;color:white;font-size:10px;padding:3px 7px}
.card-body{padding:10px}
.card-body h4{font-size:12px;font-weight:400;height:32px;overflow:hidden}
.price{font-weight:700;margin-top:5px}
.price span{font-weight:400;font-size:11px;color:#666}
.wa{position:fixed;bottom:18px;left:18px;background:#25D366;color:white;padding:10px 16px;border-radius:30px;text-decoration:none;z-index:100}
</style>
</head>
<body>

<div class="top-announce"><div> &nbsp; FREE DELIVERY ACROSS GULF • CASH ON DELIVERY • PREMIUM QUALITY • FREE DELIVERY ACROSS GULF • CASH ON DELIVERY • PREMIUM QUALITY • FREE DELIVERY ACROSS GULF • CASH ON DELIVERY • </div></div>

<div class="header">
<div class="logo"><img src="/static/logo1.png" onerror="this.style.display='none'">GULFARA</div>
<div class="search-box"><input placeholder="Search luxury collection..."><button>🔍</button></div>
<div>👤 🛒</div>
</div>

<div class="hero">
<div class="side-label">PREMIUM • LUXURY • GULFARA</div>
<img src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=1400">
<div class="hero-overlay">
<div style="font-size:11px;letter-spacing:3px;margin-bottom:10px">GULFARA COLLECTION</div>
<h1>MEGA SALE<br>DISCOUNT<br><span>50%</span><br>OFF</h1>
<div style="margin-top:12px;font-size:12px;letter-spacing:2px">CASH ON DELIVERY - PREMIUM QUALITY</div>
</div>
</div>

<div class="section">
<div class="sec-title">SHOP BY CATEGORY</div>
<div class="cat-wrap">
<div class="cat"><img src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=200"><p>WATCHES</p></div>
<div class="cat"><img src="https://images.unsplash.com/photo-1541643600914-78b084683601?w=200"><p>PERFUMES</p></div>
<div class="cat"><img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=200"><p>SHOES</p></div>
<div class="cat"><img src="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=200"><p>THOBES</p></div>
<div class="cat"><img src="https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=200"><p>ACCESSORIES</p></div>
<div class="cat"><img src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=200"><p>HOME</p></div>
</div>
</div>

<div class="section" style="background:#fafafa">
<div class="sec-title">HOT SELLING</div>
<div class="grid-4">
<div class="card"><div class="card-img"><span class="badge">-50%</span><img src="https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=300"></div><div class="card-body"><h4>Luxury Leather Watch</h4><div class="price">SAR 199 <span>SAR 399</span></div></div></div>
<div class="card"><div class="card-img"><span class="badge">-50%</span><img src="https://images.unsplash.com/photo-1541643600914-78b084683601?w=300"></div><div class="card-body"><h4>Royal Oud Perfume</h4><div class="price">SAR 149 <span>SAR 299</span></div></div></div>
<div class="card"><div class="card-img"><span class="badge">-50%</span><img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300"></div><div class="card-body"><h4>Premium Sneakers</h4><div class="price">SAR 189 <span>SAR 379</span></div></div></div>
<div class="card"><div class="card-img"><span class="badge">-50%</span><img src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=300"></div><div class="card-body"><h4>Modern Luxury Sofa</h4><div class="price">SAR 1299 <span>SAR 2599</span></div></div></div>
</div>
</div>

<a class="wa" href="#">💬 WhatsApp Order</a>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(TEMPLATE)

with app.app_context(): db.create_all()
if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
