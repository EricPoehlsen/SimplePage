#!C:\Python36\python.exe
#!/usr/bin/python3
import cgi
import time
import re
import os
import uuid
import glob
import bcrypt
import random
from http.cookies import SimpleCookie as Cookie
from datetime import datetime


S_DE = {
    "username": "Benutzername:",
    "password": "Passwort:",
    "password_old": "Altes Passwort:",
    "password_new": "Neues Passwort:",
    "password_check": "Passwort bestätigen:",
    "mail": "E-Mail Adresse:",
    "login": "Anmelden",
    "link": '<a href="{url}"{more}>{text}<a></p>',
    "url": "Deine persönliche Webseite:",
    "files": "Dateien",
    "settings": "Einstellungen",
    "user_settings": "Benutzerkonto",
    "acl": "Zugriffsberechtigungen",
    "acl_inherit": "ACL von folgender Seite verwenden ...",
    "acl_owner": "Besitzer:",
    "acl_writer": "Bearbeiter:",
    "acl_commenter": "Kommentator:",
    "acl_reader": "Leser:",
    "edit_title": "Seite bearbeiten",
    "comment_title": "Diesen Beitrag kommentieren ...",
    "comment": "Kommentar: ",
    "comments": "Kommentare ...",
    "comment_head": "<b>{url1}{user}{url2}</b> schrieb am %d.%m.%Y um %H:%M:",
    "comment_created": "Dein Kommentar wurde gespeichert.",
    "spam_challenge": "Bitte gib das {num} Wort an: <i>{words}</i>",
    "spam_nums": ["erste", "zweite", "dritte", "vierte", "fünfte"],
    "send": "Abschicken",
    "upload": "Hochladen",
    "delete": "Löschen",
    "delete_files": "Ausgewählte Dateien löschen",
    "move_copy_info": "Verschiebe oder kopiere die gewählten Dateien zu folgender Seite:",
    "move": "Verschieben",
    "copy": "Kopieren",
    "perm_login": "Angemeldet bleiben.",
    "register": "Registrieren",
    "no_edit": "Bearbeitung nicht möglich!",
    "terms": 'Ich akzeptiere die <a href="/site/impressum.de.html">Nutzungsbedingungen</a>.',
    "edit_time" :"Zuletzt bearbeitet am %d.%m.%Y um %H:%M.",
    "user_created": "<b>Benutzerkonto wurde erfolgreich angelegt.</b><br/>",
    "user_login": "<b>Anmeldung erfolgreich.</b><br/>",
    "logged_in": 'Du bist derzeit angemeldet als {user}.',
    "logout": 'Du kannst dich natürlich einfach <a href="{url}?logout">abmelden</a>.',
    "to_page": '<p>Weiter zur eigentlichen <a href="{url}">Seite</a>.</p>',
    "w_weak_pwd": "<b>Du hast ein unsicheres Passwort gewählt!</b></br>",
    "w_locked": "<b>Diese Datei wird seit %d.%m.%Y um %H:%M von {user} bearbeitet. "
        "Möglicherweise wurde die Bearbeitung abgebrochen, es kann hier allerdings "
        "zu einem Bearbeitungskonflikt kommen!</b></br>",
    "w_locked_self": "<b>Auf dieser Datei ist eine aktive Bearbeitungssperre, die "
        "am %d.%m.%Y um %H:%M von dir gesetzt wurde. Bevor du weitermachst, solltest "
        "du prüfen, ob du diese Seite noch in einem anderen Fenster zur Bearbeitung "
        "geöffnet hast.</b></br>",
    "e_locked": "<b>Diese Datei ist derzeit durch {user} in Bearbeitung.</b><br/>",
    "e_user_needed": "<b>Es muss ein Name angegeben werden.</b><br/>",
    "e_empty_comment": "<b>Der Kommentar ist zu kurz.</b></br>",
    "e_spam_check": "<b>Die Spamschutzfrage wurde falsch beantwortet</b></br>",
    "e_user_badname": "<b>Der Name enthält unzulässige Zeichen.</b></br>",
    "e_user_exists": "<b>Dieses Benutzerkonto kann nicht angelegt werden.</b><br/>",
    "e_mail_exists": "<b>Für diese E-Mail existiert bereits ein Nutzerkonto.</b><br/>",
    "e_mail_invalid": "<b>Das sieht nicht nach eine gültigen E-Mail-Adresse aus.</b><br/>",
    "e_url_invalid": "<b>Das sieht nicht nach einer gültigen URL aus.</b><br/>",
    "e_user_registered": "<b>Registrierter Nutzername. Bitte melde dich an, "
        "um mit diesem Namen zu kommentieren.</b></br>",
    "e_pwd_mismatch": "<b>Die angegebenen Passwörter stimmen nicht überein.</b><br/>",
    "e_incomplete": "<b>Anmeldeformular unvollständig ausgefüllt.</b></br>",
    "e_terms": "<b>Die Nutzungsbedingungen wurden nicht akzeptiert.</b></br>",
    "e_login": "<b>Benutzername oder Passwort falsch.</b><br/>",
    "e_cannot_create_dir": "<b>Eine neue Seite muss innerhalb "
        "eines bestehenden Verzeichnisses angelegt werden!</b><br/>",
    "e_no_login": "<b>Nur angemeldete Benutzer können Seiten bearbeiten</b><br/>",
    "e_401_title": '401 Zugriff verweigert',
    "e_401_generic": 'Nur angemeldete Benutzer können auf diese Resource zugreifen',
    "e_401_settings": 'Bitte melde dich an, um die Seiteneinstellungen zu bearbeiten.',
    "e_401_files": 'Der Zugriff auf das Dateiverzeichnis ist nur angemeldeten Nutzern möglich',
    "e_401_read": 'Diese Seite steht nur angemeldeten Nutzern zur Verfügung',
    "e_403_title": '403 Zugriff verweigert',
    "e_403_generic": 'Unzureichende Berechtigung zum Zugriff auf diese Resource',
    "e_403_settings": 'Unzureichende Berechtigung zum Bearbeiten der Einstellungen.',
    "e_403_files": 'Unzureichende Berechtigung zum Zugriff auf das Dateiverzeichnis',
    "e_403_read": 'Unzureichende Berechtigung zum Lesen dieser Seite',
    "e_404_title": '404 Nicht gefunden</h2>',
    "e_404_body": 'Keine Resource unter der angegebenen URL gefunden.',

}

S_EN = {
    "username": "Username:",
    "password": "Password:",
    "password_old": "Your current password:",
    "password_new": "Your new password:",
    "password_check": "Confirm password:",
    "mail": "E-mail address:",
    "url": "Your personal webpage:",
    "register": "Register account",
    "login": "Login",
    "link": '<a href="{url}"{more}>{text}<a></p>',
    "files": "Files",
    "settings": "Settings",
    "user_settings": "User account settings",
    "acl": "Access Control List",
    "acl_inherit": "Use the ACL from the following page ...",
    "acl_owner": "Owner:",
    "acl_writer": "Editor:",
    "acl_commenter": "Commenter:",
    "acl_reader": "Reader:",
    "edit_title": "Edit page",
    "comment_title": "Comment on this post ...",
    "comment": "Comment: ",
    "comments": "Comments ...",
    "comment_head": "<b>{url1}{user}{url2}</b> schrieb am %d.%m.%Y um %H:%M:",
    "comment_created": "Your comment was posted.",
    "spam_challenge": "Please write the {num} word: <i>{words}</i>",
    "spam_nums": ["first", "second", "third", "fourth", "fifth"],
    "send": "Send",
    "upload": "Upload",
    "delete_files": "Delete selected files",
    "delete": "Delete",
    "move_copy_info": "Move or copy files to the specified target page:",
    "move": "Move",
    "copy": "Copy",
    "no_edit": "You can't edit this page!",
    "perm_login": "Stay logged in",
    "user_created": "<b>User account created.</b><br/>",
    "user_login": "<b>You have logged in successfully.</b><br/>",
    "logged_in": '<p>You are currently logged in as {user}.</p>',
    "logout": '<p>If you want you can simply <a href="{url}?logout">logout</a>.</p>',
    "to_page": '<p>Continue to the <a href="{url}page">page</a>.</p>',
    "terms": 'I do accept the <a href="/site/impressum.en.html">terms of use</a>.',
    "edit_time": "Last edited on %Y/%m/%d at %I:%M %p",
    "w_weak_pwd": "<b>Your chosen password appears rather weak.</b></br>",
    "w_locked": "<b>This file was locked by {user} on %Y/%m/%d at %I:%M %p. "
        "Maybe the editing was cancelled, a editing conflict is possible!</b></br>",
    "w_locked_self": "<b>You locked this file for editing on %Y/%m/%d at %I:%M %p."
        "Please check if you have still an open edit window for this page.</b></br>",
    "e_locked": "<b>This page is currently locked by {user}.</b><br/>",
    "e_user_needed": "<b>You need to provide a name with this comment.</b><br/>",
    "e_empty_comment": "<b>Your comment is not long enough.</b></br>",
    "e_spam_check": "<b>You did not answer the anti spam challenge correctly</b></br>",
    "e_user_badname": "<b>The chosen name contains illegal characters.</b></br>",
    "e_user_exists": "<b>User account can't be created.</b><br/>",
    "e_mail_exists": "<b>This e-mail address is already registered.</b><br/>",
    "e_mail_invalid": "<b>That does not look like a valid e-mail address.</b><br/>",
    "e_url_invalid": "<b>That does not look like a valid url.</b><br/>",
    "e_user_registered": "<b>Registered username. Please login to post with this identity.",
    "e_pwd_mismatch": "<b>Passwords do not match.</b><br/>",
    "e_terms": "<b>You have to accept the terms of use to create an account.</b><br/>",
    "e_incomplete": "<b>Registration form incomplete.</b></br>",
    "e_login": "<b>Username or password incorrect.</b><br/>",
    "e_no_login": "</b>You need to log in to edit a page.</b><br/>",
    "e_cannot_create_dir": "<b>A new page must be a sub-directory to an existing directory!</b><br/>",
    "e_401_title": '401 Access Denied</h2>',
    "e_401_generic": 'Only logged in users can access this resource.',
    "e_401_settings": 'Please log in to edit page settings.',
    "e_401_files": 'Only logged in users may access this file directory.',
    "e_401_read": 'Only logged in users may access this page.',
    "e_403_title": '403 Access Denied',
    "e_403_generic": 'You are not authorized to access this resource',
    "e_403_settings": 'You are not authorized to change the settings of this page.',
    "e_403_files": 'You are not permitted to access this directory.',
    "e_403_read": 'You are not authorized to read this page.',
    "e_404_title": '404 Not Found',
    "e_404_body": 'Unfortunatly the server can&amp;t locate a file at this location.',
}

