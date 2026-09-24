from datetime import date,timedelta

def setup(client,h):
    c=client.post("/api/clients",headers=h,json={"name":"Ana","phone":"11999999999","email":"ana@example.com","active":True}).json()
    s=client.post("/api/services",headers=h,json={"name":"Consulta","description":"Avaliação","duration_minutes":60,"price":120,"active":True}).json()
    p=client.post("/api/professionals",headers=h,json={"name":"Dra. Lia","phone":None,"email":"lia@example.com","notes":None,"active":True,"service_ids":[s["id"]]}).json()
    day=date.today()+timedelta(days=(7-date.today().weekday())%7 or 7)
    hours=[{"weekday":i,"start_time":"08:00","end_time":"18:00","active":i<5} for i in range(7)]
    hours[day.weekday()]["active"]=True
    assert client.put("/api/business-hours",headers=h,json=hours).status_code==200
    return c,s,p,day

def test_register_login_and_crud(client,auth):
    assert client.post("/api/auth/login",json={"email":"teste@example.com","password":"Senha123!"}).status_code==200
    c,s,p,_=setup(client,auth)
    assert c["name"]=="Ana" and s["duration_minutes"]==60 and p["services"][0]["id"]==s["id"]
    assert client.delete(f"/api/clients/{c['id']}",headers=auth).status_code==204

def test_appointment_conflict_status_and_reports(client,auth):
    c,s,p,day=setup(client,auth); payload={"client_id":c["id"],"service_id":s["id"],"professional_id":p["id"],"date":str(day),"start_time":"10:00","price":None,"notes":None}
    made=client.post("/api/appointments",headers=auth,json=payload); assert made.status_code==201 and made.json()["end_time"].startswith("11:00")
    assert client.post("/api/appointments",headers=auth,json={**payload,"start_time":"10:30"}).status_code==409
    item=made.json(); assert client.patch(f"/api/appointments/{item['id']}/status",headers=auth,json={"status":"confirmed"}).status_code==200
    assert client.patch(f"/api/appointments/{item['id']}/status",headers=auth,json={"status":"completed"}).status_code==200
    assert client.get(f"/api/reports/appointments?start={day}&end={day}",headers=auth).json()["completed"]==1
    assert client.get("/api/dashboard",headers=auth).status_code==200

def test_outside_hours_and_block(client,auth):
    c,s,p,day=setup(client,auth); base={"client_id":c["id"],"service_id":s["id"],"professional_id":p["id"],"date":str(day),"price":120,"notes":None}
    assert client.post("/api/appointments",headers=auth,json={**base,"start_time":"19:00"}).status_code==409
    assert client.post("/api/blocked-times",headers=auth,json={"professional_id":p["id"],"date":str(day),"start_time":"12:00","end_time":"13:00","reason":"Almoço"}).status_code==201
    assert client.post("/api/appointments",headers=auth,json={**base,"start_time":"12:15"}).status_code==409
