from flask import Flask, render_template_string, request, redirect, session
import uuid

app = Flask(__name__)
app.secret_key = "vipmarket123"

users = {}  # email -> password
pets = []   # list of dicts: {id, owner, name, price, img}

@app.route('/')
def home():
    return render_template_string('''
    <html>
    <head>
        <title>🐾 Emo Pet Market VIP</title>
        <style>
            body {
                background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
                color: white;
                font-family: 'Trebuchet MS', sans-serif;
                text-align: center;
            }
            h1 {
                text-shadow: 0 0 15px gold;
            }
            .pet {
                display: inline-block;
                background: rgba(20,20,40,0.8);
                border-radius: 15px;
                padding: 15px;
                margin: 10px;
                width: 220px;
                box-shadow: 0 0 20px #e3c617;
                transition: transform 0.3s;
            }
            .pet:hover { transform: scale(1.05); }
            .btn {
                background: linear-gradient(90deg, gold, orange);
                color: black;
                padding: 10px 15px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-weight: bold;
                box-shadow: 0 0 10px gold;
                transition: 0.2s;
            }
            .btn:hover {
                background: linear-gradient(90deg, orange, gold);
                transform: scale(1.05);
            }
            .topbar {
                margin-bottom: 15px;
                background: rgba(0,0,0,0.3);
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0 0 10px #555;
            }
            a { color: #ffd700; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="topbar">
            <h1>🐾 Emo Pet Market VIP</h1>
            {% if "user" in session %}
                <p>Hoşgeldin, <b>{{session["user"]}}</b> | 
                <a href="/logout">Çıkış</a> |
                <a href="/add_pet" class="btn">Yeni İlan Ekle</a></p>
            {% else %}
                <a href="/login" class="btn">Giriş Yap</a>
                <a href="/register" class="btn">Kayıt Ol</a>
            {% endif %}
        </div>

        <h2>Satıştaki Petler</h2>
        {% for pet in pets %}
            <div class="pet">
                <img src="{{pet.img}}" width="160" style="border-radius:10px;"><br><br>
                <b>{{pet.name}}</b><br>
                <span style="color:#ffd700;">{{pet.price}} TL</span><br><br>
                <button class="btn" onclick="alert('💬 Lütfen Emo daha eklemedi satışları 😅')">Satın Al</button>
                <p style="font-size:12px; color:#ccc;">Sahip: {{pet.owner}}</p>
            </div>
        {% else %}
            <p>Henüz pet yok. Hemen bir ilan ekle!</p>
        {% endfor %}
    </body>
    </html>
    ''', pets=pets)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users:
            return "Bu e-posta zaten kayıtlı!"
        users[email] = password
        session['user'] = email
        return redirect('/')
    return '''
    <body style="background:linear-gradient(135deg,#1f1c2c,#928dab);color:white;text-align:center;">
    <h2 style="text-shadow:0 0 10px gold;">⭐ Kayıt Ol ⭐</h2>
    <form method="post">
        <input name="email" placeholder="E-posta" style="padding:8px;border-radius:8px;"><br><br>
        <input name="password" type="password" placeholder="Şifre" style="padding:8px;border-radius:8px;"><br><br>
        <button class="btn" style="background:linear-gradient(90deg,gold,orange);">VIP Kayıt</button>
    </form>
    <p><a href="/">🏠 Ana Sayfa</a></p>
    </body>
    '''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['user'] = email
            return redirect('/')
        return "Yanlış e-posta veya şifre!"
    return '''
    <body style="background:linear-gradient(135deg,#1f1c2c,#928dab);color:white;text-align:center;">
    <h2 style="text-shadow:0 0 10px gold;">✨ Giriş Yap ✨</h2>
    <form method="post">
        <input name="email" placeholder="E-posta" style="padding:8px;border-radius:8px;"><br><br>
        <input name="password" type="password" placeholder="Şifre" style="padding:8px;border-radius:8px;"><br><br>
        <button class="btn" style="background:linear-gradient(90deg,gold,orange);">VIP Giriş</button>
    </form>
    <p><a href="/">🏠 Ana Sayfa</a></p>
    </body>
    '''


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        img = request.form['img']
        pet = {
            "id": str(uuid.uuid4())[:8],
            "owner": session['user'],
            "name": name,
            "price": price,
            "img": img or "https://placekitten.com/200/200"
        }
        pets.append(pet)
        return redirect('/')
    return '''
    <body style="background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:white;text-align:center;">
    <h2 style="text-shadow:0 0 10px gold;">🆕 Yeni İlan Ekle</h2>
    <form method="post">
        <input name="name" placeholder="Pet Adı" style="padding:8px;border-radius:8px;"><br><br>
        <input name="price" placeholder="Fiyat (TL)" style="padding:8px;border-radius:8px;"><br><br>
        <input name="img" placeholder="Resim Linki (URL)" style="padding:8px;border-radius:8px;"><br><br>
        <button class="btn">Kaydet</button>
    </form>
    <p><a href="/">🏠 Ana Sayfa</a></p>
    </body>
    '''


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request

app = Flask(__name__)

# Ana sayfa
@app.route('/')
def home():
    return render_template('index.html')

# İlan ekleme sayfası
@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        pet_name = request.form['pet_name']
        price = request.form['price']
        owner = request.form['owner']
        # Burada veritabanına kayıt yapılabilir (ileride ekleriz)
        return f"<h2>{pet_name} adlı pet başarıyla eklendi!</h2><a href='/'>Ana sayfaya dön</a>"
    return render_template('add_pet.html')

