from django.shortcuts import render,redirect,get_object_or_404
from contact.models import Contact
from contact.forms import ContactForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


@login_required(login_url='contact:login')
def create(request):
    form_action=reverse('contact:create')
    if request.method=='POST':
        form=ContactForm(request.POST,request.FILES)
        context={
        'form':form,
        'form_action':form_action,
        }
        if form.is_valid():
            contact=form.save(commit=False)
            contact.owner=request.user
            messages.success(request,f'Contato salvo por {contact.owner}')
            contact.save()
            return redirect('contact:update',contact_id=contact.pk)
        return render(
        request,
        'contact/create.html',
        context
        )
    #FOMULARIO LIMPO
    context = {
        'form': ContactForm(),
        'form_action': form_action
    }
    return render(
        request,
        'contact/create.html',
        context
    )


@login_required(login_url='contact:login')
def update(request,contact_id):
    contact=get_object_or_404(Contact,pk=contact_id,show=True,owner=request.user)
    form_action=reverse('contact:update',args=(contact_id,))
    if request.method=='POST':
        form=ContactForm(request.POST,request.FILES,instance=contact)
        context={
        'form':form,
        'form_action':form_action
        }
        if form.is_valid():
            contact=form.save()
            return redirect('contact:update',contact_id=contact.pk)
        return render(
        request,
        'contact/create.html',
        context
        )
    #FOMULARIO LIMPO
    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action
    }
    return render(
        request,
        'contact/create.html',
        context
    )
@login_required(login_url='contact:login')
def delete(request,contact_id):
    contact=get_object_or_404(
        Contact,pk=contact_id,show=True,owner=request.user
    )
    confirmation=request.POST.get('confirmation','no')
    if confirmation=='yes':
        contact.delete()
        return redirect('contact:index')

    return render(request,
    'contact/contact.html',
                  {
                      'contact':contact,
                      'confirmation':confirmation,
                  })