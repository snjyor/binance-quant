from datetime import datetime, timedelta
from time import sleep

def next_run_interval_time(time_interval):
    if time_interval.endswith('m'):
        # date = datetime.now()
        time_interval = int(time_interval.strip('m'))
        target_min = (int(datetime.now().minute / time_interval) + 1) * time_interval

        if target_min < 60:
            target_time = datetime.now().replace(minute=target_min, second=0, microsecond=0)
        else:
            if datetime.now().hour == 23:
                target_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                target_time += timedelta(days=1)
            else:
                target_time = datetime.now().replace(hour=datetime.now().hour + 1, minute=0, second=0, microsecond=0)
            # 睡眠到靠近运行时间之前
        if (target_time - datetime.now()).seconds < 1:
            print('运行时间不足，下一周期再试！')
        # print('下一运行时间：', target_time)
        return target_time

    elif time_interval.endswith('h'):
        # date = datetime.now()
        time_interval = int(time_interval.strip('h'))
        target_hour = (int(datetime.now().hour / time_interval) + 1) * time_interval

        if datetime.now().hour < 23:
            target_time = datetime.now().replace(hour=target_hour, minute=0,second=0, microsecond=0)
        else:
            target_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            target_time += timedelta(days=1)

        if (target_time - datetime.now()).seconds < 1:
            print('运行时间不足，下一周期再试！')
        # print('下一运行时间：', target_time)
        return target_time
    else:
        exit("time_interval.endswith is not 'm' or 'h'")


def sleep_to_next_runtime(time_interval):
    # 睡眠到下次运行时间
    next_run_time = next_run_interval_time(time_interval)
    print('下次运行时间：', next_run_time)
    sleep(max(0, (next_run_time - datetime.now()).seconds))
    while True:
        if datetime.now() < next_run_time:
            continue
        else:
            break
    return next_run_time





