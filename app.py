from flask import Flask, request, redirect, render_template_string
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
    rating = db.Column(db.Float, default=4.8)

# ===== HTML TEMPLATES IN ONE FILE =====
HOME_HTML = """
<!DOCTYPE html>
<html>
<head><title>GULFARA</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;text-align:center;background:#fff;margin:0}
.header{background:black;color:gold;padding:20px}
.header h1{margin:0;letter-spacing:3px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:15px;padding:20px}
@media(min-width:700px){.grid{grid-template-columns:1fr 1fr 1fr}}
.card{border:2px solid gold;border-radius:12px;padding:12px}
.card img{width:100%;height:150px;object-fit:cover;border-radius:8px}
.btn{background:black;color:gold;padding:12px 25px;text-decoration:none;border-radius:8px;display:inline-block;margin:20px;font-size:18px}
</style>
</head>
<body>
<div class="header"><h1>GULFARA</h1><p>Premium Collection</p></div>
<h2>Featured - One From Each Category</h2>
<div class="grid">
{% for p in featured %}
<div class="card">
<img src="{{p.image}}">
<h3>{{p.category}}</h3>
<p>{{p.name}}</p>
<b>Rs. {{p.price}}</b><br>
<small>⭐ {{p.rating}}</small>
</div>
{% endfor %}
</div>
<a href="/catalog" class="btn">VIEW FULL CATALOG</a>
<br><a href="/admin" style="color:gray">Admin - Add Product</a>
</body>
</html>
"""

CATALOG_HTML = """
<!DOCTYPE html>
<html>
<head><title>Catalog - GULFARA</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{font-family:Arial;text-align:center}.grid{display:grid;grid-template-columns:1fr 1fr;gap:15px;padding:20px}.card{border:1px solid #ddd;padding:10px;border-radius:10px}.card img{width:100%;height:130px;object-fit:cover}</style>
</head>
<body>
<h1>GULFARA - Full Catalog</h1>
<a href="/catalog">All</a> |
<a href="/catalog?cat=Watches">Watches</a> |
<a href="/catalog?cat=Perfume">Perfume</a> |
<a href="/catalog?cat=Shoes">Shoes</a> |
<a href="/catalog?cat=Clothes">Clothes</a> |
<a href="/catalog?cat=Accessory">Accessory</a> |
<a href="/catalog?cat=Home">Home</a>
<div class="grid">
{% for p in products %}
<div class="card"><img src="{{p.image}}"><p>{{p.name}}</p><b>Rs. {{p.price}}</b><br>⭐ {{p.rating}}</div>
{% endfor %}
</div>
<br><a href="/">Back to Home</a>
</body>
</html>
"""

ADMIN_HTML = """
<!DOCTYPE html>
<html><body style="font-family:Arial;padding:20px">
<h1>Admin - Add Product (GULFARA)</h1>
<form method="POST" style="background:#f5f5f5;padding:20px;border-radius:10px">
<input name="name" placeholder="Product Name" required style="width:100%;padding:10px;margin:5px"><br>
<select name="category" style="width:100%;padding:10px;margin:5px">
<option>Watches</option><option>Perfume</option><option>Shoes</option><option>Clothes</option><option>Accessory</option><option>Home</option>
</select><br>
<input name="price" placeholder="Price" type="number" required style="width:100%;padding:10px;margin:5px"><br>
<input name="image" placeholder="Image Link (https://...)" required style="width:100%;padding:10px;margin:5px"><br>
<button style="background:gold;padding:10px 20px">ADD PRODUCT</button>
</form>
<hr>
<h3>All Products ({{products|length}})</h3>
{% for p in products %}
{{p.id}} - {{p.category}} - {{p.name}} - Rs.{{p.price}} <a href="/delete/{{p.id}}">[Delete]</a><br>
{% endfor %}
<br><a href="/">Home</a>
</body></html>
"""

@app.route('/')
def home():
    cats = ['Watches','Perfume','Shoes','Clothes','Accessory','Home']
    featured = []
    for c in cats:
        p = Product.query.filter_by(category=c).first()
        if p: featured.append(p)
    return render_template_string(HOME_HTML, featured=featured)

@app.route('/catalog')
def catalog():
    cat = request.args.get('cat')
    products = Product.query.filter_by(category=cat).all() if cat else Product.query.all()
    return render_template_string(CATALOG_HTML, products=products)

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        db.session.add(Product(name=request.form['name'], category=request.form['category'], price=int(request.form['price']), image=request.form['image']))
        db.session.commit()
        return redirect('/admin')
    return render_template_string(ADMIN_HTML, products=Product.query.all())

@app.route('/delete/<int:id>')
def delete(id):
    p = Product.query.get(id)
    if p:
        db.session.delete(p)
        db.session.commit()
    return redirect('/admin')

def init_db():
    db.create_all()
    if Product.query.count() == 0:
        dummy = [
            ("Classic Leather Watch","Watches",5500,"https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"),
            ("Royal Oud Perfume","Perfume",3500,"https://images.unsplash.com/photo-1541643600914-78b084683601?w=400"),
            ("Premium Sneakers","Shoes",4200,"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"),
            ("Designer Kurta","Clothes",3000,"https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400"),
            ("Elegant Sunglasses","Accessory",1800,"https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400"),
            ("Aroma Burner","Home",1500,"https://images.unsplash.com/photo-1513694203232-719a280e022f?w=400"),
            ("Smart Watch Pro","Watches",7500,"https://images.unsplash.com/photo-1508685096489-7aacd43bd3b2?w=400"),
            ("Floral Attar","Perfume",2800,"https://images.unsplash.com/photo-1594035910387-fea47794261f?w=400"),
        ]
        for n,c,pr,img in dummy:
            db.session.add(Product(name=n, category=c, price=pr, image=img))
        db.session.commit()

# Auto create database on start - Fix for Render
with app.app_context():
    db.create_all()
    if Product.query.count() == 0:
        dummy = [
            ("Classic Leather Watch","Watches",5500,"https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"),
            ("Royal Oud Perfume","Perfume",3500,"https://images.unsplash.com/photo-1541643600914-78b084683601?w=400"),
            ("Premium Sneakers","Shoes",4200,"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"),
            ("Designer Kurta","Clothes",3000,"https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400"),
            ("Elegant Sunglasses","Accessory",1800,"https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400"),
            ("Aroma Burner","Home",1500,"https://images.unsplash.com/photo-1513694203232-719a280e022f?w=400"),
        ]
        for n,c,pr,img in dummy:
            db.session.add(Product(name=n, category=c, price=pr, image=img))
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
