from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util
from django.http import HttpResponse, HttpResponseRedirect
import random
from django import forms
from django.urls import reverse


def converter(title):

    content = util.get_entry(title)
    markdowner = Markdown()

    if content == None:
        return None
    
    else:
        return markdowner.convert(content)

    
def search(request):

    if request.method == "POST":
        title = request.POST['q']
        content = converter(title)

        if content:
            return render(request, "encyclopedia/entry.html", {
                "content":content,
                "title": title
        })

        else:
            entries = util.list_entries()
            matching_entries = []

            for entry in entries:
                if title.lower() in entry.lower():
                    matching_entries.append(entry)
            
            return render(request, "encyclopedia/search.html", {
                "entries":matching_entries,
                "title":title
            })
                        
    return render(request, "encyclopedia/new_page.html")    

def entry(request, title):

    content = converter(title)

    if content == None:
        return render(request, "encyclopedia/error.html")
    
    else:
        return render(request, "encyclopedia/entry.html", {
            "content":content,
            "title": title
        })

def index(request): 

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()    
    })

def new_page(request):

    if request.method == "POST":
        title = request.POST['newtitle']
        content = request.POST['newinput']

        checkentry = util.get_entry(title)

        if checkentry:
            return render(request, "encyclopedia/error2.html")
        
        else:
            util.save_entry(title, content)
            converted = converter(title)

            return render(request, "encyclopedia/entry.html", {
                "content":converted,
                "title": title
            })

    return render(request, "encyclopedia/new_page.html")


def random_page(request):

    allcontent = util.list_entries()
    random_content = random.choice(allcontent)
    converted = converter(random_content)

    return render(request, "encyclopedia/entry.html", {
        "content":converted,
        "title":random_content
    })

def edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = util.get_entry(title)

        return render (request, 'encyclopedia/edit.html', {
            "title":title,
            "content":content
        })


def editsave(request):
    if request.method == 'POST':
        title = request.POST['title']
        new_content = request.POST['editsave']
        util.save_entry(title, new_content)
        converted = converter(title)

        return render(request, "encyclopedia/entry.html", {
        "content":converted,
        "title":title
    })

