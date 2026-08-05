import json
import subprocess
from pathlib import Path
class pair:
  def Get(self):
      print("Enter Device Info")
      self.usr = input("username: ")
      self.ip = input("IP: ")
      self.port = input("port: ")

      self.device = {
        "username":self.usr,
        "host":self.ip,
        "port":self.port
      }
      
      try:
          with open("devices.json","x") as file:
              json.dump({"devices": []}, file, indent=4)
      except FileExistsError:
          pass

      with open("devices.json","r") as file:
          self.data=json.load(file)
          self.exist = any(
            device["username"] == self.usr
            and device["host"] == self.ip
            and device["port"] == self.port
            for device in self.data["devices"]
          )
          
  
  def Exec(self):
      if self.exist:
          print("Device is already paired.")
      else:
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


          with open(pub_key,"r") as file:
              key=file.read();
          ssh_key = subprocess.run(
            [
              "ssh",
              "-p", self.port,
              f"{self.usr}@{self.ip}",
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
                  self.port,
                  f"{self.usr}@{self.ip}",
                  "echo Paired!!"
                ],
                capture_output=True,
                text=True
              )
              if ssh.returncode == 0 and ssh.stdout.strip() == "Paired!!":
                  self.data["devices"].append(self.device)
              else:
                  print("Verification Failed!!")
          else:
              print("Pairing Failed!!")
              return         
phone = pair()
phone.Get()
phone.Exec()
