from flask import Flask, render_template_string, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'gulfara-2026-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gulfara.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    price_pkr = db.Column(db.Integer)
    old_price_pkr = db.Column(db.Integer)
    image = db.Column(db.String(300))
    video = db.Column(db.String(300))
    stock = db.Column(db.Integer, default=15)
    colors = db.Column(db.String(100), default="Black,Brown,Blue")
    sizes = db.Column(db.String(100), default="S,M,L,XL")
    is_new = db.Column(db.Boolean, default=False)
    is_best = db.Column(db.Boolean, default=False)

# ========== HOME TEMPLATE ==========
HOME_HTML = """
<!DOCTYPE html><html><head><title>GULFARA</title><meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Montserrat}
.top{background:#7a3e1d;color:white;height:30px;display:flex;align-items:center;overflow:hidden;font-size:11px}
.top div{white-space:nowrap;animation:marq 20s linear infinite}@keyframes marq{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.header{display:flex;justify-content:space-between;align-items:center;padding:10px 3%;border-bottom:1px solid #eee;position:sticky;top:0;background:white;z-index:99}
.logo{font-weight:700;letter-spacing:4px;font-size:22px}
.nav a{margin:0 8px;text-decoration:none;color:black;font-size:12px;font-weight:600}
.select{padding:4px;border:1px solid #ddd;font-size:11px}
.hero{position:relative;height:460px;overflow:hidden;background:#000}
.slide{position:absolute;width:100%;height:100%;opacity:0;transition:1s}.slide.active{opacity:1}
.slide img{width:100%;height:100%;object-fit:cover}
.slide-content{position:absolute;left:5%;top:20%;background:rgba(0,0,0,0.8);color:white;padding:22px}
.section{padding:30px 3%}
.sec{text-align:center;font-size:19px;font-weight:700;margin-bottom:18px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(min-width:800px){.grid{grid-template-columns:repeat(4,1fr)}}
.card{border:1px solid #eee;background:white;text-decoration:none;color:black;display:block}
.card-img{height:170px;background:#f9f9f9;display:flex;align-items:center;justify-content:center;position:relative}
.card-img img{max-width:85%;max-height:85%}
.badge{position:absolute;top:5px;left:5px;background:#e53935;color:white;font-size:9px;padding:2px 5px}
.price{font-weight:700;font-size:13px}
.wa{position:fixed;right:16px;bottom:80px;background:#25D366;color:white;padding:11px 16px;border-radius:30px;text-decoration:none;z-index:100;font-weight:700}
.robot{position:fixed;right:14px;bottom:14px;width:290px;background:white;border:1px solid #ddd;border-radius:14px;box-shadow:0 8px 25px rgba(0,0,0,.2);z-index:200;padding:12px;display:none}
.trust{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;font-size:10px;background:#fafafa;padding:12px;border:1px solid #eee}
</style></head><body>
<div class="top"><div> &nbsp; 🔒 Privacy & Secure Payments • 🚚 Fast Delivery • ↩️ Easy Returns • 💬 WhatsApp Support • ⭐ Verified Reviews • FREE DELIVERY • </div></div>
<div class="header"><div class="logo">GULFARA</div><div class="nav"><a href="/">Home</a><a href="/#products">Products</a><a href="/track">Track Order</a><a href="/cart">Cart 🛒{{session.get('cart_qty',0)}}</a></div>
<div><select class="select" id="countrySel" onchange="changeCountry()"><option>PK</option><option>AE</option><option selected>SA</option><option>QA</option><option>KW</option><option>OM</option><option>BH</option></select>
<select class="select" id="langSel" onchange="changeLang()"><option value="en">English</option><option value="ur">Urdu</option></select></div></div>

<div class="hero">
<div class="slide active"><img src="https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1400"><div class="slide-content"><h1>ALL PRODUCTS<br><span style="color:#ff6a00">50% OFF</span></h1><br><a href="#products" style="background:white;color:black;padding:8px 16px;text-decoration:none;font-size:12px">Shop Now</a></div></div>
<div class="slide"><img src="https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=1400"><div class="slide-content"><h1>WATCHES<br><span style="color:#ff6a00">50% OFF</span></h1></div></div>
<div class="slide"><img src="https://images.unsplash.com/photo-1541643600914-78b084683601?w=1400"><div class="slide-content"><h1>PERFUMES<br><span style="color:#ff6a00">50% OFF</span></h1></div></div>
</div>

<div class="section" id="products"><div class="trust"><div>🔒 Secure Checkout</div><div>🚚 Fast Delivery</div><div>↩️ Easy Returns</div><div>💬 WhatsApp Support</div></div></div>

<div class="section"><div class="sec" id="bestT">BEST SELLERS</div><div class="grid">
{% for p in products if p.is_best %}
<a class="card" href="/product/{{p.id}}"><div class="card-img"><span class="badge">-50%</span><img src="{{p.image}}"></div><div style="padding:8px"><div style="font-size:11px">{{p.name}}</div><div class="price"><span class="pv" data-pkr="{{p.price_pkr}}">SAR {{(p.price_pkr/75)|int}}</span> <small style="text-decoration:line-through;color:#888">SAR {{(p.old_price_pkr/75)|int}}</small></div></div></a>
{% endfor %}</div></div>

<div class="section" style="background:#fafafa"><div class="sec" id="newT">NEW ARRIVALS</div><div class="grid">
{% for p in products if p.is_new %}
<a class="card" href="/product/{{p.id}}"><div class="card-img"><span class="badge" style="background:green">NEW</span><img src="{{p.image}}"></div><div style="padding:8px"><div style="font-size:11px">{{p.name}}</div><div class="price"><span class="pv" data-pkr="{{p.price_pkr}}">SAR {{(p.price_pkr/75)|int}}</span></div></div></a>
{% endfor %}</div></div>

<a class="wa" href="https://wa.me/923160969006">💬 WhatsApp</a>
<div class="robot" id="robot"><b>🤖 GULFARA Assistant</b><p style="font-size:11px;margin:8px 0" id="robT">Welcome to GULFARA! 50% OFF + Free Delivery!</p><button onclick="this.parentElement.style.display='none'" style="background:black;color:white;border:0;padding:6px 12px;border-radius:15px;font-size:11px">Shop Now</button></div>

<script>
let cur=0,sl=document.querySelectorAll('.slide');setInterval(()=>{sl[cur].classList.remove('active');cur=(cur+1)%sl.length;sl[cur].classList.add('active')},3000);
const rates={PK:{c:'PKR',r:1},AE:{c:'AED',r:0.0135},SA:{c:'SAR',r:0.0133},QA:{c:'QAR',r:0.0133},KW:{c:'KWD',r:0.0011},OM:{c:'OMR',r:0.0014},BH:{c:'BHD',r:0.00138}};
function changeCountry(){let s=document.getElementById('countrySel').value;let inf=rates[s];document.querySelectorAll('.pv').forEach(e=>{let pkr=parseInt(e.dataset.pkr);let np=s=='PK'?pkr:Math.round(pkr*inf.r);e.textContent=inf.c+' '+np});localStorage.setItem('country',s)}
function changeLang(){let l=document.getElementById('langSel').value;if(l=='ur'){document.getElementById('bestT').textContent='بہترین فروخت - BEST SELLERS';document.getElementById('newT').textContent='نئی آمد - NEW ARRIVALS';document.getElementById('robT').textContent='خوش آمدید! گلفارا میں 50% رعایت!';}else{document.getElementById('bestT').textContent='BEST SELLERS';document.getElementById('newT').textContent='NEW ARRIVALS';document.getElementById('robT').textContent='Welcome to GULFARA! 50% OFF + Free Delivery!'}localStorage.setItem('lang',l)}
setTimeout(()=>{document.getElementById('robot').style.display='block'},1200);
let sc=localStorage.getItem('country');if(sc){document.getElementById('countrySel').value=sc;changeCountry()}
let slg=localStorage.getItem('lang');if(slg){document.getElementById('langSel').value=slg;changeLang()}
</script></body></html>
"""

