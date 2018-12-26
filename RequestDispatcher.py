from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
from BiologicalDatabase import BiologicalDatabase
import random
import string

####### PARAMETERS ########
admin_username = 'ugent'
admin_password = 'ugent'
address = '127.0.0.1'
port = 8081
###########################

db = BiologicalDatabase()

web_url = 'http://' + str(address) + ':' + str(port)
admin_url_shuffle = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

class RequestDispatcher(SimpleHTTPRequestHandler):
    def __request_and_send_html(self, html_name):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            msg = self.__request_scheme(html_name)
            self.wfile.write(msg)
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
    def __request_and_send_css(self, css_name):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            msg = self.__request_scheme(css_name)
            self.wfile.write(msg)
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
            return
    def __request_and_send_js(self, js_name):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            msg = self.__request_scheme(js_name)
            self.wfile.write(msg)
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
            return
    def __parse_variables(self, post_body, amount_of_variables):
        var_list = list()
        startpos = 0
        for i in range(0, amount_of_variables):
            startpos = post_body.find('=', startpos) + 1
            if i == amount_of_variables - 1:
                endpos = len(post_body)
            else:
                endpos = post_body.find('&', startpos)
            var = post_body[startpos:endpos].replace('+', ' ').replace('%3A%2F%2F','://').replace('%2F', '/')
            var_list.append(var)
        return var_list

    def __generate_table(self):
        # import
        header = ['Header1', 'Header2', 'Header3', 'Header4']
        rows = [['R1C1', 'R1C2', 'R1C3', 'R1C4'], ['R2C1', 'R2C2', 'R2C3', 'R2C4']]

        # make headers
        header_content = ''
        for cell in header:
            header_content += '<div class="cell">' + cell + '</div>'
        header_html = '<div class="tblrow header green">' + header_content + '</div>'

        # make rows
        rows_html = ''
        for row in rows:
            rows_html += '<div class="tblrow">'
            for cell in row:
                rows_html += '<div class="cell">' + cell + '</div>'
            rows_html += '</div>'

        # piece headers and row together
        html_piece = '<div id=table_wrapper class="table_wrapper">' + \
                     '<div class="table">' + \
                     header_html + \
                     rows_html + \
                     '</div>' + \
                     '</div>'
        return html_piece
    def __table_list_format_to_html(self, header, rows):
        if header[1] == 'lysin_id':
            lysin_table = True
        else:
            lysin_table = False
        # convert unicodes to string
        h = list()
        for cell in header:
            h.append(str(cell))
        header = h
        id_of_element_to_toggle = 0
        r = list()
        for row in rows:
            cells = list()
            for cell in row:
                if cell == row[0]: # means we are dealing with the borrelia id
                    cell = '<a href="http://127.0.0.1:8081/queryl?borreliaid='+str(cell)+'&lysinuniprotid=&lysinname=&conserveddomains=&properties=&amount=all">'\
                           +str(cell)+'</a>'
                if lysin_table:
                    if cell == row[4]:
                        id_of_element_to_toggle += 1
                        cell = '<p id=' + str(id_of_element_to_toggle) + ' style="display:none;">' + '</br>' + cell + '</p>'
                        button = '<button class="btn btn-default" onclick = "toggle_visibility('+ str(id_of_element_to_toggle) +');"">sequence</button>'
                        cell = button + cell
                cells.append(str(cell))
            r.append(cells)
        rows = r

        # make headers
        header_content = ''
        for cell in header:
            header_content += '<div class="cell">' + cell + '</div>'
        header_html = '<div class="tblrow header green">' + header_content + '</div>'

        # make rows
        rows_html = ''
        for row in rows:
            rows_html += '<div class="tblrow">'
            for cell in row:
                rows_html += '<div class="cell">' + cell + '</div>'
            rows_html += '</div>'

        # piece headers and row together
        html_piece = '<div id=table_wrapper class="table_wrapper">' + \
                     '<div class="table">' + \
                     header_html + \
                     rows_html + \
                     '</div>' + \
                     '</div>'
        return html_piece

    def __generate_all_borrelia_table(self, number):
        header, rows = db.query_borrelia_table_all()
        rows = rows[0:number]
        html = self.__table_list_format_to_html(header, rows)
        return html
    def __generate_subset_borrelia_table_by_borrelia_id(self, borrelia_id, number):
        header, rows = db.query_borrelia_table_by_borrelia_id(borrelia_id)
        if number != 'all':
            number = int(number)
            if len(rows) > number:
                rows = rows[0:number]
        html = self.__table_list_format_to_html(header, rows)
        return html
    def __generate_subset_borrelia_table_by_borrelia_name(self, borrelia_name, number):
        header, rows = db.query_borrelia_table_by_borrelia_name(borrelia_name)
        if number != 'all':
            number = int(number)
            if len(rows) > number:
                rows = rows[0:number]
        html = self.__table_list_format_to_html(header, rows)
        return html

    def __generate_all_lysins_table(self, number):
        header, rows = db.query_lysins_table_all()
        rows = rows[0:number]
        html = self.__table_list_format_to_html(header, rows)
        return html
    def __generate_subset_lysins_table_by_borrelia_id(self, borrelia_id, number):
        header, rows = db.query_lysins_table_by_borrelia_id(borrelia_id)
        if number != 'all':
            number = int(number)
            if len(rows) > number:
                rows = rows[0:number]
        html = self.__table_list_format_to_html(header, rows)
        return html
    def __generate_subset_lysins_table_by_lysin_uniprotid(self, lysin_uniprotid, number):
        header, rows = db.query_lysins_table_by_lysin_id(lysin_uniprotid)
        if number != 'all':
            number = int(number)
            if len(rows) > number:
                rows = rows[0:number]
        html = self.__table_list_format_to_html(header, rows)
        return html
    def __generate_subset_lysins_table_by_lysin_name(self, lysin_name, number):
        header, rows = db.query_lysins_table_by_lysin_name(lysin_name)
        if number != 'all':
            number = int(number)
            if len(rows) > number:
                rows = rows[0:number]
        html = self.__table_list_format_to_html(header, rows)
        return html
    def __generate_subset_lysins_table_by_conserved_domains(self, conserveddomains, number):
        header, rows = db.query_lysins_table_by_conserved_domains(conserveddomains)
        if number != 'all':
            number = int(number)
            if len(rows) > number:
                rows = rows[0:number]
        html = self.__table_list_format_to_html(header, rows)
        return html
    def __generate_subset_lysins_table_by_properties(self, properties, number):
        header, rows = db.query_lysins_table_by_properties(properties)
        if number != 'all':
            number = int(number)
            if len(rows) > number:
                rows = rows[0:number]
        html = self.__table_list_format_to_html(header, rows)
        return html

    def __request_scheme(self, scheme_name):
        # HTML schemes
        # /
        if scheme_name == 'index.html':
            file = open("html/index.html", 'r')
            html = file.read()
            return html
        elif scheme_name == 'queryb.html':
            file = open("html/queryb.html", 'r')
            html = file.read()
            table = self.__generate_all_borrelia_table(20)
            html = html.replace('<TABLE_INSERT_WITH_PYTHON_REPLACE>', table)
            return html
        elif scheme_name == 'queryl.html':
            file = open("html/queryl.html", 'r')
            html = file.read()
            table = self.__generate_all_lysins_table(20)
            html = html.replace('<TABLE_INSERT_WITH_PYTHON_REPLACE>', table)
            return html
        elif scheme_name == 'about.html':
            file = open("html/about.html", 'r')
            html = file.read()
            return html
        elif scheme_name == 'login.html':
            file = open("html/login.html", 'r')
            html = file.read()
            return html
        elif scheme_name == 'admin_page.html':
            file = open("html/admin_page.html", 'r')
            html = file.read()
            return html
        elif scheme_name == 'querybresult.html':
            file = open("html/querybresult.html", 'r')
            html = file.read()
            return html
        elif scheme_name == 'querylresult.html':
            file = open("html/querylresult.html", 'r')
            html = file.read()
            return html

        # CSS schemes
        elif scheme_name == 'bootstrap.min.css':
            file = open('css/bootstrap.min.css', 'r')
            css = file.read()
            return css
        elif scheme_name == 'bootstrap.css':
            file = open('css/bootstrap.css', 'r')
            css = file.read()
            return css
        elif scheme_name == 'simple-sidebar.css':
            file = open('css/simple-sidebar.css', 'r')
            css = file.read()
            return css
        elif scheme_name == 'table.css':
            file = open('css/table.css', 'r')
            css = file.read()
            return css

        # JS schemes
        elif scheme_name == 'jquery.js':
            file = open('js/jquery.js', 'r')
            js = file.read()
            return js
        elif scheme_name == 'bootstrap.js':
            file = open('js/bootstrap.js', 'r')
            js = file.read()
            return js
        elif scheme_name == 'bootstrap.min.js':
            file = open('js/bootstrap.min.js', 'r')
            js = file.read()
            return js

    # GET
    def do_GET(self):
        # HTML paths
        if self.path == '/' or self.path == '/?' or self.path == '/#':
            self.path = "/index.html"
            self.__request_and_send_html('index.html')

        elif self.path == '/queryb' or self.path == '/?queryb' or self.path == '/queryb?':
            self.path = "/queryb.html"
            self.__request_and_send_html('queryb.html')
        elif '/queryb?' in self.path and 'borreliaid' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            borrelianame, borreliaid = self.__parse_variables(self.path, 2)
            msg = self.__request_scheme('querybresult.html')
            if borrelianame != '':
                msg = msg.replace('<BODYTEXT>', 'Hits for Borrelia name: {}'.format(borrelianame))
                table = self.__generate_subset_borrelia_table_by_borrelia_name(borrelianame, 'all')
                msg = msg.replace('<TABLE_INSERT_WITH_PYTHON_REPLACE>', table)
            elif borreliaid != '':
                msg = msg.replace('<BODYTEXT>', 'Hits for Borrelia id: {}'.format(borreliaid))
                table = self.__generate_subset_borrelia_table_by_borrelia_id(borreliaid, 'all')
                msg = msg.replace('<TABLE_INSERT_WITH_PYTHON_REPLACE>', table)
            else:
                msg = msg.replace('<BODYTEXT>', 'Please give either an id or name.')
            self.wfile.write(msg)

        elif self.path == '/queryl' or self.path == '/?queryl' or self.path == '/queryl?':
            self.path = "/queryl.html"
            self.__request_and_send_html('queryl.html')
        elif '/queryl?' in self.path and 'borreliaid' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            borreliaid, lysinuniprotid, lysinname, conserveddomains, properties, amount = self.__parse_variables(self.path, 6)
            msg = self.__request_scheme('querylresult.html')
            if borreliaid != '':
                msg = msg.replace('<BODYTEXT>', 'Results ({}) for Borrelia id: {}'.format(amount, borreliaid))
                table = self.__generate_subset_lysins_table_by_borrelia_id(borreliaid, amount)
                msg = msg.replace('<TABLE_INSERT_WITH_PYTHON_REPLACE>', table)
            elif lysinuniprotid != '':
                msg = msg.replace('<BODYTEXT>', 'Results ({}) for Lysin uniprot id: {}<br> (click on the borrelia id to find corresponding lysins)'.format(amount,lysinuniprotid))
                table = self.__generate_subset_lysins_table_by_lysin_uniprotid(lysinuniprotid, amount)
                msg = msg.replace('<TABLE_INSERT_WITH_PYTHON_REPLACE>', table)
            elif lysinname != '':
                msg = msg.replace('<BODYTEXT>', 'Results ({}) for Lysin name: {}<br> (click on the borrelia id to find corresponding lysins)'.format(amount, lysinname))
                table = self.__generate_subset_lysins_table_by_lysin_name(lysinname, amount)
                msg = msg.replace('<TABLE_INSERT_WITH_PYTHON_REPLACE>', table)
            elif conserveddomains != '':
                msg = msg.replace('<BODYTEXT>', 'Results ({}) for Lysin conserved domain(s): {}<br> (click on the borrelia id to find corresponding lysins)'.format(amount, conserveddomains))
                table = self.__generate_subset_lysins_table_by_conserved_domains(conserveddomains, amount)
                msg = msg.replace('<TABLE_INSERT_WITH_PYTHON_REPLACE>', table)
            elif properties != '':
                msg = msg.replace('<BODYTEXT>', 'Results ({}) for Lysin properties: {}<br> (click on the borrelia id to find corresponding lysins)'.format(amount, properties))
                table = self.__generate_subset_lysins_table_by_properties(properties, amount)
                msg = msg.replace('<TABLE_INSERT_WITH_PYTHON_REPLACE>', table)
            else:
                msg = msg.replace('<BODYTEXT>', 'Please enter at least one field.')
            self.wfile.write(msg)

        elif self.path == '/about' or self.path == '/?about' or self.path == '/about?':
            self.path = "/about.html"
            self.__request_and_send_html('about.html')

        elif self.path == '/login' or self.path == '/?login' or self.path == '/login?':
            self.path = "/login.html"
            self.__request_and_send_html('login.html')

        elif self.path == ('/admin_page/'+admin_url_shuffle) or self.path == ('/?admin_page/'+admin_url_shuffle) or self.path == ('/admin_page/'+admin_url_shuffle+'?'):
            self.path = "/admin_page.html"
            self.__request_and_send_html('admin_page.html')

        elif '/admin_page/add_borrelia' in self.path and 'borreliaid' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            borreliaid, borrelianame = self.__parse_variables(self.path, 2)
            msg = self.__request_scheme('admin_page.html')
            try:
                db.add_borrelia_to_borrelia_table(borreliaid, borrelianame)
                msg2 = msg.replace('<p>        </p>', 'Added the following to the borrelia table: <br> ID: {} <br> Name: {} </br><br> <a href="{}" class="btn btn-default">Close</a><br></br>'.format(borreliaid,borrelianame, (web_url + '/admin_page/' + admin_url_shuffle)))
            except:
                msg2 = msg.replace('<p>        </p>', 'ERROR while adding the following: <br> ID:{} <br> Name: {} <br> Duplicate Entry? </br><br> <a href="{}" class="btn btn-default">Close Error</a><br></br>'.format(borreliaid, borrelianame, (web_url + '/admin_page/' + admin_url_shuffle)))
            self.wfile.write(msg2)
        elif '/admin_page/add_lysin' in self.path and 'borreliaid' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            borreliaid, lysinuniprotid, lysinname, conserveddomains, properties = self.__parse_variables(self.path, 5)
            msg = self.__request_scheme('admin_page.html')
            try:
                db.add_entry_to_lysins_table(borreliaid, lysinuniprotid, lysinname, conserveddomains, properties)
                msg2 = msg.replace('<p>         </p>', 'Added the following to the lysins table: <br> '
                                                       'Borrelia ID: {} <br> '
                                                       'Lysin Uniprot ID: {} <br> '
                                                       'Lysin Name: {} <br> '
                                                       'Conserved Domains: {} <br>'
                                                       'Properties: {} </br>'
                                                       '<br> <a href="{}" class="btn btn-default">Close</a><br></br>'.format(borreliaid,lysinuniprotid,lysinname, conserveddomains, properties, (web_url + '/admin_page/' + admin_url_shuffle)))
            except:
                msg2 = msg.replace('<p>         </p>', 'ERROR while adding the following to the lysins table: <br> '
                                                       'Borrelia ID: {} <br> '
                                                       'Lysin Uniprot ID: {} <br> '
                                                       'Lysin Name: {} <br> '
                                                       'Conserved Domains: {} <br>'
                                                       'Properties: {} </br>'
                                                       '<br> <a href="{}" class="btn btn-default">Close Error</a><br></br>'.format(borreliaid,lysinuniprotid,lysinname, conserveddomains, properties, (web_url + '/admin_page/' + admin_url_shuffle)))
            self.wfile.write(msg2)

        elif '/admin_page/deleteborreliabyid' in self.path and 'borreliaid' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            borreliaid = self.__parse_variables(self.path, 1)[0]
            msg = self.__request_scheme('admin_page.html')
            try:
                db.delete_borrelia_from_borrelia_table_by_borrelia_id(borreliaid)
                msg2 = msg.replace('<p>          </p>', 'Removed all entries with Borrelia ID: {}'
                                                       '<br> <a href="{}" class="btn btn-default">Close</a><br></br>'.format(borreliaid,(web_url + '/admin_page/' + admin_url_shuffle)))
            except:
                msg2 = msg.replace('<p>          </p>', 'ERROR while removing all entries with Borrelia ID: {}<br> '
                                                       '<br> <a href="{}" class="btn btn-default">Close Error</a><br></br>'.format(borreliaid,(web_url + '/admin_page/' + admin_url_shuffle)))
            self.wfile.write(msg2)
        elif '/admin_page/deleteborreliabyname' in self.path and 'borrelianame' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            borrelianame = self.__parse_variables(self.path, 1)[0]
            msg = self.__request_scheme('admin_page.html')
            try:
                db.delete_borrelia_from_borrelia_table_by_borrelia_name(borrelianame)
                msg2 = msg.replace('<p>          </p>', 'Removed all entries with Borrelia Name: {}'
                                                       '<br> <a href="{}" class="btn btn-default">Close</a><br></br>'.format(borrelianame,(web_url + '/admin_page/' + admin_url_shuffle)))
            except:
                msg2 = msg.replace('<p>          </p>', 'ERROR while removing all entries with Borrelia Name: {}<br> '
                                                       '<br> <a href="{}" class="btn btn-default">Close Error</a><br></br>'.format(borrelianame,(web_url + '/admin_page/' + admin_url_shuffle)))
            self.wfile.write(msg2)

        elif '/admin_page/deletelysinbyid' in self.path and 'borreliaid' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            borreliaid = self.__parse_variables(self.path, 1)[0]
            msg = self.__request_scheme('admin_page.html')
            try:
                db.delete_lysin_from_lysins_table_by_borrelia_id(borreliaid)
                msg2 = msg.replace('<p>           </p>', 'Removed all entries with Borrelia ID: {}'
                                                        '<br> <a href="{}" class="btn btn-default">Close</a><br></br>'.format(
                    borreliaid, (web_url + '/admin_page/' + admin_url_shuffle)))
            except:
                msg2 = msg.replace('<p>           </p>', 'ERROR while removing all entries with Borrelia ID: {}<br> '
                                                        '<br> <a href="{}" class="btn btn-default">Close Error</a><br></br>'.format(
                    borreliaid, (web_url + '/admin_page/' + admin_url_shuffle)))
            self.wfile.write(msg2)
        elif '/admin_page/deletelysinbyuniprotid' in self.path and 'lysinuniprotid' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            lysinuniprotid = self.__parse_variables(self.path, 1)[0]
            msg = self.__request_scheme('admin_page.html')
            try:
                db.delete_lysin_from_lysins_table_by_lysin_uniprotid(lysinuniprotid)
                msg2 = msg.replace('<p>           </p>', 'Removed all entries with Lysin Uniprot ID: {}'
                                                        '<br> <a href="{}" class="btn btn-default">Close</a><br></br>'.format(
                    lysinuniprotid, (web_url + '/admin_page/' + admin_url_shuffle)))
            except:
                msg2 = msg.replace('<p>           </p>', 'ERROR while removing all entries with Lysin Uniprot ID: {}<br> '
                                                        '<br> <a href="{}" class="btn btn-default">Close Error</a><br></br>'.format(
                    lysinuniprotid, (web_url + '/admin_page/' + admin_url_shuffle)))
            self.wfile.write(msg2)
        elif '/admin_page/deletelysinbyname' in self.path and 'lysinname' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            lysinname = self.__parse_variables(self.path, 1)[0]
            msg = self.__request_scheme('admin_page.html')
            try:
                db.delete_lysin_from_lysins_table_by_lysin_name(lysinname)
                msg2 = msg.replace('<p>           </p>', 'Removed all entries with Lysin Name: {}'
                                                         '<br> <a href="{}" class="btn btn-default">Close</a><br></br>'.format(
                    lysinname, (web_url + '/admin_page/' + admin_url_shuffle)))
            except:
                msg2 = msg.replace('<p>           </p>',
                                   'ERROR while removing all entries with Lysin Name: {}<br> '
                                   '<br> <a href="{}" class="btn btn-default">Close Error</a><br></br>'.format(
                                       lysinname, (web_url + '/admin_page/' + admin_url_shuffle)))
            self.wfile.write(msg2)
        elif '/admin_page/deletelysinbyconserveddomains' in self.path and 'conserveddomains' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            conserveddomains = self.__parse_variables(self.path, 1)[0]
            msg = self.__request_scheme('admin_page.html')
            try:
                db.delete_lysin_from_lysins_table_by_conserveddomain(conserveddomains)
                msg2 = msg.replace('<p>           </p>', 'Removed all entries with Lysin Conserved Domain(s): {}'
                                                         '<br> <a href="{}" class="btn btn-default">Close</a><br></br>'.format(
                    conserveddomains, (web_url + '/admin_page/' + admin_url_shuffle)))
            except:
                msg2 = msg.replace('<p>           </p>',
                                   'ERROR while removing all entries with Lysin Conserved Domain(s): {}<br> '
                                   '<br> <a href="{}" class="btn btn-default">Close Error</a><br></br>'.format(
                                       conserveddomains, (web_url + '/admin_page/' + admin_url_shuffle)))
            self.wfile.write(msg2)
        elif '/admin_page/deletelysinbyproperties' in self.path and 'properties' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            properties = self.__parse_variables(self.path, 1)[0]
            msg = self.__request_scheme('admin_page.html')
            try:
                db.delete_lysin_from_lysins_table_by_properties(properties)
                msg2 = msg.replace('<p>           </p>', 'Removed all entries with Lysin Properties: {}'
                                                         '<br> <a href="{}" class="btn btn-default">Close</a><br></br>'.format(
                    properties, (web_url + '/admin_page/' + admin_url_shuffle)))
            except:
                msg2 = msg.replace('<p>           </p>',
                                   'ERROR while removing all entries with Lysin Properties: {}<br> '
                                   '<br> <a href="{}" class="btn btn-default">Close Error</a><br></br>'.format(
                                       properties, (web_url + '/admin_page/' + admin_url_shuffle)))
            self.wfile.write(msg2)

        elif self.path == '/admin_page/reset_borrelia_table' or self.path == '/admin_page/reset_borrelia_table?':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            db.clear_entire_lysins_table()
            db.clear_entire_borrelia_table()
            html = """<!DOCTYPE html>
                                        <html>
                                        <body>
                                        <p>The MySQL tables 'borrelia' and 'lysins' have been reset!</p>
                                        <form action="{}">
                                            <input type="submit" value="Okay" />
                                        </form>
                                        </body>
                                        </html>
                                        """.format((web_url + '/admin_page/'+admin_url_shuffle))
            self.wfile.write(html)
        elif self.path == '/admin_page/reset_lysins_table' or self.path == '/admin_page/reset_lysins_table?':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            db.clear_entire_lysins_table()
            html = """<!DOCTYPE html>
                                        <html>
                                        <body>
                                        <p>The MySQL table 'lysins' has been reset!</p>
                                        <form action="{}">
                                            <input type="submit" value="Okay" />
                                        </form>
                                        </body>
                                        </html>
                                        """.format((web_url + '/admin_page/'+admin_url_shuffle))
            self.wfile.write(html)

        # CSS paths
        elif self.path == '/bootstrap.min.css' or self.path == '/bootstrap.min.css?':
            self.__request_and_send_css('bootstrap.min.css')
        elif self.path == '/bootstrap.css' or self.path == '/bootstrap.css?':
            self.__request_and_send_css('bootstrap.css')
        elif self.path == '/simple-sidebar.css' or self.path == '/simple-sidebar.css?':
            self.__request_and_send_css('simple-sidebar.css')
        elif self.path == '/table.css' or self.path == '/table.css?':
            self.__request_and_send_css('table.css')

        # JS paths
        elif self.path == '/jquery.js' or self.path == '/jquery.js?':
            self.__request_and_send_js('jquery.js')
        elif self.path == '/bootstrap.js' or self.path == '/bootstrap.js?':
            self.__request_and_send_js('bootstrap.js')
        elif self.path == '/bootstrap.min.js' or self.path == '/bootstrap.min.js?':
            self.__request_and_send_js('bootstrap.min.js')
        return

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # admin login
        if self.path=='/login_attempt':
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)

            [username, password] = self.__parse_variables(post_body, 2)
            if admin_username == username:
                if admin_password == password:
                    admin_page_url = web_url + '/admin_page/' + admin_url_shuffle
                    msg = """<!DOCTYPE html>
                                                <html>
                                                <head>
                                                <meta http-equiv="refresh" content="3; url={}" />
                                                </head>
                                                <body>
                                                <p>
                                                Access granted. Automatically redirecting you to the admin page
                                                <br></br>
                                                or click here:
                                                <form action="{}" method="get">
                                                <input type="submit" value="Redirect"></form>
                                                </p>
                                                </body>
                                                </html>
                                        """.format(admin_page_url, admin_page_url)
                    self.wfile.write(msg)
                else:
                    u = web_url + '/login'
                    msg = """<!DOCTYPE html>
                                                <html>
                                                <body>
                                                <p>Wrong password!</p>
                                                <form action="{}" method="get">
                                                <input type="submit" value="Back"></form>
                                                </body>
                                                </html>
                                        """.format(u)
                    self.wfile.write(msg)
            else:
                u = web_url + '/login'
                msg = """<!DOCTYPE html>
                                            <html>
                                            <body>
                                            <p>Username not recognised!</p>
                                            <form action="{}" method="get">
                                            <input type="submit" value="Back"></form>
                                            </body>
                                            </html>
                                    """.format(u)
                self.wfile.write(msg)


def run():
    print('starting server...')

    # Server settings
    # Choose port 8081, for port 80, which is normally used for a http server, you need root access
    server_address = (address, port)
    print(web_url)
    httpd = SocketServer.TCPServer(server_address, RequestDispatcher)
    print('running server...')
    httpd.serve_forever()
run()
