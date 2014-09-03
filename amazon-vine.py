#!/usr/bin/env python

# Copyright 2014, Timur Tabi

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import re
import time
import urllib2
#import HTMLParser
from bs4 import BeautifulSoup
import mechanize
import webbrowser

url = 'https://www.amazon.com/gp/vine/newsletter?ie=UTF8&tab=US_Default'

br = mechanize.Browser()

# Necessary for Amazon.com
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13')]
br.set_handle_referer(True)
br.set_handle_redirect(mechanize.HTTPRedirectHandler)
#br.set_handle_refresh(False)
#br.set_handle_refresh(mechanize.HTTPRefreshProcessor(), max_time=1)
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

while True:
    while True:
        print 'Reading', url
        try:
            br.open(url)
            break
        except urllib2.HTTPError as e:
            print e
        except urllib2.URLError as e:
            print 'URL Error', e
        except Exception as e:
            print 'General Error', e

    # Select the sign-in form
    br.select_form(name='signIn')
    br['email'] = os.getenv('AMAZON_USERID')
    br['password'] = os.getenv('AMAZON_PASSWORD')

    try:
        print 'Logging in ...'
        response = br.submit()
        print response.geturl()
        break
    except urllib2.HTTPError as e:
        print e
    except urllib2.URLError as e:
        print 'URL Error', e
    except Exception as e:
        print 'General Error', e

# We've logged in, so load the page we want
#print 'Loading', url
#br.open(url)

#print response.info()

print 'Reading response ...'
html = response.read()
print 'Parsing response ...'
soup = BeautifulSoup(html)

# Get initial list of items
list = set()
for link in soup.find_all('a'):
    l = link.get('href')
    if l:
        m = re.search('asin=([0-9A-Z]*)', link.get('href'))
        if m:
            list.add(m.group(1))

print list

while True:
    print 'Waiting ...'
    time.sleep(1 * 60)

    while True:
        print 'Reloading ...'
        try:
            response = br.reload()
            print response.geturl()
            break
        except urllib2.HTTPError as e:
            print e
        except urllib2.URLError as e:
            print 'URL Error', e
        except Exception as e:
            print 'General Error', e

    print 'Parsing response ...'
    html = response.read()
    soup = BeautifulSoup(html)

    for link in soup.find_all('a'):
        l = link.get('href')
        if l:
            m = re.search('asin=([0-9A-Z]*)', link.get('href'))
            if m:
                if m.group(1) not in list:
                    print m.group(1)
                    # https://www.amazon.com/gp/vine/product?ie=UTF8&asin=B000A13OF2&tab=US_Default

