from django.shortcuts import render
from django import forms
from markdown2 import Markdown
from . import util
import shutil

markdowner = Markdown()

class NewTaskForm(forms.Form):
    search = forms.CharField()



class NewEntryForm(forms.Form):
    e_name = forms.CharField(label='Entry name')
    e_text = forms.CharField(label='Entry text', widget=forms.Textarea)



def index(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            search_res = form.cleaned_data["search"]
            entries = util.list_entries()
            if search_res in entries:
                return render(request, f"encyclopedia\{search_res}.html", {
                    "contains": markdowner.convert(util.get_entry(search_res))
                })
            elif search_res:
                entry_res = []
                for entry in entries:
                    if search_res in entry:
                        entry_res.append(entry)
                if entry_res:
                    return render(request, "encyclopedia/index.html", {
                        "entries": entry_res,
                        "search_form": NewTaskForm()
                    })
                else:
                    return render(request, "encyclopedia/not_found.html")
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "search_form": NewTaskForm()
        })

def entry(request, name):
    entries = util.list_entries()
    if name in entries:
        return render(request, f"encyclopedia\{name}.html", {
        "contains": markdowner.convert(util.get_entry(name)),
        "search_form": NewTaskForm()
        })
    else:
        return render(request, "encyclopedia/not_found.html")

def new_entry (request):
    form = NewEntryForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            e_name = form.cleaned_data["e_name"]
            e_text = form.cleaned_data["e_text"]
            entries = util.list_entries()
            if e_name in entries:
                return render(request, "encyclopedia/entry_exists.html")
            else:
                util.save_entry(e_name, e_name + e_text)
                shutil.copy("encyclopedia/templates/encyclopedia/HTML.html", f"encyclopedia/templates/encyclopedia/{e_name}.html")
                return render(request, f"encyclopedia\{e_name}.html", {
                    "contains": markdowner.convert(util.get_entry(e_name)),
                    "search_form": NewTaskForm()
                })
        else:
            return render(request, "encyclopedia/not_found.html")
    elif request.method == "GET":
        return render(request, "encyclopedia/new_entry.html", {
        "new_entry_form": NewEntryForm()
        })