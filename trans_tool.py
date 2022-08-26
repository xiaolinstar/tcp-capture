import datetime
import os.path
import random


def get_avail_algo():
    cmd = 'sysctl net.ipv4.tcp_available_congestion_control'
    algos = []
    with os.popen(cmd, 'r') as f:
        text = f.read()
        algos.extend(text.split()[2:])
    return algos
    # print('Available algos are as follows:')


def upload_algo():
    algos = ['tcp_westwood', 'tcp_vegas', 'tcp_bic', 'tcp_htcp', 'tcp_bbr']
    for algo in algos:
        os.system('sudo modprobe -a {}'.format(algo))


class TransTool:

    def __init__(self, server_ip, server_port=5001, iperf=True):
        self.server_ip = server_ip
        self.server_port = server_port
        self.bool_iperf = iperf
        self.format = 'M'

    def trans_tcp(self, dir_path, f_name, win_size, algo, duration):
        if self.bool_iperf:
            self.tcp_iperf(dir_path, f_name, win_size, algo, duration)
        else:
            self.tcp_iperf3(dir_path, f_name, win_size, algo, duration)

    def tcp_iperf(self, dir_path, f_name, win_size, algo, duration, suffix='.txt'):
        file = os.path.join(dir_path, f_name + suffix)
        cmd = 'sudo iperf -c {} -p {} -w {} -f {} -i 1 -Z {} -t {} >> {}'.format(self.server_ip,
                                                                                 self.server_port, win_size,
                                                                                 self.format,
                                                                                 algo, duration, file)
        os.system(cmd)

    def tcp_iperf3(self, dir_path, f_name, win_size, algo, duration, suffix='.txt'):
        file = os.path.join(dir_path, f_name + suffix)
        cmd = 'sudo iperf3 -c {} -p {} -w {} -f {} -i 1 -C {} -t {} --logfile {}'.format(self.server_ip,
                                                                                         self.server_port, win_size,
                                                                                         self.format,
                                                                                         algo, duration, file)
        os.system(cmd)
