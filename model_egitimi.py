import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
# confusion_matrix kütüphanesini de ekledik
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib

# 1. Veri Setini Oku
df = pd.read_csv("trafik_verisi.csv")

# 2. Girdileri (X) ve Çıktıyı (y) Ayır
X = df[["saat", "gun", "hava"]]
y = df["etiket"]

# 3. Veriyi Eğitim ve Test Olarak Böl (%80 Eğitim, %20 Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Modeli Oluştur ve Eğit
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# 5. Modelin Başarısını Test Et
tahminler = model.predict(X_test)

# --- RAPOR İÇİN PERFORMANS ÇIKTILARI (ACCURACY, HATA ORANI VE CONFUSION MATRIX) ---
basari_orani = accuracy_score(y_test, tahminler)
hata_orani = 1.0 - basari_orani

print("-" * 40)
print(f"Modelin Başarı Oranı (Accuracy): %{basari_orani * 100:.2f}")
print(f"Modelin Hata Oranı (Error Rate): %{hata_orani * 100:.2f}")
print("-" * 40)

# Karmaşıklık Matrisi (Confusion Matrix)
cm = confusion_matrix(y_test, tahminler)
print("Karmaşıklık Matrisi (Confusion Matrix):")
print(cm)
print("-" * 40)
# ----------------------------------------------------------------------------------

# 6. Eğitilmiş Modeli Kaydet
joblib.dump(model, "model.pkl")