import grpc
from user_pb2 import UserRequest, Empty
import user_pb2_grpc

def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = user_pb2_grpc.UserServiceStub(channel)

    # Listar todos
    response = stub.ListUsers(Empty())
    print("Users:", response.users)

    # Buscar usuário por ID
    try:
        user = stub.GetUser(UserRequest(id=1))
        print("User 1:", user)
    except grpc.RpcError as e:
        print(f"Erro: {e.code()} - {e.details()}")

if __name__ == "__main__":
    run()
