import subprocess
import sys
import pandas as pd
import os


# python3 gen_net.py <report_dir> <file_list.csv> <net.csv>
with open(sys.argv[2], 'r') as f:
    flist = f.readlines()
    for dir_ in flist:
        dir_path = sys.argv[1] + dir_[:-1]
        p = subprocess.call('cd CICFlowMeter-4.0/bin/ && ./cfm ' +
                            dir_path + ' ../../net/', shell=True)
        os.rename('net/tcpdump.pcap_Flow.csv', 'net/' + dir_[:-1] + '.csv')

attributes = ['Sum ', 'Max ']
features = ['Flow Duration', 'Tot Fwd Pkts', 'Tot Bwd Pkts',
            'TotLen Fwd Pkts', 'TotLen Bwd Pkts', 'Fwd IAT Tot', 'Bwd IAT Tot',
            'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags',
            'Fwd Header Len', 'Bwd Header Len',
            'FIN Flag Cnt', 'SYN Flag Cnt', 'RST Flag Cnt', 'PSH Flag Cnt',
            'ACK Flag Cnt', 'URG Flag Cnt', 'CWE Flag Count', 'ECE Flag Cnt',
            'Init Fwd Win Byts', 'Init Bwd Win Byts',
            'Fwd Act Data Pkts']
headers = [att + ft for ft in features for att in attributes ]
headers.insert(0, 'Num of flow')

data = dict()
for header in headers:
    data[header] = list()
with open(sys.argv[2], 'r') as f:
    flist = f.readlines()
    for dir_ in flist:
        flow_path = 'net/' + dir_[:-1] + '.csv'
        try:
            flow = pd.read_csv(flow_path)
            data['Num of flow'].append(len(flow.index))
            for feature in features:
                data['Sum ' + feature].append(flow[feature].sum())
                data['Max ' + feature].append(max(flow[feature], default=0))          
        except Exception as e:
            print(e)
            data['Num of flow'].append(0)
            for feature in features:
                data['Sum ' + feature].append(0)
                data['Max ' + feature].append(0)
    
    dp = pd.DataFrame.from_dict(data)
    dp.to_csv(sys.argv[3], index=None, columns=headers)
