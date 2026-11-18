# 🚗 Vhology — Vehicle Budget Advisor (Wizard + AI Chat)

Ek **wizard-style** Streamlit app jo aap ko budget ke andar behtareen vehicle dhoond kar
deta hai — asli photos, faide/nuqsan, modifications, **PakWheels buy link**, aur ek
**ChatGPT-powered chatbot** jo har sawal ka jawab deta hai.

## ✨ Features

- **Fast UI:** har photo card pehle **chhoti 480px image** load karta hai; agar koi
  network us size ko block kare to khud badi original image par **auto-fallback**
  (broken image ka chance zero), aur baqi images **lazy-load** hoti hain
- **Step 1 — Vehicle type select:** 14 categories (Car, Bike, Scooter, Cycle, Rickshaw,
  Van, Tractor, Boat, Helicopter, Aircraft, Jet...) bade **photo cards** ki shakal me
- **Step 2 — Budget:** slider + presets (5 Lakh → 10 Crore)
- **Step 3 — Results:** matching vehicles ki photo cards → card par click → **detail view**
  - Badi asli photo, naam, qeemat
  - ✅ **Faide (Pros)** aur ❌ **Nuqsan (Cons)**
  - 🛠️ Popular **modifications**
  - 🛒 **Buy on PakWheels** button + **[ MORE PLATFORMS ]** row: OLX Pakistan,
    CarDekho, Google Prices aur Images — har vehicle ke liye live links
- **💬 V-Bot AI Chat — corner dock (bottom-right):** ek hi chatbot, page ke kony me fixed
  panel — ChatGPT (`gpt-4o-mini`) dataset context ke sath juda hua hai, **har topic par
  baat karta hai** (vehicles bhi, studies/jokes/general bhi) aur **sara jawab ENGLISH me**
  deta hai. Status header dikhata hai 🟢 ChatGPT ON / 🟡 Fallback mode, quick-question
  chips aur 🗑 clear button ke sath
- **Zero-error fallback:** ChatGPT key na ho ya API fail ho to bhi built-in rule engine
  se **har haal me English jawab** milta hai — zero errors
- **ML (Kaggle-trained):**
  - `train_vehicle_model.ipynb` — Kaggle par chala kar `model.joblib` banayein
  - Random Forest **price estimate** + KNN **similar vehicles** detail view me
  - Agar `model.joblib` repo me na ho to app CSV se khud train kar legi
- **10,126 vehicles** ka dataset — cycle se le kar helicopter/private jets tak:
  Toyota, Suzuki, Honda, KIA, Hyundai, MG, Changan, Haval, BYD, Chery, Omoda, Ora,
  Jaecoo, Jetour, Deepal, Audi, BMW, Mercedes-Benz, Tesla, bikes (Honda/Yamaha/Suzuki/
  Road Prince/United), e-bikes, cycles, rickshaws, boats, helicopters, aircraft aur
  private jets — har model ke trims × saal (used) variants ke sath

## 🔑 ChatGPT connect karne ka tareeqa (optional)

App ChatGPT ke **bina bhi 100% chalti hai** (fallback engine). ChatGPT on karne ke liye:

1. [platform.openai.com](https://platform.openai.com) se API key lein
2. Repo me local `secrets.toml` banayein: `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```
   (ya Streamlit Cloud → app settings → **Secrets** me wahi line paste karein)
3. Deploy — chat ab real ChatGPT se jawab dega

## 📁 Files

```
app.py                      wizard app (3 steps + detail view + ML insights + V-Bot corner chat)
ai.py                       ChatGPT integration + zero-error English fallback engine (corner dock)
ml.py                       RF price model + KNN + helpers (money, split_list)
images.py                   real vehicle photos + fast 480px pair helper
vehicles.csv                dataset — 10,126 vehicles, 14 categories
train_vehicle_model.ipynb   Kaggle notebook — model.joblib banata hai
requirements.txt            deployment packages
```

## 🚀 Deploy (Streamlit Cloud)

1. Is `vehicle` folder ke files GitHub par ek **naye repo** me push karein
2. [share.streamlit.io](https://share.streamlit.io) → New app → repo select karein
3. **Main file path:** `app.py` → Deploy
4. (Optional) App **Settings → Secrets** me `OPENAI_API_KEY = "sk-..."` add karein

> **Note:** photos Wikimedia Commons se hotlink hain (stable URLs) — repo halka rehta
> hai. Prices approximate hain; exact rate ke liye har card par **Buy on PakWheels**
> button ya [ MORE PLATFORMS ] links use karein.

## 🧠 Model workflow

1. `vehicles.csv` ko Kaggle par upload karein (dataset bana kar notebook me attach karein)
2. `train_vehicle_model.ipynb` → Run All → `model.joblib` download karein
3. Us file ko repo me add karein — app automatic best model use kare gi
