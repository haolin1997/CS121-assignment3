from django.views.generic import TemplateView
from django.shortcuts import render
from .utils import SearchResults
from . import *
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'config')))
from Indexer import *
from QueryProcessor import QueryProcessor 
import numpy as np
import math
import time
from nltk.stem import PorterStemmer
from string import ascii_lowercase


class SearchView(TemplateView):
    template_name = "icssearch/result.html"

    def get_context_data(self, **kwargs):

        context = super(SearchView, self).get_context_data(**kwargs)

        #{'view': <googlesearch.views.SearchView object at 0x1036cd0d0>}

        results = []
        try:
            results = []

            index = Indexer()
            query = self.request.GET.get('q', '')
            start_time = time.time() #Return the time to start the search 
            qp = QueryProcessor() 
            urlid = qp.search(query)
            temp = []
            if not urlid:
                print('no url find with given query')
            else:
                #url_id = open('doc_id.txt', 'r').read()
                #url_dict = eval(url_id)
                with open('doc_id.json', 'r') as url_id:
                    url_dict = json.load(url_id, strict=False)
                for i, j in enumerate(urlid):
                    result_str = "#%3d: %s" %(i+1,url_dict[str(j)])
                    results.append( (result_str, url_dict[str(j)]) )

            total_time = time.time() - start_time #The total time used to complete the search
            #time_str = "The search took time %f seconds" % (total_time)
            #print(time_str)
            #results = SearchResults(results)
            pages = self.calculate_pages()
            
        except:
            print("Error occured")
            page = 1
            pages = [0, 1, 2]


        # Defaults
        context.update({
            'items': [],
            'total_results': 0,
            'current_page': 0,
            'prev_page': 0,
            'next_page': 0,
            'search_terms': self.request.GET.get('q', ''),
            'error': results,
            'total_time': 0,
        })

        context.update({
            'items': results,
            'total_results': 20, 
            'current_page': pages[1],
            'prev_page': pages[0],
            'next_page': pages[2],
            'search_terms': self.request.GET.get('q', ''),
            'total_time': total_time,

        })

        return context

    def calculate_pages(self):
        current_page = int(self.request.GET.get('p', 1))
        return (current_page - 1, current_page, current_page + 1)

    def page_to_index(self, page=None):
        if page is None:
            page = self.request.GET.get('p', 1)

        return int(page) * int(SEARCH_RESULTS_PER_PAGE) + 1 - int(SEARCH_RESULTS_PER_PAGE)


def index(request):
    return render(request, 'icssearch/index.html')
