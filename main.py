import tomxin.tx_mysql
import house_info
import house_record
import user_info
import time
import traceback
import urllib
import tomxin.tx_time
import tomxin.tx_proxy_ip

def houst_main():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "开始爬取")
    sql = "select city_name,dou_ban_url from city"
    result = tomxin.tx_mysql.select(sql)
    for row in result:
        city = row[0]
        print(tomxin.tx_time.now_time() + city +"  开始爬取")
        url_num = row[1]

        # 爬取租房信息
        houstList = house_info.getHouse(url_num)

        # 查询改城市需要判断的用户记录
        recordList = house_record.get_record(city)

        # 对比租房信息和用户设置的key
        user_info.check_info(houstList, recordList)

        print(tomxin.tx_time.now_time() + city +"  爬取成功")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "爬取成功，休息4分钟")
    #休息4分钟
    time.sleep(4 * 60)

    #晚上10点后不再监控
    if str(time.strftime('%H', time.localtime())) == "22":
        print("晚上10点，程序开始休眠")
        time.sleep(60*60*9)



retry_num = 3  # 重试次数
sleep_time = 5  # 休息时间（单位分钟）
project_name = "简单找房"  # 项目名称
error_num = 0
if __name__ == '__main__':
    print(tomxin.tx_time.now_time() + "【" + project_name + "】启动成功")
    #清空ip.txt
    tomxin.tx_proxy_ip.line_write_txt("ip.txt", [])
    #爬取代理ip
    tomxin.tx_proxy_ip.judge_proxy_ip("https://www.douban.com/group/463347/")
    while (1):
        try:
            houst_main()
            error_num = 0
        except Exception as e:
            message = "【严重 {project_name}】系统出现第{error_num}次异常，休息{sleep_time}分钟后重试，具体请查看日志：{log_code}，错误码为：" + str(e)
            if retry_num == error_num:
                message = "【严重 {project_name}】系统出现第{error_num}次异常，项目重试次数上限，已经退出程序，错误码为：" + str(e)
            message = message.replace("{project_name}", project_name)
            message = message.replace("{sleep_time}", str(sleep_time))
            message = message.replace("{error_num}", str(error_num + 1))
            message = message.replace("{log_code}", str(int(time.time())))
            print(tomxin.tx_time.now_time() + message)
            print(traceback.format_exc())
            message = urllib.parse.quote(message)
            url = "http://wxmsg.dingliqc.com/send?msg=" + message + "&userIds=orPQ808n2X4vtf-1cIihSnbHqisoITWXlbsk3I"
            tomxin.tx_request.get(url)
            if retry_num == error_num:
                exit()
            time.sleep(sleep_time * 60)
            error_num = error_num + 1


