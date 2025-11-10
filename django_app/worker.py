import redis
import json
import time
from django.utils import timezone
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comunicacao.settings")
django.setup()

from notificacoes.models import Notification

# Redis client
redis_client = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=False)

def send_notification(notification):
    # Simula envio de notificação
    print(f"[Worker] Enviando via {notification.channel} para {notification.recipient_id}: {notification.message}")
    notification.status = "delivered"
    notification.sent_at = timezone.now()
    notification.save()
    print(f"[Worker] Notificação {notification.id} marcada como enviada.")

def run_worker():
    print("[Worker] Iniciando worker da fila de notificações...")
    while True:
        try:
            # Bloqueia até ter item na fila
            item = redis_client.blpop("notification_queue", timeout=5)
            if item:
                _, payload_json = item
                payload = json.loads(payload_json.decode("utf-8"))
                notification_id = payload.get("id")
                
                if not notification_id:
                    print("[Worker] Notificação sem ID recebida na fila!")
                    continue

                notification = Notification.objects.filter(id=notification_id).first()
                if not notification:
                    print(f"[Worker] Notificação {notification_id} não encontrada no banco!")
                    continue

                send_notification(notification)
        except Exception as e:
            print(f"[Worker] Erro ao processar fila: {e}")
        time.sleep(0.1)

if __name__ == "__main__":
    run_worker()