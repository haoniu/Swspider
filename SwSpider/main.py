# -*- coding: utf-8 -*-
__author__ = 'Sam'
__date__ = '2018/10/23 16:40'

import sys
import os

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","jobbole"])