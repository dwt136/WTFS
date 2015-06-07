from gevent import monkey; monkey.patch_all(dns=False)
from const import *
from pyquery import PyQuery as pq
import requests
import urlparse, urllib, urllib2, cookielib
import gevent
import re
import os
import random
import mimetypes
import string


_BOUNDARY_CHARS = string.digits + string.ascii_letters
forbidden_file_char = re.compile(ur'[^\.\-\(\)\[\]\{\}_a-zA-Z1-9\u4e00-\u9fa5]+')

def dealName(s):
    return forbidden_file_char.sub('_', s)


def courseId(url):
    return urlparse.parse_qs(urlparse.urlparse(url).query)['course_id'][0]


def parseFields(elem):
    qs = urlparse.parse_qs(urlparse.urlparse(elem.attrib['href'].encode('utf-8')).query)
    return {k: v[0] for k, v in qs.iteritems()}


class Learn():

    def _get(self, url, parse=True, **kwargs):
        req = urllib2.Request(url + '?' + urllib.urlencode(kwargs))
        res = self.opener.open(req).read()
        return pq(unicode(res, 'utf-8')) if parse else res


    def _post(self, url, parse=True, **kwargs):
        req = urllib2.Request(url, urllib.urlencode(kwargs))
        res = self.opener.open(req).read()
        return pq(unicode(res, 'utf-8')) if parse else unicode(res, 'utf-8')

    def _multipart(self, url, fields, files):
        data, headers = self._encode_multipart(fields, files)
        req = urllib2.Request(url, data=data, headers=headers)
        return urllib2.urlopen(req).read()


    def _encode_multipart(self, fields, files, boundary=None):
        def escape_quote(s):
            return s.replace('"', '\\"')
        if boundary is None:
            boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(30))
        lines = []
        for name, value in fields.iteritems():
            lines.extend((
                '--{0}'.format(boundary),
                'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)),
                '',
                str(value),
            ))
        for name, value in files.iteritems():
            filename = value['filename']
            if 'mimetype' in value:
                mimetype = value['mimetype']
            else:
                mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            lines.extend((
                '--{0}'.format(boundary),
                'Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(
                        escape_quote(name), escape_quote(filename)),
                'Content-Type: {0}'.format(mimetype),
                '',
                value['content'],
            ))
        lines.extend((
            '--{0}--'.format(boundary),
            '',
        ))
        body = '\r\n'.join(lines)
        headers = {
            'Content-Type': 'multipart/form-data; boundary={0}'.format(boundary),
            'Content-Length': str(len(body)),
        }
        return (body, headers)


    def _fetchList(self, url, course_id, off, dictionary, key):
        """
        get url with param course_id, filter '#table_box a', pass 'off' items,
        and get the rest items into dictionary[key], where key is 'key', value
        is params in href of the item.
        e.g: fetchList(URL['FILE'], 12345, 3, self.files, 'MyCourse') will
        fetch MyCourse's (course_id=12345) course file into dict
        self.files, with params in href as value (like file_id and so).
        """
        print '  Reading %s: %s' % (course_id, url)
        d = self._get(url, course_id=course_id)
        items = d('#table_box a')
        items = items[off:]
        dictionary[key] = {dealName(i.text.strip()) if i.text is not None
                else dealName(i.find('font').text): parseFields(i) for i in items}


    def __init__(self):
        self.courses = {}
        self.notifications = {}
        self.infos = {}
        self.files = {}
        self.homeworks = {}
        self.discusses = {}
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def login(self, username, password):
        username = username.strip()
        if len(username) == 0:
            print 'No username is given'
            return False
        if len(password) == 0:
            print 'No password is given'
            return False
        res = self._post(URL['LOGIN'], userid=username, userpass=password).html()
        if res.find('window.alert') >= 0:
            print 'Fail Authorization'
            return False
        return True

    def read_to_mem(self):
        print ' Reading courses'
        d = self._get(URL['COURSE'])
        courses = d('#info_1 a')
        for i in courses:
            href = i.attrib['href']
            if href.find('course_id') >= 0:
                self.courses[i.text.strip()] = courseId(href)
        print ' Reading resources'
        g_list = []
        for name, course_id in self.courses.iteritems():
            g_list.append(gevent.spawn(self._fetchList,
                    URL['NOTIFICATION'], course_id, 0,
                    self.notifications, name))
            g_list.append(gevent.spawn(self._fetchList,
                    URL['FILE'], course_id, 3,
                    self.files, name))
            g_list.append(gevent.spawn(self._fetchList,
                    URL['HOMEWORK'], course_id, 0,
                    self.homeworks, name))
            g_list.append(gevent.spawn(self._fetchList,
                    URL['DISCUSS'], course_id, 0,
                    self.discusses, name))
        gevent.joinall(g_list)
        return True

    def get_courses(self):
        return self.courses.keys()

    def get_notifications(self, course_name):
        return self.notifications[course_name].keys()

    def get_files(self, course_name):
        return self.files[course_name].keys()

    def get_homeworks(self, course_name):
        return self.homeworks[course_name].keys()

    def get_discusses(self, course_name):
        return self.discusses[course_name].keys()

    def get_info(self, course_name):
        print 'Fetching info of %s' % course_name
        course_id = self.courses[course_name]
        d = self._get(URL['INFO'], course_id=course_id)
        res = d('#table_box').text()
        return res.encode('utf-8')

    def get_notification(self, course_name, notification_name):
        print 'Fetching notification %s of %s' % (notification_name, course_name)
        d = self._get(URL['NOTIFICATION_DETAIL'],
                **self.notifications[course_name][notification_name])
        res = d('#table_box').text()
        return res.encode('utf-8')

    def get_discuss(self, course_name, discuss_name):
        print 'Fetching discuss %s of %s' % (discuss_name, course_name)
        d = self._get(URL['DISCUSS_DETAIL'],
                **self.discusses[course_name][discuss_name])
        res = d('table').text()
        return res.encode('utf-8')

    def get_homework_detail(self, course_name, homework_name):
        print 'Fetching homework %s detail of %s' % (homework_name, course_name)
        d = self._get(URL['HOMEWORK_DETAIL'],
                **self.homeworks[course_name][homework_name])
        res = d('textarea')[0].text
        return res.encode('utf-8')

    def get_file(self, course_name, file_name):
        print 'Fetching file %s of course %s' % (file_name, course_name)
        res = self._get(URL['FILE_DOWNLOAD'], parse=False,
                **self.files[course_name][file_name])
        return res

    def get_submit_file(self, course_name, hw_name):
        print 'Fetching submitted file %s of course %s' % (hw_name, course_name)
        d = self._get(URL['HOMEWORK_SUBMIT'],
                **self.homeworks[course_name][hw_name])
        a = d('#table_box a')
        res = a[0] if len(a) > 0 else None
        return ('', '') if res is None else (self._get(URL['FILE_DOWNLOAD'],
                parse=False, **parseFields(res)), dealName(res.text.strip()))

    def submit(self, course_name, hw_name, data, filename):
        d = self._get(URL['HOMEWORK_SUBMIT'],
                **self.homeworks[course_name][hw_name])
        a = {}
        for i in d('#F1 input'):
            if i.name != 'Submit' and i.name is not None and i.name != 'upfile':
                a[i.name] = i.value
        rand = '%d0%d' % (random.randint(0, 10000), random.randint(0, 10000))
        a['post_homewk_link'] = a['newfilename'] + rand + '_' + filename
        a['filename'] = a['newfilename'] + rand + '_' + filename;
        a['upfile'] = None
        files = {'file': {'filename': filename, 'content': data} }
        res = self._multipart(URL['HOMEWORK_UPLOAD'], a, files)
        inputs = pq(res)('FORM input')
        params = {i.name: i.value for i in inputs}
        self._post(URL['HOMEWORK_HANDIN'], **params)
