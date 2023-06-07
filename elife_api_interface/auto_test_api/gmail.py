import traceback

from elife_public_method.module_encapsulation.times_method import TimeMethod


class Gmail:
    def codeEmail(self, body):
        import tempfile
        fp = tempfile.TemporaryFile()  # 创建临时文件
        fp.write(body.encode('utf-8'))
        fp.seek(0)
        data = str(fp.readline())[2: -5]
        if data.isdigit():  # 判断字符串中是否存在字母，长度大于15
            pass
        else:
            fp.readline()
            data = str(fp.readline())[2: -5]
        if data.isdigit():  # 判断字符串中是否存在字母，长度大于15
            pass
        else:
            data = "False"
        return data

    def emailDetail(self, body):
        import tempfile
        datastr = ""
        fp = tempfile.TemporaryFile()  # 创建临时文件
        fp.write(body.encode('utf-8'))
        fp.seek(0)
        for line in fp.readlines():  ##readlines(),函数把所有的行都读取进来；
            img_file = str(line.strip())  ##删除行后的换行符，img_file 就是每行的内容啦
            if len(img_file) > 3 and "<https://voice.google.com>" not in img_file and "YOUR ACCOUNT" not in img_file:
                datastr += img_file[2:-1]
            if "YOUR ACCOUNT" in img_file:
                break
        return datastr

    def selectGmail(self, type):
        try:
            import imaplib
            import email
            import tempfile
            import time

            imap = imaplib.IMAP4_SSL("imap.gmail.com")  # establish connection

            imap.login("dev2elifetransfer@gmail.com", "auskojgqeppsmzqq")  # login

            status, messages = imap.select("INBOX")  # select inbox

            numOfMessages = int(messages[0])  # get number of messages

            data = "False"
            dataList = {}
            for i in range(numOfMessages, numOfMessages - 5, -1):
                res, msg = imap.fetch(str(i), "(RFC822)")  # fetches the email using it's ID

                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])

                        # subject, From = obtain_header(msg)

                        # if msg.is_multipart():
                        # # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                if int(type) == 1:
                                    data = self.codeEmail(body)
                                else:
                                    date = msg['Date']
                                    try:
                                        month_all = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
                                                     'Nov', 'Dec']
                                        gmailDate = f"{date[12:16]}-{str(month_all.index(date[8:11]) + 1)}-{date[5:7]} " \
                                                    f"{date[17:25]}"
                                        gmailDate = TimeMethod().dayTimeUpate(gmailDate, 8)
                                    except:
                                        gmailDate = date
                                    data = self.emailDetail(body)
                                    if gmailDate in dataList:
                                        dataList[f"{gmailDate}-1"] = data
                                    else:
                                        dataList[gmailDate] = data
                                    break
                                if data == "False":
                                    pass
                                else:
                                    break
                    if data not in "False" and type == 1:
                        break
                if data not in "False" and type == 1:
                    break

            imap.close()
            if type == 1:
                return data
            else:
                return dataList
        except:
            print(traceback.print_exc())
            return "False"

if __name__ == "__main__":
    # type： 1 gmailCode 2 userCode
    # 来源：1、gmailCode driver app根据手机号获取验证码，all ride获取验证码
    #      2、待扩展
    # type = sys.argv[1]
    pass