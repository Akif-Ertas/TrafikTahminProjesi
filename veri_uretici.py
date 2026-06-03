import pandas as pd
import random

veri = []
# Rastgelelik için olası durumları tanımladık
olasi_durumlar = ["dusuk", "orta", "yuksek"]

for _ in range(1500):
    saat = random.randint(0, 23)
    gun = random.randint(1, 7) 
    hava = random.randint(0, 7) 

    # --- GERÇEKÇİLİK (GÜRÜLTÜ) FAKTÖRÜ ---
    # %15 ihtimalle kuralları ezip, kaza veya yol çalışması olmuş gibi rastgele bir sonuç ata
    if random.random() < 0.15:
        etiket = random.choice(olasi_durumlar)
    
    # Kalan %85'lik kısımda bizim normal mantıksal kurallarımız işlesin
    else:
        if gun in [1, 2, 3, 4, 5]:
            if saat in [7, 8, 9, 17, 18, 19]:
                etiket = "yuksek"
            elif saat in [23, 0, 1, 2, 3, 4, 5]:
                etiket = "dusuk"
            else:
                etiket = "orta" if hava in [0, 3, 4] else "yuksek"
                
        else:
            if saat in [12, 13, 14, 15, 16]:
                etiket = "orta" if hava in [0, 3, 4] else "yuksek"
            else:
                etiket = "dusuk"

        if hava in [5, 6, 7] and etiket == "dusuk":
            etiket = "orta"
            
        if hava == 7 and saat in [7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19]:
            etiket = "yuksek"

    veri.append([saat, gun, hava, etiket])

df = pd.DataFrame(veri, columns=["saat", "gun", "hava", "etiket"])
df.to_csv("trafik_verisi.csv", index=False)

print("Sürpriz faktörlü (gerçekçi) 1500 satırlık trafik_verisi.csv başarıyla güncellendi.")