import sqlite3, time, json

DB = "data_actions.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_type TEXT,
                    payload TEXT,
                    created_at INTEGER
                   )""")
    conn.commit()
    conn.close()

def store_action(action_type, payload):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO actions (action_type, payload, created_at) VALUES (?,?,?)",
                (action_type, json.dumps(payload), int(time.time())))
    conn.commit()
    conn.close()
    return {"status": "stored", "action_type": action_type}

def create_task(structured):
    title = structured.get("title") or (structured.get("text","")[:80])
    payload = {"title": title, "body": structured}
    return store_action("create_task", payload)

def create_invoice(structured):
    payload = {"invoice": structured}
    return store_action("create_invoice", payload)

def create_issue(structured):
    payload = {"issue": structured}
    return store_action("create_issue", payload)

def create_note(structured):
    payload = {"note": structured}
    return store_action("create_note", payload)
