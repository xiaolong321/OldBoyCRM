# !/usr/bin/env python3
# coding:utf-8
from django.utils.safestring import mark_safe


class PageInfo:
    def __init__(self, current_page, all_count, per_item=10):
        self.CurrentPage = int(current_page)
        self.AllCount = all_count
        self.PerItem = per_item

    @property
    def start(self):
        return (self.CurrentPage - 1) * self.PerItem

    @property
    def end(self):
        return self.CurrentPage * self.PerItem

    @property
    def all_page_count(self):
        temp = divmod(self.AllCount, self.PerItem)
        if temp[1] == 0:
            all_page_count = temp[0]
        else:
            all_page_count = temp[0] + 1

        return all_page_count


def Page(page, all_page_count,url_path):
    page_html = []

    # first_html = "<a href='/crm/customers_library/%d'>首页</a>" % (1,)
    first_html = '''<li class="footable-page-arrow">
									<a class="action_url" data-page="first" href='#' href_url="%s/%d">«</a>
								</li>'''% (url_path,1)
    page_html.append(first_html)

    if page <= 1:
        # pre_html = "<a href=''>前一页</a>"
        pre_html = '''<li class="footable-page-arrow">
									<a class="action_url" data-page="prev" href="#">‹</a>
								</li>'''

    else:
        # pre_html = "<a href='/crm/customers_library/%d'>前一页</a>" % (page - 1,)
        pre_html = '''<li class="footable-page-arrow">
									<a class="action_url" data-page="prev" href='#' href_url="%s/%d">‹</a>
								</li>''' % (url_path,page - 1)
    page_html.append(pre_html)

    if all_page_count < 5:
        begin = 0
        end = all_page_count
    else:
        if page < 5:
            begin = 0
            end = 5
        else:
            if page + 2 > all_page_count:
                begin = page - 3
                end = all_page_count
            else:
                begin = page - 3
                end = page + 2

    for i in range(begin, end):
        if page == i + 1:
            # a_html = "<a style='color:red' href='/crm/customers_library/%d' > %d </a>" % (i + 1, i + 1)
            a_html = '''<li class="footable-page" >
									<a class="action_url" data-page="" href='#' href_url="%s/%d" style='color:white;background:#5e455b;'>%d</a>
								</li>''' % (url_path,i + 1, i + 1)
        else:
            # a_html = "<a  href='/crm/customers_library/%d' > %d </a>" % (i + 1, i + 1)
            a_html = '''<li class="footable-page">
									<a class="action_url" data-page="" href='#' href_url="%s/%d">%d</a>
								</li>''' % (url_path,i + 1, i + 1)
        page_html.append(a_html)

    if page < all_page_count:
        # aft_html = "<a href='/crm/customers_library/%d'>下一页</a>" % (page + 1)
        aft_html = '''  <li class="footable-page-arrow">
						    <a class="action_url"class="action_url" data-page="next" href='#' href_url="%s/%d">›</a>
					    </li>''' % (url_path,page + 1)

    else:
        # aft_html = "<a href=''>下一页</a>"
        aft_html = '''<li class="footable-page-arrow">
							<a class="action_url" data-page="next" href="#">›</a>
					</li>'''
    page_html.append(aft_html)
    if all_page_count >0:

        end_html = '''<li class="footable-page-arrow"><a class="action_url" data-page="last" href='#' href_url="%s/%d">»</a></li>'''% (url_path,all_page_count)
    else:
        end_html = '''<li class="footable-page-arrow"><a class="action_url" data-page="last" href='#' href_url="%s/%d">»</a></li>''' % (url_path, 1)

    page_html.append(end_html)

    return mark_safe(' '.join(page_html))
