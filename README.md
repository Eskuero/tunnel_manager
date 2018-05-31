# Tunnel Forwarder
This tool helps setting up SystemD units to manage SSH tunnels as traffic forwarders between two servers. It was developed as a class project.

## Disclaimer
 - **Responsibility:** It's meant only for **educational** purposes. It's provided as it is, without guarantees. **Any damage** derived from the usage of the tool is entirely **user's responsibility**.
 - **License:** This code is licensed under:

    [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.txt)

## Usage
### Requirements
 - The remote server must have an OpenSSH Server with the **GatewayPorts** option to **yes** on **/etc/ssh/sshd_config**
 - The SSH authentication on the remote server must be configured with a **public key that should be passwordless** on the client. This is because SystemD units won't prompt user for input.
 - **By default the tunnels will be installed as user units** for the one executing the script so they won't run until he logs in. To allow the units **to spawn on system boot and remain after owner's logout** the root user must enable lingering through this command.
```
loginctl enable-linger <username>
```
### Parameters
Listening port on the remote server a.k.a the one Internet clients will be connecting to.
```
REMOTE_PORT 8080
```
---
Remote server from where we will tunneling the requests. It may be a FQDN or an IP address
```
REMOTE_HOST 192.168.224.4
```
---
User for login on the remote server. Defaults to the $USER executing the script
```
REMOTE_USER eskuero
```
---
Final port where the requests will be forwarded to after leaving the tunnel
```
DESTINY_PORT 80
```
---
Final server where the requests will be forwarded to after leaving the tunnel. It may be a FQDN or an IP address. Defaults to localhost
```
DESTINY_HOST localhost
```
---
Name assigned to identify the tunnel. Must be a single and unique word
```
TUNNEL_NAME nginx
```
Choose whether to enable the SystemD unit to be loaded on boot/user login or have manual activation. Defaults to no

    LOAD_ONBOOT yes
### Execution
```
python3 tunnelmanager.py <config-file>
```
As of now the configuration file is mandatory. If not provided as an argument the script will prompt for it's location. In the future the program may implement an interactive shell for tuning all the parameters.
