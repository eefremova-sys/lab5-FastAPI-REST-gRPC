import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
PROTO_DIR = ROOT / "app" / "proto"
OUT_DIR = ROOT / "app" / "generated"
OUT_DIR.mkdir(parents=True, exist_ok=True)

cmd = [
    sys.executable, "-m", "grpc_tools.protoc",
    f"-I{PROTO_DIR}",
    f"--python_out={OUT_DIR}",
    f"--grpc_python_out={OUT_DIR}",
    str(PROTO_DIR / "glossary.proto"),
]

print("Running:", " ".join(cmd))
res = subprocess.run(cmd)
if res.returncode != 0:
    print("protoc failed", res.returncode)
    sys.exit(res.returncode)

grpc_file = OUT_DIR / "glossary_pb2_grpc.py"
if grpc_file.exists():
    txt = grpc_file.read_text(encoding="utf8")
    txt = txt.replace("import glossary_pb2 as glossary__pb2", "from . import glossary_pb2 as glossary__pb2")
    grpc_file.write_text(txt, encoding="utf8")
    print("Patched imports in", grpc_file)
print("Done. Generated to:", OUT_DIR)
