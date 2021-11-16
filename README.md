usage: pochelper [-h] [--config CONFIG] [--cmd CMD] [-o filename]
                 [-i filename]
                 hosts [hosts ...]

Run an ansible playbook on POC devices.

positional arguments:
  hosts                 which devices to configure or command

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       send a configuration to the device in set format
  --cmd CMD, --command CMD
                        send a configuration to the device in set format
  -o filename, --out filename
                        write output to a file
  -i filename, --inventory filename
                        Name of inventory file


The pochelper script allows you to run a command or apply a configuration across multiple devices at the same time.
As long as your devices are SSH reachable and have the IPs in the inventory file, it should run through. This assumes
all of your lab devices have the same login information, such as jnpr/Juniper1.

To modify for your POC:
- edit inventory file
    - change device login (ansible_user + ansible_password)
    - add device 'categories' like the example ones: srx, nfx, qfx, etc
    - replace ssh IPs with your own
- if needed, use the virtual environment for python
    - `source venv/bin/activate`
- run the script!

Examples:
- `./pochelper nfx --cmd "show version"`
- `./pochelper nfx --configure "set interfaces ge-0/0/0.0 family inet address 1.1.1.1" -o output_file.txt`

This project was made with the help of Erik Sherk (sherk@juniper.net) and used in conjuction with a large customer POC.
It was especially useful for configuring IKE + IPSEC on all of the SRX devices.
