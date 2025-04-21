from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from flask_session import Session

app = Flask(__name__)
app.secret_key = "rahasia"  # Ganti dengan yang lebih aman
app.config["MONGO_URI"] = "mongodb://localhost:27017/rental_mobil"  # Ganti dengan URI MongoDB yang sesuai
app.config['SESSION_TYPE'] = 'filesystem'  # Session disimpan di filesystem
Session(app)  # Menginisialisasi session
mongo = PyMongo(app)

@app.route('/')
def guest_page():
    mobil_data = list(mongo.db.mobil.find({}, {"_id": 0}))
    return render_template("guest.html", daftar_mobil=mobil_data)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if not username or not password:
            flash("Username and password are required.", "warning")
            return redirect(url_for("register"))

        existing_user = mongo.db.users.find_one({"username": username})
        if existing_user:
            flash("Username already exists.", "danger")
            return redirect(url_for("register"))

        hashed_pw = generate_password_hash(password)
        mongo.db.users.insert_one({"username": username, "password": hashed_pw})
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Proses login di sini, misalnya validasi username dan password
        username = request.form['username']
        password = request.form['password']
        
        # Cek validasi login (misalnya cek ke MongoDB)
        user = mongo.db.users.find_one({'username': username})
        
        if user and check_password_hash(user['password'], password):  # Use check_password_hash
            session['logged_in'] = True  # Set session login
            return redirect(url_for('admin_panel'))  # Redirect ke admin panel setelah login
            
        return "Invalid credentials"  # Jika login gagal
    
    return render_template('login.html')  # Tampilkan halaman login


@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Hapus session logged_in
    return redirect(url_for('login'))  # Arahkan ke halaman login setelah logout

@app.route('/admin_panel')
def admin_panel():
    # Cek apakah user sudah login (session 'logged_in' ada)
    if 'logged_in' not in session:
        return redirect(url_for('login'))  # Jika tidak ada session, arahkan ke halaman login

    # Ambil data mobil dari database
    mobil = list(mongo.db.mobil.find({}, {"_id": 0}))
    
    # Tampilkan halaman admin panel dengan data mobil
    return render_template('admin.html', mobil=mobil)
    


@app.route('/update_status', methods=['POST'])
def update_status():
    plat = request.form.get('plat')
    status = request.form.get('status')
    mongo.db.mobil.update_one({'plat': plat}, {'$set': {'status': status}})
    return redirect(url_for('admin_panel'))

@app.route('/mobil', methods=['GET'])
def get_all_mobil():
    try:
        # Ambil data dari koleksi mobil tanpa _id
        data = list(mongo.db.mobil.find({}, {"_id": 0}))
        
        # Jika data ditemukan, kirimkan sebagai response dalam format JSON
        if data:
            return jsonify(data)
        else:
            return jsonify({"message": "Tidak ada daftar mobil"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


