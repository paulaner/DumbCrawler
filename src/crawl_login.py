__author__ = 'Alan'


import sys
import urllib2
import urllib
import cookielib

reload(sys)
sys.setdefaultencoding("utf8")

login_url = 'http://www.renren.com/login.do'
login_domain = 'renren.com'


class Login(object):
    def __init__(self):
        self.name = ''
        self.pass_word = ''
        self.domain = ''

        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def set_login_info(self, user_name, pass_word, domain):
        self.name = user_name
        self.pass_word = pass_word
        self.domain = domain

    def login(self):
        login_params = {'domain': self.domain, 'email': self.name, 'password': self.pass_word}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        req = urllib2.Request(login_url, urllib.urlencode(login_params), headers=headers)
        response = urllib2.urlopen(req)
        self.operate = self.opener.open(req)
        page = response.read()
        print page

if __name__ == '__main__':
    user_login = Login()
    username = 'hyattgra@126.com'
    password = '1010406796'
    domain = login_domain
    user_login.set_login_info(username, password, domain)
    user_login.login()