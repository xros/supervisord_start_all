#!/usr/bin/env python
#coding=utf-8
# 从2014年4月2日开始维护
"""主要用于测试supervisord 的内容


"""
import uuid
import hashlib
import json
import base64
import torndb
import MySQLdb
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import define, options
# This is vital for JSON dumps the method: __default
from datetime import date, datetime, timedelta
import logging


# define 完成后，同时生成一个options里面的属性，在下面方便 torndb.Connection
define("port", default=8000, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="mysql", help="database name")
define("mysql_user", default="root", help="database user")
define("mysql_password", default="", help="database password")
define("secret", default="secret_pass", help="secret key")

db = torndb.Connection(
        host=options.mysql_host, database=options.mysql_database,
        user=options.mysql_user, password=options.mysql_password,time_zone="+8:00")

def get_token():
    """
    Generate a hash that can be used as an application secret
    """
    hash = hashlib.sha1(str(uuid.uuid1()))
    hash.update(options.secret)
    return hash.hexdigest()

def __default(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    else:
        raise TypeError('%r is not JSON serializable' % obj)

def json_dumps(s):
    """

    """
    return json.dumps(s,ensure_ascii=False,default=__default)

def get_now():
    # 得到现在的时间，例如：
    # '2013-12-31 12:29:54'
    # 上海在东八区
    #local_time = datetime.now() + timedelta(hours=8)
    local_time = datetime.now()
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    return local_time.strftime(ISOTIMEFORMAT)



class BaseHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        global db
        db = torndb.Connection(
                host=options.mysql_host, database=options.mysql_database,
                user=options.mysql_user, password=options.mysql_password,
                time_zone="+8:00")
        return db

    def write_error(self, status_code, **kwargs):
        if status_code==500:
            ret = {"ret":"9","msg":u"系统出错！！"}
            self.write(json_dumps(ret))
            return
        else:
            super(BaseHandler, self).write_error(status_code, **kwargs)




class TestPage1Handler(BaseHandler):
    def get(self, *args, **kwargs):
        ret = {'msg':'', 'ret':"0"}
        try:
            sql1 = "SELECT User FROM user WHERE Host='127.0.0.1'"
            db_username = self.db.get(sql1)
        except Exception as e:
            ret = {'msg':'Database error', 'ret':"1"}
            self.write(json_dumps(ret))
            return
        else:
            ret['result'] = {"test":"okay"}
            ret['result'].update({'db_username': db_username['User']})
            logging.info('A request to test page 1')
        self.write(json_dumps(ret))
        return


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # 测试 torndb 效率
            (r"/testpage1", TestPage1Handler),                           # 测试


            #(r"/update/dealer/profile", UpdateProfileHandler)
            #(r"")
        ]

        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(),no_keep_alive=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()


