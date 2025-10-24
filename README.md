# Demonstração de API Management (REST + SOAP + gRPC)

Ponto de entrada único que inicia três servidores em paralelo:
- FastAPI (REST): http://localhost:8000 (versões montadas em /api/v1 e /api/v2)
- Flask (SOAP): http://localhost:8001/soap (WSDL em /wsdl)
- gRPC: 0.0.0.0:50051 (veja `grpc_server/client.py` para uso)

## Pré-requisitos

- Python instalado (recomendado 3.11+)
- Acesso a um terminal Bash (Linux)

## 1) Criar e ativar um ambiente virtual (venv)

É recomendado usar um ambiente virtual para isolar as dependências do projeto.

```bash
# criar a venv na pasta .venv
python3 -m venv .venv

# ativar a venv (Linux/Bash)
source .venv/bin/activate

# opcional: atualizar o pip dentro da venv
python -m pip install --upgrade pip
```

Para sair da venv depois, use:

```bash
deactivate
```

## 2) Instalar as dependências

Com a venv ativa, instale os pacotes listados em `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 3) Compilar os stubs gRPC (se você alterar o .proto)

Se você modificar o arquivo `grpc_server/user.proto`, gere novamente os stubs Python:

```bash
python -m grpc_tools.protoc \
  -I=grpc_server \
  --python_out=grpc_server \
  --grpc_python_out=grpc_server \
  grpc_server/user.proto
```

Observação: Os stubs (`user_pb2.py` e `user_pb2_grpc.py`) já estão versionados. Só é necessário recompilar se o `.proto` mudar.

## 4) Executar a aplicação

Com a venv ativa e as dependências instaladas, execute o ponto de entrada que sobe os três servidores:

```bash
python main.py
```

Para encerrar, pressione `Ctrl+C`. Todos os servidores serão desligados de forma limpa.

## 5) (Opcional) Testar o cliente gRPC

Com o servidor gRPC rodando, você pode testar o cliente de exemplo:

```bash
python grpc_server/client.py
```

---

## Referências rápidas

- REST (FastAPI): http://localhost:8000
  - v1: http://localhost:8000/api/v1
  - v2: http://localhost:8000/api/v2
- SOAP (Flask): http://localhost:8001/soap (WSDL em http://localhost:8001/soap/wsdl)
- gRPC: 0.0.0.0:50051
