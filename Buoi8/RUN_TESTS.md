# Cach chay test (don gian)

## 1) Chuan bi

```bash
cd Buoi8
python -m venv .venv
.venv\Scripts\activate
pip install flask sqlalchemy pytest
```

## 2) Chay app

Mo terminal 1:

```bash
cd Buoi8
.venv\Scripts\activate
python app.py
```

App chay mac dinh tai `http://127.0.0.1:5000`.

## 3) Unit test (pytest)

Mo terminal 2:

```bash
cd Buoi8
.venv\Scripts\activate
pytest -q tests/test_app.py
```

## 4) Integration test bang Newman

Cài Newman:

```bash
npm install -g newman
```

Chay collection:

```bash
cd Buoi8
newman run Library_Management_Postman_Collection.json --env-var base_url=http://127.0.0.1:5000
```

## 5) Performance test bang k6

Cài k6, sau do chay:

```bash
cd Buoi8
k6 run performance/k6-smoke.js
```

Hoac doi URL:

```bash
k6 run -e BASE_URL=http://127.0.0.1:5000 performance/k6-smoke.js
```

## 6) Performance test bang JMeter (CLI)

Cài JMeter, sau do chay:

```bash
cd Buoi8
jmeter -n -t performance/LibraryManagement.jmx -l performance/results.jtl -e -o performance/jmeter-report
```

Bao cao HTML se nam trong `performance/jmeter-report`.