class WikiParse(object):
    def __init__(self, page, content):
        self.content = content

        self.base_dir = page.cnf["base_dir"]
        self.directory = page.directory
        self.name = page.name
        self.user_rank = page.data.get("user_rank")

        # keeping track of opened tags
        self.p = 0
        self.b = 0
        self.i = 0
        self.u = 0
        self.span = 0
        self.ol = 0
        self.ul = 0
        self.table = 0

    def parse(self):
        """ Parse the current content """

        parsed_content = []

        for line in self.content:

            # for everyone but global writers and owners
            # 'unsafe' chars are rewritten to html entities
            if self.user_rank not in ["writer", "owner"]:
                line = line.replace("&", "&amp;")
                line = line.replace("<", "&lt;")
                line = line.replace(">", "&gt;")
                line = line.replace("'", "&#39;")
                line = line.replace('"', "&quot;")

            # handling linebreaks
            line = line.replace("\r", "")
            line = line.replace("\n", "")
            if line.endswith("  "):
                line = line.strip()
                line += "<br/>"

            # parse headers
            if re.findall("(^~[tkp~]?~? )", line):
                # first close open tags ...
                parsed_content = self.terminate(parsed_content)

                if line.startswith("~p "):
                    line = "<h5>" + line[3:] + "</h5>"
                elif line.startswith("~~~ "):
                    line = "<h4>" + line[4:] + "</h4>"
                elif line.startswith("~~ "):
                    line = "<h3>" + line[3:] + "</h3>"
                elif line.startswith("~ "):
                    line = "<h2>" + line[2:] + "</h2>"
                elif line.startswith("~k "):
                    line = "<h2>" + line[3:] + "</h2>"
                elif line.startswith("~t "):
                    line = "<h2>" + line[3:] + "</h2>"
                parsed_content.append(line)
                continue  # headers do not allow further formatting

            # empty line terminates a lot of stuff!
            if len(line) == 0:
                parsed_content = self.terminate(parsed_content)
            else:
                # parse lists
                if line[0] in ["-", "*"]:
                    line, parsed_content = self.list_parse(line, parsed_content)
                elif line.startswith("~|"):
                    line = self.table_parse(line)
                # start paragraph
                elif self.p == 0:
                    line = "<p>" + line
                    self.p +=1

            # parse formatting
            # horizontal line
            line = line.replace("~=", "<hr/>")

            # bold, italic, underline ...
            biu_tags = re.findall("~[*_/]{1,3}|[*_/]{1,3}~", line)
            for tag in biu_tags:
                parsed_tag = ""
                for element in tag:
                    if element == "*":
                        parsed_tag += "<b>"
                        if tag.startswith("~"): self.b += 1
                        if tag.endswith("~"): self.b -= 1
                    elif element == "/":
                        parsed_tag += "<i>"
                        if tag.startswith("~"): self.i += 1
                        if tag.endswith("~"): self.i -= 1
                    elif element == "_":
                        parsed_tag += "<u>"
                        if tag.startswith("~"): self.i += 1
                        if tag.endswith("~"): self.i -= 1
                if tag.endswith("~"):
                    parsed_tag = parsed_tag.replace("<", "</")
                line = line.replace(tag, parsed_tag, 1)

            # color and size
            col_tags = re.findall("~@[0-9abcdef]{6}|~%\d+|[%@]~", line)
            for tag in col_tags:
                parsed_tag = ""
                if tag.startswith("~@"):
                    parsed_tag = '<span style="color:#' + tag[2:] + '">'
                elif tag.startswith("~%"):
                    parsed_tag = '<span style="font-size:' + tag[2:] + 'pt">'
                elif tag.endswith("~"):
                    parsed_tag = "</span>"

                line = line.replace(tag, parsed_tag, 1)

            # parse ~URL and ~WIKI
            urls = re.findall("~(?:WIKI|URL)\([^~]+\)=\S+", line)
            for url in urls:
                parsed_url = self.url_parse(url)
                line = line.replace(url, parsed_url)

            # parse ~IMG
            imgs = re.findall("~IMG\([^~]+\)=\S+", line)
            for img in imgs:
                parsed_img = self.img_parse(img)
                line = line.replace(img, parsed_img)

            parsed_content.append(line)
        return parsed_content

    def terminate(self, parsed_content):
        while self.b > 0:
            self.b -= 1
            parsed_content[-1] += "</b>"
        while self.i > 0:
            self.i -= 1
            parsed_content[-1] += "</i>"
        while self.u > 0:
            self.u -= 1
            parsed_content[-1] += "</u>"
        while self.ol > 0:
            self.ol -= 1
            parsed_content[-1] += '</ol>'
        while self.ul > 0:
            self.ul -= 1
            parsed_content[-1] += '</ul>'
        while self.span > 0:
            self.span -= 1
            parsed_content[-1] += '</span>'
        while self.p > 0:
            self.p -= 1
            parsed_content[-1] += '</p>'
            # remove unnecessary line breaks ...
            # parsed_content[-1] = parsed_content[-1].replace("<br/>", "")
        if self.table:
            self.table = 0
            parsed_content[-1] += '</table>'

        return parsed_content

    def url_parse(self, url_tag):
        options, target = url_tag.split(")=")

        if options.startswith("~URL"):
            options = options[5:]
        elif options.startswith("~WIKI"):
            options = options[6:]

        text = ""
        meta = ""

        # if no options
        if options == "":
            options = target
        if "," in options:
            options = options.split(",")
        else:
            options = [options]

        for option in options:
            if option.startswith("$"):
                pass
            else:
                text = option

        if url_tag.startswith("~WIKI"):
            dir = self.directory + [self.name]
            count = 0
            for char in target:
                if char != "_": break
                count += 1

            target = target[count:]
            target = target.replace("_", "/")

            if count == 0:
                dir = []

            if count == 1:
                if target == "/up":
                    target = ""
                    dir = dir[:-1]

            if count > 1:
                count -= 1
                dir = dir[:-count]

            target = "/".join([
                "",
                self.base_dir,
                *dir,
                target
            ])

        if url_tag.startswith("~URL"):
            meta = 'target="__new" '

            target = target.replace("&amp;", "&")


        parsed_url = '<a href="{target}" {more}/>{text}</a>'.format(
            target=target,
            more=meta,
            text=text
        )
        return parsed_url

    def img_parse(self, img_tag):
        data = {}
        *options, target = img_tag.split("=")
        options = "=".join(options)
        options = options[5:-1]

        text = ""
        meta = ""
        cls = ""

        if "," in options:
            options = options.split(",")
        else:
            options = [options]

        for option in options:
            if option.startswith("$"):
                if "=" in option:
                    name, value = option.split("=")
                    if name[1:] == "align":
                        if value == "left":
                            data["class"] = 'class="left"'
                        elif value == "center":
                            data["class"] = 'class="center"'
                        elif value == "right":
                            data["class"] = 'class="right"'
                    if name[1:] == "width":
                        value = re.subn("[^[\d]", "", value)[0]
                        if int(value) > 100:
                            value = "100"
                        data["width"] = ' width="' + value + '%"'
                    if name[1:] == "subtitle":
                        data["subtitle"] = True
            else:
                text = option

        # aquire the image location
        dir = self.directory + [self.name]
        count = 0
        for char in target:
            if char != "_": break
            count += 1

        target = target[count:]
        target = target.replace("_", "/")

        if count == 0:
            dir = []

        if count == 1:
            pass

        if count > 1:
            count -= 1
            dir = dir[:-count]

        target = "/".join([
            "",
            self.base_dir,
            *dir,
            target
        ])

        if data.get("subtitle") == True:
            sub1 = " ".join(["<div", data.get("class", ""), data.get("width", "")])
            if data.get("width"):
                meta += ' width="100%" '
            sub1 = sub1.strip() + '>'
            sub2 = '<p class="subtitle">' + text + '</div>'
        else:
            sub1 = ""
            sub2 = ""
            meta += " ".join([data.get("width", ""), data.get("class", "")])

        parsed_img = '{sub1}<img src="{target}" {more} alt="{text}" title="{text}" />{sub2}'.format(
            sub1=sub1,
            target=target,
            more=meta,
            text=text,
            sub2=sub2,
        )

        return parsed_img

    def list_parse(self, line, parsed_content):
        """ Parses ordered and unordered lists """

        ul = 0
        ol = 0

        for letter in line:
            if letter == "*": ul += 1
            if letter == "-": ol += 1
            if letter not in ["*", "-"]: break

        # no mixup !!
        if ul > 0 and ol > 0:
            return line, parsed_content

        # remove the markup
        line = line[ul+ol:].strip()

        # mark the line as list_item
        line = '<li>' + line + '</li>'

        # handle unordered lists
        if ul > 0:
            while self.ul < ul:
                line = '<ul>' + line
                self.ul += 1

            while self.ul > ul:
                parsed_content[-1] += '</ul>'
                self.ul -= 1
        else:
            while self.ul > ul:
                parsed_content[-1] += '</ul>'
                self.ul -= 1

        # handle ordered lists
        if ol > 0:
            while self.ol < ol:
                line = '<ol>' + line
                self.ol += 1
            while self.ol > ol:
                parsed_content[-1] += '</ol>'
                self.ol -= 1
        else:
            while self.ol > ol:
                parsed_content[-1] += '</ol>'
                self.ol -= 1

        return line, parsed_content

    def table_parse(self, line):
        line = line.replace("~|", "").replace("|~", "")
        cols = line.split("|")

        # defintion line!
        if self.table == 0:
            self.table = {"line_num": 0}
            table = '<table'
            total_width = 0
            colgroup = "<colgroup>"

            for i, data in enumerate(cols):
                line_width = 0
                if i == 0 and " " in data and len(data) > 2:
                    line_width, *data = data.split()
                    data = " ".join(data)
                    line_width = re.subn("[^\d]", "", line_width)
                align = data[-1]
                width = re.subn("[^\d]", "", data)[0]
                if align == "l": align = "left"
                elif align == "c": align = "center"
                elif align == "r": align = "right"
                elif align == "j": align = "justify"
                else: align = None

                col = '<col'
                if align:
                    col += ' align="'+align+'"'
                if width:
                    col += ' width="'+width+'%"'
                    total_width += int(width)

                col += '/>'
                colgroup += col

            if total_width:
                table += ' width="'+str(total_width)+'%"'
            table += '>'
            colgroup += '</colgroup>'
            return table + colgroup

        # any other line
        parsed_line = '<tr>'
        for i, data in enumerate(cols):
            color = ""
            if data.startswith("("):
                col_value = re.subn("[^a-f0-9]", "", data[1:7])[0]
                color = ' bgcolor = "#'+ col_value + '"'
                data = data[8:]
            cell = '<td'
            if color: cell += color
            cell += '>' + data + '</td>'
            parsed_line += cell
        parsed_line += '</tr>'

        return parsed_line


