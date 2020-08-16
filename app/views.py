from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    form = ReviewForm
    review_result = ''
    is_review_exist = False

    if request.session.get('reviewed_products'):
        if pk in request.session['reviewed_products']:
            is_review_exist = True

    if request.method == 'POST':
        if not request.session.get('reviewed_products'):
            request.session['reviewed_products'] = []

        if pk in request.session['reviewed_products']:
            review_result = 'Вы уже оставляли отзыв к этому товару!'
        else:
            text = request.POST.get('text')
            review = Review(text=text, product=Product.objects.get(pk=pk))
            request.session.modified = True
            request.session['reviewed_products'].append(pk)
            review.save()
            review_result = 'Отзыв добавлен успешно'

    reviews = Review.objects.filter(product_id=pk)
    context = {
        'form': form,
        'product': product,
        'reviews': reviews,
        'review_result': review_result,
        'is_review_exist': is_review_exist
    }

    return render(request, template, context)
