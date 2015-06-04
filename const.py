import re

OLD = 'old'
NEW = 'new'
NOTIFICATION = 'notification'
INFO = 'info'
FILE = 'file'
HOMEWORK = 'homework'
HOMEWORK_DETAIL= 'detail'
HOMEWORK_ATTACH = 'attach'
HOMEWORK_SUBMIT = 'submit'
DISCUSS = 'discuss'


PATTERNS = {
    'ROOT': r'^/$',
    'COURSES': r'^/(new|old)$',
    'COURSE': r'^/(new|old)/[^/]+$',
    'INFO': r'^/(new|old)/[1-9\-]+/info$',
    'NOTIFICATIONS': r'^/(new|old)/[1-9\-]+/notification$',
    'NOTIFICATION': r'^/(new|old)/[1-9\-]+/notification/[^/]+$',
    'FILES': r'^/(new|old)/[1-9\-]+/file$',
    'FILE': r'^/(new|old)/[1-9\-]+/file/[^/]+$',
    'HOMEWORKS': r'^/(new|old)/[1-9\-]+/homework$',
    'HOMEWORK': r'^/(new|old)/[1-9\-]+/homework/[^/]+$',
    'HOMEWORK_DETAIL': r'^/(new|old)/[1-9\-]+/homework/[^/]+/detail$',
    'HOMEWORK_ATTACH': r'^/(new|old)/[1-9\-]+/homework/[^/]+/attach$',
    'HOMEWORK_ATTACH_FILE': r'^/(new|old)/[1-9\-]+/homework/[^/]+/attach/[^/]+$',
    'HOMEWORK_SUBMIT': r'^/(new|old)/[1-9\-]+/homework/[^/]+/submit$',
    'HOMEWORK_SUBMIT_FILE': r'^/(new|old)/[1-9\-]+/homework/[^/]+/submit/[^/]+$',
    'DISCUSS': r'^/(new|old)/[1-9\-]+/discuss$',
    'DISCUSS_FILE': r'^/(new|old)/[1-9\-]+/discuss/[^/]+$',
}
PATTERNS = {k: re.compile(v) for k, v in PATTERNS.iteritems()}

OLD_URL = dict(
    LOGIN='https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp',
    COURSE='http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp',
    NOTIFICATION='https://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/getnoteid_student.jsp',
    INFO='https://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/course_info.jsp',
    FILE='https://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/download.jsp',
    HOMEWORK='https://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/hom_wk_brw.jsp',
    HOMEWORK_DETAIL='http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/hom_wk_detail.jsp',
    HOMEWORK_SUBMIT='http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/hom_wk_submit.jsp',
    HOMEWORK_REVIEW='http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/hom_wk_view.jsp',
    DISCUSS='https://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/gettalkid_student.jsp',
    DISCUSS_DETAIL='http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/talk_reply_student.jsp',
    BASE_URL='http://learn.tsinghua.edu.cn',
)


NEW_URL = dict(
    LOGIN='https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/fa8077873a7a80b1cd6b185d5a796617/0?/j_spring_security_thauth_roaming_entry',
    COURSE='http://learn.cic.tsinghua.edu.cn/f/student/courselist',
    NOTIFICATION='http://learn.cic.tsinghua.edu.cn/b/myCourse/notice/list/',
    INFO='http://learn.cic.tsinghua.edu.cn/f/student/courseinfo/',
    FILE='http://learn.cic.tsinghua.edu.cn/f/student/courseware/',
    HOMEWORK='http://learn.cic.tsinghua.edu.cn/f/student/homework/',
    HOMEWORK_DETAIL='http://learn.cic.tsinghua.edu.cn/b/myCourse/homework/list4Student/',
    HOMEWORK_SUBMIT='http://learn.cic.tsinghua.edu.cn/f/student/homework/hw_detail/',
    HOMEWORK_REVIEW='http://learn.cic.tsinghua.edu.cn/f/student/homework/hw_result/',
    DISCUSS='http://learn.cic.tsinghua.edu.cn/b/topic/list/1/',
    DISCUSS_DETAIL='http://learn.cic.tsinghua.edu.cn/f/student/forum/courseReplyList/',
    BASE_URL='http://learn.cic.tsinghua.edu.cn',
)
