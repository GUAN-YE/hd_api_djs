#coding=utf-8
import urlparse
import re
from django.core.paginator import Paginator, InvalidPage
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
import math

urlnames = {'next':_('Next'), 'previous':_('Previous'), 'first':_('First'), 'last':_('Last')}

class QuerysetWrapper(object):
    def __init__(self, t):
        self.list = t
        
    def count(self):
        return len(self.list)
    
    def __getslice__(self, i, j):
        return self.list[max(0, i):max(0, j):]

class Page(object):
    def __init__(self, queryset, request=None, pageno=1, paginate_by=20, urlprefix=None,urlnames=urlnames):
        if isinstance(queryset, QuerySet):
            self.queryset = queryset
        else:
            self.queryset = QuerysetWrapper(queryset)
        self.paginate_by = paginate_by
        self.request = request
        if urlprefix == None and request:
            newurl = re.sub(r'page=\d*', '', self.request.get_full_path())
            self.urlprefix = newurl
        else:
            self.urlprefix = urlprefix
        self.urlname = urlnames
        self.pageno = pageno
        
        paginator = Paginator(self.queryset, paginate_by)
        
        lastpage = math.ceil(1.0*paginator.count/paginate_by)
        
        if self.request and not pageno:
            try:
                page = self.request.GET['page']
            except:
                try:
                    page = self.request.POST.get('page','1')
                except:
                    page = self.pageno
        else:
            page = self.pageno
        try:
            if isinstance(page, str):
                if not page.isdigit():
                    page = 'last'
                    page = lastpage
            page = int(page)
            if page > lastpage:
                page = lastpage
                
            object_list = paginator.page(page).object_list
        except (InvalidPage, ValueError):
            object_list = []
        self.is_paginated = paginator.count > 1
        self.results_per_page = paginate_by
        try:
            self.has_next = paginator.page(page).has_next()
            self.has_previous = paginator.page(page).has_previous()
        except:
            self.has_next = False
            self.has_previous = False
        
        self.page = page
        self.next = page + 1
        self.previous = page - 1
        self.pages = paginator.count
        self.hits = paginator.num_pages
        self.object_list = object_list
        
        
    def next_url(self):
        if self.has_next:
            return '<a href="%spage=%d">%s</a>' % (self.fix_url(self.urlprefix), self.next, self.urlname['next'])
        return ''
        
    def previous_url(self):
        if self.has_previous:
            return '<a href="%spage=%d">%s</a>' % (self.fix_url(self.urlprefix), self.previous, self.urlname['previous'])
        else:
            return ''
        
    def first_url(self):
        if self.pages > 1:
            return '<a href="%spage=1">%s</a>' % (self.fix_url(self.urlprefix), self.urlname['first'])
        else:
            return ''
    
    def last_url(self):
        if self.pages > 1:
            return '<a href="%spage=%d">%s</a>' % (self.fix_url(self.urlprefix), self.pages, self.urlname['last'])
        else:
            return ''
        
    def fix_url(self, url):
        if url.find('?') == -1:
            url = url + '?'
        else:
            if not url.endswith('&') and not url.endswith('?'):
                url = url + '&'
        return url
    
    def page_url(self):
        """
        create page link url 
        exmple: <div><a href="group?page=2">2</a></div>
        """
        start_num = 1
        end_num = 1
        page_url = u''
        page_pre = u''
        page_last = u''
        #总页数小于等于显示分页数
        if self.hits <= 10:
            end_num = self.hits
         
        if self.hits > 10:
            if self.page-8 >=0:
                page_pre = u'<a href="%(href)spage=1">1</a><a href="%(href)spage=2">2</a>...' % {'href':self.fix_url(self.urlprefix)}
                start_num = self.page - 3
            if self.page+6 <= self.hits:
                page_last = u'..<a href="%(href)spage=%(self.page_pre)d">%(self.page_pre)d</a><a href="%(href)spage=%(self.page)d">%(self.page)d</a>' % {'href':self.fix_url(self.urlprefix),'self.page_pre':self.hits-1,'self.page':self.hits}
                
                if page_pre:
                    end_num = self.page + 3
                       
                else:
                    end_num = 8
            else:
                
                end_num = self.hits
                #start_num = self.page - 8
        page_url += page_pre   
        for n in range(start_num, end_num+1):
            if n == self.page:
                page_url += u'<a href="%(href)spage=%(self.page)d" class="current">%(self.page)d</a>' % {'href':self.fix_url(self.urlprefix),'self.page':n}    
            else:
                page_url += u'<a href="%(href)spage=%(self.page)d">%(self.page)d</a>' % {'href':self.fix_url(self.urlprefix),'self.page':n}     
        
        #设置上一页
        if self.page >1:
            page_url = u'<a href="%(href)spage=%(self.page)d">上一页</a>' % {'href':self.fix_url(self.urlprefix),'self.page':self.page-1} + page_url   
        if self.page < self.hits:
            page_last += u'<a href="%(href)spage=%(self.page)d">下一页</a>' % {'href':self.fix_url(self.urlprefix),'self.page':self.page+1}     
        page_url = u'<div class=page_list>'+ page_url + page_last + '</div>'
        if self.hits <=1:
            return ''
        return page_url
    
    def english_page_url(self):
        """
        create page link url 
        exmple: <div><a href="group?page=2">2</a></div>
        """
        start_num = 1
        end_num = 1
        page_url = u''
        page_pre = u''
        page_last = u''
        #总页数小于等于显示分页数
        if self.hits <= 10:
            end_num = self.hits
         
        if self.hits > 10:
            if self.page-8 >=0:
                page_pre = u'<li><a href="%(href)spage=1">1</a></li><li><a href="%(href)spage=2">2</a></li><li>...</li>' % {'href':self.fix_url(self.urlprefix)}
                start_num = self.page - 3
            if self.page+6 <= self.hits:
                page_last = u'<li>...</li><li><a href="%(href)spage=%(self.page_pre)d">%(self.page_pre)d</a></li><li><a href="%(href)spage=%(self.page)d">%(self.page)d</a></li>' % {'href':self.fix_url(self.urlprefix),'self.page_pre':self.hits-1,'self.page':self.hits}
                
                if page_pre:
                    end_num = self.page + 3
                       
                else:
                    end_num = 8
            else:
                
                end_num = self.hits
                #start_num = self.page - 8
        page_url += page_pre   
        for n in range(start_num, end_num+1):
            if n == self.page:
                page_url += u'<li class=on><a href="%(href)spage=%(self.page)d">%(self.page)d</a></li>' % {'href':self.fix_url(self.urlprefix),'self.page':n}    
            else:
                page_url += u'<li><a href="%(href)spage=%(self.page)d">%(self.page)d</a></li>' % {'href':self.fix_url(self.urlprefix),'self.page':n}     
        
        #设置上一页
        if self.page >1:
            page_url = u'<li ><a href="%(href)spage=%(self.page)d">Prev</a></li>' % {'href':self.fix_url(self.urlprefix),'self.page':self.page-1} + page_url   
        if self.page < self.hits:
            page_last += u'<li ><a href="%(href)spage=%(self.page)d">Next</a></li>' % {'href':self.fix_url(self.urlprefix),'self.page':self.page+1}     
        page_url = u'<div class="jx_page1"><ul>'+ page_url + page_last + '</ul></div>'
        if self.hits <=1:
            return ''
        return page_url

    def english_page_ajax_url(self,action='list'):
        """
        create page link url 
        exmple: <div><a href="group?page=2">2</a></div>
        """
        start_num = 1
        end_num = 1
        page_url = u''
        page_pre = u''
        page_last = u''
        #总页数小于等于显示分页数
        if self.hits <= 10:
            end_num = self.hits
         
        if self.hits > 10:
            if self.page-8 >=0:
                page_pre = u'<li><a onclick="go(\'%(action)s\',1)" href="javascript:void(0)">1</a></li><li><a onclick="go(\'%(action)s\',2)" href="javascript:void(0)">2</a></li><li>...</li>' % {'action':action}
                start_num = self.page - 3
            if self.page+6 <= self.hits:
                page_last = u'<li>...</li><li><a onclick="go(\'%(action)s\',%(self.page_pre)d)" href="javascript:void(0)">%(self.page_pre)d</a></li><li><a onclick="go(\'%(action)s\',%(self.page)d)" href="javascript:void(0)">%(self.page)d</a></li>' % {'action':action,'self.page_pre':self.hits-1,'self.page':self.hits}
                
                if page_pre:
                    end_num = self.page + 3
                       
                else:
                    end_num = 8
            else:
                
                end_num = self.hits
                #start_num = self.page - 8
        page_url += page_pre   
        for n in range(start_num, end_num+1):
            if n == self.page:
                page_url += u'<li class="on"><a onclick="go(\'%(action)s\',%(self.page)d)" href="javascript:void(0)">%(self.page)d</a></li>' % {'action':action,'self.page':n}    
            else:
                page_url += u'<li><a onclick="go(\'%(action)s\',%(self.page)d)" href="javascript:void(0)">%(self.page)d</a></li>' % {'action':action,'self.page':n}     
        
        #设置上一页
        if self.page >1:
            page_url = u'<li><a onclick="go(\'%(action)s\',%(self.page)d)" href="javascript:void(0)">Prev</a></li>' % {'action':action,'self.page':self.page-1} + page_url   
        if self.page < self.hits:
            page_last += u'<li><a onclick="go(\'%(action)s\',%(self.page)d)" href="javascript:void(0)">Next</a></li>' % {'action':action,'self.page':self.page+1}     
        page_url = u'<div class="jx_page1"><ul>'+ page_url + page_last + '</ul></div>'
        if self.hits <=1:
            return ''
        return page_url
    
    def page_ajax_url(self, action='list'):
            """
            create page link url 
            exmple: <div><a href="group?page=2">2</a></div>
            <a onclick="go(\'%(action)s\',3)" href="javascript:void(0)">3</a>
            """
            start_num = 1
            end_num = 1
            page_url = u''
            page_pre = u''
            page_last = u''
            #总页数小于等于显示分页数
            if self.hits <= 10:
                end_num = self.hits
             
            if self.hits > 10:
                if self.page-8 >=0:
                    page_pre = u'<a onclick="go(\'%(action)s\',1)" href="javascript:void(0)">1</a><a onclick="go(\'%(action)s\',2)" href="javascript:void(0)">2</a>...' % {'action':action}
                    start_num = self.page - 3
                if self.page+6 <= self.hits:
                    page_last = u'..<a onclick="go(\'%(action)s\',%(self.page_pre)d)" href="javascript:void(0)">%(self.page_pre)d</a><a onclick="go(\'%(action)s\',%(self.page)d)" href="javascript:void(0)">%(self.page)d</a>' % {'action':action,'self.page_pre':self.hits-1,'self.page':self.hits}
                    
                    if page_pre:
                        end_num = self.page + 3
                           
                    else:
                        end_num = 8
                else:
                    
                    end_num = self.hits
                    #start_num = self.page - 8
            page_url += page_pre
            for n in range(start_num, int(end_num)+1):
                if n == self.page:
                    page_url += u'<a onclick="go(\'%(action)s\',%(self.page)d)" href="javascript:void(0)" class="current">%(self.page)d</a>' % {'action':action,'self.page':n}    
                else:
                    page_url += u'<a onclick="go(\'%(action)s\',%(self.page)d)" href="javascript:void(0)">%(self.page)d</a>' % {'action':action,'self.page':n}     
            
            # 设置上一页
            if self.page >1:
                page_url = u'<a onclick="go(\'%(action)s\',%(self.page)d)" href="javascript:void(0)">上一页</a>' % {'action':action,'self.page':self.page-1} + page_url   
            if self.page < self.hits:
                page_last += u'<a onclick="go(\'%(action)s\',%(self.page)d)" href="javascript:void(0)">下一页</a>' % {'action':action,'self.page':self.page+1}     
            page_url = u'<div class=page_list>'+ page_url + page_last + '</div>'
            if self.hits <=1:
                return ''
            return page_url   

