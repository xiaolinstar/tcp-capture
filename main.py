from trans_tool import *
from option import args


if __name__ == '__main__':

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
