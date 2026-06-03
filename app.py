from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import joblib

app = Flask(__name__)
# Sayfa yönlendirmelerinde geçici hafıza (session) kullanabilmek için bir gizli anahtar tanımlıyoruz
app.secret_key = "trafik_projesi_ozel_anahtari"

# Modeli Yükle
model = joblib.load("model.pkl")

def veritabani_olustur():
    conn = sqlite3.connect('trafik.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tahminler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            saat INTEGER,
            gun INTEGER,
            hava INTEGER,
            sonuc TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Ana Sayfa (Burada veritabanındaki kayıtları çekip ekrana göndereceğiz)
@app.route('/')
def index():
    conn = sqlite3.connect('trafik.db')
    c = conn.cursor()
    # En son yapılan tahminler en üstte görünsün diye 'ORDER BY id DESC' kullanıyoruz
    c.execute("SELECT saat, gun, hava, sonuc FROM tahminler ORDER BY id DESC")
    kayitlar = c.fetchall()
    conn.close()
    
    # Yönlendirmeden gelen bir tahmin sonucu varsa alıyoruz ve hafızadan siliyoruz (Yenileme hatasını önler)
    sonuc = session.pop('sonuc', None)
    
    return render_template('index.html', tahminler=kayitlar, sonuc=sonuc)

# Tahmin İşlemi Rotaları
@app.route('/tahmin', methods=['POST'])
def tahmin_yap():
    if request.method == 'POST':
        saat = int(request.form.get('saat'))
        gun = int(request.form.get('gun'))
        hava = int(request.form.get('hava'))
        
        tahmin_sonucu = model.predict([[saat, gun, hava]])[0]
        
        # Veritabanına Kayıt
        conn = sqlite3.connect('trafik.db')
        c = conn.cursor()
        c.execute("INSERT INTO tahminler (saat, gun, hava, sonuc) VALUES (?, ?, ?, ?)", (saat, gun, hava, tahmin_sonucu))
        conn.commit()
        conn.close()
        
        # MÜKERRER KAYIT HATASININ ÇÖZÜMÜ:
        # Sonucu geçici hafızaya (session) atıp, kullanıcıyı ana sayfaya yönlendiriyoruz.
        session['sonuc'] = tahmin_sonucu
        
        return redirect(url_for('index'))

if __name__ == '__main__':
    veritabani_olustur()
    app.run(debug=True)