def get_page_url(request,allCount,pageSize,pageIndex,urlprefix=None):
        """
        create page link url 
        exmple: <div><a href="group?page=2">2</a></div>
        ----------------------------------------------------
         徐威        2010-01-28        添加request参数
         张钦佩      2010-05-13        添加默认的urlprefix
        """
        hits = 0 #总页数        
        #如果没有制定的urlprefix，则默认为当前请求的url
        if urlprefix == None:
            newurl = re.sub(r'page=\d*', '', request.get_full_path())
            urlprefix = newurl
        else:
            urlprefix = urlprefix           
        urlprefix = urlparsequery(request, urlprefix)
        if allCount>pageSize:
            hits = allCount/pageSize
            if allCount%pageSize != 0:
                hits = hits+1
        else:
            hits = 1
        start_num = 1
        end_num = 1
        page_url = u''
        page_pre = u''
        page_last = u''
        #总页数小于等于显示分页数
        if hits <= 10:
            end_num = hits
         
        if hits > 10:
            if pageIndex-8 >=0:
                page_pre = u'<a href="%(href)spage=1">1</a><a href="%(href)spage=2">2</a>...' % {'href':urlprefix}
                start_num = pageIndex - 3
            if pageIndex+6 <= hits:
                page_last = u'..<a href="%(href)spage=%(pageindex_pre)d">%(pageindex_pre)d</a><a href="%(href)spage=%(pageindex)d">%(pageindex)d</a>' % {'href':urlprefix,'pageindex_pre':hits-1,'pageindex':hits}
                
                if page_pre:
                    end_num = pageIndex + 3
                       
                else:
                    end_num = 8
            else:
                
                end_num = hits
                #start_num = page - 8
        page_url += page_pre   
        for n in range(start_num, end_num+1):
            if n == pageIndex:
                page_url += u'<a href="%(href)spage=%(pageindex)d" class="current">%(pageindex)d</a>' % {'href':urlprefix,'pageindex':n}    
            else:
                page_url += u'<a href="%(href)spage=%(pageindex)d">%(pageindex)d</a>' % {'href':urlprefix,'pageindex':n}     
        
        #设置上一页
        if pageIndex >1:
            page_url = u'<a href="%(href)spage=%(pageindex)d">上一页</a>' % {'href':urlprefix,'pageindex':pageIndex-1} + page_url   
        if pageIndex < hits:
            page_last += u'<a href="%(href)spage=%(pageindex)d">下一页</a>' % {'href':urlprefix,'pageindex':pageIndex+1}     
        page_url = u'<div class=page_list>'+ page_url + page_last + '</div>'
        if hits <=1:
            return ''
        return page_url

