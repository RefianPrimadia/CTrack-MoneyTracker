from flask import Flask, render_template, request, redirect, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

users = {}
data_user = {}

def get_user():
    return session.get("user")

@app.route("/")
def dashboard():
    user = get_user()
    if not user:
        return redirect("/login")

    if user not in data_user:
        data_user[user] = {
            "saldo": 0,
            "riwayat": []
        }

    d = data_user[user]
    status = "Aman"
    if d["saldo"] < 0:
        status = "⚠️ Pengeluaran melebihi pemasukan"

    return render_template("dashboard.html", d=d, status=status)

@app.route("/transaksi", methods=["POST"])
def transaksi():
    user = get_user()
    jenis = request.form["jenis"]
    jumlah = int(request.form["jumlah"])
    catatan = request.form["catatan"]

    if jenis == "masuk":
        data_user[user]["saldo"] += jumlah
        ket = "Pemasukan"
    else:
        data_user[user]["saldo"] -= jumlah
        ket = "Pengeluaran"

    data_user[user]["riwayat"].append({
        "tanggal": datetime.now().strftime("%d-%m-%Y"),
        "keterangan": ket,
        "jumlah": jumlah,
        "catatan": catatan
    })

    return redirect("/")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        if u in users and users[u] == p:
            session["user"] = u
            return redirect("/")
        return "Login gagal"
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        users[request.form["username"]] = request.form["password"]
        return redirect("/login")
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)