from django.shortcuts import render

from .models import FikaID, Transaction
from .forms import ProviderChoiceForm


# Create your views here.
def home(request):
    return render(request, 'core/home.html')


def redeem(request, fika_code):
    # Check if fika_code valid and under limit
    try:
        fika_id = FikaID.objects.get(fika_code=fika_code)
        if not fika_id.count < fika_id.customer.limit:
            # Fika ID limit reached error
            return render(request, 'core/error.html', {'error': 'Sorry, het limiet voor deze code is bereikt.'})

        if request.method == 'POST':
            form = ProviderChoiceForm(request.POST)
            # If form is not valid, we simply reload the page
            # If it is valid, we create a transaction and
            if form.is_valid():
                # Generate transaction based on fika_id object and form.provider
                t = Transaction(provider_id=form['provider'].value(), customer_id=fika_id.customer.id, fika_id=fika_id)
                t.save()

                # Increase fika_id count
                fika_id.count += 1
                fika_id.save()

                # Render success
                return render(request, 'core/success.html')
        else:
            form = ProviderChoiceForm()
        return render(request, 'core/redeem.html', {'form': form})

    except FikaID.DoesNotExist:
        # Fika ID not found error
        return render(request, 'core/error.html', {'error': 'Sorry, deze code bestaat niet.'})