class SimplePage(object):
    def __init__(self):
        self.msg = {}
        self.post = None
        self.cnf = None
        self.name = ""
        self.directory = []
        self.lang = ""
        self.status = "200 OK"
        self.query = []
        self.content = []
        self.secondary = None
        self.data = {}

    def make_config(self):
        self.cnf = {
            "base_url": "https://www.eric-poehlsen.de/site",
            "base_dir": "site",
            "file_ext": "wiki",
            "old_name": "old",
            "cur_name": "cur",
            "comments": "com",
            "acl_name": "acl",
            "stat_name": "static",
            "languages": ["de", "en"],
            "lock_time": 1800,
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
            if ext[0] in self.cnf["languages"]:
                self.lang = ext[0]

            ext = ext[-1]

    def post_handler(self):
        """ handle a post request by the user agent """

        if os.environ["REQUEST_METHOD"] == "POST":
            self.post = cgi.FieldStorage()
            if self.query[0] in ["login", "logout"]:
                self.post_login()
            if self.query[0] == "register":
                self.post_register()
            if self.query[0] == "user":
                self.post_user()
            if self.query[0] == "edit":
                self.post_edit()
            if self.query[0] == "files":
                self.post_files()
            if self.query[0] == "settings":
                self.post_settings()
            if self.post.getvalue("comment"):
                self.post_comment()

    def post_login(self):
        """ login in a user with the credentials transmitted via POST """

        # the relevant field data ...
        perm = self.post.getvalue("perm_login")
        user = self.post.getvalue("user")
        pwd = self.post.getvalue("pwd")

        self.data["error"] = err = []
        self.data["login"] = False

        invalid_username = re.findall("[^a-zA-Z0-9]", user)
        if invalid_username:
            err.append(self.msg["e_user_badname"])
            return

        # get the user file
        path = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            "users." + self.cnf["file_ext"]
        )
        userfile = open(path, mode="r", encoding="utf-8")
        user_data = userfile.readlines()
        userfile.close()

        modified = []
        for entry in user_data:
            if entry.count(" ") != 7: continue
            username, pwd_hash, usermail, userurl, rank, session, expires, ip = entry.split()

            now = time.time()
            expires = float(expires)
            # remove expired sessions:
            if now > expires:
                session = "-"
                expires = "0"
                ip = "-"

            # check if given credentials match a user
            if username == user:
                pwd = bytes(pwd, encoding="utf-8")
                chk = bytes(pwd_hash, encoding="utf-8")
                if bcrypt.checkpw(pwd, chk):
                    # found a match ...

                    self.data["login"] = True
                    self.data["user"] = user

                    # create a new session for this login
                    session = new_id = str(uuid.uuid4())

                    if perm:
                        valid_for = 86400 * 180
                    else:
                        valid_for = 3600
                    expires = now + valid_for

                    if os.environ.get('HTTP_X_FORWARDED_FOR'):
                        ip = os.environ['HTTP_X_FORWARDED_FOR']
                        ip = ip.split(',')[0].strip()
                    else:
                        ip = os.environ['REMOTE_ADDR']

                    # create the session cookie
                    cookie = Cookie()
                    cookie["session"] = new_id
                    if perm:
                        cookie["session"]["expires"] = valid_for
                    cookie["session"]["domain"] = os.environ["HTTP_HOST"]
                    cookie["session"]["path"] = "/" + self.cnf["base_dir"]
                    self.data["cookie"] = cookie.output()
                # user exists but password is wrong ...
                else:
                    err.append(self.msg["e_login"])

            # write the (modified) record to the list
            entry = [
                username,
                pwd_hash,
                usermail,
                userurl,
                rank,
                session,
                str(expires),
                ip
            ]
            entry = " ".join(entry) + "\n"
            modified.append(entry)

        # write the modified login list on a successful login
        if modified and self.data["login"]:
            userfile = open(path, mode="w", encoding="utf-8")
            userfile.writelines(modified)
            userfile.close()

        # looks like the username does not exists ...
        if not self.data["login"]:
            err.append(self.msg["e_login"])

    def post_register(self):
        """ handle registering of a new user with the given data ..."""

        # read the fields
        user = self.post.getvalue("user")
        pwd = self.post.getvalue("pwd")
        pwd_check = self.post.getvalue("pwd_check")
        url = self.post.getvalue("url", "-")
        mail = self.post.getvalue("mail")
        terms = self.post.getvalue("terms")

        self.data["warn"] = warn = []
        self.data["error"] = err = []
        if not user or not pwd or not pwd_check or not mail or not terms:
            err.append(self.msg["e_incomplete"])
            return

        # get current users
        path = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            "users." + self.cnf["file_ext"]
        )
        userfile = open(path, mode="r", encoding="utf-8")
        user_data = userfile.readlines()
        userfile.close()

        # username okay?
        illegal = re.findall("[^a-zA-Z0-9]", user)
        if len(illegal) > 0:
            err.append(self.msg["e_user_badname"])

        # mail okay?
        if mail.count("@") != 1 and mail.count(".") < 1:
            err.append(self.msg["e_mail_invalid"])
        mail = mail.replace(" ", "")
        mail = mail.replace("<", "")
        mail = mail.replace(">", "")

        # url okay?
        if len(url) > 1 and not url.startswith("http"):
            err.append(self.msg["e_url_invalid"])
        elif len(url) <= 1:
            url = "-"
        url = url.replace(" ", "")
        url = url.replace("<", "")
        url = url.replace(">", "")

        # username or mail already registered?
        for entry in user_data:
            if entry.count(" ") != 7: continue
            username, pwd_hash, usermail, userurl, rank, session, time, ip = entry.split()
            if username == user:
                err.append(self.msg["e_user_exists"])
                break
            if usermail == mail:
                err.append(self.msg["e_mail_exists"])
                break

        # passwords okay?
        if pwd != pwd_check:
            err.append(self.msg["e_pwd_mismatch"])

        # weak password?
        words = []
        for lang in self.cnf["languages"]:
            word_path = os.path.join(
                os.environ["DOCUMENT_ROOT"],
                self.cnf["base_dir"],
                "words." + lang + "." + self.cnf["file_ext"]
            )
            file = open(word_path, mode="r", encoding="utf-8")
            words += list(file.readlines())
            file.close()
        words = set([w.lower().strip() for w in words])
        special = re.findall("[^a-zA-Z0-9]", pwd)
        nums = re.findall("[\d]", pwd)
        upper = re.findall("[A-Z]", pwd)
        word_att = pwd.lower in words
        short = len(pwd) < 8
        if not special or not nums or not upper or word_att or short:
            self.data["warn"] += self.msg["w_weak_pwd"]

        # terms accepted?
        if not terms:
            err.append(self.msg["e_terms"])

        if len(err) > 0:
            return

        pwd_hash = bcrypt.hashpw(bytes(pwd, encoding="utf-8"), bcrypt.gensalt())
        user_entry = "{user} {pwd_hash} {mail} {url} visitor - 0 -\n".format(
            user=user,
            pwd_hash=pwd_hash.decode("utf-8"),
            mail=mail,
            url=url,
        )
        userfile = open(path, mode="a", encoding="utf-8")
        userfile.write(user_entry)
        userfile.close()

    def post_user(self):
        """ handle updating user data  ..."""

        # read the fields
        user = self.data.get("user")
        pwd = self.post.getvalue("pwd", "")
        pwd_new = self.post.getvalue("pwd_new", "")
        pwd_check = self.post.getvalue("pwd_check", "")
        url = self.post.getvalue("url", "-")
        mail = self.post.getvalue("mail", "")

        self.data["error"] = err = []

        # get current users
        path = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            "users." + self.cnf["file_ext"]
        )
        userfile = open(path, mode="r", encoding="utf-8")
        user_data = userfile.readlines()
        userfile.close()

        edited_user_data = []
        for entry in user_data:
            if entry.count(" ") != 7: continue
            user_name, pwd_hash, old_mail, old_url, rank, session, expires, ip = entry.split()
            if user_name == user:

                # changing password?
                if len(pwd) + len(pwd_check) + len(pwd_new) > 0:
                    # check current password:
                    check = bcrypt.checkpw(
                        bytes(pwd, encoding="utf-8"),
                        bytes(pwd_hash, encoding="utf-8")
                    )
                    # passwords okay?
                    if not check or pwd_new != pwd_check:
                        err.append(self.msg["e_pwd_mismatch"])
                    # the new password_hash
                    else:
                        pwd_hash = bcrypt.hashpw(bytes(pwd_new, encoding="utf-8"), bcrypt.gensalt())
                        pwd_hash = pwd_hash.decode(encoding="utf-8")

                if mail.count("@") != 1 and mail.count(".") < 1:
                    err.append(self.msg["e_mail_invalid"])

                if len(url) > 1 and not url.startswith("http"):
                    err.append(self.msg["e_url_invalid"])
                elif len(url) <= 1:
                    url = "-"

                if len(err) == 0:
                    user_entry = " ".join([
                        user,
                        pwd_hash,
                        mail,
                        url,
                        rank,
                        session,
                        expires,
                        ip
                    ])
                else:
                    user_entry = entry

                edited_user_data.append(user_entry)

            else:
                edited_user_data.append(entry)

        userfile = open(path, mode="w", encoding="utf-8")
        userfile.writelines(edited_user_data)
        userfile.close()

    def post_edit(self):
        """ handle the page edit, store old version write new version"""

        # check user rank for writing rights:
        if self.data.get("rank") not in ["writer", "owner"]:
            return

        content = self.post.getvalue("content")

        dir = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            *self.directory,
            self.name
        )
        
        cur_filename = "{name}.{lang}.{ext}".format(
            name=self.cnf["cur_name"],
            lang=self.lang,
            ext=self.cnf["file_ext"]
        )

        cur_name = os.path.join(dir, cur_filename)

        # store the old version of the file ...
        if os.path.exists(cur_name):
            old_base_name = "{name}.{lang}*".format(
                name=self.cnf["old_name"],
                lang=self.lang,
            )
            old_base_name = os.path.join(dir, old_base_name)
            old_versions = glob.glob(old_base_name)

            new_num = 0
            l_ext = len(self.cnf["file_ext"]) + 1
            for version in old_versions:
                try:
                    num = int(version[-(l_ext + 6):-l_ext])
                    if num > new_num:
                        new_num = num
                except ValueError: pass
            new_num += 1

            old_name = "{name}.{lang}.{num}.{ext}".format(
                name = self.cnf["old_name"],
                lang = self.lang,
                num = str(new_num).zfill(6),
                ext = self.cnf["file_ext"]
            )
            old_name = os.path.join(dir, old_name)
            os.rename(cur_name, old_name)

        content = content.replace("\r", "")
        content = content.split("\n")

        # prepare meta information ...
        if os.environ.get('HTTP_X_FORWARDED_FOR'):
            ip = os.environ['HTTP_X_FORWARDED_FOR']
            ip = ip.split(',')[0].strip()
        else:
            ip = os.environ.get('REMOTE_ADDR', "NO_IP")

        meta = [
            str(self.data.get("user")),
            str(time.time()),
            ip
        ]

        file = open(cur_name, "w", encoding="utf-8")
        file.write("\n".join(content + meta))
        file.close()

        lock_file = os.path.join(dir, ".lock")
        if os.path.exists(lock_file):
            os.remove(lock_file)

    def post_comment(self):
        """ comment posting """

        # does the current user have sufficient rights?
        if self.data.get("rank") not in ["commenter", "writer", "owner"]:
            return

        # retrieve the fields
        username = self.post.getvalue("user")
        url = self.post.getvalue("url")
        check = self.post.getvalue("check")
        challenge = self.post.getvalue("challenge")
        comment = self.post.getvalue("comment")
        terms = self.post.getvalue("terms")
        
        self.data["error"] = []

        # check for the presence of field data ...
        if not username:
            self.data["error"].append(self.msg["e_user_needed"])
        if not url: url = ""

        if not terms:
            self.data["error"].append(self.msg["e_terms"])

        if not check:
            self.data["error"].append(self.msg["e_spam_check"])
        else:
            hash = bytes(challenge, encoding="utf-8")
            check = bytes(check, encoding="utf-8")
            if not bcrypt.checkpw(check, hash):
                self.data["error"].append(self.msg["e_spam_check"])

        if not comment:
            self.data["error"].append(self.msg["e_empty_comment"])
        elif len(comment) < 5:
                self.data["error"].append(self.msg["e_empty_comment"])

        if len(self.data["error"]) > 0: return

        # cleanup the data: 
        def strip(data, amp=True):
            """ small helper function to remove unsave characters """

            if amp: data = data.replace("&", "&amp;")
            data = data.replace("<", "&lt;")
            data = data.replace(">", "&gt;")
            data = data.replace('"', "&quot;")
            data = data.replace("'", "&#39;")
            return data

        username = strip(username)
        comment = strip(comment)
        url = strip(url, amp=False)

        # getting time and poster IP
        now = str(time.time())
        if os.environ.get('HTTP_X_FORWARDED_FOR'):
            user_ip = os.environ['HTTP_X_FORWARDED_FOR']
            user_ip = user_ip.split(',')[0].strip()
        else:
            user_ip = os.environ['REMOTE_ADDR']

        # check if selected name is a registered name:
        userfile = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            "users." + self.cnf["file_ext"]
        )
        users = open(userfile, mode="r", encoding="utf-8")
        user_data = users.readlines()
        users.close()
        for user in user_data:
            user = user.split()[0]
            if user == username:
                if user != self.data.get("user"):
                    self.data["error"].append(self.msg["e_user_registered"])
                    return
                break

        # build relevant filenames
        dir = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            *self.directory,
            self.name
        )

        search = "".join([
            dir,
            "/",
            self.cnf["comments"],
            "*.",
            self.cnf["file_ext"]
        ])

        current_comments = glob.glob(search)
        l_ext = len(self.cnf["file_ext"]) + 1

        highest = 0
        for c in current_comments:
            num = c[-(l_ext+6):-l_ext]
            if num.isdigit():
                num = int(num)
                if num > highest: highest = num

        highest += 1
        
        filename = "{name}.{num}.{ext}".format(
            name=self.cnf["comments"],
            num = str(highest).zfill(6),
            ext = self.cnf["file_ext"]
        )

        # store comment
        comment_data = "\n".join([username, url, now, user_ip, comment])

        path = os.path.join(dir, filename)
        file = open(path, mode="w", encoding="utf-8")
        file.write(comment_data),
        file.close()

    def post_files(self):
        """ handle the post requests of the files form """

        # does the current user have sufficient rights?
        if self.data.get("rank") not in ["writer", "owner"]:
            return

        import shutil

        dir = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            *self.directory,
            self.name
        )

        selection = self.post.getvalue("sel")
        if selection and not isinstance(selection, list):
            selection = [selection]

        # remove a file
        delete = self.post.getvalue("del")
        if delete:

            for filename in selection:
                path = os.path.join(dir, filename)
                if os.path.isfile(path):
                    os.remove(path)

        # parse target
        target = self.post.getvalue("target")
        new_dir = self.directory + [self.name]
        if target:
            count = 0
            for char in target:
                if char != "_": break
                count += 1

            target = target[count:]
            target = target.replace("_", "/")

            if count == 0:
                new_dir = []

            if count == 1:
                pass

            if count > 1:
                count -= 1
                new_dir = new_dir[:-count]

            new_dir = os.path.join(
                os.environ["DOCUMENT_ROOT"],
                *new_dir,
                target
            )

        # move a file to a different folder
        move = self.post.getvalue("move")
        if move and target and selection:
            for filename in selection:
                old_path = os.path.join(dir, filename)
                new_path = os.path.join(new_dir, filename)

        # move a file to a different folder
        copy = self.post.getvalue("copy")
        if copy and target and selection:
            for filename in selection:
                old_path = os.path.join(dir, filename)
                new_path = os.path.join(new_dir, filename)

        # handle a file upload ...
        if "file" not in self.post: return

        files = self.post["file"]
        if not isinstance(files, list):
            files = [files]

        dir = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            *self.directory,
            self.name
        )

        for file in files:
            if not file.file: continue
            if len(file.filename) < 1: continue


            path = os.path.join(dir, file.filename)
            num = 1
            while os.path.exists(path):
                if "." in file.filename:
                    *name, ext = file.filename.split(".")
                    name = ".".join(name)
                    ext = "." + ext
                else:
                    name = file.filename
                    ext = ""
                new_name = name + str(num) + ext
                path = os.path.join(dir, new_name)
                num += 1

            with open(path, 'wb') as new_file:
                shutil.copyfileobj(file.file, new_file, 100000)

    def post_settings(self):
        """ handle the post data for the setting page"""

        # secondary check to make sure the user is authenticated
        if self.data.get("rank") != "owner":
            return

        def strip(data, inherit = False):
            if inherit:
                return re.subn("[^a-zA-Z0-9/]", "", data)[0]
            return re.subn("[^a-zA-Z0-9#\n]", "", data)[0]

        owner = strip(self.post.getvalue("owner", self.data.get("user", "")))
        writer = strip(self.post.getvalue("writer", ""))
        commenter = strip(self.post.getvalue("commenter", ""))
        reader = strip(self.post.getvalue("reader", ""))
        inherit = strip(self.post.getvalue("inherit", ""), inherit=True)

        owner = ":owner\n" + owner
        writer = ":writer\n" + writer
        commenter = ":commenter\n" + commenter
        reader = ":reader\n" + reader

        acl_data = "\n".join([owner, writer, commenter, reader])

        if inherit:
            acl_data = "!" + inherit + "\n"

        path = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            *self.directory,
            self.name,
            self.cnf["acl_name"] + "." + self.cnf["file_ext"]
        )
        if owner == "" and inherit == "":
            os.remove(path)
        else:
            acl = open(path, mode="w", encoding="utf-8")
            acl.write(acl_data)
            acl.close()

    def query_del(self):
        num = None
        for entry in self.query:
            if entry.startswith("del"):
                num = entry.split("=")[-1]
                break

        if not num or not num.isdigit():
            return

        if self.data.get("rank") not in ["writer", "owner"]:
            if self.data.get("user"):
                self.e403()
                return
            else:
                self.e401()
                return

        num = num.zfill(6)

        filename = self.cnf["comments"] + "." + num + "." + self.cnf["file_ext"]

        path = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            *self.directory,
            self.name,
            filename
        )

        if os.path.isfile(path):
            os.remove(path)

    def query_logout(self, session_id):

        root = os.environ["DOCUMENT_ROOT"]
        base = self.cnf.get("base_dir")
        users = "users." + self.cnf["file_ext"]
        path = os.path.join(root, base, users)
        user_file = open(path, "r", encoding="utf-8")
        user_data = user_file.readlines()
        user_file.close()

        logged_out = False
        new_data = []
        for entry in user_data:
            if entry.count(" ") != 7: continue
            user, pwd_hash, mail, url, rank, stored_id, expires, ip = entry.split()
            if stored_id == session_id:
                stored_id = " "
                expires = "0"
                ip = " "
                logged_out = True

            new_entry = [user, pwd_hash, mail, url, rank, stored_id, expires, ip]
            new_entry = " ".join(new_entry) + "\n"
            new_data.append(new_entry)

        if logged_out:
            sessions_file = open(path, "w", encoding="utf-8")
            sessions_file.writelines(new_data)
            sessions_file.close()

    def cookie_handler(self):
        """ The user supplied a cookie - is it valid? """

        cookie = os.environ.get("HTTP_COOKIE")

        if cookie:
            session_id = cookie.split("=")[-1]

            # validate cookie content (it is user input after all)
            valid = re.match(
                "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
                session_id
            )
            if not valid:
                return

            # did the user request a logout?
            if self.query[0] == "logout":
                self.query_logout(session_id)
                return

            # check validity of cookie and assign user data
            root = os.environ["DOCUMENT_ROOT"]
            base = self.cnf.get("base_dir")
            users = "users." + self.cnf["file_ext"]
            path = os.path.join(root, base, users)
            user_file = open(path, "r", encoding="utf-8")
            user_data = user_file.readlines()
            user_file.close()

            for entry in user_data:
                if entry.count(" ") != 7: continue
                user, pwd_hash, mail, url, rank, stored_id, expires, ip = entry.split()
                if stored_id == session_id:
                    self.data["user"] = user
                    self.data["login"] = True
                    self.data["user_url"] = url if url != "-" else ""
                    self.data["user_mail"] = mail

                    # set global rank (if enabled)
                    if self.cnf.get("rank_override"):
                        self.data["user_rank"] = rank.strip()
                    break

    def check_acl(self):
        """ find and check the appropriate access control list """

        acl = []
        local_dir = [d for d in self.directory] + [self.name]

        # traverse the directory tree up until one is found
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

                # check if that acl is a 'link'
                while acl[0].startswith("!"):
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
                    else: break

        # retrieve user rank from selected access control list
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

    def get_lang(self):
        """ Autodetect the users language for the HTTP_ACCEPT_LANGUAGE"""

        if not self.lang:
            default = self.cnf["languages"][0]
            user_languages = os.environ.get("HTTP_ACCEPT_LANGUAGE", default)
            invalid = re.findall("[^a-zA-Z0-9\.\-,;=]+", user_languages)

            # autodetect preferred language .. .
            if not invalid:
                user_languages = re.split("[,;]", user_languages)[::-1]
                q = 0
                languages = []
                for entry in user_languages:
                    if entry.startswith("q="):
                        try:
                            q = float(entry[2:])
                        except ValueError:
                            q = 0
                    else:
                        lang = entry[0:2]
                        languages.append([q, lang.lower()])
                languages = sorted(languages, reverse=True)
                for lang in languages:
                    if lang[1] in self.cnf["languages"]:
                        self.lang = lang[1]
                else:
                    self.lang = default

        # set message strings
        if self.lang == "de":
            self.msg = S_DE
        if self.lang == "en":
            self.msg = S_EN
        else:
            self.msg = S_EN

    def headers(self, status="200 OK", cont_type="text/plain"):
        """ prepare the header string """

        header = "Status: " + status + "\n"
        header += "Content-Type: " + cont_type + "\n"

        # setting cookie if login is successful
        login = self.data.get("login")
        cookie = self.data.get("cookie")
        if login and cookie:
            header += cookie + "\n"
        header += "\n"

        return header

    def html_head(self):
        filename = "_header." + self.lang + "." + self.cnf["file_ext"]
        path = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            filename
        )
        file = open(path, mode="r", encoding="utf-8")
        for line in file:
            self.content.append(line)
        file.close()

    def page_menu(self):
        """ build pages menu and language selector """

        content = [
            '<div class="main">'
            '<div class="lang">'
        ]
        base_dir = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            *self.directory,
            self.name
        )

        base_url = "/".join([
            self.cnf["base_dir"],
            *self.directory,
            self.name
        ])

        if base_url.endswith("/"): base_url = base_url[:-1]

        link_base = '<a href="{url}"><img {cls}src="{src}" title="{txt}" alt="{txt}"/></a>'

        if self.data.get("rank") in ["writer", "owner"]:
            # adding the edit icon ...
            url = "/" + base_url + "." + self.lang + "?edit"
            src = "/" + self.cnf["base_dir"] + "/edit.png"

            edit_button = link_base.format(
                url=url,
                src=src,
                txt=self.msg["edit_title"],
                cls='class="icon_button"'
            )
            content.append(edit_button)

            # and the files icon
            url = "/" + base_url + "." + self.lang + "?files"
            src = "/" + self.cnf["base_dir"] + "/folder.png"

            files_button = link_base.format(
                url=url,
                src=src,
                txt=self.msg["edit_title"],
                cls='class="icon_button"'
            )
            content.append(files_button)

        # adding a setting button
        if self.data.get("rank") == "owner":
            url = "/" + base_url + "." + self.lang + "?settings"
            src = "/" + self.cnf["base_dir"] + "/settings.png"

            set_button = link_base.format(
                url=url,
                src=src,
                txt=self.msg["settings"],
                cls='class="icon_button"'
            )
            content.append(set_button)

        # user management button
        if self.data.get("user"):
            url = "/" + base_url + "." + self.lang + "?user"
            src = "/" + self.cnf["base_dir"] + "/user.png"

            user_button = link_base.format(
                url=url,
                src=src,
                txt=self.msg["user_settings"],
                cls='class="icon_button"'
            )
            content.append(user_button)

        # this is the language selector
        for lang in self.cnf["languages"]:
            path = os.path.join(
                base_dir,
                "{cur}.{lang}.{ext}".format(
                    cur=self.cnf["cur_name"],
                    lang=lang,
                    ext=self.cnf["file_ext"]
                )
            )
            if os.path.exists(path):
                url = "/" + base_url + "." + lang
                src = "/" + self.cnf["base_dir"] + "/flag." + lang + ".png"

                img = link_base.format(
                    url=url,
                    src=src,
                    txt=lang.upper(),
                    cls='class="lang_img"'
                )
                content.append(img)
        content += ['</div>', '</div>']

        self.content += content

    def nav_bar(self):
        """ Add the appropriate navbar to the site """

        filename = "_navbar." + self.lang + "." + self.cnf["file_ext"]
        path = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            filename
        )
        file = open(path, mode="r", encoding="utf-8")
        for line in file:
            self.content.append(line)
        file.close()

    def show_login_form(self):
        """writes the login form into the page content list"""

        content = [
            '<div class="main">',
            '<h2>' + self.msg["login"] + '</h2>',
        ]

        if os.environ["REQUEST_METHOD"] == "POST":
            if self.data.get("error"):
                content += ['<div class="error">'] + self.data["error"] + ["</div>"]
            else:
                content += [self.msg["user_login"] + "<br/>"]

        # current page base_url for links
        url = os.path.join(
            "/",
            self.cnf["base_dir"],
            *self.directory,
            self.name
        )

        # is user currently logged in?
        if self.data.get("user"):
            user = self.data["user"]
            content += [
                '<p>' + self.msg["logged_in"].format(user=user) + '<br/>',
                self.msg["logout"].format(url=url) + '</p>',
                self.msg["to_page"].format(url=url),
            ]
        # nope, display login form
        else:
            content += [
                '<form method="post">',
                '<p>' + self.msg["username"],
                '<input type="text" name="user" /></p>',
                '<p>' + self.msg["password"],
                '<input type="password" name="pwd" /></p>',
                '<p><input type="checkbox" name="perm_login" class="small" />',
                self.msg["perm_login"] + '</p>',
                '<button name="' + self.msg["login"] + '">' + self.msg["login"] + '</button>'
                '<a class="menu" href="' + url + '?register">' + self.msg["register"] + '</a>'
                '</form>'
            ]
        content += ['</div>']
        self.content += content

    def show_user_form(self):
        """writes the login form into the page content list"""

        # only logged in users can changes user data
        if not self.data.get("user"):
            self.e401()
            return

        # we need the currently stored data ...
        path = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            "users." + self.cnf["file_ext"]
        )

        user_file = open(path, mode="r", encoding="utf-8")
        user_data = user_file.readlines()
        user_file.close()

        user = self.data.get("user")
        self.data["user_mail"] = mail = ""
        self.data["user_url"] = url = ""

        for entry in user_data:
            user_name, pwd_hash, mail_stored, url_stored, *session = entry.split()
            if user == user_name:
                mail = mail_stored
                url = url_stored
                break

        content = [
            '<div class="main">',
            '<h2>' + self.msg["user_settings"] + '</h2>',
        ]

        if os.environ["REQUEST_METHOD"] == "POST":
            if self.data.get("error"):
                content += ['<div class="error">'] + self.data["error"] + ["</div>"]

        content += [
            '<form method="post">',
            '<p>' + self.msg["username"] + '<br/>',
            '<b>' + user + '</b></p>',
            '<p>' + self.msg["mail"] + '<br/>',
            '<input type="email" name="mail"  value="' + mail + '"/></p>',
            '<p>' + self.msg["url"] + '<br/>',
            '<input type="url" name="url"  value="' + url + '"/></p>',
            '<p>' + self.msg["password_old"] + '<br/>',
            '<input type="password" name="pwd" /></p>',
            '<p>' + self.msg["password_new"] + '<br/>',
            '<input type="password" name="pwd_new" /></p>',
            '<p>' + self.msg["password_check"] + '<br/>',
            '<input type="password" name="pwd_check" /></p>',
            '<button name="' + self.msg["send"] + '">' + self.msg["send"] + '</button>',
            '</form>',
        ]
        content += ['</div>']
        self.content += content


    def show_registration_form(self):
        """writes the registration form into the page content list"""

        created = False
        user = ""
        url = ""
        mail = ""
        content = [
            '<div class="main">',
            '<h2>' + self.msg["register"] + '</h2>',
        ]

        if os.environ["REQUEST_METHOD"] == "POST":
            user = self.post.getvalue("user", "")
            mail = self.post.getvalue("mail", "")
            url = self.post.getvalue("url", "")

            if self.data.get("error"):
                content += ['<div class="error">'] + ["".join(self.data["error"])] + ["</div>"]
            else:
                if self.data.get("warn"):
                    content += ['<div class="warn">'] + ["".join(self.data["warn"])] + ["</div>"]
                content += [self.msg["user_created"] + "<br/>"]
                created = True

        if not created:
            if self.data.get("warn"):
                content += ['<div class="warn">'] + self.data["warn"] + ["</div>"]
            content += [
                '<form method="post">',
                '<p>' + self.msg["username"] + '<br/>',
                '<input type="text" name="user" value="' + user + '"/></p>',
                '<p>' + self.msg["mail"] + '<br/>',
                '<input type="email" name="mail"  value="' + mail + '"/></p>',
                '<p>' + self.msg["url"] + '<br/>',
                '<input type="url" name="url"  value="' + url + '"/></p>',
                '<p>' + self.msg["password"] + '<br/>',
                '<input type="password" name="pwd" /></p>',
                '<p>' + self.msg["password_check"] + '<br/>',
                '<input type="password" name="pwd_check" /></p>',
                '<p><input type="checkbox" name="terms" class="small" />',
                self.msg["terms"]+'</p>',
                '<button name="' + self.msg["register"] + '">' + self.msg["register"] + '</button>',
                '</form>',
            ]

        content += ['</div>']
        self.content += content

    def show_comment_form(self):
        """adds a comment form to the page contents"""

        if self.data.get("rank") not in ["owner", "writer", "commenter"]:
            return


        created = False
        content = [
            '<div class="main">',
            '<h3>' + self.msg["comment_title"] + '</h3>',
        ]

        user = self.data.get("user", "")
        comment = ""
        url = self.data.get("user_url", "")

        if os.environ["REQUEST_METHOD"] == "POST":
            if "user" in self.post:
                user = self.post.getvalue("user")
            if "comment" in self.post:
                comment = self.post.getvalue("comment")
            if "url" in self.post:
                url = self.post.getvalue("url")

            if self.data.get("error"):
                content += ['<div class="error">'] + self.data["error"] + ["</div>"]
            elif len(comment) > 0:
                content += [self.msg["comment_created"] + "<br/>"]
                created = True

        if not created:
            # spam challenge
            path = os.path.join(
                os.environ["DOCUMENT_ROOT"],
                self.cnf["base_dir"],
                "words." + self.lang + "." + self.cnf["file_ext"]
            )

            wordfile = open(path, mode="r", encoding="utf-8")
            words = wordfile.readlines()
            wordfile.close()

            selection = [random.randint(0, 999) for i in list(range(5))]
            selected_words = [words[s].strip() for s in selection]

            num = random.randint(0, 4)

            challengeinfo = self.msg["spam_challenge"].format(
                num=self.msg["spam_nums"][num],
                words = ", ".join(selected_words)
            )

            s_word = selected_words[num]
            b_word = bytes(s_word, encoding="utf-8")
            word_hash = bcrypt.hashpw(b_word, bcrypt.gensalt())
            word_hash = word_hash.decode("utf-8")

            if self.data.get("user"):
                content += [
                    '<form method="post">',
                    '<p>' + self.msg["username"] + '<br/>',
                    '<input type="text" name="user" value="' + user + '" /></p>',
                    '<p>' + self.msg["url"] + '<br/>',
                    '<input type="text" name="url" value="'+url+'" /></p>',
                    '<input type="hidden" name="check" value="' + s_word + '"/>',
                    '<input type="hidden" name="challenge" value="' + word_hash + '"/>'
                    '<p>' + self.msg["comment"] + '<br/>',
                    '<textarea name="comment">' + comment + '</textarea></p>',
                    '<input type="hidden" name="terms" value="1" />',
                    '<button name="' + self.msg["send"] + '">' + self.msg["send"] + '</button>',
                    '</form>',
                ]
            else:
                content += [
                    '<form method="post">',
                    '<p>' + self.msg["username"] + '<br/>',
                    '<input type="text" name="user" value="' + user + '" /></p>',
                    '<p>' + self.msg["url"] + '<br/>',
                    '<input type="text" name="url" value="' + url + '" /></p>',
                    '<p>' + challengeinfo + '<br/>',
                    '<input type="text" name="check" /></p>',
                    '<input type="hidden" name="challenge" value="' + word_hash + '"/>',
                    '<p>' + self.msg["comment"] + '<br/>',
                    '<textarea name="comment">' + comment + '</textarea></p>',
                    '<p><input type="checkbox" name="terms" class="small" />',
                    self.msg["terms"] + '</p>',
                    '<button name="' + self.msg["send"] + '">' + self.msg["send"] + '</button>',
                    '</form>',
                ]

        content += ['</div>']
        self.content += content

    def show_edit_form(self):
        """ display an edit form """

        # check the users write access:
        if self.data.get("rank") not in ["owner", "writer"]:
            if self.data.get("user"):
                self.e403()
                return
            else:
                self.e401()
                return

        # okay continue ...

        self.data["error"] = []
        self.data["warn"] = []

        data = []
        base = os.environ["DOCUMENT_ROOT"]

        dir = os.path.join(
            base,
            self.cnf["base_dir"],
            *self.directory,
            self.name
        )

        filename = "{name}.{lang}.{ext}".format(
            name=self.cnf["cur_name"],
            lang=self.lang,
            ext=self.cnf["file_ext"],
        )
        path = os.path.join(dir, filename)
        lock_file = os.path.join(dir, ".lock")


        # try to create the necessary directory ...
        try:
            os.mkdir(dir)
        except (FileExistsError, FileNotFoundError) as e:
            if isinstance(e, FileNotFoundError):
                self.data["error"].append(self.msg["e_cannot_create_dir"])

        # check for the lockfile
        if not self.data["error"] and os.path.exists(lock_file):
            lock = open(lock_file, mode="r", encoding="utf-8")
            lock_user, lock_time = lock.read().split()
            lock.close()
            lock_time = float(lock_time)
            now = time.time()

            # locked by other user
            if self.data["user"] != lock_user:
                if lock_time + self.cnf["lock_time"] > now:
                    err = self.msg["e_locked"].format(user=lock_user)
                    self.data["error"].append(err)
                else:
                    warn = self.msg["w_locked"].format(user=lock_user)
                    warn = datetime.strftime(
                        datetime.fromtimestamp(lock_time),
                        warn
                    )
                    self.data["warn"].append(warn)
            # own lock
            else:
                warn = self.msg["w_locked_self"].format(user=lock_user)
                warn = datetime.strftime(
                    datetime.fromtimestamp(lock_time),
                    warn
                )
                self.data["warn"].append(warn)

        # something went wrong ...
        if self.data["error"]:
            content = [
                '<div class="main">',
                '<h2>' + self.msg["no_edit"] + '</h2>'
            ]
            content += self.data["error"]
            content += [
                '</div>'
            ]

            self.content += content

        # show the edit window ...
        else:
            # create new lock
            lock = open(lock_file, mode="w", encoding="utf-8")
            lock_data = "{user} {now}".format(
                user=self.data["user"],
                now=time.time()
            )
            lock.write(lock_data)
            lock.close()

            # get current content ...
            if os.path.exists(path):
                file = open(path, mode="r", encoding="utf-8")
                data += file.readlines()
                file.close()

                data = [l.replace("\r", "") for l in data]
                data = [l.replace("\n", "") for l in data]
                data = data[:-3]

            content = [
                '<div class="main">',
                '<h2>' + self.msg["edit_title"] + '</h2>',
            ]

            if self.data.get("warn"):
                content += ['<div class="warn">'] + self.data["warn"] + ["</div>"]

            content += [
                '<form method="post">',
                '<textarea rows="15" cols="80" name="content">'
            ]
            content += data
            content += [
                '</textarea>',
                '<button name="' + self.msg["send"] + '">' + self.msg["send"] + '</button>',
                '</form>',
                '</div>'
            ]
            self.content += content

    def show_files(self):
        """ adding the file folder to the page content"""

        # check the users rank
        if self.data.get("rank") not in ["owner", "writer"]:
            if self.data.get("user"):
                self.e403(info="files")
                return
            else:
                self.e401(info="files")
                return

        # display upload form
        upload = [
            '<div class="main">',
            '<h2>' + self.msg["files"] + '</h2>',
            '<form enctype="multipart/form-data" method = "POST" >',
            '<input type = "hidden" name = "MAX_FILE_SIZE" value = "10240000" />',
            '<p> Choose file ... </p>',
            '<input name="file", type="file" multiple="true" />',
            '<p><button value="upload" name="upload">' + self.msg["upload"] + '</button></p>',
        ]
        self.content += upload

        # show files
        dir = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            *self.directory,
            self.name,
            "*"
        )

        table = ['<div class="main"><table width="100%">']
        files = glob.glob(dir)
        for n, path in enumerate(files):
            table += ["<tr>"]
            path = path.replace("\\", "/")
            *_, filename = path.split("/")
            if filename.endswith(self.cnf["file_ext"]): continue
            if not os.path.isfile(path): continue

            size = os.path.getsize(path)
            size_text = "0B"
            for i, u in enumerate(["B", "KB", "MB", "GB", "TB"]):
                if 1024 ** i > size: break
                s = size / (1024 ** i)
                size_text = str(round(s,1)) + u

            marker = '<input type="checkbox" class="small" name="sel" value="'+filename+'" />'
            row = "<td>{mark}</td><td>{file}</td><td>{size}</td>".format(
                file=filename,
                size=size_text,
                mark=marker
            )
            table += [row]
            table += ["</tr>"]
        table += ["</table>", "</div>"]

        file_actions = [
            '<p><button value="del" name="del" type="submit">' + self.msg["delete_files"] + '</button></p>',
            '<p>' + self.msg["move_copy_info"] + '</p>',
            '<p><input type="text" name="target"/><br/>',
            '<button value="move" name="move" type="submit">' + self.msg["move"] + '</button>'
            '<button  value="copy" name="copy" type="submit">' + self.msg["copy"] + '</button></p>',
        ]

        if files:
            self.content += table
            self.content += file_actions

        self.content += [
            '</form>',
            '</div>'
        ]


    def show_settings(self):
        """ write the setting screen to the page contents """

        if self.data.get("rank") != "owner":
            if self.data.get("user"):
                self.e403()
                return
            else:
                self.e401()
                return

        owners = []
        writers = []
        commenters = []
        readers = []
        inherit = ""

        base_path = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
        )

        acl_name = self.cnf["acl_name"] + "." + self.cnf["file_ext"]

        # get all available acls ...
        existing_acls = list(os.walk(base_path))

        acl_names = []
        # we won't need the base_path
        if existing_acls:
            strip_base = len(existing_acls[0][0])

        for dir, sub_dirs, files in existing_acls:
            if acl_name not in files: continue
            stripped_dir = dir[strip_base:]
            stripped_dir = stripped_dir.replace("\\", "/")
            while "//" in stripped_dir:
                stripped_dir = stripped_dir.replace("//", "/")

            if stripped_dir.startswith("/"):
                stripped_dir = stripped_dir[1:]

            acl_names.append(stripped_dir)

        path = os.path.join(
            base_path,
            *self.directory,
            self.name,
            acl_name
        )

        cur_rank = ""
        if os.path.exists(path):
            file = open(path, encoding="utf-8", mode="r")
            acl = file.readlines()
            file.close()

            for line in acl:
                line = line.strip()
                if line.startswith("!"):
                    inherit = line[1:]
                    break
                if line.startswith(":"):
                    if line.startswith(":owner"): cur_rank = "owner"
                    if line.startswith(":writer"): cur_rank = "writer"
                    if line.startswith(":commenter"): cur_rank = "commenter"
                    if line.startswith(":reader"): cur_rank = "reader"
                    continue
                if cur_rank == "owner": owners.append(line)
                if cur_rank == "writer": writers.append(line)
                if cur_rank == "commenter": commenters.append(line)
                if cur_rank == "reader": readers.append(line)

        if not owners:
            owners.append(self.data["user"])

        available_acls=[]
        for entry in acl_names:
            if entry == inherit:
                selected = " selected"
            else:
                selected = ""
            o = '<option' + selected + '>' + entry + '</option>'
            available_acls.append(o)

        form = [
            '<div class="main">',
            '<h2>' + self.msg["settings"] + '</h2>',
            '<form method = "POST" >',
            '<h3>' + self.msg["acl"] + '</h3>',
            '<p><b>' + self.msg["acl_owner"] + '</b>',
            '<textarea rows="2" cols="80" name="owner">' + "\n".join(owners) + '</textarea></p>',
            '<p><b>' + self.msg["acl_writer"] + '</b>',
            '<textarea rows="4" cols="80" name="writer">' + "\n".join(writers) + '</textarea></p>',
            '<p><b>' + self.msg["acl_commenter"] + '</b>',
            '<textarea rows="4" cols="80" name="commenter">' + "\n".join(commenters) + '</textarea></p>',
            '<p><b>' + self.msg["acl_reader"] + '</b>',
            '<textarea rows="4" cols="80" name="reader">' + "\n".join(readers) + '</textarea></p>',
            '<p><b>' + self.msg["acl_inherit"] + '</b><br/>',
            '<select size="5" name="inherit">' + "\n".join(available_acls) + '</select></p>',
            '<p><button value="' + self.msg["send"] + '">' + self.msg["send"] + '</button></p>',
            '</form>',
            '</div>'
        ]
        self.content += form

    def html_foot(self):
        mod_time = datetime.fromtimestamp(self.data.get("mod_time", time.time()))
        mod_time = mod_time.strftime(self.msg["edit_time"])
        login_url = os.path.join("/", self.cnf["base_dir"], *self.directory, self.name)
        user_info = self.msg["link"].format(
            url=login_url+"?login",
            more="",
            text=self.msg["login"]
        )

        if self.data.get("user"):
            user_info = self.msg["logged_in"].format(
                user=self.data["user"]
            )

        content = [
            '<div class="main">',
            '<hr>',
            '<p class="footer">' + mod_time + '</p>',
            '<p class="footer">' + user_info + '</p>',
            '<div>',
            '</body>',
            '</html>'
        ]

        self.content += content

    def get_content(self):
        if self.data.get("rank") not in ["reader", "commenter", "writer", "owner"]:
            if self.data.get("user"):
                self.e403(info="read")
                return
            else:
                self.e401(info="read")
                return

        if self.query:
            self.query_del()
            if self.status != "200 OK":
                return

        content = []

        filename = "{name}.{lang}.{ext}".format(
            name=self.cnf["stat_name"],
            lang=self.lang,
            ext=self.cnf["file_ext"],
        )

        path = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            *self.directory,
            self.name,
            filename
        )

        if not os.path.isfile(path):
            self.parse_current()

        try:
            content.append('<div class="main">')
            file = open(path, mode="r", encoding="utf-8")
            content += file.readlines()
            file.close()
            content.append('</div>')
            self.content += content
            self.data["mod_time"] = os.path.getmtime(path)

        except FileNotFoundError:
            self.e404()

    def get_comments(self):
        """ retrieve comments for this page and add them to the page content"""

        # if the user has insufficient rights leave silently ...
        if self.data.get("rank") not in ["commenter", "writer", "owner"]:
            return

        content = []
        comment_names = "{name}.*.{ext}".format(
            name=self.cnf["comments"],
            lang=self.lang,
            ext=self.cnf["file_ext"],
        )

        dir = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            *self.directory,
            self.name,
        )

        comments = glob.glob(dir + "/" + comment_names)
        if comments:
            content += ['<div class="main">']

        for comment in comments:
            file = open(comment, mode="r", encoding="utf-8")
            comment_data = file.readlines()
            file.close()

            username = comment_data[0].strip()
            url = comment_data[1].strip()
            post_time = float(comment_data[2])
            post_time = datetime.fromtimestamp(post_time)
            text = "<br/>".join(comment_data[4:])
            text = text.replace("\n", "")

            if url != "":
                url1 = '<a href="' + url + '">'
                url2 = '</a>'
            else:
                url1 = url2 = ""

            title = datetime.strftime(post_time, self.msg["comment_head"])
            title = title.format(
                url1=url1,
                user=username,
                url2=url2
            )

            dc = ""
            if self.data["rank"] in ["owner", "writer"]:
                src = "/" + self.cnf["base_dir"] + "/del.png"
                alt = self.msg["delete"]
                num = os.path.split(comment)[1].split(".")[-2]
                num = str(int(num))
                url = "/".join([
                    "",
                    self.cnf["base_dir"],
                    *self.directory,
                    self.name
                ])
                url += "?del=" + num
                img = '<img src="{src}" alt="{alt}" title="{alt}" />'.format(
                    src=src,
                    alt=alt
                )
                dc = '<a href="{url}">{img}</a>'.format(
                    url=url,
                    img=img
                )

            next_comment = [
                '<hr />',
                '<div class="comment">',
                dc + title + '<br/>',
                text,
                '</div>'
            ]

            content += next_comment

        if content:
            content += ['</div>']

        self.content += content

    def parse_current(self):
        """ Stores a parsed version of the file """

        dir = os.path.join(
            os.environ["DOCUMENT_ROOT"],
            self.cnf["base_dir"],
            *self.directory,
            self.name,
        )

        cur_name = "{name}.{lang}.{ext}".format(
            name=self.cnf["cur_name"],
            lang=self.lang,
            ext=self.cnf["file_ext"],
        )

        path = os.path.join(dir, cur_name)

        if os.path.isfile(path):
            file = open(path, mode="r", encoding="utf-8")
            data = file.readlines()
            file.close()

            parser = WikiParse(page, data)
            parsed = parser.parse()
            filename = "{name}.{lang}.{ext}".format(
                name=self.cnf["cur_name"],
                lang=self.lang,
                ext=self.cnf["file_ext"],
            )

            path = os.path.join(dir, path)
            file = open(path, mode="w", encoding="utf-8")
            for line in parsed:
                file.write(line + "\n")
            file.close()

    def showenv(self):
        content = []
        for k, v in os.environ.items():
            content.append(k + ": " + v + "<br/>")
        self.content += ['<div class="main">'] + content + ["</div>"]

    def e401(self, info=None):
        """ creates a 401 error page """

        # only one error is handled!
        if self.status != "200 OK":
            return

        title = '<h2>' + self.msg["e_401_title"] + '</h2>'
        text = self.msg["e_401_generic"]
        if info == "read": text = self.msg["e_401_read"]
        if info == "files": text = self.msg["e_401_files"]
        if info == "settings": text = self.msg["e_401_settings"]
        if info == "comments":
            text = self.msg["e_401_comments"]
            title = ""

        self.status = "401 Not Authorized"
        self.content += [
            '<div class="main">',
            title,
            '<p>' + text + '</p>',
            '</div>'
        ]

    def e403(self, info=None):
        """ creates a 403 error page """

        # only one error is handled!
        if self.status != "200 OK":
            return

        title = '<h2>' + self.msg["e_403_title"] + '</h2>'
        text = self.msg["e_403_generic"]
        if info == "read": text = self.msg["e_403_read"]
        if info == "files": text = self.msg["e_403_files"]
        if info == "settings": text = self.msg["e_403_settings"]
        if info == "comments":
            title = ""
            text = self.msg["e_403_comments"]

        self.status = "403 Forbidden"
        self.content += [
            '<div class="main">',
            title,
            '<p>' + text + '</p>',
            '</div>'
        ]

    def e404(self):
        """ creates a 404 error page"""

        # only one error is handled!
        if self.status != "200 OK":
            return

        self.status = "404 Not Found"
        self.content += [
            '<div class="main">',
            '<h2>' + self.msg["e_404_title"] + '</h2>',
            '<p>' + self.msg["e_404_body"] + '</p>',
            '</div>'
        ]


