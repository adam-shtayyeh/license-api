Python License API

1. Install requirements:
   pip install -r requirements.txt

2. Create database:
   python create_db.py

3. Add an ID:
   python add_id.py

4. Run API:
   python app.py

Endpoint:
POST http://127.0.0.1:5000/check-id

JSON body:
{
  "id": "123456789"
}

Response if found:
{
  "success": true
}

Response if not found:
{
  "success": false
}