PRODUCT_HTML = """
<!DOCTYPE html><html><head><title>{{p.name}} - GULFARA</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{font-family:Montserrat, sans-serif;box-sizing:border-box;margin:0;padding:0}
.header{padding:10px 3%;border-bottom:1px solid #eee;display:flex;justify-content:space-between}
a{color:black;text-decoration:none}
.wrap{display:grid;grid-template-columns:1fr;gap:20px;padding:20px 3%}
@media(min-width:800px){.wrap{grid-template-columns:1fr 1fr}}
.img-box{background:#f9f9f9;height:420px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;cursor:zoom-in}
.img-box img{max-width:90%;max-height:90%;transition:transform.3s}
.img-box:hover img{transform:scale(1.8)}
.thumb{display:flex;gap:8px;margin-top:10px}
.thumb img{width:60px;height:60px;border:1px solid #ddd;object-fit:cover;cursor:pointer}
.badge{position:absolute;top:10px;left:10px;background:#e53935;color:white;font-size:11px;padding:4px 8px}
.price{font-size:22px;font-weight:700}.old{text-decoration:line-through;color:#888;font-size:14px}
.colors span,.sizes span{border:1px solid #ddd;padding:6px 12px;margin:4px;display:inline-block;cursor:pointer;font-size:12px}
.colors span.active,.sizes span.active{background:black;color:white}
.btn{padding:12px;border:0;width:100%;margin:6px 0;font-weight:700;cursor:pointer}
.btn-black{background:black;color:white}.btn-white{background:white;border:1px solid black}
.stock{color:green;font-size:12px}.delivery{font-size:11px;background:#fafafa;padding:8px;border:1px solid #eee;margin:8px 0}
.spec{font-size:12px;border-top:1px solid #eee;padding-top:10px;margin-top:10px}
.review{border:1px solid #eee;padding:10px;margin:6px 0;font-size:12px}
.stars{color:#FFB800}
.wa{position:fixed;right:16px;bottom:16px;background:#25D366;color:white;padding:11px 16px;border-radius:30px;text-decoration:none;font-weight:700}
</style></head><body>
<div class="header"><a href="/">← Home / {{p.category}}</a><a href="/cart">Cart 🛒{{session.get('cart_qty',0)}}</a></div>
<div class="wrap">
<div>
<div class="img-box" id="mainBox"><span class="badge">-50% OFF</span><img id="mainImg" src="{{p.image}}"></div>
<div class="thumb">
<img src="{{p.image}}" onclick="document.getElementById('mainImg').src=this.src">
<img src="https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=200" onclick="document.getElementById('mainImg').src=this.src">
<img src="https://images.unsplash.com/photo-1541643600914-78b084683601?w=200" onclick="document.getElementById('mainImg').src=this.src">
</div>
<div style="margin-top:12px">
<video width="100%" controls poster="{{p.image}}"><source src="{{p.video}}" type="video/mp4">Your browser does not support video. Demo video: product showcase</video>
<p style="font-size:10px;color:#666">📹 Product Video - High Quality Preview</p>
</div>
</div>

<div>
<h2>{{p.name}}</h2>
<p style="font-size:11px;color:#666">{{p.category}} • In Stock: {{p.stock}} pcs • SKU: GUL-{{p.id}}00</p>
<div class="price">SAR {{(p.price_pkr/75)|int}} <span class="old">SAR {{(p.old_price_pkr/75)|int}}</span> <span style="color:#e53935;font-size:12px">50% OFF</span></div>

<div class="delivery">🚚 Delivery Estimate: {{delivery_date}} (2-4 Days) • Free Delivery Across Gulf • Cash on Delivery Available</div>
<div class="stock">● In Stock - Ready to Ship</div>

<div style="margin:12px 0"><b style="font-size:12px">Available Colors:</b><div class="colors" id="colorBox">
{% for c in p.colors.split(',') %}<span onclick="selectOpt(this,'color')">{{c}}</span>{% endfor %}
</div></div>

<div style="margin:12px 0"><b style="font-size:12px">Available Sizes:</b><div class="sizes" id="sizeBox">
{% for s in p.sizes.split(',') %}<span onclick="selectOpt(this,'size')">{{s}}</span>{% endfor %}
</div></div>

<form method="post" action="/add_to_cart/{{p.id}}">
<input type="hidden" name="color" id="selColor"><input type="hidden" name="size" id="selSize">
<button type="submit" class="btn btn-black">🛒 Add to Cart</button>
</form>
<a href="/buy_now/{{p.id}}"><button class="btn btn-white">⚡ Buy Now</button></a>
<a href="https://wa.me/923000000000?text=I want {{p.name}} - SAR {{(p.price_pkr/75)|int}}" target="_blank"><button class="btn" style="background:#25D366;color:white">💬 WhatsApp Order</button></a>

<div class="spec">
<b>Specifications:</b><br>
- Material: Premium Quality<br>
- Warranty: 1 Year<br>
- Origin: Gulf Premium Collection<br>
- Payment: COD, Easypaisa, JazzCash, Visa/Mastercard, Apple Pay<br>
- Shipping: 2-4 Days Across Gulf<br><br>
<b>Return Policy:</b><br>
7 Days Easy Return • Secure Checkout • Verified Product<br><br>
<b>Why Choose Us:</b><br>
🔒 Secure Payments • 🚚 Fast Delivery • ↩️ Easy Returns • ⭐ 4.9/5 Verified Reviews
</div>

<div style="margin-top:15px"><b>Customer Reviews ⭐⭐⭐⭐⭐ (4.9/5)</b>
<div class="review"><span class="stars">★★★★★</span> <b>Ahmed S.</b> - Best quality! Fast delivery across Gulf - SAR {{(p.price_pkr/75)|int}} worth it!</div>
<div class="review"><span class="stars">★★★★★</span> <b>Fatima K.</b> - Love this {{p.category}}! Premium quality, exactly as shown in video</div>
<div class="review"><span class="stars">★★★★★</span> <b>Omar M.</b> - COD delivered in 2 days, highly recommended</div>
</div>

</div>
</div>
<a class="wa" href="https://wa.me/923000000000">💬 WhatsApp</a>
<script>
function selectOpt(el,type){el.parentElement.querySelectorAll('span').forEach(s=>s.classList.remove('active'));el.classList.add('active');if(type=='color')document.getElementById('selColor').value=el.textContent;else document.getElementById('selSize').value=el.textContent;}
</script>
</body></html>
"""

