#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask  # pip install flask

app = Flask(__name__)

if __name__ == "__main__":  # python main.py
    import controleur

    app.add_url_rule('/', 'pda', view_func=controleur.page_d_accueil)
    try:
        app.run(host='127.0.0.1', port=8000)  # method that run the application
        # app.run(host='0.0.0.0', port=4001)
    except Exception as ex:
        pass
