from const import *
from pyquery import PyQuery as pq
import urllib, urllib2, cookielib


ok = dict(success=1)


def fail(error=''):
    return dict(success=0, error=error)


class Learn():

    def _get(self, url, **kwargs):
        res = urllib2.urlopen(url + '?' + urllib.urlencode(kwargs)).read()
        return pq(unicode(res, "utf-8"))

    def _post(self, url, **kwargs):
        headers = {"User-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
        req = urllib2.Request(url, urllib.urlencode(kwargs), headers)
        res = self.opener.open(req).read()
        return pq(unicode(res, "utf-8"))

    def __init__(self):
        self.courses = []
        self.notifications = {}
        self.nnotifications = {}
        self.infos = {}
        self.ninfos = {}
        self.files = {}
        self.nfiles = {}
        self.homeworks = {}
        self.nhomeworks = {}
        self.discusses = {}
        self.ndiscusses = {}
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def login(self, username, password):
        username = username.strip()
        if len(username) == 0:
            return fail('No username is given')
        if len(password) == 0:
            return fail('No password is given')
        res = self._post(OLD_URL['LOGIN'], userid=username, userpass=password).html()
        if res.find('window.alert') >= 0:
            return fail('Fail Authorization')
        self._post(NEW_URL['LOGIN'], i_user=username, i_pass=password)
        return ok

    def read_to_mem(self):
        d = self._get(OLD_URL['COURSE'])
        courses = d('#info_1 a')
        self.courses = [i.text.strip() for i in courses]

    def get_courses(self):
        return self.courses
