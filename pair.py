import devices
import subprocess
from pathlib import Path

def pair(port, usr, ip):
    device = {
        "username": usr,
        "host": ip,
        "port": port
    }

    ssh_dir = Path.home() / ".ssh"
    ssh_dir.mkdir(exist_ok=True)

    priv_key = ssh_dir / "dassh-ed25519"
    pub_key = ssh_dir / "dassh-ed25519.pub"

    if pub_key.exists() and priv_key.exists():
        pass
    else:
        print("Generating Keys🔑🔑")
        keygen = subprocess.run(
            [
                "ssh-keygen",
                "-t",
                "ed25519",
                "-f",
                str(priv_key),
                "-N",
                ""
            ],
            capture_output=True,
            text=True
        )

        if keygen.returncode == 0:
            print("Keys Generated")
        else:
            print("Generation Failed")
            print(keygen.stderr)
            return

    with open(pub_key, "r") as file:
        key = file.read()

    ssh_key = subprocess.run(
        [
            "ssh",
            "-p", port,
            f"{usr}@{ip}",
            "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
        ],
        input=key,
        capture_output=True,
        text=True
    )

    if ssh_key.returncode == 0:
        ssh = subprocess.run(
            [
                "ssh",
                "-i",
                str(priv_key),
                "-o",
                "BatchMode=yes",
                "-p",
                port,
                f"{usr}@{ip}",
                "echo Paired!!"
            ],
            capture_output=True,
            text=True
        )

        if ssh.returncode == 0 and ssh.stdout.strip() == "Paired!!":
            if devices.add(device):
                print("Paired successfully.")
                return
        else:
            print("Verification Failed!!")
    else:
        print("Pairing Failed!!")
        return


if __name__ == "__main__":
    pair(
        input("Port: "),
        input("Username: "),
        input("IP: ")
    )
