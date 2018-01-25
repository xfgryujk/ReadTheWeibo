# -*- coding: utf-8 -*-

import pickle
import re
import sys
from logging import getLogger
from queue import Queue
from threading import Thread

import pyttsx3
from PyQt5.QtCore import QObject, QTimer

from login_dlg import LoginDlg
from popup_post import PopupPost
from weibo import Weibo

logger = getLogger(__name__)

SESSION_PATH = 'data/session.pickle'

TAG_REG = re.compile('<.*?>')
HAHAHA_REG = re.compile('哈{4,}')
HHH_REG = re.compile('h{4,}', re.IGNORECASE)


class ReadTheWeibo(QObject):

    def __init__(self, *args):
        super().__init__(*args)

        # 微博session、API
        self.weibo = None
        # 登录
        self.load_session()
        if not self.weibo.is_login():
            dlg = LoginDlg()
            # 如果还是没登录则退出
            if not dlg.exec():
                sys.exit(0)
            self.weibo.cookies = dlg.weibo_cookies

        # 显示微博弹窗
        self.show_post = True
        # 微博弹窗
        self._popup_post = PopupPost(self)
        # 读出微博
        self.speak_post = True
        # TTS引擎
        self._tts = pyttsx3.init()
        self._tts.connect('finished-utterance', self._on_finish_speaking)

        # 微博队列
        self._post_queue = Queue()
        # 定时器、线程
        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self._update_posts)
        self._tts_loop_thread = None

    def load_session(self):
        self.weibo = None
        try:
            with open(SESSION_PATH, 'rb') as f:
                self.weibo = pickle.load(f)
        except OSError:  # 打开文件错误
            pass
        except pickle.PickleError:
            logger.exception('反序列化Weibo时出错：')
        if self.weibo is None:
            self.weibo = Weibo()

    def save_session(self):
        try:
            with open(SESSION_PATH, 'wb') as f:
                self.weibo = pickle.dump(self.weibo, f)
        except (OSError, pickle.PickleError):
            logger.exception('序列化Weibo时出错：')

    def start(self):
        if self._tts_loop_thread is None:
            self._tts_loop_thread = Thread(target=self._tts.startLoop)
            self._tts_loop_thread.daemon = True
            self._tts_loop_thread.start()
        if not self._update_timer.isActive():
            self._update_timer.start(25 * 1000)
            self._update_posts()

    def stop(self):
        if self._update_timer.isActive():
            self._update_timer.stop()
        if self._tts_loop_thread is not None:
            self._tts.endLoop()
            self._tts_loop_thread.join()
            self._tts_loop_thread = None

    def _update_posts(self):
        """
        获取未读微博
        """

        # TODO 测试完后改回
        # try:
        #     n_unread = self.weibo.get_n_unread()
        #     if n_unread > 0:
        #         posts = self.weibo.get_friend_feed()[n_unread - 1::-1]
        #         for post in posts:
        #             self._post_queue.put(post)
        # except ConnectionResetError:
        #     pass
        # except:
        #     logger.exception('获取新微博时出错：')

        # 测试
        post = {
            'user': {'screen_name': 'test'},
            'text': '这是一条测试'
        }
        for i in range(5):
            self._post_queue.put(post)

        self._process_new_post()

    def _process_new_post(self):
        """
        处理队列中的新微博，如果正在发声或队列为空则什么也不做
        """

        if self._tts.isBusy() or self._post_queue.empty():
            return
        post = self._post_queue.get_nowait()
        logger.debug('处理微博：%s：%s\n剩余%d条',
                     post['user']['screen_name'], post['text'],
                     self._post_queue.qsize())

        if self.show_post:
            self._popup_post.show_post(post)
        if self.speak_post:
            self._tts.say(self._filter_tts_content(post))

    @staticmethod
    def _filter_tts_content(post):
        """
        处理微博，准备TTS
        :param post: 微博
        :return: 处理后的微博内容
        """

        user = post['user']['screen_name']
        content = post['text']

        content = TAG_REG.sub('，', content)
        content = HAHAHA_REG.sub('哈哈哈哈', content)
        content = HHH_REG.sub('hhhh', content)
        content = '{}说：{}'.format(user, content)
        return content

    def on_popup_post_close(self):
        """
        微博弹窗被关闭
        """

        logger.debug('on_popup_post_close')
        # 如果是手动关闭，停止发声，如果是发声结束关闭，什么也不做
        self._tts.stop()

    def on_popup_post_hide(self):
        """
        微博弹窗被隐藏
        """

        logger.debug('on_popup_post_hide')
        self._process_new_post()

    def _on_finish_speaking(self, name, completed):
        """
        结束发声
        :param name: say的参数，未使用
        :param completed: 发声正常结束
        """

        logger.debug('_on_finish_speaking, completed = %s', completed)
        # 如果是手动关闭，什么也不做，如果是发声结束关闭，关闭窗口
        if completed:
            self._popup_post.close()