def get_ajax_page_url(request,allCount,pageSize,pageIndex):
        """
        create page link url 
        exmple: <div><a href="group?page=2">2</a></div>
        ----------------------------------------------------
         徐威        2010-01-28        添加request参数
         张钦佩      2010-05-13        添加默认的urlprefix
        """
        hits = 0 #总页数        
        if allCount>pageSize:
            hits = allCount/pageSize
            if allCount%pageSize != 0:
                hits = hits+1
        else:
            hits = 1
        start_num = 1
        end_num = 1
        page_url = u''
        page_pre = u''
        page_last = u''
        #总页数小于等于显示分页数
        action="list"
        if hits <= 10:
            end_num = hits
         
        if hits > 10:
            if pageIndex-8 >=0:
                page_pre = u'<a onclick="go(\'%(action)s\',1)" href="javascript:void(0)"><li>1</li></a><a onclick="go(\'%(action)s\',2)" href="javascript:void(0)"><li>2</li></a><li>...</li>' % {'action':action}
                start_num = pageIndex - 3
            if pageIndex+6 <= hits:
                page_last = u'<li>...</li><a onclick="go(\'%(action)s\',%(pageindex_pre)d)" href="javascript:void(0)"><li>%(pageindex_pre)d</li></a><a onclick="go(\'%(action)s\',%(pageindex)d)" href="javascript:void(0)"><li>%(pageindex)d</li></a>' % {'action':action,'pageindex_pre':hits-1,'pageindex':hits}
                
                if page_pre:
                    end_num = pageIndex + 3
                       
                else:
                    end_num = 8
            else:
                
                end_num = hits
                #start_num = pageIndex - 8
        page_url += page_pre   
        for n in range(start_num, end_num+1):
            if n == pageIndex:
                page_url += u'<a onclick="go(\'%(action)s\',%(pageindex)d)" href="javascript:void(0)"><li class="on">%(pageindex)d</li></a>' % {'action':action,'pageindex':n}    
            else:
                page_url += u'<a onclick="go(\'%(action)s\',%(pageindex)d)" href="javascript:void(0)"><li>%(pageindex)d</li></a>' % {'action':action,'pageindex':n}     
        
        #设置上一页
        if pageIndex >1:
            page_url = u'<a onclick="go(\'%(action)s\',%(pageindex)d)" href="javascript:void(0)"><li>上一页</li></a>' % {'action':action,'pageindex':pageIndex-1} + page_url   
        if pageIndex < hits:
            page_last += u'<a onclick="go(\'%(action)s\',%(pageindex)d)" href="javascript:void(0)"><li>下一页</li></a>' % {'action':action,'pageindex':pageIndex+1}     
        page_url = u'<div class=Page_box><ul>'+ page_url + page_last + '</ul></div>'
        if hits <=1:
            return ''
        return page_url
    
def urlparsequery(request,url):
    """
    功能说明：将GET中的请求条件放入url
    ----------------------------------------------------------------
    修改人        修改时间            修改原因
    ----------------------------------------------------------------
    张钦佩        2010-05-13
    """
    if url.find('?') == -1:
        url = url + '?'
    else:
        if not url.endswith('&') and not url.endswith('?'):
            url = url + '&'
    return url
          