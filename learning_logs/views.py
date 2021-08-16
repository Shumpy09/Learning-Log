from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404

from .models import Entry, Topic
from .forms import EntryForm, TopicForm

# Create your views here.

def index(request):
    """Strona główna dla aplikacji Learning_Log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Wyświetlenie wszystkich tematów"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Wyświetla pojedyczny temat i wszystkie powiązane z nim wpisy."""
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_onwer(request, topic.owner)

    '''# Upewniamy się, że temat należy do bieżącego użytkownika
    if topic.owner != request.user:
        raise Http404'''
        
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Dodaj nowy temat."""
    if request.method != 'POST':
        # nie przekazano żadnych danych, należy utworzyć pusty formularz
        form = TopicForm()
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    
    # Wyświetlenie pustego formularza
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Dodaj nowy wpis"""
    topic = Topic.objects.get(id=topic_id)

    check_topic_onwer(request, topic.owner)
    if request.method != 'POST':
        # nie przekazano żadnych danych, należy utworzyć pusty formularz
        form = EntryForm()
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć
        form = EntryForm(data=request.POST)
        
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    # Wyświelenie pustego formularza
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edycja istniejącego wpisu"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_onwer(request, topic.owner)
    '''
    # pobieramy wpis i temat powiązany z danym wpisem; jezeli uzytk. nie jest wlasicielem - wskaz blad 404 
    if topic.owner != request.user: 
        raise Http404
    '''
    if request.method != 'POST':
        # Żądanie początkowe, wypełnienie formularza aktualną treścią wpisu
        form = EntryForm(instance=entry)
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id = topic.id)
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


def check_topic_onwer(request, owner):
    if owner != request.user: 
        raise Http404