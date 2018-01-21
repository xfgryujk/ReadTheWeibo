# -*- coding: utf-8 -*-

from time import sleep
import re

import pyttsx3

from weibo import Weibo

wb = Weibo({
    'SUB': '略',
})
tts = pyttsx3.init()

TAG_REG = re.compile('<.*?>')


def main():
    while True:
        try:
            n_unread = wb.get_n_unread()
            if n_unread > 0:
                posts = wb.get_friend_feed()[n_unread - 1::-1]

                for post in posts:
                    user = post['user']['screen_name']
                    content = post['text']

                    print('{}：{}\n'.format(user, content))

                    content = TAG_REG.sub('，', content)
                    tts.say('{}说：{}'.format(user, content))
                    tts.runAndWait()
        except Exception as e:
            print(e)

        sleep(25)


if __name__ == '__main__':
    main()
