#-*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

"""
Base maker for template generation
"""
__author__ = "chutong"

import sys, os
import codecs
try:
	import ConfigParser
except: # Python3
	import configparser as ConfigParser
import logging
from jinja2 import Environment, PackageLoader


class BaseMaker(object):
	""" Base Template Maker

	Example:
		$ python bin/base_maker.py -t=tempalte_name1,template_name2

	Attributes:
		template: list of string, define template used in templates/
		_common_params: params used in all templates, edited in conf/maker.conf [common]
		template_params_dict: template name related with special params, edited in conf/maker.conf [your_template_name]
	"""
	def __init__(self, templates=[]):
		self._templates = templates
		self._common_params = {}
		self._template_params_dict = {}

	def _generate(self, template_params_dict):
		""" Special parameters generated based on template_params_dict """
		return {}

	def _make(self, template, logger):
		try:
			template_t = self.env.get_template('.'.join([template, 'py']))
			if template_t:
				logger.info('template %s begins to make' % template)
				params = {} if template not in self._template_params_dict else self._template_params_dict[template]
				# add common params
				params.update(self._common_params)
				# add generated params
				params.update(self._generate(self._template_params_dict[template]))
				output_info = template_t.render(params)
				if 'model_name' in params:
					output_filename = os.path.join(self.output_path, '.'.join([params['model_name'], 'py']))
				else:
					output_filename = os.path.join(self.output_path, '.'.join([template, 'py']))
				with codecs.open(output_filename, 'w', encoding='utf-8') as fp_w:
					fp_w.write(output_info)
					
				logger.info('template %s ends to make' % template)
			else:
				logger.error('template %s not defined in templates folder' % template)
				
		except Exception as e:
			logger.exception(e)

	def _load_params(self, conf):
		try:

			for each_section in conf.sections():
				if each_section == 'common':
					self._common_params = dict(conf.items('common'))
				else:
					section_params = dict(conf.items(each_section))
					self._template_params_dict[each_section] = section_params

		except Exception as e:
			logger.exception(e)

	def init(self, conf, logger, script_name, basepath):
		
		# Jinja2 load
		self.env = Environment(loader = PackageLoader(script_name, 'templates'))

		# parameters load
		self._load_params(conf)
		self.output_path = conf.get('common', 'output_path') if conf.has_option('common', 'output_path') else 'output'

	def make(self, logger):

		logger.info('task %s begins' % self.__class__.__name__ )
		[ self._make(template, logger) for template in self._templates ]
		logger.info('task %s ends' % self.__class__.__name__ )


def split_filename(filename):
	paths = os.path.split(filename)
	return os.path.splitext(paths[-1])[0]


if __name__ == '__main__':

	try:
		basepath = os.path.abspath(sys.path[0])

		script_name = os.path.splitext(os.path.basename(__file__))[0]
		logging.basicConfig(filename=os.path.join(basepath, 'logs/' + script_name + '.log'), level=logging.DEBUG,
			format = '[%(filename)s:%(lineno)s - %(funcName)s %(asctime)s;%(levelname)s] %(message)s',
			datefmt = '%a, %d %b %Y %H:%M:%S'
			)
		logger = logging.getLogger('BaseMaker')

		example_word = """example:

			python base_maker.py -t base_template1.py,base_template2.py
			python base_maker.py -t templates/base_template.py -c conf/marker.conf
			python base_maker.py -t templates/base_template.py 
			python base_maker.py -t base_template.py -c conf/marker.conf
			python base_maker.py -t base_template
		"""

		import argparse
		parser = argparse.ArgumentParser(prog='base_maker', description='template maker', epilog=example_word, formatter_class=argparse.RawDescriptionHelpFormatter)
		parser.add_argument('-t', '--templates', help='template names to make, should be defined as section name in conf, and have related file in templates/ folder', type=str)
		parser.add_argument('-c', '--confpath', help='configuration path for template detail info', type=str, default=os.path.join(basepath, 'conf/maker.conf'))
		args = parser.parse_args()
		if not args.templates:
			parser.print_help()
			raise ValueError("no template input from CLI")
		elif not args.confpath:
			parser.print_help()
			raise ValueError("no confpath input from CLI")
		else:
			conf = ConfigParser.RawConfigParser()
			conf.read(args.confpath)
			new_templates = []
			[ new_templates.append(split_filename(template.strip())) for template in args.templates.split(',') ]
			bm = BaseMaker(new_templates)
			bm.init(conf, logger, script_name, basepath)
			bm.make(logger)
	except ValueError, e:
		logger.exception(e)
	except Exception,e:
		logging.exception(e)
