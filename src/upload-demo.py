#coding:utf-8
import tornado.ioloop
import tornado.web
import tornado.options
import os
import datetime
import logging
import random
import traceback

# Get logger
LOG = logging.getLogger(__name__)

# Set up image directory
IMAGE_DIR = "tmp/"

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.render("login-success.html", name=name)

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        password = self.get_argument("password")

        # Assume the default password is likely "4321"
        if '4321' not in password:
            self.render("login-failure.html")
            
        self.set_secure_cookie("user", self.get_argument("username"))
        self.redirect("/")

class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        headers = self.request.headers
        body = self.request.body
        orig_name = self.get_current_user() + "-" + self.get_argument("name")
        # extension = orig_name[orig_name.rfind('.'):]
        # time = datetime.datetime.now()

        # Obtain image file name to store
        try:
            tmp_path = os.path.join(os.path.dirname(__file__), IMAGE_DIR)
            tmp_file = os.path.join(tmp_path, orig_name)
        except OSError:
            LOG.info(traceback.format_exc())
            raise HTTPError(500, 'tmp file path error')
        
        # Determine the upload method
        if 'application/octet-stream' in headers['Content-Type']:
            # Write binary stream to the local directory
            self.saveOctetStream(tmp_file, body)
        else:
            LOG.info(str(headers))
            raise HTTPError(500, 'wrong Content-Type: upload')

        self.finish()

    def saveOctetStream(self, filename, content):
        '''
        Description: Store the octet stream to the local file
        Parameters:
            filename: the destination file path
            content: the completed binary data to store
        '''
        try:
            with open(filename, "wb") as outfile:
                outfile.write(content)
        except IOError:
            LOG.info(traceback.format_exc())
            raise HTTPError(500, 'upload process error')

    def check_xsrf_cookie(self):
        pass

class SlideHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("slide.html", 
                files=self.get_img_files(self.get_current_user(), IMAGE_DIR))

    def get_img_files(self, prefix, path):
        filepath = os.path.join(os.path.dirname(__file__), path)
        files = os.listdir(filepath)
        cated = []
        for item in files:
            cated.append(os.path.join(path, item))
        img_files = filter(lambda x:prefix in x, cated)
        return img_files

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/tmp/(.*)", tornado.web.StaticFileHandler,
        {'path': os.path.join(os.path.dirname(__file__), IMAGE_DIR)}),
    (r"/static/(.*)", tornado.web.StaticFileHandler, 
        dict(path=settings['static_path'])),
    (r"/upload", UploadHandler),
    (r"/slide", SlideHandler),
], debug=True, **settings)

if __name__ == "__main__":
    tornado.options.parse_config_file("config.conf")
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
