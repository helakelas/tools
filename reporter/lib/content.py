#-*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :


""" Element With Business Logic"""
__author__ = "chutong"


import pandas as pd
from base import Leaf 


class Content(Leaf):
	"""
	Render each part of a report
	"""
	def __init__(self, conf, name=''):
		# define data_query
		self._data_query = None
		# define renderer
		self._renderer = None
		# define query dimenions
		self._dimensions = []
		# define query metrics 
		self._metrics = []
		# set name
		self._name = name
		# dataframe for content
		self._df = None

	def set_data_query(self, data_query):
		self._data_query = data_query

	def set_renderer(self, renderer):
		self._renderer = renderer

	@property
	def name(self):
		return self._name

	@property
	def handler(self):
		return self._handler

	@handler.setter
	def handler(self, handler):
		self._handler = handler

	@property
	def dimensions(self):
		return self._dimensions

	@dimensions.setter
	def dimensions(self, dimensions=[]):
		self._dimensions = dimensions

	@property
	def metrics(self):
		return self._metrics

	@metrics.setter
	def metrics(self, metrics=[]):
		self._metrics = metrics

	@property
	def df(self, logger):
		return self._df

	@df.setter
	def df(self, df):
		if not isinstance(df, pd.DataFrame):
			raise TypeError("df must be a DataFrame")
		self._df = df

	@property
	def df_attributes(self):
		if self._df.empty:
			raise ValueError("Dataframe is Empty, call query_df first")
		return self._df.columns.values.tolist()

	def _check_attribute(self, logger):
		# we may permit no df input, if only render word
		#if not df_columns:
		#	return False
		df_columns = self.df_attributes
		for attribute in (self._dimensions + self._metrics):
			if attribute not in df_columns:
				logger.error('attribute[%s] not in input dataframe' % attribute)
				return False
		return True

	def query_df(self, logger):
		if not self._data_query:
			raise ValueError("data_query is None")
		self._df = self._data_query.query(logger)

	def render(self, logger):
		try:
			if self._df.empty:
				self._df = self._data_query.query(logger)
			if not self._check_attribute(logger):
				raise ValueError("part dimensions %s or metrics %s not defined in dataframe columns %s" % (str(self._dimensions), str(self._metrics), str(self.df_attributes)))
			self._renderer.name = self._name
			self._renderer.run(self._df, self._dimensions, self._metrics, self._handler, logger)
		except ValueError as e:
			logger.exception(e)
		except Exception as e:
			logger.exception(e)