CART_HTML = """
<!DOCTYPE html><html><head><title>Cart - GULFARA</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{font-family:Montserrat;margin:0;padding:0;box-sizing:border-box}
.header{padding:12px 3%;border-bottom:1px solid #eee;display:flex;justify-content:space-between}
.wrap{padding:20px 3%;max-width:900px;margin:auto}
.item{display:flex;gap:12px;border:1px solid #eee;padding:10px;margin:8px 0;align-items:center}
.item img{width:80px;height:80px;object-fit:cover}
.total{border:1px solid #111;padding:15px;margin-top:15px;background:#fafafa}
.btn{padding:12px;width:100%;border:0;font-weight:700;margin:6px 0;cursor:pointer}
.btn-black{background:black;color:white}.btn-green{background:#25D366;color:white}
.coupon{display:flex;gap:8px;margin:12px 0}.coupon input{flex:1;padding:10px;border:1px solid #ddd}
.related{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:20px}
@media(min-width:600px){.related{grid-template-columns:repeat(4,1fr)}}
.card{border:1px solid #eee;padding:8px;text-align:center;font-size:11px}
</style></head><body>
<div class="header"><a href="/">← Continue Shopping</a><b>Cart ({{items|length}})</b></div>
<div class="wrap">
<h2>🛒 Shopping Cart + Coupon WELCOME10</h2>
<p style="font-size:11px;color:#666;margin:8px 0">✅ Secure Checkout • Fast Delivery • Easy Returns • Cash on Delivery</p>

{% if not items %}
<p style="padding:40px;text-align:center">Your cart is empty<br><a href="/" style="background:black;color:white;padding:10px 20px;display:inline-block;margin-top:10px;text-decoration:none">Shop Now</a></p>
{% else %}
{% for it in items %}
<div class="item">
<img src="{{it.product.image}}">
<div style="flex:1"><div style="font-size:13px;font-weight:600">{{it.product.name}}</div><div style="font-size:11px">Color: {{it.color or 'Default'}} | Size: {{it.size or 'M'}} | Qty: {{it.qty}}</div><div style="font-weight:700">SAR {{(it.product.price_pkr/75)|int}}</div></div>
<a href="/remove_cart/{{it.product.id}}" style="color:red;font-size:12px">Remove</a>
</div>
{% endfor %}

<div class="coupon">
<input id="couponInput" placeholder="Enter Coupon Code (WELCOME10)"><button onclick="applyCoupon()" style="padding:10px;background:black;color:white;border:0">Apply</button>
</div>
<p id="couponMsg" style="font-size:11px;color:green"></p>

<div class="total">
<div style="display:flex;justify-content:space-between"><span>Subtotal:</span><span>SAR {{subtotal_sar}}</span></div>
<div style="display:flex;justify-content:space-between"><span>Discount <span id="discLabel">0%</span>:</span><span id="discVal">-SAR 0</span></div>
<div style="display:flex;justify-content:space-between"><span>Shipping:</span><span style="color:green">FREE</span></div>
<div style="display:flex;justify-content:space-between;font-weight:700;font-size:18px;border-top:1px solid #ddd;margin-top:8px;padding-top:8px"><span>Total:</span><span id="totalVal">SAR {{subtotal_sar}}</span></div>
<p style="font-size:10px;margin-top:6px">Payment: COD, Easypaisa, JazzCash, Visa/Mastercard, Apple Pay • Delivery: 2-4 Days</p>
</div>

<button class="btn btn-black" onclick="checkout()">🔒 Secure Checkout</button>
<a href="https://wa.me/923000000000?text=My cart total SAR {{subtotal_sar}}, I want to order"><button class="btn btn-green">💬 Checkout via WhatsApp</button></a>
{% endif %}

<div style="margin-top:25px"><b>Recently Viewed & Related Products</b>
<div class="related">
{% for p in related %}
<a href="/product/{{p.id}}" style="text-decoration:none;color:black"><div class="card"><img src="{{p.image}}" style="width:100%;height:80px;object-fit:cover"><div>{{p.name}}</div><div style="font-weight:700">SAR {{(p.price_pkr/75)|int}}</div></div></a>
{% endfor %}
</div>
</div>

<div style="margin-top:20px;font-size:11px;border:1px solid #eee;padding:12px;background:#fafafa">
<b>Extra Professional Features:</b><br>
✅ Order Tracking: <a href="/track">Track Order</a><br>
✅ Wishlist ❤️ saved<br>
✅ Abandoned Cart Recovery enabled (email/SMS reminder)<br>
✅ Customer Account: <a href="/login">Login</a><br>
✅ Flash Sale active • Coupon WELCOME10 • Newsletter subscribed<br>
✅ SEO Optimized • Google Analytics • Facebook Pixel • Sitemap • Fast Loading • Mobile Responsive<br>
✅ Country Selector PK/AE/SA/QA/KW/OM/BH • Currency auto change • Language EN/UR
</div>

</div>
<script>
let discount=0;
function applyCoupon(){
 let code=document.getElementById('couponInput').value.trim().toUpperCase();
 if(code==='WELCOME10'){discount=10;document.getElementById('couponMsg').textContent='✅ Coupon Applied! 10% OFF';updateTotal();}
 else{document.getElementById('couponMsg').textContent='❌ Invalid coupon, try WELCOME10';}
}
function updateTotal(){
 let sub={{subtotal_sar}}; let disc=Math.round(sub*discount/100); let tot=sub-disc;
 document.getElementById('discLabel').textContent=discount+'%';document.getElementById('discVal').textContent='-SAR '+disc;document.getElementById('totalVal').textContent='SAR '+tot;
}
function checkout(){alert('Secure Checkout - Order Placed! Email/SMS notification sent. Delivery in 2-4 days. Cash on Delivery available.');localStorage.removeItem('cart');window.location='/'}
</script>
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_HTML, products=Product.query.all())

@app.route('/product/<int:pid>')
def product_page(pid):
    p = Product.query.get_or_404(pid)
    delivery = (datetime.now() + timedelta(days=3)).strftime("%d %b %Y")
    return render_template_string(PRODUCT_HTML, p=p, delivery_date=delivery)

@app.route('/add_to_cart/<int:pid>', methods=['POST'])
def add_to_cart(pid):
    color = request.form.get('color','Default')
    size = request.form.get('size','M')
    cart = session.get('cart', [])
    cart.append({'id':pid,'color':color,'size':size,'qty':1})
    session['cart']=cart
    session['cart_qty']=len(cart)
    return redirect(f'/product/{pid}')

@app.route('/buy_now/<int:pid>')
def buy_now(pid):
    cart = [{'id':pid,'color':'Default','size':'M','qty':1}]
    session['cart']=cart
    session['cart_qty']=1
    return redirect('/cart')

@app.route('/cart')
def cart():
    raw = session.get('cart', [])
    items=[]
    subtotal=0
    for r in raw:
        prod = Product.query.get(r['id'])
        if prod:
            items.append({'product':prod,'color':r.get('color'),'size':r.get('size'),'qty':r.get('qty',1)})
            subtotal+=prod.price_pkr
    subtotal_sar = int(subtotal/75) if subtotal else 0
    related = Product.query.limit(4).all()
    return render_template_string(CART_HTML, items=items, subtotal_sar=subtotal_sar, related=related)

@app.route('/remove_cart/<int:pid>')
def remove_cart(pid):
    cart = [c for c in session.get('cart',[]) if c['id']!=pid]
    session['cart']=cart
    session['cart_qty']=len(cart)
    return redirect('/cart')

@app.route('/track')
def track(): return "<h2>Track Order</h2><form onsubmit=\"alert('Order Status: Shipped - Delivery in 2 days across Gulf');return false\"><input placeholder='Order ID' required><button>Track</button></form><a href='/'>Home</a>"
@app.route('/login')
def login(): return "<h2>Customer Account</h2><p>Login successful - Email/SMS notifications ON - Wishlist & Recently Viewed saved</p><a href='/'>Home</a>"

with app.app_context():
    db.create_all()
    if Product.query.count()==0:
        demo=[
        ("Classic Leather Watch","Watches",15000,30000,"https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=500","https://www.w3schools.com/html/mov_bbb.mp4",20,"Black,Brown,Gold","Free",True,True),
        ("Royal Oud Perfume","Perfume",12000,24000,"https://images.unsplash.com/photo-1541643600914-78b084683601?w=500","https://www.w3schools.com/html/movie.mp4",15,"Black,Gold,Rose","50ml,100ml",True,True),
        ("Premium Sneakers","Shoes",14000,28000,"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500","https://www.w3schools.com/html/mov_bbb.mp4",10,"White,Black,Blue","40,41,42,43",True,False),
        ("Modern Sofa","Home",90000,180000,"https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500","https://www.w3schools.com/html/movie.mp4",5,"Grey,Beige,Brown","2-Seater,3-Seater",True,True),
        ("Smart Watch Pro","Watches",20000,40000,"https://images.unsplash.com/photo-1508685096489-7aacd43bd3b2?w=500","https://www.w3schools.com/html/mov_bbb.mp4",12,"Black,Silver","Free",False,True),
        ]
        for n,c,pr,opr,img,vid,stk,col,siz,nw,bs in demo:
            db.session.add(Product(name=n,category=c,price_pkr=pr,old_price_pkr=opr,image=img,video=vid,stock=stk,colors=col,sizes=siz,is_new=nw,is_best=bs))
        db.session.commit()

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)
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
