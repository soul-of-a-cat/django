from django.shortcuts import render

import catalog.models


def item_list(request):
    template = "catalog/item_list.html"
    queryset = catalog.models.Item.objects.all()
    context = {"items": queryset}
    return render(
        request,
        template,
        context,
    )


def item_detail(request, num):
    template = "catalog/item.html"
    item = catalog.models.Item.objects.filter(id=num)
    if item:
        category = catalog.models.Category.objects.filter(
            id=item[0].category_id,
        )
        context = {
            "item_name": item[0].name,
            "item_text": item[0].text,
            "category": category.name,
            "tags": list(item[0].tags.all()),
        }
    else:
        context = {
            "item_name": "",
            "item_text": "",
            "category": "",
            "tags": "",
        }
    return render(
        request,
        template,
        context,
    )
