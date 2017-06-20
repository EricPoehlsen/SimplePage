#!C:\Python36\python.exe
#!/usr/bin/python3
import os


class SimpleFile(object):
    """ Simple File serves files for the Simple Page website

    It is used to enforce the directory acl to stored files
    """


    def __init__(self):
        self.cnf = None
        self.name = ""
        self.directory = []
        self.status = "200 OK"
        self.data = {}

    def make_config(self):
        self.cnf = {
            "base_url": "https://www.eric-poehlsen.de/site",
            "base_dir": "site",
            "file_ext": "wiki",
            "acl_name": "acl",
            "rank_override": True
        }

    def parse_url(self):
        """ deconstructing the request url """

        base = os.environ.get("REQUEST_URI", "/")

        # remove query string
        base, *query = base.split("?")
        query = "?".join(query)
        self.query = query.split("&")

        # check if this is an existing file
        path = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            base[1:]
        )
        if os.path.isfile(path): self.data["file_path"] = path

        if base.endswith("/"): base = base[:-1]
        *directory, filename = base.split("/")
        name, *ext = filename.split(".")
        if not isinstance(ext, list):
            ext = [ext]

        base_dir = self.cnf.get("base_dir")
        if not base_dir.startswith("/"):
            base_dir = "/" + base_dir

        directory = "/".join(directory)

        if len(directory) > len(base_dir):
            directory = directory[len(base_dir):]
        else:
            directory = ""

        self.directory = [i for i in directory.split("/") if i]
        self.name = name

        if ext:
            ext = ext[-1]

            # setting mime_type
            mimetypes = {
                "css": "text/css",
                "xml": "application/xml",
                "png": "image/png",
                "jpg": "image/jpg",
                "jpeg": "image/jpg",
                "jpe": "image/jpg",
                "gif": "image/gif",
                "tif": "image/tif",
                "tiff": "image/tif",
                "txt": "text/plain",
                "htm": "text/html",
                "html": "text/html",
            }
            self.data["mime_type"] = mimetypes.get(ext, "application/octet")

    def cookie_handler(self):
        """ The user supplied a cookie - is it valid? """

        root = os.environ["DOCUMENT_ROOT"]
        base = self.cnf.get("base_dir")
        if base.startswith("/"):
            base = base[1:]

        cookie = os.environ.get("HTTP_COOKIE")

        if cookie:
            session_id = cookie.split("=")[-1]

            users = "users." + self.cnf["file_ext"]
            path = os.path.join(root, base, users)
            user_file = open(path, "r", encoding="utf-8")
            user_data = user_file.readlines()
            user_file.close()

            for entry in user_data:
                if entry.count(" ") != 7: continue
                user, pwd_hash, mail, url, rank, stored_id, expires, *ip = entry.split()
                if stored_id == session_id:
                    self.data["user"] = user
                    self.data["login"] = True

                    # set global rank (if enabled)
                    if self.cnf.get("rank_override"):
                        self.data["user_rank"] = rank.strip()
                    break

    def check_acl(self):
        """ retrieve ACL for this page or a parent page """

        # find the relevant acl
        acl = []
        local_dir = [d for d in self.directory] + [self.name]
        for i in range(len(local_dir) + 1):
            path = os.path.join(
                os.environ["DOCUMENT_ROOT"],
                self.cnf["base_dir"],
                *local_dir,
                self.cnf["acl_name"] + "." + self.cnf["file_ext"]
            )
            local_dir = local_dir[:-1]

            if os.path.exists(path):
                file = open(path, mode="r", encoding="utf-8")
                acl = file.readlines()
                file.close()

                if not acl[0].startswith("!"):
                    break
                else:
                    dir = acl[0][1:].strip()
                    path = os.path.join(
                        os.environ["DOCUMENT_ROOT"],
                        self.cnf["base_dir"],
                        dir,
                        self.cnf["acl_name"] + "." + self.cnf["file_ext"]
                    )
                    if os.path.exists(path):
                        file = open(path, mode="r", encoding="utf-8")
                        acl = file.readlines()
                        file.close()
                    break

        # check the acl
        rank = None
        for entry in acl:
            entry = entry.strip()
            if entry.startswith(":"):
                rank = entry[1:]
                continue

            if self.data.get("user") == entry and not self.data.get("rank"):
                self.data["rank"] = rank
                continue

            elif entry == "#all" and not self.data.get("rank"):
                self.data["rank"] = rank

        # override the acl rank with a higher user rank
        if self.cnf.get("rank_override"):
            acl_rank = self.data.get("rank", "visitor")
            user_rank = self.data.get("user_rank", "visitor")
            rank_level = {
                "visitor": 0,
                "reader": 1,
                "commenter": 2,
                "writer": 3,
                "owner": 4
            }

            if rank_level[user_rank] > rank_level[acl_rank]:
                self.data["rank"] = user_rank

        ranks = ["reader", "commenter", "writer", "owner"]
        if self.data.get("rank") not in ranks:
            if self.data.get("user"):
                self.status = "403 Forbidden"
            else:
                self.status = "401 Not Authorized"

    def headers(self, status="200 OK", cont_type="text/plain"):
        """ printing the header to the http stream """
        header = "Status: " + status + "\n"
        header += "Content-Type: " + cont_type + "\n"

        # setting cookie if login is successful
        login = self.data.get("login")
        cookie = self.data.get("cookie")
        if login and cookie:
            header += cookie + "\n"
        header += "\n"

        return header

    def serve_file(self):
        """ serves an existing file ... """

        import sys

        headers = self.headers(status=self.status, cont_type=self.data["mime_type"])
        sys.stdout.buffer.write(headers.encode(encoding="utf-8"))

        if self.status.startswith("2"):
            file = open(self.data["file_path"], mode="rb")
            while True:
                buffer = file.read(4096)
                if buffer:
                    sys.stdout.buffer.write(buffer)
                else:
                    break
            file.close()

def test():
    os.environ["DOCUMENT_ROOT"] = "C:/Users/Eric/Documents/Homepages/"
    os.environ["REQUEST_METHOD"] = "GET"
    os.environ["REQUEST_URI"] = "/site/test/sub/1.jpg"


if __name__ == "__main__":
    # running test?
    if not os.environ.get("DOCUMENT_ROOT"):
        test()

    # initializing the page (Nothing in here must print anything!)
    file = SimpleFile()
    file.make_config()
    file.parse_url()
    file.cookie_handler()
    file.check_acl()

    # and serve it to the user ...
    file.serve_file()