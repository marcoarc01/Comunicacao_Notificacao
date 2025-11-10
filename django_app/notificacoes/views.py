import json
import redis
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

# Conecta ao Redis (nome do serviço no docker-compose)
redis_client = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=True)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = Notification.objects.all()
        recipient_id = self.request.query_params.get("recipient_id")
        status_ = self.request.query_params.get("status")
        recipient_type = self.request.query_params.get("recipient_type")
        priority = self.request.query_params.get("priority")

        if recipient_id:
            queryset = queryset.filter(recipient_id=recipient_id)
        if status_:
            queryset = queryset.filter(status=status_)
        if recipient_type:
            queryset = queryset.filter(recipient_type=recipient_type)
        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset

    @action(detail=False, methods=["post"], url_path="receive")
    def receive_external_notification(self, request):
        # recebe json externo e cria notificação
        data = request.data
        required = ["recipient_id", "recipient_type", "channel", "message"]
        for field in required:
            if field not in data:
                return Response(
                    {"error": f"Campo obrigatório ausente: {field}"}, status=400
                )

        notification = Notification.objects.create(
            recipient_id=data["recipient_id"],
            recipient_type=data["recipient_type"],
            channel=data["channel"],
            subject=data.get("subject", ""),
            message=data["message"],
            status="queued",
            priority=data.get("priority", "normal"),
            created_at=timezone.now(),
        )

        # Adiciona o JSON à fila Redis
        payload = {
            "id": str(notification.id),
            "recipient_id": notification.recipient_id,
            "recipient_type": notification.recipient_type,
            "channel": notification.channel,
            "message": notification.message,
            "priority": notification.priority,
        }
        redis_client.rpush("notification_queue", json.dumps(payload))
        print(f"[Fila] Notificação adicionada: {notification.id}")

        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
