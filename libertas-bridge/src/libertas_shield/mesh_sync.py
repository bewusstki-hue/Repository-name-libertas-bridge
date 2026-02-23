import time, hashlib
from datetime import datetime

class MeshSync:
    def __init__(self):
        self.node_id = str(hash(time.time()))[:8]
        self.knowledge_base = {}
        print(f"🌐 Mesh Node {self.node_id}")

    def add_knowledge(self, topic, content):
        eid = hashlib.md5(f"{topic}{content}".encode()).hexdigest()[:8]
        self.knowledge_base[eid] = {
            "topic": topic,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        print(f"🌐 Hinzugefügt: {topic}")

    def broadcast_knowledge(self):
        print(f"📡 Broadcasting {len(self.knowledge_base)} Items...")
