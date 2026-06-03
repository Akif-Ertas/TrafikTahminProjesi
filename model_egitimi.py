import pandas as pd 
from sklearn.tree import DecisionTreeClassifier #karar agaci (decision tree) 
from sklearn.model_selection import train_test_split #egitim ve test olarak boler
from sklearn.metrics import accuracy_score, confusion_matrix #makine ogrenmesi (hata orani hesaplama)
import joblib #egittigimiz modeli kaydetmek icin kullaniyoruz.

# trafik_verisini okur
df = pd.read_csv("trafik_verisi.csv")

# girdileri ayirir
X = df[["saat", "gun", "hava"]]
y = df["etiket"]

# egitim ve test verisi olarak boluyoruz(1500 satirlik verinin 8/10u egitim icin 2/10unu test icin veriyoruz)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# hangi sartlarda trafik ne oluyor makine onu ogreniyor
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# test verisi ile tahmin yapiyoruz
tahminler = model.predict(X_test)

# yapilan tahminin hata oranini hesapliyoruz
basari_orani = accuracy_score(y_test, tahminler)
hata_orani = 1.0 - basari_orani

print("-" * 40)
print(f"Modelin Başarı Oranı (Accuracy): %{basari_orani * 100:.2f}")
print(f"Modelin Hata Oranı (Error Rate): %{hata_orani * 100:.2f}")
print("-" * 40)

# karmasiklik matrisini hesaplayarak modelin hangi durumlarda ne kadar dogru tahmin yaptigini gosteriyoruz
cm = confusion_matrix(y_test, tahminler)
print("Karmaşıklık Matrisi (Confusion Matrix):")
print(cm)
print("-" * 40)

# her seferinde bastan egitmemek icin model.pkl dosyasina kaydediyoruz
joblib.dump(model, "model.pkl")