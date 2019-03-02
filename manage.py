#!/usr/bin/env python
import os, urllib
import bs4, requests
from flask import Flask, render_template, request, Markup
import sys

app = Flask(__name__)




@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = ''
    if request.method == "POST":
        try:
            url = request.form['url']
            r = requests.get(url)
            page_content=bs4.BeautifulSoup(r.content, "html.parser")

        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return render_template('index.html', errors=errors)
        if page_content:
            urlAsString=str(url)
            if 'dailymail' in urlAsString and 'article' in urlAsString:
                results=''
                byline = page_content.find('a', attrs={'class':'author'})
                paragraphs = page_content.find_all('p', attrs={'class':'mol-para-with-font'})
                parsedText=byline.getText() + '\n'
                for paragraph in paragraphs:
                    parsedText += (paragraph.getText() +'\n')
                results=Markup(parsedText)
            else:
                errors.append(
                    "Please only enter addresses that point to articles on mailonline"
                )

    return render_template('index.html', errors=errors, results=results)

if __name__ == "__main__":
    app.run()
