import json
import devices
import subprocess
from pathlib import Path
priv_key = Path.home() / ".ssh" / "dassh-ed25519"
class Connect:
    def connect(self, device):
        usr = device["username"]
        ip = device["host"]
        port = device["port"]
        self.proc = subprocess.Popen(
                [
                    "ssh",
                    "-i",str(priv_key),
                    "-o","BatchMode=yes",
                    "-p",str(port),
                    f"{usr}@{ip}",
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
                )
        if self.proc.poll() is not None:
            print("Connection failed")
        return self.proc
    def run(self, cmd):

        self.proc.stdin.write(cmd + "\necho __Done__\n")
        self.proc.stdin.flush()
        output = []
        while True:
            line = self.proc.stdout.readline()
            if line.strip() == "__Done__":
                break
            output.append(line)
        return "".join(output)
    def disconnect(self):
        self.proc.stdin.write("\nexit\n")
        self.proc.stdin.flush()
        self.proc.wait()
if __name__ == "__main__":
    ct = Connect()           
    ct.connect(
        "8022",
        "u0_a245",
        "realme-c11-2021"
    )
    print(ct.run("pwd"))
    print(ct.run("whoami"))
    print(ct.run("ls"))
    ct.disconnect()

