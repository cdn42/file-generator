from flask import Flask, make_response, render_template, send_from_directory, jsonify, request
import os
import datetime
import requests
import string
import random

import config as config
import modules

# GLOBAL Variables


APPNAME = "file-generator"
VERSION = "v0.2"


app = Flask(__name__)


# Functions

def getjsontext (url):
# Get JSON data
	jsonResponse = requests.get(url)
	return (json.loads(jsonResponse.text))


@app.route('/', methods=['GET'])
def root_page():

    # Get document types

    ft = config.filetypes()
    documents = ft.documents()
    compressed = ft.compressed()

    return render_template('index.html', doctype_list = documents, comptype_list = compressed )


@app.route('/list', methods=['GET'])
def list_alltypes():

    return (make_response(jsonify({'error': 'specify type'}), 200))


@app.route('/list/documents', methods=['GET'])
def list_doctypes():


    return (make_response(jsonify({'filetypes': modules.documents.filetypes}), 200))


@app.route('/list/compress', methods=['GET'])
def list_compresstypes():


    return (make_response(jsonify({'filetypes': modules.compress.filetypes}), 200))

@app.route('/list/encrypt', methods=['GET'])
def list_encrypttypes():


    return (make_response(jsonify({'filetypes': modules.encrypt.filetypes}), 200))


def make_filename(doctype):

    stringLength = 8
    chars = string.ascii_lowercase + string.digits
    uid = ''.join(random.choice(chars) for i in range(stringLength))

    return(doctype + "-" + datetime.datetime.now().strftime("%Y%m%d") + "-" + uid)

def sanitise(u_string):

    return (u_string
        .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        .replace("'", "&#39;").replace('"', "&quot;")
        )

@app.route('/fetch', methods=['GET'])
def fetch():

    return make_response(jsonify('error', 'try fetch/[document_type]'), 404)


@app.route('/fetch/<string:u_doctype>', methods=['GET'])
def fetch_document(u_doctype):

    compress = False
    encrypt = False
    malware = False

    sourcefile = config.respath() + "plaintext.txt"

    if request.args:

        print ("Arguments supplied: " + str(request.query_string))

        # We have some optional parameters

        if 'compress' in request.args:
            compress = True

        if 'malware' in request.args:
            sourcefile = config.respath() + "eicar.txt"
            malware = True

    t_doctype= sanitise(u_doctype)

    # generate the file
    if t_doctype in modules.documents.filetypes:

        print ("Creating " + t_doctype)
        print ("Compress " + str(compress))
        print ("Malware: " + str(malware))

        method = getattr(modules.documents, 'doc_' + t_doctype)
        file = method(make_filename(t_doctype), sourcefile)

        osfilepath = config.filespath() + file.fullname

        returnfile = file.fullname
        returnmimetype = file.mimetype

        print (returnfile)

        if compress:

            print ('[Compressing]')

            u_compresstype = request.args['compress']
            t_compresstype = sanitise(u_compresstype)

            print (modules.compress.filetypes)

            if t_compresstype in modules.compress.filetypes:

                method = getattr(modules.compress, 'cmp_' + t_compresstype)

                compressedfile = method(returnfile, osfilepath)
                returnfile = compressedfile.fullname
                returnmimetype = compressedfile.mimetype
                print("Compressed to: " + compressedfile.fullname)
                osfilepath = config.filespath() + compressedfile.fullname

        exists = os.path.isfile(osfilepath)
        if exists:
            return (send_from_directory(os.path.join(config.apppath(), 'files'), returnfile ,mimetype=returnmimetype, as_attachment=True))


    return make_response(jsonify('error','file generation failed'), 500)





# Main Application Loop
if __name__ == '__main__':

    # Ensure an empty files directory exists
    if not os.path.exists('files'):
        os.makedirs('files')

    # Let's go :)
    app.run(debug=True, host='0.0.0.0', port=config.appport())



