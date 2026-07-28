import subprocess
import json
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
          with open(r"C:\Users\prana\.ssh\id_ed25519.pub","r") as file:
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
                  with open("devices.json", "w") as file:
                      json.dump(self.data, file, indent=4)
                      print(self.data)
              else:
                  print("Verification Failed!!")
          else:
              print("Pairing Failed!!")
              return         
phone = pair()
phone.Get()
phone.Exec()