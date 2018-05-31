import os
import sys
import shutil

print("Helper script to expose local services on a public server")

# If we received an argument we assume it's the configuration file
try:
	file = sys.argv[1]
# If it was empty we prompt the user to specify one
except IndexError:
	file = input("No configuration file was provided, please specify one: ")

# Open the file containing the parameters
try:
	config = open(file, "r")
except FileNotFoundError:
	print("The file " + file + " was not found.")
	sys.exit(1)
# Default parameter values
vars = {
	"REMOTE_PORT": "",
	"REMOTE_HOST": "",
	"REMOTE_USER": os.environ['USER'],
	"DESTINY_PORT": "",
	"DESTINY_HOST": "localhost",
	"TUNNEL_NAME": "",
	"LOAD_ONBOOT": "no"
}

# Loop through every line to store the variables on a list
for line in config:
	if line[0] != "#":
		line = line.split()
		vars[line[0]] = line[1]

# We loop through every parameter and report empty ones
error = "false"
for (key, value) in vars.items():
	if value == "":
		print("The " + key + " parameter is not set")
		error = "true"
if error == "true":
	print("Fix missing parameters and try again")
	sys.exit(1)

# Use the recovered values to build the tunnel circuit, the login credentials and the final command
circuit = vars['REMOTE_PORT'] + ":" + vars['DESTINY_HOST'] + ":" + vars['DESTINY_PORT']
login = vars['REMOTE_USER'] + "@" + vars['REMOTE_HOST']
command = shutil.which("ssh") + " -NT -R " + circuit + " " + login

# We make sure that the directory for systemd units already exists
userdir = os.environ["HOME"] + "/.config/systemd/user/"
os.makedirs(userdir, exist_ok=True)
# We compose a new .unit file for the ssh tunnel
temp = open("unit.tmp", "w")
temp.write("[Unit]\n")
temp.write("Description=" + vars['TUNNEL_NAME'] + " tunnel forwarder\n")
temp.write("[Service]\n")
temp.write("ExecStart=" + command + "\n")
temp.write("[Install]\n")
temp.write("WantedBy=default.target\n")
temp.close()
# We install to the final directory and enable the unit on boot
os.rename("unit.tmp", userdir + "forward_tunnel_" + vars['TUNNEL_NAME'] + ".service")
if vars['LOAD_ONBOOT'] == 'yes':
	os.system("systemctl --user enable forward_tunnel_" + vars['TUNNEL_NAME'] + ".service")
