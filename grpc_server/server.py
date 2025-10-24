import grpc
from concurrent import futures
import time

from user_pb2 import UserResponse, UserList, Empty
import user_pb2_grpc

# "Banco" de usuários
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
            return UserResponse()
        return UserResponse(**user)

    def ListUsers(self, request, context):
        return UserList(users=[UserResponse(**u) for u in USERS.values()])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server running on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
