from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import joblib

app = Flask(__name__)
# gecici hafiza icin gizli anahtar tanimliyoruz
app.secret_key = "trafik_projesi_ozel_anahtari"

model = joblib.load("model.pkl") #modeli yukle
#Gerekli web (Flask) ve veritabanı (SQLite) kütüphanelerini çağırır. Flask(__name__) ile sitemizi başlatırız. Sayfa yönlendirmelerinde verilerin silinmemesi (session kullanabilmek) için bir gizli anahtar belirleriz. En önemlisi joblib.load ile az önce eğittiğimiz beyni (model.pkl) sistemin içine takarız

#trafik.db olusturur ve tahminler diye bir tablo olustururuz. id,saat,gun,hava,sonuc sutunu olusturur
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

# Ana Sayfa (Burada veritabanindaki kayitlari cekip ekrana gonderecegiz)
@app.route('/')
def index():
    conn = sqlite3.connect('trafik.db')
    c = conn.cursor()
    # en son yapilan tahminler en ustte gorunsun diye order by id desc kullanıyoruz
    c.execute("SELECT saat, gun, hava, sonuc FROM tahminler ORDER BY id DESC")
    kayitlar = c.fetchall()
    conn.close()
    
    # Yönlendirmeden gelen bir tahmin sonucu varsa alıyoruz ve hafızadan siliyoruz (Yenileme hatasını önler)
    sonuc = session.pop('sonuc', None)
    
    return render_template('index.html', tahminler=kayitlar, sonuc=sonuc)

# post metoduyla /tahmin rotasina veri alir ve phyton degiskenlerine esitler(sayi olarak)
@app.route('/tahmin', methods=['POST'])
def tahmin_yap():
    if request.method == 'POST':
        saat = int(request.form.get('saat'))
        gun = int(request.form.get('gun'))
        hava = int(request.form.get('hava'))
        
        #kullanicidan alinan 3 veriyi yapay zekaya verip tahmin et deriz. sonucu da tahmin_sonucu degiskenine atariz
        tahmin_sonucu = model.predict([[saat, gun, hava]])[0]
       
        # tahmin sonucunu veritabanina kaydediyoruz
        conn = sqlite3.connect('trafik.db')
        c = conn.cursor()
        c.execute("INSERT INTO tahminler (saat, gun, hava, sonuc) VALUES (?, ?, ?, ?)", (saat, gun, hava, tahmin_sonucu))
        conn.commit()
        conn.close()
        
        # yenileyince veritabanina ayni seyi tekrar kaydetme sorunu cozumu
        # Sonucu geçici hafızaya (session) atıp, kullanıcıyı ana sayfaya yönlendiriyoruz.
        session['sonuc'] = tahmin_sonucu
        return redirect(url_for('index'))

if __name__ == '__main__':
    veritabani_olustur()
    app.run(debug=True)