def test():
    os.environ["DOCUMENT_ROOT"] = "C:/Users/Eric/Documents/Homepages/"
    os.environ["REQUEST_METHOD"] = "GET"
    os.environ["REQUEST_URI"] = "/site/test?parse"


if __name__ == "__main__":
    # running test?
    if not os.environ.get("DOCUMENT_ROOT"):
        test()

    # initializing the page (Nothing in here must print anything!)
    page = SimplePage()
    page.make_config()
    page.parse_url()
    page.get_lang()
    page.cookie_handler()
    page.check_acl()
    page.post_handler()

    # do we serve an existing file or generating a file?

    # build the content
    page.html_head()
    page.nav_bar()
    page.page_menu()

    if os.environ.get("REDIRECT_STATUS") == "403":
        page.e403()
    elif page.query[0] == "login":
        page.show_login_form()
    elif page.query[0] == "logout":
        page.show_login_form()
    elif page.query[0] == "register":
        page.show_registration_form()
    elif page.query[0] == "user":
        page.show_user_form()
    elif page.query[0] == "files":
        page.show_files()
    elif page.query[0] == "settings":
        page.show_settings()
    elif page.query[0] == "test":
        page.showenv()
    elif page.query[0] == "parse":
        page.parse_current()
        page.get_content()
        page.get_comments()
        page.show_comment_form()
    elif page.query[0] == "edit":
        if os.environ["REQUEST_METHOD"] == "GET":
            page.show_edit_form()
        else:
            page.get_content()
            page.get_comments()
            page.show_comment_form()
    else:
        page.get_content()
        page.get_comments()
        page.show_comment_form()

    # debug line ..
    page.content += [page.data.get("info")]
    page.html_foot()

    # serve the page
    print(page.headers(status=page.status, cont_type="text/html"))
    for line in page.content:
        print(line)