"""Exercise running local Django, Express, MongoDB and Flask without mocks."""
import datetime, json, os, re, sys, uuid, secrets
from pathlib import Path
import requests

base = os.environ.get("DEALERSHIP_BASE", "http://127.0.0.1:18000")
run_id = uuid.uuid4().hex[:12]
username = "smoke_" + run_id
password = secrets.token_urlsafe(24)
review_text = "Integration smoke test " + run_id + ": staff were helpful and excellent."
s = requests.Session()
checks = []
def check(label, response, predicate):
    ok = bool(predicate(response))
    checks.append({"check": label, "http_status": response.status_code, "passed": ok})
    if not ok: raise AssertionError(label + " failed: " + response.text[:400])
try:
    r=s.get(base+"/",timeout=10); check("home page",r,lambda x:x.status_code==200)
    r=s.get(base+"/dealers/",timeout=10); check("frontend entry",r,lambda x:x.status_code==200 and "<html" in x.text.lower())
    scripts=re.findall(r'<script[^>]+src="([^"]+)',r.text)
    if not scripts: raise AssertionError("frontend script not declared")
    r=s.get(base+scripts[0],timeout=10); check("frontend JavaScript asset",r,lambda x:x.status_code==200 and len(x.content)>1000)
    payload={"userName":username,"password":password,"firstName":"Demo","lastName":"Tester","email":username+"@example.invalid"}
    r=s.post(base+"/djangoapp/register",json=payload,timeout=10); check("registration",r,lambda x:x.status_code==200 and x.json().get("status")=="Authenticated")
    r=s.get(base+"/djangoapp/logout",timeout=10); check("logout",r,lambda x:x.status_code==200)
    r=s.post(base+"/djangoapp/login",json={"userName":username,"password":password},timeout=10); check("login",r,lambda x:x.status_code==200 and x.json().get("status")=="Authenticated")
    r=s.get(base+"/djangoapp/get_dealers",timeout=10); check("dealers through real Express and MongoDB",r,lambda x:x.status_code==200 and len(x.json().get("dealers",[]))>0)
    dealer=r.json()["dealers"][0]; dealer_id=dealer["id"]
    r=s.get(base+"/djangoapp/dealer/"+str(dealer_id),timeout=10); check("dealer details",r,lambda x:x.status_code==200 and len(x.json().get("dealer",[]))>0)
    review={"name":"Demo Tester","dealership":dealer_id,"review":review_text,"purchase":True,"purchase_date":"2026-11-10","car_make":"Demo","car_model":"Example","car_year":2020}
    r=s.post(base+"/djangoapp/add_review",json=review,timeout=10); check("add review through real Express and MongoDB",r,lambda x:x.status_code==200 and x.json().get("status")==200)
    r=s.get(base+"/djangoapp/reviews/dealer/"+str(dealer_id),timeout=30); check("read added review and call real Flask sentiment",r,lambda x:x.status_code==200 and any(v.get("review")==review_text and v.get("sentiment") is not None for v in x.json().get("reviews",[])))
    ok=True
except Exception as exc:
    checks.append({"check":"execution error","passed":False,"message":str(exc)}); ok=False
result={"timestamp":datetime.datetime.now().astimezone().isoformat(),"mode":"live localhost HTTP, Express, isolated MongoDB and Flask; no mocks", "mongo":os.environ.get("DEALERSHIP_MONGO_DESCRIPTION", "container local-demo-mongo, 127.0.0.1:27098, database dealership_test"), "test_user":username,"checks":checks,"passed":ok}
out=Path(__file__).resolve().parents[1]/"evidence";out.mkdir(exist_ok=True);(out/os.environ.get("DEALERSHIP_EVIDENCE_FILENAME", "live-http-2026-11-10.json")).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,indent=2));sys.exit(0 if ok else 1)
