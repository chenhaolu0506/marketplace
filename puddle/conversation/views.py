from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .models import Conversation
from .forms import MessageForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.createdBy == request.user:
        return redirect('dashboard:index')

    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])
    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.createdBy)
            conversation.save()

            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.createdBy = request.user
            msg.save()
        return redirect('item:detail', pk=item_pk)
    else:
        form = MessageForm()
        return render(request, 'conversation/new.html', {
            'form': form
        })

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.createdBy = request.user
            msg.save()
            return redirect('conversation:detail', pk=pk)
    else:
        form = MessageForm()
    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })