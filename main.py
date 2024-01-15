#This script extracts router hostname/IP information from a CSV file and creates IP SLA UDP-Jitter configurations for a full mesh of probes connecting the routers listed in routers.csv.

import csv

#Probe configuration template
template = """!
ip sla {sla_num}
 udp-jitter {destination_ip} 2000 source-ip {source_ip} interval 2000 num-packets 149
 tos {tos}
 request-data-size 256
 tag {src_node}_TO_{dest_node}_{tos_str}
 owner PROBES
 frequency 300
!
ip sla schedule {sla_num} life forever start-time now
"""

#Type of service key value pairs
tos_strings = {
    64: 'PRI1',
    32: 'PRI2',
    16: 'PRI3',
    8: 'PRI4',
    4: 'PRI5',
}

#Open the CSV file
with open('routers.csv', 'r') as file:
    reader = csv.DictReader(file)
    routers = [row for row in reader]

#Main loop to build the template with data from the csv file and write them to a file
for source_router in routers:
    sla_num = 10
    source_node = source_router['node name']
    source_ip = source_router['management ip']
    filename = str.format('{}_probes.txt', source_node)
    with open(filename, 'w') as config_file:
        for dest_router in routers:
            dest_node = dest_router['node name']
            dest_ip = dest_router['management ip']
            if source_router != dest_router:
                for tos in [64, 32, 16, 8, 4]:
                    config = template.format(
                    sla_num=sla_num,
                    destination_ip=dest_ip,
                    source_ip=source_ip,
                    tos=tos,
                    tos_str=tos_strings[tos],
                    src_node=source_node,
                    dest_node=dest_node
                    )
                    config_file.write(config)
                    sla_num += 10
