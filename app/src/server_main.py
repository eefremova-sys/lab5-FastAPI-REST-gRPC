import logging
from concurrent import futures
import grpc

try:
    from app.generated import glossary_pb2 as pb
    from app.generated import glossary_pb2_grpc as pb_grpc
    from app.src.glossary import glossary
    from app.src.models import Entry as EntryModel
except ImportError:
    import sys
    import os
    root_dir = os.path.join(os.path.dirname(__file__), '../..')
    root_dir = os.path.abspath(root_dir)
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    from app.generated import glossary_pb2 as pb
    from app.generated import glossary_pb2_grpc as pb_grpc
    from app.src.glossary import glossary
    from app.src.models import Entry as EntryModel

class GlossaryService(pb_grpc.GlossaryServiceServicer):
    def __init__(self):
        self._store = glossary

    def AllEntries(self, request, context):
        entries_map = {}

        for key, entry in self._store.items():
            entries_map[key] = pb.Entry(
                name=entry.name,
                description=entry.description,
                reference=entry.reference or ""
            )
            
        return pb.GetAllResponse(entries=entries_map)


    def GetEntry(self, request, context):
        key = request.key

        if key not in self._store:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"'{key}' не обнаружен в базе")
            return pb.EntryResponse()

        e = self._store[key]

        return pb.EntryResponse(
            entry=pb.Entry(name=e.name, 
            description=e.description, 
            reference=e.reference or "")
        )


    def PostEntry(self, request, context):
        key = request.key

        if key in self._store:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(f"'{key}' уже есть в словаре")
            return pb.EntryResponse()

        t = EntryModel(
            name=request.entry.name, 
            description=request.entry.description, 
            reference=request.entry.reference or None
        )
        self._store[key] = t

        return pb.EntryResponse(
            entry=pb.Entry(name=t.name, 
            description=t.description, 
            reference=t.reference or "")
        )


    def ModifyEntry(self, request, context):
        key = request.key

        if key not in self._store:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"'{key}' не обнаружен в базе")
            return pb.EntryResponse()

        entry = self._store[key]

        if request.HasField('description'):
            entry.description = request.description
        if request.HasField('reference'):
            entry.reference = request.reference
        self._store[key] = entry

        return pb.EntryResponse(
            entry=pb.Entry( name=entry.name, 
            description=entry.description, 
            reference=entry.reference or "")
        )


    def DeleteEntry(self, request, context):
        key = request.key

        if key not in self._store:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"'{key}' не обнаружен в базе")
            return pb.EntryResponse()

        removed = self._store.pop(key)

        return pb.EntryResponse(
            entry=pb.Entry( name=removed.name, 
            description=removed.description, 
            reference=removed.reference or "")
        )


def serve(host="0.0.0.0", port=50051):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    pb_grpc.add_GlossaryServiceServicer_to_server(GlossaryService(), server)
    
    addr = f"{host}:{port}"
    server.add_insecure_port(addr)
    server.start()
    print(f"gRPC Glossary server listening at {addr}")
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
