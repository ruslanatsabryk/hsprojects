from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render
from collections import deque
from django.shortcuts import redirect

line = {"change_oil": 0, "inflate_tires": 0, "diagnostic": 0}
que_change_oil = deque()
que_inflate_tires = deque()
que_diagnostic = deque()
number_of_ticket = None


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        welcome = '<h2>Welcome to the Hypercar Service!<h2>'
        return HttpResponse(welcome)


class Menu(View):
    menu_items = [
        ('change_oil', 'Change oil'),
        ('inflate_tires', 'Inflate tires'),
        ('diagnostic', 'Diagnostic'),
    ]

    def get(self, request, *args, **kwargs):
        context = {'menu': self.menu_items}
        return render(request, 'tickets/menu.html', context)


class ChangeOil(View):
    def get(self, request, *args, **kwargs):
        wait = line["change_oil"] * 2
        line["change_oil"] += 1
        number = line["change_oil"] + line["inflate_tires"] + line["diagnostic"]
        que_change_oil.appendleft(number)
        context = {"number": number, "wait": wait}
        return render(request, 'tickets/get_ticket.html', context)


class InflateTires(View):
    def get(self, request, *args, **kwargs):
        wait = line["change_oil"] * 2 + line["inflate_tires"] * 5
        line["inflate_tires"] += 1
        number = line["change_oil"] + line["inflate_tires"] + line["diagnostic"]
        que_inflate_tires.appendleft(number)
        context = {"number": number, "wait": wait}
        return render(request, 'tickets/get_ticket.html', context)


class Diagnostic(View):
    def get(self, request, *args, **kwargs):
        wait = line["change_oil"] * 2 + line["inflate_tires"] * 5 + line["diagnostic"] * 30
        line["diagnostic"] += 1
        number = line["change_oil"] + line["inflate_tires"] + line["diagnostic"]
        que_diagnostic.appendleft(number)
        context = {"number": number, "wait": wait}
        return render(request, 'tickets/get_ticket.html', context)


class Processing(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/processing.html', context=line)

    def post(self, request, *args, **kwargs):
        global number_of_ticket
        if len(que_change_oil) > 0:
            number_of_ticket = {'number_of_ticket': que_change_oil.pop()}
            line["change_oil"] -= 1
        elif len(que_inflate_tires) > 0:
            number_of_ticket = {'number_of_ticket': que_inflate_tires.pop()}
            line["inflate_tires"] -= 1
        elif len(que_diagnostic) > 0:
            number_of_ticket = {'number_of_ticket': que_diagnostic.pop()}
            line["diagnostic"] -= 1
        else:
            number_of_ticket = {'number_of_ticket': 0}
        return redirect('/next')


class Next(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/next.html', context=number_of_ticket)
