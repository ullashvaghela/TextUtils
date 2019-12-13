from django.http import HttpResponse
from django.shortcuts import render
from string import punctuation

def index(request):
    params = {'name':'Ullash','From':'India'}
    return render(request,"index.html",params)
    #return HttpResponse("<h1>hello</h1>")

def about(request):
    return HttpResponse("About hello")

def analyze(request):
    djtext = request.POST.get('text','default')
    removepunc = request.POST.get('removepunc','false')
    fullcaps = request.POST.get('capitalize','false')
    newlineremove = request.POST.get('newlineremover','false')
    extraspaceremover = request.POST.get('extraspaceremover','false')
    '''
    chars = []
    for char in djtext:
        chars.append(char)
    '''    
    if removepunc == "true":
        analyzed_text = ""
        for char in djtext:
            if char not in punctuation:
                analyzed_text = analyzed_text + char
        params = {'purpose':'Remove Punctuation','analyzed_text':analyzed_text}
        djtext = analyzed_text
    if fullcaps == "true":
        analyzed_text = ""
        analyzed_text = djtext.upper()
        params = {'purpose':'Capitalize','analyzed_text':analyzed_text}
        djtext = analyzed_text
    if newlineremove == "true":
        analyzed_text = ""
        for char in djtext:
            if char!='\n' and char!="\r":
                analyzed_text = analyzed_text + char
        params = {'purpose':'Remove New Line','analyzed_text':analyzed_text}
        djtext = analyzed_text
    if extraspaceremover == "true":
        analyzed_text = ""
        for index, char in enumerate(djtext):
            if not(djtext[index] == " " and djtext[index+1]==" "):
                analyzed_text = analyzed_text + char
        params = {'purpose':'Remove Extra Space','analyzed_text':analyzed_text}
    if(removepunc!='true' and fullcaps!='true' and newlineremove!='true' and extraspaceremover!='true'):
        params={'purpose':'You Need to add Text for Analyze', 'analyzed_text':'Error:'}
    return render(request,'analyze.html',params)

'''
def capfirst(request):
    return HttpResponse('capfirst')

def newlineremove(request):
    return HttpResponse('newlineremove')

def spaceremover(request):
    return HttpResponse('spaceremover')

def charcount(request):
    return HttpResponse('charcount')
'''