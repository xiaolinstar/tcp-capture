import argparse
import os
from trans_tool import *

home = os.environ['HOME']


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server_ip', type=str, default='47.94.104.34', help='The server ip that you would set a '
                                                                              'connection with')
    parser.add_argument('--server_port', type=str, default='5001', help='The server port that you would set a '
                                                                        'connection with')
    parser.add_argument('--dir_path', type=str, default='{}/Documents/algos'.format(home), help='The root directory '
                                                                                                'to store all data.')
    parser.add_argument('--duration', type=int, default=300, help='The duration of data transition.')
    parser.add_argument('--bool_iperf', type=bool, default=True, help='True: iperf, False: iperf3.')
    parser.add_argument('--test_num', type=int, default=500)
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    args = parse_opt()
    aliyun = args.server_ip
    aliyun_port = args.server_port
    dir_p = args.dir_path
    dura = args.duration
    is_iperf = args.bool_iperf
    window_sizes = ['4K', '8K', '16K', '32K', '64K', '128K']
    test_num = args.test_num

    upload_algo()
    avail_algos = get_avail_algo()
    if len(avail_algos) > 5:
        print('Available algos are as follows:')
        print(', '.join(avail_algos))

        tool = TransTool(aliyun, aliyun_port, is_iperf)

        # make the root dir

        if not os.path.exists(dir_p):
            os.mkdir(dir_p)

        # make the dirs of available algos
        for a in avail_algos:
            algo_p = os.path.join(dir_p, a)
            if not os.path.exists(algo_p):
                os.mkdir(algo_p)
            else:
                # remove all files in root dir
                cmd = 'rm -rf {}/*'.format(algo_p)
                os.system(cmd)

        algo_nums = dict(zip(avail_algos, [0 for _ in avail_algos]))
        for i in range(test_num):
            random_algo = random.choice(avail_algos)
            w_size = random.choice(window_sizes)

            curr_time = datetime.datetime.now().strftime('%H %M %S').split()
            h = int(curr_time[0])
            if 8 < h < 22:
                t_sign = 1
            else:
                t_sign = 0

            algo_nums[random_algo] += 1
            filename = 'packet_{}_{}_{}_{}'.format(w_size, random_algo, t_sign, algo_nums[random_algo])
            print('A data transfer is in progress with window_size: {}, algo: {}'.format(w_size, random_algo))
            tool.trans_tcp(os.path.join(dir_p, random_algo), filename, w_size, random_algo, dura)

    else:
        print('Please check the available algos.')
