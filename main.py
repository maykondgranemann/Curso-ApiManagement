from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from v1.users import app as app_v1
from v2.users import app as app_v2

# Criação da aplicação principal (FastAPI - REST)
app = FastAPI(
    title="User API - Multi Version Demo",
    description="Demonstração prática de versionamento RESTful com FastAPI",
    version="2.0"
)

# Montagem das versões
app.mount("/api/v1", app_v1)
app.mount("/api/v2", app_v2)


# CORS (opcional – restrinja se preferir)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ex.: ["https://localhost:9443"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Healthcheck simples
@app.get("/healthz")
def healthz():
    return {"status": "ok"}


# --- Inicialização unificada (REST + SOAP + gRPC) ---
def _start_fastapi():
    """Inicia o servidor FastAPI (Uvicorn) na porta 8000."""
    import uvicorn

    config = uvicorn.Config(app, host="0.0.0.0", port=8080, log_level="info")
    server = uvicorn.Server(config)
    server.run()


def _start_flask_soap():
    """Inicia o servidor Flask (SOAP) na porta 8001."""
    from soap_server import app as flask_app

    # Evita problemas de sinal/reloader ao rodar em thread
    flask_app.run(host="0.0.0.0", port=8081, use_reloader=False)


def _start_grpc():
    """Cria e inicia o servidor gRPC na porta 50051 e retorna a instância."""
    import grpc
    from concurrent import futures
    from grpc_server import user_pb2_grpc, user_pb2

    # "Banco" de usuários (mantém compatível com a implementação atual)
    USERS = {
        1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
        2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
    }

    class UserService(user_pb2_grpc.UserServiceServicer):
        def GetUser(self, request, context):
            user = USERS.get(request.id)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.UserResponse()
            return user_pb2.UserResponse(**user)

        def ListUsers(self, request, context):
            return user_pb2.UserList(
                users=[user_pb2.UserResponse(**u) for u in USERS.values()]
            )

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server running on port 50051")
    return server


if __name__ == "__main__":
    # Sobe os 3 serviços em paralelo na mesma execução
    from threading import Thread

    grpc_server = _start_grpc()

    Thread(target=_start_flask_soap, daemon=True).start()
    Thread(target=_start_fastapi, daemon=True).start()

    try:
        # Mantém o processo vivo e permite Ctrl+C encerrar tudo
        grpc_server.wait_for_termination()
    except KeyboardInterrupt:
        grpc_server.stop(0)