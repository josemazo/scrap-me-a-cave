import abc
import smtplib


class EmailSender(object):

    def __init__(self, sender_email='', sender_name=''):
        self.sender_name = sender_name
        self.sender_email = sender_email
        pass

    @abc.abstractmethod
    def login(self, password):
        return

    @abc.abstractmethod
    def send_email(self, to='', subject='', message=''):
        return

    @abc.abstractmethod
    def logout(self):
        return


class GmailSender(EmailSender):

    _server_url = 'smtp.gmail.com'
    _port = 587

    def login(self, password):
        self._server = smtplib.SMTP(self._server_url, self._port)
        self._server.ehlo()
        self._server.starttls()
        self._server.login(self.sender_email, password)

    def send_email(self, to='', subject='', message=''):
        msg = '\r\n'.join(['From: {0}',
                           'To: {1}',
                           'Subject: {2}',
                           '',
                           '{3}'])
        msg = msg.format(self.sender_name, to, subject, message)
        self._server.sendmail(self.sender_email, to, msg)

    def logout(self):
        self._server.quit()
