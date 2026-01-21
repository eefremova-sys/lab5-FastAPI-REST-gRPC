import grpc

try:
    from app.generated import glossary_pb2 as pb
    from app.generated import glossary_pb2_grpc as pb_grpc
except ImportError:
    import sys
    import os
    root_dir = os.path.join(os.path.dirname(__file__), '../..')
    root_dir = os.path.abspath(root_dir)
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    from app.generated import glossary_pb2 as pb
    from app.generated import glossary_pb2_grpc as pb_grpc


def run(address="localhost:50051"):
    channel = grpc.insecure_channel(address)
    stub = pb_grpc.GlossaryServiceStub(channel)


    print("\n=== 1. Получить все записи ===")
    try:
        resp = stub.AllEntries(pb.GetAllRequest())
        for key, entry in resp.entries.items():
            print(f"{key}: {entry.name} — {entry.description}")
            if entry.reference:
                print(f"  Ссылка: {entry.reference}")
    except grpc.RpcError as e:
        print("ERROR:", e.code(), e.details())


    print("\n=== 2. Получить одну запись (vulnerability) ===")
    try:
        r = stub.GetEntry(pb.GetEntryRequest(key="vulnerability"))
        print("Найдена запись:", r.entry.name)
        print("Описание:", r.entry.description)
        if r.entry.reference:
            print("Ссылка:", r.entry.reference)
    except grpc.RpcError as e:
        print("ERROR:", e.code(), e.details())


    print("\n=== 3. Создать новую запись ===")
    try:
        entry = pb.Entry(
            name="new_notes",
            description="Описание нового метода",
            reference="https://example.com"
        )
        created = stub.PostEntry(
            pb.PostEntryRequest(key="new_notes", entry=entry)
        )
        print("Создана запись:", created.entry.name)
        print("Описание:", created.entry.description)
    except grpc.RpcError as e:
        print("ERROR:", e.code(), e.details())


    print("\n=== 4. Обновить запись ===")
    try:
        updated = stub.ModifyEntry(
            pb.ModifyEntryRequest(
                key="new_notes",
                description="Новое обновлённое описание"
            )
        )
        print("Обновлена запись:", updated.entry.name)
        print("Новое описание:", updated.entry.description)
    except grpc.RpcError as e:
        print("ERROR:", e.code(), e.details())


    print("\n=== 5. Удалить запись ===")
    try:
        deleted = stub.DeleteEntry(pb.DeleteEntryRequest(key="new_notes"))
        print("Удалена запись:", deleted.entry.name)
    except grpc.RpcError as e:
        print("ERROR:", e.code(), e.details())


if __name__ == "__main__":
    run()
