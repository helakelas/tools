#-*- coding: utf-8 -*-
#!/usr/bin/env python
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

""" 
{{ model_capital_name }} Task
"""
__author__ = '{{ author }}@163.com'


import os
import sys
try:
    import cPickle as pickle
except:
    import pickle
import simplejson as json
import pandas as pd

from base import Task


class {{ model_capital_name }}(Task):
    """ 
	{{ model_capital_name }} Monitor Task
	"""
    def __init__(self, sender, object_level, frequency, valid, name):
        super({{ model_capital_name }}, self).__init__(object_level, frequency, valid, name)
		self.sender = sender

    def _load(self, conf, logger):
        try:
			self.start_dt = conf.get('{{ model_name }}', 'start_dt')
			self.end_dt = conf.get('{{ model_name }}', 'end_dt')
        	self.{{ model_name }}_filename = conf.get('status_monitor', '{{ model_name }}_filename')
            with open(self.{{ model_name }}_filename, 'r') as fp_r:
				pass
        except Exception as e:
            logger.exception(e)

    def _dump(self, logger):
        try:
            with open(self.{{ model_name }}_filename, 'w') as fp_w:
				pass
        except Exception as e:
            logger.exception(e)

	def run(self, now, logger):
		self.sender.add_head_title(u'时间段 %s - %s' % (self.start_dt, self.end_dt))
		result_df = pd.DataFrame()

		# fill result_df as your need
		pass

		self.sender.add_head_table(result_df.to_html(index=False, escape=False))
		self.sender.send_mail(now, logger)
