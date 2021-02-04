import csv
from django.http import HttpResponse
from django.views import View
from django.core.cache import cache
from django.shortcuts import render

class Search(View):
    def get(self, request):
        context = {}
        if 'q' in self.request.GET:
            company_name = self.request.GET['q'].upper()
            cols = list(cache.get(next(cache.iter_keys(f"*{company_name}*"))).keys())
            rows = []
            for row in cache.iter_keys(f"*{company_name}*"):
                r = []
                for col in cols:
                    r.append(cache.get(row)[col])
                rows.append(r)

            context['cols'] = cols
            context['rows'] = rows
            context['csv_available'] = company_name
        return render(request, 'website/index.html', context=context)


class DownloadCSV(View):
    def post(self, request, query):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={query.lower()}.csv'

        writer = csv.writer(response)
        company_name = query.upper()

        cols = list(cache.get(next(cache.iter_keys(f"*{company_name}*"))).keys())
        writer.writerow(cols)

        rows = []
        for row in cache.iter_keys(f"*{company_name}*"):
            r = []
            for col in cols:
                r.append(cache.get(row)[col])
            rows.append(r)
            writer.writerow(r)

        return response
