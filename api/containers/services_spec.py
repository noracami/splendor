import os.path

import paramiko
import pinject
from flask import Flask


from api.biz.account.normal_account_service import NormalAccountService

from api.common.mail.system_mailer import SystemMailer
from api.common.updated_at_utils import UpdatedAtUtils
from config.api_config import Config

service_classes = [

    NormalAccountService,

    SystemMailer,


    UpdatedAtUtils,

]


class BindingSpec(pinject.BindingSpec):
    """Binding setup"""

    def __init__(self, app: Flask):
        self.app = app

    def configure(self, bind):
        bind('app', to_instance=self.app)
        bind('cache', to_instance=self.app.rediscache)
        bind('config', to_instance=Config())
        bind('logger', to_instance=self.app.logger)
        bind('user_sql_session', to_instance=self.app.userDBSession)

    @pinject.provides(in_scope=pinject.SINGLETON)
    def provide_cronjob(self) -> paramiko.SSHClient():
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                hostname=Config().CRONJOB_HOST, username=Config().CRONJOB_USER, password=Config().CRONJOB_PWD)
        except Exception as e:
            print(f"[!] Cannot connect to the SSH Server. \n {e}")  # noqa : T201
            exit()

        return client