import web

#render function takes template roots
render = web.template.render('templates/')

#db setting
db = web.database(dbn='mysql', user='root', pw='raspberry', db='testdb')
urls = (
        '/', 'index',
        '/measure', 'measure'
        )

# additional history.html shows GET, POST command history.
# History is stored in additional mysql table name "history".

# Index files shows the list in the table, form boxes for add, delete, update.
class index:
        def GET(self):
                temps = db.select('temp')
                m=db.insert('history', title="GET")
                return render.index(temps)

# Add an element with the title according to the user input in "todo" table.
class measure:
        def POST(self):
		#Read Temperature
                raise web.seeother('/')

if __name__ == "__main__":
        app = web.application(urls, globals())
        app.run()


