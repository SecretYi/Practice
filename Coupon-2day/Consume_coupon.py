from get_network_date import Network_time
from create_coupon import mysql_info
from datetime import datetime

coupon_id = input("请输入您的消费券ID：")

def select_user():
    """查询出当前消费券的使用人和失效日期"""
    sql = "SELECT * FROM coupon WHERE coupon_id = %s"
    data = [coupon_id]
    data = mysql_info(sql,data)[0]
    print(data)
    old_user = data[3]
    Expired_date = data[2]
    return old_user,Expired_date


if __name__ == '__main__':
    try:
        data  = select_user()
        old_user = data[0]#使用消费券的用户
        Expired_date = datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S')#将失效日期转为datetime格式的时间   未下面的时间比较做准备
        network_date = Network_time()[2]#拿到当前的北京时间
        if network_date > Expired_date:
            #检查消费券是否失效
            print("您使用的优惠券已过期！！！")
        elif old_user == None:
            #如果old_user等于空，则说明未被使用过
            new_user = input("请输入您的姓名：")
            sql = "update coupon SET `user`= %s WHERE coupon_id = %s"  # 向当前coupon_id插入消费人
            data = [new_user, coupon_id]
            mysql_info(sql, data)
            user = mysql_info("SELECT * FROM coupon WHERE coupon_id = %s",[coupon_id])[0][3]
            Expired_date = mysql_info("SELECT * FROM coupon WHERE coupon_id = %s",[coupon_id])[0][2]
            # print(Expired_date)
        else:
            user = mysql_info("SELECT * FROM coupon WHERE coupon_id = %s", [coupon_id])[0][3]
            print("您输入的消费券已 {} 被使用过！！！".format(user))
    except:
        print("\n您输入的优惠劵不存在")