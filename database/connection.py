import mysql.connector
import threading

SERVER_CONFIG = {
    "south": {
        "primary": {
            "host": "localhost",
            "database": "csdlpt_hcm_master",
            "user": "root",
            "password": "101205"
        },
        "replica": {
            "host": "localhost",
            "database": "csdlpt_hcm_replica",
            "user": "root",
            "password": "101205"
        },
        "label": "Miền Nam (TP.HCM)"
    },
    "north": {
        "primary": {
            "host": "localhost",
            "database": "csdlpt_hn_master",
            "user": "root",
            "password": "101205"
        },
        "replica": {
            "host": "localhost",
            "database": "csdlpt_hn_replica",
            "user": "root",
            "password": "101205"
        },
        "label": "Miền Bắc (Hà Nội)"
    }
}

_server_status = {
    "south_primary": True,
    "south_replica": True,
    "north_primary": True,
    "north_replica": True,
}
_lock = threading.Lock()


def get_server_status():
    with _lock:
        return dict(_server_status)
    
def set_server_status(key, value):   
    with _lock:
        _server_status[key] = value

def create_connection(config):
    return mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )


class DBConnection:
    def __init__(self, conn, label, readonly, failover):
        self.conn = conn
        self.label = label
        self.server_label = label  # 🔥 FIX LUÔN
        self.is_readonly = readonly
        self.is_failover = failover

    def execute(self, sql, params=()):
        if self.is_readonly and not sql.strip().upper().startswith("SELECT"):
            raise PermissionError("⚠️ Replica chỉ cho phép READ")

        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(sql, params)
        return cursor

    def fetchall(self, sql, params=()):
        return self.execute(sql, params).fetchall()

    def fetchone(self, sql, params=()):
        return self.execute(sql, params).fetchone()

    def commit(self):
        if not self.is_readonly:
            self.conn.commit()


def _get_raw_connection(config):
    """Trả về connection raw (dùng cho admin/replication)."""
    return mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )


def get_connection(region):
    region = region.lower()
    cfg = SERVER_CONFIG[region]

    status = get_server_status()

    if status.get(f"{region}_primary", True):
        conn = create_connection(cfg["primary"])
        return DBConnection(conn, f"🟢 {cfg['label']} - Primary", False, False)

    elif status.get(f"{region}_replica", True):
        conn = create_connection(cfg["replica"])
        return DBConnection(conn, f"🟡 {cfg['label']} - Replica", True, True)

    else:
        raise ConnectionError("❌ Cả server đều sập")
    

def replicate_all():
    try:
        # copy từ HCM master → HCM replica
        master = create_connection(SERVER_CONFIG["south"]["primary"])
        replica = create_connection(SERVER_CONFIG["south"]["replica"])

        m_cur = master.cursor(dictionary=True)
        r_cur = replica.cursor()

        # ví dụ replicate bảng rides
        m_cur.execute("SELECT * FROM rides")
        rows = m_cur.fetchall()

        r_cur.execute("DELETE FROM rides")

        for row in rows:
            r_cur.execute(
                """INSERT INTO rides (
                    ride_id,user_id,driver_id,
                    pickup_location,dropoff_location,city,
                    status,created_at,code,distance_km,duration_min,
                    fare,vehicle,payment,user_rating,cancel_reason,
                    region,ride_date,ride_time
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                tuple(row.values())
            )

        replica.commit()

        m_cur.close()
        r_cur.close()
        master.close()
        replica.close()

        return True

    except Exception as e:
        print("Replication error:", e)
        return False