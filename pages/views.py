from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()
            sender_name = message.sender_name
            # You might want to add a success message or redirect to a thank you page
            messages.success(request,f'Thank {sender_name} your message sent successfully to us.')
            return redirect('pages:thank_you')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'pages/contact_us.html', context)


from django.views.generic import TemplateView


class ThankTemplateView(TemplateView):
    template_name = "pages/thank_you.html"