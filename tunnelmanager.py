import os

print("Helper script to expose local services on a public server")

# Open the file containing the parameters
config = open("config", "r")
vars = {}

# Loop through every line to store the variables on a list
for line in config:
    if line[0] != "#":
        line = line.split()
        vars[line[0]] = line[1]

# Use the recovered values to build the tunnel circuit, the login credentials and the final command
circuit = vars['REMOTE_PORT'] + ":" + vars['DESTINY_HOST'] + ":" + vars['DESTINY_PORT']
login = vars['REMOTE_USER'] + "@" + vars['REMOTE_HOST']
command = "ssh -fNT -R " + circuit + " " + login
# Setup the SSH tunnel
os.system(command)
