from flask import Flask, render_template_string, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gulfara.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    price = db.Column(db.Integer)
    image = db.Column(db.String(300))

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>GULFARA</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Montserrat', sans-serif}
.top-bar{background:#7a3e1d;color:white;height:32px;display:flex;align-items:center;overflow:hidden;font-size:12px}
.top-bar div{white-space:nowrap;animation:marq 20s linear infinite}
@keyframes marq{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.header{display:flex;justify-content:space-between;align-items:center;padding:12px 4%;border-bottom:1px solid #eee;position:sticky;top:0;background:white;z-index:99}
.logo{font-weight:700;font-size:26px;letter-spacing:5px}
.logo img{height:35px}
.search{flex:1;max-width:450px;margin:0 15px;display:flex;border:1px solid #ddd}
.search input{flex:1;padding:9px;border:0;outline:none}
.search button{background:black;color:white;border:0;padding:0 15px}

/* SLIDER */
.hero{position:relative;height:500px;overflow:hidden;background:#000}
.slide{position:absolute;top:0;left:0;width:100%;height:100%;opacity:0;transition:opacity 1s ease}
.slide.active{opacity:1}
.slide img.bg{width:100%;height:100%;object-fit:cover;opacity:0.85}
.slide-content{position:absolute;left:6%;top:20%;background:rgba(0,0,0,0.85);color:white;padding:28px 34px}
.slide-content h1{font-size:48px;line-height:0.9}
.slide-content h1 span{color:#ff6a00}
.side-label{position:absolute;left:0;top:0;bottom:0;width:32px;background:#7a3e1d;color:white;writing-mode:vertical-rl;display:flex;align-items:center;justify-content:center;font-size:11px;z-index:3}

.section{padding:40px 4%}
.sec-title{text-align:center;font-size:22px;margin-bottom:25px}
.cat-wrap{display:flex;gap:20px;justify-content:center;flex-wrap:wrap}
.cat{width:110px;text-align:center;cursor:pointer;text-decoration:none;color:black}
.cat img{width:110px;height:110px;border-radius:50%;object-fit:cover;border:2px solid #eee;transition:0.3s}
.cat:hover img{transform:scale(1.08);border-color:black}
.grid-4{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(min-width:900px){.grid-4{grid-template-columns:repeat(4,1fr)}}
.card{border:1px solid #eee;background:white}
.card-img{height:210px;background:#f9f9f9;display:flex;align-items:center;justify-content:center}
.card-img img{max-width:90%;max-height:90%}
.card-body{padding:10px}
.price{font-weight:700}

/* WHATSAPP RIGHT SIDE */
.wa-btn{position:fixed;right:18px;bottom:90px;background:#25D366;color:white;padding:12px 18px;border-radius:30px;text-decoration:none;z-index:100;box-shadow:0 4px 10px rgba(0,0,0,0.2);font-weight:600}

/* WELCOME ROBOT */
.robot{position:fixed;right:20px;bottom:20px;width:300px;background:white;border:1px solid #ddd;border-radius:15px;box-shadow:0 5px 25px rgba(0,0,0,0.2);z-index:200;padding:15px;display:none}
.robot-head{display:flex;align-items:center;gap:10px;font-weight:700}
.robot-head span{font-size:28px}
.robot p{font-size:13px;margin:10px 0;line-height:1.4}
.robot button{background:black;color:white;border:0;padding:8px 14px;border-radius:20px;font-size:12px;cursor:pointer}

/* STARS FEEDBACK */
.reviews{background:#fafafa}
.review-card{background:white;border:1px solid #eee;padding:15px;text-align:center}
.stars{color:#FFB800}
</style>
</head>
<body>

<div class="top-bar"><div> &nbsp; FREE DELIVERY ACROSS GULF • CASH ON DELIVERY • PREMIUM QUALITY • FREE DELIVERY ACROSS GULF • </div></div>

<div class="header">
<div class="logo"><img src="/static/logo1.png" onerror="this.style.display='none'">GULFARA</div>
<div class="search"><input placeholder="Search..."><button>🔍</button></div>
<div>👤 🛒</div>
</div>

<div class="hero" id="hero">
<div class="side-label">PREMIUM • LUXURY • GULFARA</div>

<div class="slide active">
<img class="bg" src="https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1400">
<div class="slide-content"><h1>ALL IN ONE<br>COLLECTION<br><span>50%</span> OFF</h1></div>
</div>
<div class="slide"><img class="bg" src="https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=1400"><div class="slide-content"><h1>PREMIUM<br>WATCHES<br><span>50%</span> OFF</h1></div></div>
<div class="slide"><img class="bg" src="https://images.unsplash.com/photo-1541643600914-78b084683601?w=1400"><div class="slide-content"><h1>LUXURY<br>PERFUMES<br><span>50%</span> OFF</h1></div></div>
<div class="slide"><img class="bg" src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=1400"><div class="slide-content"><h1>STYLISH<br>SHOES<br><span>50%</span> OFF</h1></div></div>
<div class="slide"><img class="bg" src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=1400"><div class="slide-content"><h1>MODERN<br>FURNITURE<br><span>50%</span> OFF</h1></div></div>
</div>

<div class="section">
<div class="sec-title">SHOP BY CATEGORY</div>
<div class="cat-wrap">
<a class="cat" href="/category/Watches"><img src="https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=200"><p>WATCHES</p></a>
<a class="cat" href="/category/Perfume"><img src="https://images.unsplash.com/photo-1541643600914-78b084683601?w=200"><p>PERFUME</p></a>
<a class="cat" href="/category/Shoes"><img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=200"><p>SHOES</p></a>
<a class="cat" href="/category/Clothes"><img src="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=200"><p>CLOTHES</p></a>
<a class="cat" href="/category/Home"><img src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=200"><p>HOME</p></a>
</div>
</div>

<div class="section">
<div class="sec-title">{{ cat_name if cat_name else 'HOT SELLING' }}</div>
<div class="grid-4">
{% for p in products %}
<div class="card"><div class="card-img"><img src="{{p.image}}"></div><div class="card-body"><h4 style="font-size:12px;font-weight:400">{{p.name}}</h4><div class="price">SAR {{p.price}}</div></div></div>
{% endfor %}
</div>
</div>

<div class="section reviews">
<div class="sec-title">CUSTOMER REVIEWS ⭐⭐⭐⭐⭐</div>
<div class="grid-4">
<div class="review-card"><div class="stars">★★★★★</div><p style="font-size:12px;margin:8px 0">"Best quality! Fast delivery across Gulf"</p><b style="font-size:11px">- Ahmed S.</b></div>
<div class="review-card"><div class="stars">★★★★★</div><p style="font-size:12px;margin:8px 0">"GULFARA watches are premium, love it!"</p><b style="font-size:11px">- Fatima K.</b></div>
<div class="review-card"><div class="stars">★★★★★</div><p style="font-size:12px;margin:8px 0">"Cash on delivery, very trusted store"</p><b style="font-size:11px">- Omar M.</b></div>
<div class="review-card"><div class="stars">★★★★★</div><p style="font-size:12px;margin:8px 0">"Perfume fragrance is amazing ⭐⭐⭐⭐⭐"</p><b style="font-size:11px">- Aisha R.</b></div>
</div>
</div>

<!-- WHATSAPP RIGHT -->
<a class="wa-btn" href="https://wa.me/923160969006" target="_blank">💬 WhatsApp</a>

<!-- WELCOME ROBOT -->
<div class="robot" id="robot">
<div class="robot-head"><span>🤖</span> GULFARA Assistant</div>
<p>Welcome to GULFARA! 👋<br>Premium Gulf Collection - 50% OFF<br>Free Delivery + Cash on Delivery!</p>
<button onclick="document.getElementById('robot').style.display='none'">Shop Now</button>
<button onclick="document.getElementById('robot').style.display='none'" style="background:#eee;color:black;margin-left:5px">Close</button>
</div>

<script>
let slides=document.querySelectorAll('.slide'),cur=0;
setInterval(()=>{slides[cur].classList.remove('active');cur=(cur+1)%slides.length;slides[cur].classList.add('active')},3000);
// welcome robot
setTimeout(()=>{document.getElementById('robot').style.display='block'},1500);
</script>

</body>
</html>
"""

@app.route('/')
def home():
    prods = Product.query.all()
    return render_template_string(TEMPLATE, products=prods, cat_name=None)

@app.route('/category/<name>')
def category(name):
    prods = Product.query.filter_by(category=name).all()
    if not prods:
        prods = Product.query.all()
    return render_template_string(TEMPLATE, products=prods, cat_name=name.upper())

with app.app_context():
    db.create_all()
    if Product.query.count()==0:
        demo=[
        ("Classic Leather Watch","Watches",199,"https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"),
        ("Royal Oud Perfume","Perfume",149,"https://images.unsplash.com/photo-1541643600914-78b084683601?w=400"),
        ("Premium Sneakers","Shoes",189,"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"),
        ("Designer Kurta","Clothes",129,"https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400"),
        ("Modern Sofa","Home",1299,"https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400"),
        ("Smart Watch Pro","Watches",249,"https://images.unsplash.com/photo-1508685096489-7aacd43bd3b2?w=400"),
        ]
        for n,c,pr,img in demo:
            db.session.add(Product(name=n, category=c, price=pr, image=img))
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
