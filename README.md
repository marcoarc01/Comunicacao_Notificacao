# Projeto Arquitetura
## equipe : Marco Antonio, Igor Carvalheira, Lucas Gurgel, Pedro Filipe

## Descrição do Projeto

Este projeto implementa um sistema de recebimento de notificações utilizando **Django**, **Redis** , **Postgres** e um **worker**.  
Ele permite o envio de notificações para diferentes tipos de destinatários (como pacientes ou médicos), e o processamento é feito em segundo plano — garantindo desempenho e confiabilidade.

As notificações são marcadas automaticamente como **"delivered"** após o processamento pelo worker.

---

## Tecnologias Utilizadas

- Django
- Django REST Framework (DRF)
- Redis — fila de mensagens
- Worker Python
- PostgreSQL
- Docker & Docker Compose

---

## Como Executar o Projeto


### 1. Iniciar os containers

docker compose up --build

Isso irá iniciar:
- O container do Django (web)
- O Redis
- O PostgreSQL
- O Worker

### 2. Acessar a aplicação

- API principal: http://localhost:8000/api/notifications/
- Painel administrativo (se habilitado): http://localhost:8000/admin/

---

## Fluxo de Funcionamento

1. O cliente faz uma requisição **POST** para `/api/notifications/receive/` enviando os dados da notificação.  
2. A API cria o registro com status inicial **queued**.  
3. O **worker** consome a fila do Redis e processa a notificação.  
4. Após processar, o worker altera o status para **delivered**.  

---

## teste

### Enviar uma nova notificação

curl -X POST http://localhost:8000/api/notifications/receive/ \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_id": "paciente_002",
    "recipient_type": "patient",
    "channel": "sms",
    "message": "Sua consulta foi reagendada para sexta-feira às 15h."
  }'


Onde estiver rodando o docker compose up vai aparecer os dados do worker caso a mensagem tenha sido enviada

---

