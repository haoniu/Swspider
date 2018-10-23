# -*- coding: utf-8 -*-
__author__ = 'Sam'
__date__ = '2018/10/23 10:26'

import re


line = "samb111bo1oooobooob123"
mobile = "139333256234"
#b111b
#regex_str = ".*?(b.*?b).*"

#b123
#regex_str = ".*(b.*3).*"

#booo
#regex_str = ".*(booo).*"

#amb111,bmb111
#regex_str = ".*([ab]mb111)"

#手机号正则匹配
#regex_str = "(^1[35789]\d{9}$)"
#match_obj = re.match(regex_str,mobile)

#if match_obj:
#    print(match_obj.group(1))

#birthday = "xxx出生于2010年6月1日"
#birthday = "xxx出生于2010/6/1"
#birthday = "xxx出生于2010-6-1"
#birthday = "xxx出生于2010-06-01"
birthday = "xxx出生于2010-06"
birthday = "xxx出生于2010年6月"
regex_str = ".*(2\d{3}(年|/|-)\d{1,2}((月|/|-)\d{1,2}$|(月|/|-)$|$|(月|/|-)\d{1,2}(日)))"

match_obj = re.match(regex_str,birthday)
if match_obj:
   print(match_obj.group(1))