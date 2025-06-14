# 🤖 jdszr18-InsightFabrIQ

<h3>💻 Utworzenie wirtualnego środowiska, instalacja zalezności:</h3>

| **Windows**                       | **macOS**                         |
| --------------------------------- | --------------------------------- |
| Tworzenie wirtualnego środowiska  | Tworzenie wirtualnego środowiska  |
| `py -3.11 -m venv .venv`          | `python3 -m venv .venv`           |
| Aktywacja środowiska              | Aktywacja środowiska              |
| `source .venv/Scripts/activate`   | `source .venv/bin/activate`       |
| Instalacja zależności             | Instalacja zależności             |
| `pip install -r requirements.txt` | `pip install -r requirements.txt` |

---

<h3>💻 Uruchomienie aplikacji backendowej:</h3>

```
cd backend
python3 app.py
```

<h4>⦿ Przykładowe wykorzystanie endpointu</h4>

w nowym terminalu (MacOS):

```
curl -X POST http://127.0.0.1:5000/predict \
-H "Content-Type: application/json" \
-d '{"imagePath": "1532.jpg"}'
```

w nowym terminalu (Windows):

```
Invoke-WebRequest -Uri "http://127.0.0.1:5000/predict" `
  -Method POST `
  -Body '{"imagePath": "99999.jpg"}' `
  -ContentType "application/json"
```
