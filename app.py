from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gulfara.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    price_pkr = db.Column(db.Integer)
    image = db.Column(db.String(300))
    is_new = db.Column(db.Boolean, default=False)
    is_best = db.Column(db.Boolean, default=False)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<title>GULFARA | Premium Collection</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700&family=Noto+Nastaliq+Urdu&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Montserrat', sans-serif}
.top-bar{background:#7a3e1d;color:white;height:32px;display:flex;align-items:center;overflow:hidden;font-size:11px}
.top-bar div{white-space:nowrap;animation:marq 25s linear infinite}
@keyframes marq{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.header{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;padding:10px 3%;border-bottom:1px solid #eee;position:sticky;top:0;background:white;z-index:99;gap:8px}
.logo{font-weight:700;font-size:24px;letter-spacing:4px}
.nav{display:flex;gap:12px;font-size:12px}
.nav a{text-decoration:none;color:black;font-weight:500}
.header-right{display:flex;align-items:center;gap:8px}
.search{display:flex;border:1px solid #ddd}
.search input{padding:7px;border:0;outline:none;width:110px}
.search button{background:black;color:white;border:0;padding:0 10px}
.select{padding:5px;border:1px solid #ddd;font-size:11px}
.cart-badge{background:black;color:white;border-radius:50%;padding:2px 6px;font-size:10px}
.hero{position:relative;height:480px;overflow:hidden;background:#000}
.slide{position:absolute;top:0;left:0;width:100%;height:100%;opacity:0;transition:opacity 1s}
.slide.active{opacity:1}
.slide img{width:100%;height:100%;object-fit:cover;opacity:0.8}
.slide-content{position:absolute;left:6%;top:18%;background:rgba(0,0,0,0.82);color:white;padding:25px 30px;max-width:360px}
.slide-content h1{font-size:42px;line-height:0.9}
.slide-content h1 span{color:#ff6a00}
.btn-black{background:black;color:white;padding:10px 20px;text-decoration:none;display:inline-block;margin-top:12px;font-size:12px}
.section{padding:35px 4%}
.sec-title{text-align:center;font-size:20px;font-weight:600;margin-bottom:20px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:15px}
@media(min-width:800px){.grid{grid-template-columns:repeat(4,1fr)}}
.card{border:1px solid #eee;background:white}
.card-img{height:180px;background:#f9f9f9;display:flex;align-items:center;justify-content:center;position:relative}
.card-img img{max-width:85%;max-height:85%}
.badge{position:absolute;top:6px;left:6px;background:#e53935;color:white;font-size:9px;padding:2px 6px}
.wish{position:absolute;top:6px;right:6px;background:white;border-radius:50%;width:26px;height:26px;display:flex;align-items:center;justify-content:center;cursor:pointer;border:1px solid #eee}
.price{font-weight:700;font-size:13px}
.trust{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;font-size:11px;background:#fafafa;padding:15px;border:1px solid #eee}
.flash{background:#ff3d00;color:white;text-align:center;padding:10px;font-size:14px}
.reviews.review{border:1px solid #eee;padding:12px;background:white;text-align:center}
.stars{color:#FFB800}
.faq{border:1px solid #eee;padding:10px;margin:6px 0;cursor:pointer}
.newsletter{background:#111;color:white;text-align:center;padding:25px}
.footer{background:#f5f5f5;padding:30px 4%;display:grid;grid-template-columns:1fr 1fr;gap:20px;font-size:12px}
@media(min-width:800px){.footer{grid-template-columns:repeat(4,1fr)}}
.wa{position:fixed;right:18px;bottom:85px;background:#25D366;color:white;padding:11px 18px;border-radius:30px;text-decoration:none;z-index:100;font-weight:600;box-shadow:0 4px 12px rgba(0,0,0,0.3)}
.robot{position:fixed;right:15px;bottom:15px;width:300px;background:white;border:1px solid #ddd;border-radius:15px;box-shadow:0 8px 30px rgba(0,0,0,0.2);z-index:200;padding:14px;display:none}
.urdu{font-family:'Noto Nastaliq Urdu', serif}
</style>
</head>
<body>

<div class="top-bar"><div> &nbsp; 🔒 Secure Checkout • 🚚 Fast Delivery • ↩️ Easy Returns • 💬 WhatsApp Support • ⭐ Verified Reviews • FREE DELIVERY • CASH ON DELIVERY • </div></div>
<div class="flash">⚡ FLASH SALE: <span id="countdown">02:45:30</span> - 50% OFF!</div>

<div class="header">
<div class="logo">GULFARA</div>
<div class="nav">
<a href="/">Home</a><a href="/#products">Products</a><a href="/track">Track Order</a><a href="/login">Login</a>
</div>
<div class="header-right">
<div class="search"><input id="searchInput" placeholder="Search..." onkeyup="searchProd()"><button>🔍</button></div>
<select class="select" id="countrySel" onchange="changeCountry()">
<option value="PK">PK</option><option value="AE">AE</option><option value="SA" selected>SA</option><option value="QA">QA</option><option value="KW">KW</option><option value="OM">OM</option><option value="BH">BH</option>
</select>
<select class="select" id="langSel" onchange="changeLang()">
<option value="en">English</option><option value="ur">Urdu</option>
</select>
<a href="/wishlist" style="text-decoration:none">❤️<span id="wishCount">0</span></a>
<a href="/cart" style="text-decoration:none">🛒<span class="cart-badge" id="cartCount">0</span></a>
</div>
</div>

<div class="hero">
<div class="slide active"><img src="https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1400"><div class="slide-content"><h1 id="hero1">ALL PRODUCTS<br><span>50% OFF</span></h1><a class="btn-black" href="#products">Shop Now</a></div></div>
<div class="slide"><img src="https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=1400"><div class="slide-content"><h1>PREMIUM<br>WATCHES<br><span>50% OFF</span></h1><a class="btn-black" href="/category/Watches">Shop Now</a></div></div>
<div class="slide"><img src="https://images.unsplash.com/photo-1541643600914-78b084683601?w=1400"><div class="slide-content"><h1>LUXURY<br>PERFUMES<br><span>50% OFF</span></h1><a class="btn-black" href="/category/Perfume">Shop Now</a></div></div>
<div class="slide"><img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=1400"><div class="slide-content"><h1>STYLISH<br>SHOES<br><span>50% OFF</span></h1><a class="btn-black" href="/category/Shoes">Shop Now</a></div></div>
</div>

<div class="section" id="products">
<div class="trust"><div>🔒 Secure Checkout</div><div>🚚 Fast Delivery</div><div>↩️ Easy Returns</div><div>💬 WhatsApp Support</div><div>⭐ Verified Reviews</div></div>
</div>

<div class="section">
<div class="sec-title" id="bestTitle">BEST SELLERS</div>
<div class="grid">
{% for p in products if p.is_best %}
<div class="card prod" data-name="{{p.name.lower()}}"><div class="card-img"><span class="badge">-50%</span><div class="wish" onclick="addWish({{p.id}})">❤️</div><img src="{{p.image}}"></div><div class="card-body"><h4 style="font-size:11px">{{p.name}}</h4><div class="price"><span class="priceVal" data-pkr="{{p.price_pkr}}">SAR {{ (p.price_pkr/75)|int }}</span></div><button onclick="addCart({{p.id}})" style="width:100%;margin-top:6px;background:black;color:white;border:0;padding:6px;font-size:11px">Add to Cart</button></div></div>
{% endfor %}
</div>
</div>

<div class="section" style="background:#fafafa">
<div class="sec-title" id="newTitle">NEW ARRIVALS</div>
<div class="grid">
{% for p in products if p.is_new %}
<div class="card prod" data-name="{{p.name.lower()}}"><div class="card-img"><span class="badge" style="background:green">NEW</span><div class="wish" onclick="addWish({{p.id}})">❤️</div><img src="{{p.image}}"></div><div class="card-body"><h4 style="font-size:11px">{{p.name}}</h4><div class="price"><span class="priceVal" data-pkr="{{p.price_pkr}}">SAR {{ (p.price_pkr/75)|int }}</span></div><button onclick="addCart({{p.id}})" style="width:100%;margin-top:6px;background:black;color:white;border:0;padding:6px;font-size:11px">Add to Cart</button></div></div>
{% endfor %}
</div>
</div>

<div class="section">
<div class="sec-title" id="catTitle">SHOP BY CATEGORY</div>
<div style="display:flex;gap:15px;justify-content:center;flex-wrap:wrap">
<a href="/category/Watches" style="text-align:center;text-decoration:none;color:black"><img src="https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=200" style="width:90px;height:90px;border-radius:50%"><p style="font-size:11px">WATCHES</p></a>
<a href="/category/Perfume" style="text-align:center;text-decoration:none;color:black"><img src="https://images.unsplash.com/photo-1541643600914-78b084683601?w=200" style="width:90px;height:90px;border-radius:50%"><p style="font-size:11px">PERFUME</p></a>
<a href="/category/Shoes" style="text-align:center;text-decoration:none;color:black"><img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=200" style="width:90px;height:90px;border-radius:50%"><p style="font-size:11px">SHOES</p></a>
<a href="/category/Home" style="text-align:center;text-decoration:none;color:black"><img src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=200" style="width:90px;height:90px;border-radius:50%"><p style="font-size:11px">HOME</p></a>
</div>
</div>

<div class="section" style="background:#fafafa">
<div class="sec-title">CUSTOMER REVIEWS ⭐⭐⭐⭐⭐</div>
<div class="grid">
<div class="review"><div class="stars">★★★★★</div><p style="font-size:11px;margin:6px 0">"Best quality! Fast delivery"</p><b style="font-size:10px">- Ahmed</b></div>
<div class="review"><div class="stars">★★★★★</div><p style="font-size:11px;margin:6px 0">"Premium watches, love it"</p><b style="font-size:10px">- Fatima</b></div>
<div class="review"><div class="stars">★★★★★</div><p style="font-size:11px;margin:6px 0">"COD + WhatsApp amazing"</p><b style="font-size:10px">- Omar</b></div>
<div class="review"><div class="stars">★★★★★</div><p style="font-size:11px;margin:6px 0">"Fragrance ⭐⭐⭐⭐⭐"</p><b style="font-size:10px">- Aisha</b></div>
</div>
</div>

<div class="newsletter">
<h3 id="newsTitle">Newsletter - Get 10% OFF</h3>
<input id="emailNews" placeholder="Your email"><button onclick="subscribe()" style="padding:10px;background:#7a3e1d;color:white;border:0">Subscribe</button>
<p style="font-size:10px;margin-top:8px">Coupon: WELCOME10</p>
</div>

<div class="footer">
<div><b>GULFARA</b><br>Premium Collection<br>Free Delivery<br>Cash on Delivery</div>
<div><b>Payment</b><br>PK: COD, Easypaisa, JazzCash, Bank<br>Gulf: Visa/Mastercard, Apple Pay</div>
<div><b>Support</b><br>Track Order<br>Wishlist ❤️<br>WhatsApp Live Support</div>
<div><b>Trust</b><br>🔒 Secure<br>🚚 Fast<br>↩️ Easy Returns<br>⭐ Verified Reviews</div>
</div>

<a class="wa" href="https://wa.me/923000000000" target="_blank">💬 WhatsApp</a>

<div class="robot" id="robot">
<div style="font-weight:700">🤖 GULFARA Assistant</div>
<p style="font-size:12px;margin:8px 0" id="robotText">Welcome to GULFARA! 50% OFF + Free Delivery!</p>
<button onclick="document.getElementById('robot').style.display='none'" style="background:black;color:white;border:0;padding:6px 12px;border-radius:15px;font-size:11px">Shop Now</button>
</div>

<script>
let cur=0,slides=document.querySelectorAll('.slide');
setInterval(()=>{slides[cur].classList.remove('active');cur=(cur+1)%slides.length;slides[cur].classList.add('active')},3000);
const rates={PK:{c:'PKR',r:1},AE:{c:'AED',r:0.0135},SA:{c:'SAR',r:0.0133},QA:{c:'QAR',r:0.0133},KW:{c:'KWD',r:0.0011},OM:{c:'OMR',r:0.0014},BH:{c:'BHD',r:0.00138}};
function changeCountry(){let sel=document.getElementById('countrySel').value;let info=rates[sel];document.querySelectorAll('.priceVal').forEach(el=>{let pkr=parseInt(el.dataset.pkr);let np=Math.round(pkr*info.r);if(info.c=='PKR')np=pkr;el.textContent=info.c+' '+np});localStorage.setItem('country',sel);}
function changeLang(){
 let l=document.getElementById('langSel').value;
 if(l=='ur'){
   document.getElementById('bestTitle').innerHTML='<span class="urdu">بہترین فروخت</span> - BEST SELLERS';
   document.getElementById('newTitle').innerHTML='<span class="urdu">نئی آمد</span> - NEW ARRIVALS';
   document.getElementById('catTitle').innerHTML='<span class="urdu">زمرہ جات</span> - SHOP BY CATEGORY';
   document.getElementById('newsTitle').innerHTML='<span class="urdu">نیوز لیٹر - 10% رعایت</span>';
   document.getElementById('robotText').innerHTML='خوش آمدید! گلفارا میں 50% رعایت + مفت ڈیلیوری!';
 }else{
   document.getElementById('bestTitle').textContent='BEST SELLERS';
   document.getElementById('newTitle').textContent='NEW ARRIVALS';
   document.getElementById('catTitle').textContent='SHOP BY CATEGORY';
   document.getElementById('newsTitle').textContent='Newsletter - Get 10% OFF';
   document.getElementById('robotText').textContent='Welcome to GULFARA! 50% OFF + Free Delivery!';
 }
 localStorage.setItem('lang',l);
}
function addCart(id){let c=JSON.parse(localStorage.getItem('cart')||'[]');c.push(id);localStorage.setItem('cart',JSON.stringify(c));document.getElementById('cartCount').textContent=c.length;alert('Added to Cart!');}
function addWish(id){let w=JSON.parse(localStorage.getItem('wish')||'[]');if(!w.includes(id))w.push(id);localStorage.setItem('wish',JSON.stringify(w));document.getElementById('wishCount').textContent=w.length;alert('Wishlist ❤️');}
function searchProd(){let q=document.getElementById('searchInput').value.toLowerCase();document.querySelectorAll('.prod').forEach(p=>{p.style.display=p.dataset.name.includes(q)?'':'none'});}
function subscribe(){let e=document.getElementById('emailNews').value;if(e){alert('Coupon WELCOME10 sent to '+e);}}
document.getElementById('cartCount').textContent=(JSON.parse(localStorage.getItem('cart')||'[]')).length;
document.getElementById('wishCount').textContent=(JSON.parse(localStorage.getItem('wish')||'[]')).length;
setTimeout(()=>{document.getElementById('robot').style.display='block'},1500);
let t=2*3600+45*60+30; setInterval(()=>{t--;let h=Math.floor(t/3600),m=Math.floor((t%3600)/60),s=t%60;document.getElementById('countdown').textContent=(h<10?'0':'')+h+':'+(m<10?'0':'')+m+':'+(s<10?'0':'')+s},1000);
let saved=localStorage.getItem('country'); if(saved){document.getElementById('countrySel').value=saved; changeCountry();}
let savedLang=localStorage.getItem('lang'); if(savedLang){document.getElementById('langSel').value=savedLang; changeLang();}
</script>

</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(TEMPLATE, products=Product.query.all())
@app.route('/category/<name>')
def category(name):
    f=Product.query.filter_by(category=name).all()
    return render_template_string(TEMPLATE, products=f if f else Product.query.all())
@app.route('/track')
def track(): return "<h2>Track Order</h2><p>Enter Order ID to track</p><a href='/'>Home</a>"
@app.route('/login')
def login(): return "<h2>Login / Account</h2><a href='/'>Home</a>"
@app.route('/wishlist')
def wishlist(): return "<h2>Wishlist ❤️</h2><a href='/'>Home</a>"
@app.route('/cart')
def cart(): return "<h2>Cart + Coupon WELCOME10</h2><a href='/'>Home</a>"

with app.app_context():
    db.create_all()
    if Product.query.count()==0:
        demo=[("Classic Leather Watch","Watches",15000,True,True,"https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"),("Royal Oud Perfume","Perfume",12000,True,True,"https://images.unsplash.com/photo-1541643600914-78b084683601?w=400"),("Premium Sneakers","Shoes",14000,True,False,"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"),("Modern Sofa","Home",90000,True,True,"https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400"),("Smart Watch Pro","Watches",20000,True,False,"https://images.unsplash.com/photo-1508685096489-7aacd43bd3b2?w=400"),("Executive Chair","Home",75000,False,True,"https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=400")]
        for n,c,pr,nw,bs,img in demo: db.session.add(Product(name=n, category=c, price_pkr=pr, is_new=nw, is_best=bs, image=img))
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
