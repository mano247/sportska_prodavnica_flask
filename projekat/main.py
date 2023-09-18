import flask
from flask import Flask
from flaskext.mysql import MySQL
import pymysql

app=Flask(__name__, static_url_path="/")
mysql=MySQL(app, cursorclass=pymysql.cursors.DictCursor)

app.config["MYSQL_DATABASE_USER"]="root"
app.config["MYSQL_DATABASE_PASSWORD"]="root"
app.config["MYSQL_DATABASE_DB"]="sportska_prodavnica"

app.secret_key = "98134fby1k34flSDDOLfbPG0Q58RGQNVpuifbc"

@app.route("/api/proizvodi")
def get_proizvodi():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM proizvod LEFT JOIN brend ON brend.id=brend_id LEFT JOIN pol ON pol.id=pol_id LEFT JOIN kategorija ON kategorija.id=kategorija_id")
    proizvodi = cursor.fetchall()
    return flask.jsonify(proizvodi), 201

@app.route("/api/proizvodi/<int:id>")
def get_proizvod(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM proizvod WHERE id=%s", (id, ))
    proizvod = cursor.fetchone()
    return flask.jsonify(proizvod), 201

@app.route("/api/proizvodi", methods=["POST"])
def add_proizvod():
    db = mysql.get_db()
    cursor = db.cursor()
    proizvod = flask.request.json
    cursor.execute("INSERT INTO proizvod (sifra, naziv, brend_id, pol_id, kategorija_id, opis, cena) VALUES (%(sifra)s, %(naziv)s, %(brend_id)s, %(pol_id)s, %(kategorija_id)s, %(opis)s, %(cena)s)", proizvod)
    db.commit()
    return flask.jsonify(proizvod), 201

@app.route("/api/proizvodi/<int:id>", methods=["DELETE"])
def delete_proizvod(id):
    db = mysql.get_db()
    cursor = db.cursor()
    obrisani = cursor.execute("DELETE FROM proizvod WHERE id=%s", (id, ))
    db.commit()
    if obrisani == 0:
        return flask.jsonify(None), 404
    return flask.jsonify(None), 201

@app.route("/api/proizvod/<int:id>", methods=["PUT"])
def logicko_brisanje_proizvoda(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE proizvod SET dostupnost=0 WHERE id=%s", (id, ))
    db.commit()
    return flask.jsonify(None), 201

@app.route("/api/proizvodi/<int:id>", methods=["PUT"])
def edit_proizvod(id):
    db = mysql.get_db()
    cursor = db.cursor()
    proizvod = dict(flask.request.json)
    proizvod["id"]=id
    izmenjeni = cursor.execute("UPDATE proizvod SET sifra=%(sifra)s, naziv=%(naziv)s, brend_id=%(brend_id)s, pol_id=%(pol_id)s, kategorija_id=%(kategorija_id)s, opis=%(opis)s, cena = %(cena)s, dostupnost = %(dostupnost)s WHERE id=%(id)s", proizvod)
    db.commit()
    if izmenjeni == 0:
        return flask.jsonify(None), 404
    return flask.jsonify(proizvod), 201

@app.route("/api/korisnici")
def get_korisnici():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM korisnik LEFT JOIN dodeljeno_pravo ON korisnik.id=dodeljeno_pravo.korisnik_id LEFT JOIN pravo_pristupa ON dodeljeno_pravo.pravo_pristupa_id=pravo_pristupa.id")
    korisnici = cursor.fetchall()
    return flask.jsonify(korisnici), 201

@app.route("/api/korisnici/<int:id>")
def get_korisnik(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM korisnik WHERE id=%s", (id, ))
    korisnik = cursor.fetchone()
    return flask.jsonify(korisnik), 201

@app.route("/api/korisnici", methods=["POST"])
def add_korisnik():
    db = mysql.get_db()
    cursor = db.cursor()
    korisnik = flask.request.json
    cursor.execute("INSERT INTO korisnik (ime, prezime, email, adresa, brojTelefona, korisnickoIme, lozinka) VALUES (%(ime)s, %(prezime)s, %(email)s, %(adresa)s, %(brojTelefona)s, %(korisnickoIme)s, %(lozinka)s)", korisnik)
    db.commit()
    id_dodatog_korisnika = cursor.lastrowid
    pravo_pristupa_id = korisnik.get('pravo_pristupa_id')
    cursor.execute("INSERT INTO dodeljeno_pravo (korisnik_id, pravo_pristupa_id) VALUES (%s, %s)", (id_dodatog_korisnika, pravo_pristupa_id))
    db.commit()
    return flask.jsonify(korisnik), 201

@app.route("/api/korisnici/<int:id>", methods=["DELETE"])
def delete_korisnik(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM dodeljeno_pravo WHERE korisnik_id=%s", (id, ))
    cursor.execute("DELETE FROM kupovina WHERE korisnik_id=%s", (id, ))
    obrisani_korisnik = cursor.execute("DELETE FROM korisnik WHERE id=%s", (id, ))
    db.commit()
    if obrisani_korisnik == 0:
        return flask.jsonify(None), 404
    return flask.jsonify(None), 201

@app.route("/api/korisnici/<int:id>", methods=["PUT"])
def edit_korisnik(id):
    db = mysql.get_db()
    cursor = db.cursor()
    korisnik = dict(flask.request.json)
    korisnik["id"]=id
    izmenjeni = cursor.execute("UPDATE korisnik SET ime=%(ime)s, prezime=%(prezime)s, email=%(email)s, adresa=%(adresa)s, brojTelefona=%(brojTelefona)s, korisnickoIme=%(korisnickoIme)s, lozinka = %(lozinka)s WHERE id=%(id)s", korisnik)
    db.commit()
    if izmenjeni == 0:
        return flask.jsonify(None), 404
    return flask.jsonify(korisnik), 201

@app.route("/api/kupovine")
def get_kupovine():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM kupovina LEFT JOIN korisnik ON korisnik_id=korisnik.id LEFT JOIN proizvod ON proizvod_id=proizvod.id")
    kupovine = cursor.fetchall()
    return flask.jsonify(kupovine), 201

@app.route("/api/kupovine/<int:id>")
def get_kupovina(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM kupovina WHERE id=%s", (id, ))
    kupovina = cursor.fetchone()
    return flask.jsonify(kupovina), 201

@app.route("/api/kupovine/<int:id>", methods=["DELETE"])
def delete_kupovina(id):
    db = mysql.get_db()
    cursor = db.cursor()
    izbrisan = cursor.execute("DELETE FROM kupovina WHERE id=%s", (id, ))
    db.commit()
    if izbrisan == 0:
        return flask.jsonify(None), 404
    return flask.jsonify(None), 201

@app.route("/api/kupovine", methods=["POST"])
def add_kupovina():
    db = mysql.get_db()
    cursor = db.cursor()
    kupovina = flask.request.json
    cursor.execute("INSERT INTO kupovina (korisnik_id, proizvod_id, cena, datum, vreme, kolicina) VALUES (%(korisnik_id)s, %(proizvod_id)s, %(cena)s, %(datum)s, %(vreme)s, %(kolicina)s)", kupovina)
    db.commit()
    return flask.jsonify(kupovina), 201

@app.route("/api/kupovine/<int:id>", methods=["PUT"])
def edit_kupovina(id):
    db = mysql.get_db()
    cursor = db.cursor()
    kupovina = dict(flask.request.json)
    kupovina["id"]=id
    izmenjen = cursor.execute("UPDATE kupovina SET korisnik_id=%(korisnik_id)s, proizvod_id=%(proizvod_id)s, cena=%(cena)s, datum=%(datum)s, vreme=%(vreme)s, kolicina=%(kolicina)s WHERE id=%(id)s", kupovina)
    db.commit()
    if izmenjen == 0:
        return flask.jsonify(None), 404
    return flask.jsonify(izmenjen), 201

@app.route("/api/prava")
def get_prava():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pravo_pristupa")
    prava = cursor.fetchall()
    return flask.jsonify(prava), 201

@app.route("/api/polovi")
def get_polovi():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pol")
    polovi = cursor.fetchall()
    return flask.jsonify(polovi), 201

@app.route("/api/kategorije")
def get_kategorije():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM kategorija")
    kategorije = cursor.fetchall()
    return flask.jsonify(kategorije), 201

@app.route("/api/brendovi")
def get_brendovi():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM brend")
    brendovi = cursor.fetchall()
    return flask.jsonify(brendovi), 201

@app.route("/api/dostupni_proizvodi")
def get_dostupni_proizvodi():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM proizvod LEFT JOIN brend ON brend.id=brend_id LEFT JOIN pol ON pol.id=pol_id LEFT JOIN kategorija ON kategorija.id=kategorija_id WHERE dostupnost=1")
    dostupni = cursor.fetchall()
    return flask.jsonify(dostupni), 201

@app.route("/login")
def login():
    return flask.render_template("login.tpl.html")

@app.route("/registracija")
def registracija():
    return flask.render_template("registracija.tpl.html")

@app.route("/admin")
def admin_stranica():
    korisnik = flask.session.get("korisnik")
    if korisnik is not None and korisnik.get("pravo") == "admin":
        return flask.redirect("/admin.html")
    else:
        return flask.redirect("/")
    
@app.route("/")
def home():
    return app.send_static_file("prodavnica.html")

@app.route("/login", methods=["POST"])
def login_session():
    korisnicko_ime = flask.request.form.get("korisnickoIme")
    lozinka = flask.request.form.get("lozinka")
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM korisnik LEFT JOIN dodeljeno_pravo ON korisnik.id=dodeljeno_pravo.korisnik_id LEFT JOIN pravo_pristupa ON dodeljeno_pravo.pravo_pristupa_id=pravo_pristupa.id WHERE korisnickoIme = %s AND lozinka = %s", (korisnicko_ime, lozinka))
    korisnik = cursor.fetchone()
    if korisnik is not None: 
        flask.session["korisnik"] = {
            "ime": korisnik["ime"],
            "prezime": korisnik["prezime"],
            "pravo": korisnik["naziv"],
            "id": korisnik["id"]
        }
        return flask.redirect("/")
    else:
        return flask.render_template("login.tpl.html", error_message="Neuspesna prijava! Pokusajte ponovo.")  
    
@app.route("/api/session_podaci", methods=["GET"])
def get_session_podaci():
    if "korisnik" in flask.session:
        korisnik = flask.session["korisnik"]
        return flask.jsonify(korisnik)
    else:
        return flask.jsonify({})

@app.route("/logout")
def logout():
    flask.session.clear()
    return flask.redirect("/")

@app.route("/profil")
def profil():
    return flask.redirect("profil.html")

@app.route("/moje_kupovine")
def moje_kupovine():
    db = mysql.get_db()
    cursor = db.cursor()
    korisnik = flask.session.get("korisnik")
    korisnikov_id = korisnik.get("id")
    cursor.execute("SELECT * FROM kupovina LEFT JOIN korisnik ON korisnik.id=kupovina.korisnik_id LEFT JOIN proizvod ON proizvod.id=kupovina.proizvod_id WHERE kupovina.korisnik_id=%s", (korisnikov_id, ))
    sve_kupovine = cursor.fetchall()
    return flask.render_template("kupovine.tpl.html", sve_kupovine=sve_kupovine)


if __name__ == "__main__":
    app.run()