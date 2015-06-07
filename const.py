import re

NOTIFICATION = 'notification'
INFO = 'info'
FILE = 'file'
HOMEWORK = 'homework'
HOMEWORK_DETAIL= 'detail'
HOMEWORK_SUBMIT = 'submit'
DISCUSS = 'discuss'


PATTERNS = {
    'ROOT': r'^/$',
    'COURSE': r'^/([^/]+)$',
    'INFO': r'^/([^/]+)/info$',
    'NOTIFICATIONS': r'^/([^/]+)/notification$',
    'NOTIFICATION': r'^/([^/]+)/notification/([^/]+)$',
    'FILES': r'^/([^/]+)/file$',
    'FILE': r'^/([^/]+)/file/([^/]+)$',
    'HOMEWORKS': r'^/([^/]+)/homework$',
    'HOMEWORK': r'^/([^/]+)/homework/([^/]+)$',
    'HOMEWORK_DETAIL': r'^/([^/]+)/homework/([^/]+)/detail$',
    'HOMEWORK_SUBMIT': r'^/([^/]+)/homework/([^/]+)/submit$',
    'HOMEWORK_SUBMIT_FILE': r'^/([^/]+)/homework/([^/]+)/submit/([^/]+)$',
    'DISCUSSES': r'^/([^/]+)/discuss$',
    'DISCUSS': r'^/([^/]+)/discuss/([^/]+)$',
}
PATTERNS = {k: re.compile(v) for k, v in PATTERNS.iteritems()}

URL = dict(
    LOGIN='https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp',
    COURSE='http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp',
    NOTIFICATION='https://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/getnoteid_student.jsp',
    NOTIFICATION_DETAIL='http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/note_reply.jsp',
    INFO='https://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/course_info.jsp',
    FILE='https://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/download.jsp',
    FILE_DOWNLOAD='http://learn.tsinghua.edu.cn/uploadFile/downloadFile_student.jsp',
    HOMEWORK='https://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/hom_wk_brw.jsp',
    HOMEWORK_DETAIL='http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/hom_wk_detail.jsp',
    HOMEWORK_SUBMIT='http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/hom_wk_submit.jsp',
    HOMEWORK_UPLOAD='http://learn.tsinghua.edu.cn/uploadFile/uploadFile.jsp',
    HOMEWORK_HANDIN='http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/hom_wk_handin.jsp',
    DISCUSS='https://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/gettalkid_student.jsp',
    DISCUSS_DETAIL='http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/talk_reply_student.jsp',
    BASE_URL='http://learn.tsinghua.edu.cn',
)
