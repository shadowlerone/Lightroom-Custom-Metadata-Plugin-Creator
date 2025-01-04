from pathlib import Path
import os
from enum import Enum, StrEnum, auto
import json
import logging


with open(f"{os.path.dirname(__file__)}/template.lrplugin/CustomMetadata.lua") as fp:
	CUSTOM_METADATA_TEMPLATE = fp.read()

with open(f"{os.path.dirname(__file__)}/template.lrplugin/Info.lua") as fp:
	INFO_LUA_TEMPLATE = fp.read()

with open(f"{os.path.dirname(__file__)}/template.lrplugin/Tagset.lua") as fp:
	TAGSET_TEMPLATE = fp.read()

class Value():
	def __init__(self, value: str, title: str= None):
		self.value = value
		if title:
			self.title = title
		else:
			if value == None:
				self.title = ""
			else:
				self.title = value.capitalize()
		
	def export(self):
		v = self.value
		if v == None:
			v = 'nil'
		return f"""
{{
	value = '{v}',
	title = '{self.title}',
}}
"""

class DataType(StrEnum):
	STRING = auto()
	URL = auto()
	ENUM = auto()

class Field():
	def __init__(
			self, 
			id:str, 
			title:str = None, 
			dataType:DataType = DataType.STRING, 
			searchable:bool = True, 
			browsable:bool = True, 
			values:list[Value] = None, 
			allowPluginToSetOtherValues = True
		):
		self.update_id(id)
		self.update_title(title)
		self.update_type(dataType)
		self.searchable = searchable
		self.browsable = browsable
		if values:
			self.values = values
		else:
			self.values = []
		self.allowPluginToSetOtherValues = allowPluginToSetOtherValues

	def update_type(self, dataType: DataType) -> int:
		if dataType not in DataType:
			raise ValueError
		self.dataType = dataType

		if dataType == DataType.ENUM:
			return 1 # tell the controller to update the UI
		else:
			return 0

	def update_id(self, new_id:str):
		self.id = new_id

	def update_title(self, title:str = None):
		if title:
			self.title = title
		else:
			self.title = self.id

	def update_searchable(self, s):
		self.searchable = s

	def update_browsable(self, b):
		if b:
			if self.searchable:
				self.browsable = b
			else:
				self.browsable = False
				raise ValueError("browsable cannot be set if searchable is false")
		else:
			self.searchable = b
	
	def add_value(self, title=None, value=None):
		self.values.append(
			Value(title=title, value=value)
		)
		if value == None:
			if any([v.value == None for v in self.values ]):
				pass # warning: multiple None values. Only one allowed.
			pass
		# return len(self.values) - 1

	def remove_value(self, index:int):
		self.values.pop(index)
		pass

	def update_value(self, index:int, title:str=None, value:str=None):
		if title:
			pass
		if value:
			pass

	def export(self) -> str:
		dictionary = {
			'id': self.id,
			'title': self.title,
			'dataType': str(self.dataType),
			'searchable': self.searchable,
			'browsable': self.browsable,
			'allowPluginToSetOtherValues': self.allowPluginToSetOtherValues
		}
		if self.dataType == 'enum':
			dictionary['values'] = self.values
		return Field.dict_to_string(dictionary)
	
	def dict_to_string(d) -> str:
		if d['dataType'] == 'enum':
			value_string = ", ".join([v.export() for v in d['values']])
			return f"""
{{
	id = '{d['id']}',
	title = '{d['title']}',
	dataType = '{d['dataType']}',
	searchable = {str(d['searchable']).lower()},
	browsable = {str(d['browsable']).lower()},
	values = {{ {value_string},  allowPluginToSetOtherValues = {str(d['allowPluginToSetOtherValues']).lower()}}}
}}
"""
		else:
			return f"""{{
	id = '{d['id']}',
	title = '{d['title']}',
	dataType = '{d['dataType']}',
	searchable = {str(d['searchable']).lower()},
	browsable = {str(d['browsable']).lower()},
}}
"""


class MetadataFields():
	fields:list[Field] = []
	def __init__(self, schemaVersion:int = 1, metadataFields:list[Field] = []):
		self.schemaVersion = schemaVersion
		if metadataFields:
			self.fields = metadataFields

	def add_field(self, field:Field):
		self.fields.append(field)

	def remove_field(self, index:int):
		self.fields.pop(index)

	def __getitem__(self, key):
		return self.field[key]
	
	def __setitem__(self,key, newvalue):
		self.field[key] = newvalue

	def export(self) -> str:
		return ",".join([f.export() for f in self.fields])


class Plugin():
	def __init__(self, name:str, SdkVersion:int = 2, metadataProvider:str = "CustomMetadata.lua", mfields:MetadataFields = None):
		self.name = name
		self.id = f"shadowlerone.{self.name}.Metadata"
		self.sdkversion = SdkVersion
		self.MetadataProvider = metadataProvider
		if mfields:
			self.MetadataFields = mfields
		else:
			self.MetadataFields = MetadataFields()

	def export(self):
		plugin_base_path = Path(f"tmp/{self.name}.lrplugin")
		plugin_base_path.mkdir(parents=True, exist_ok=True)
		# Write Info.lua
		with open(plugin_base_path/"Info.lua", "w") as fp:
			fp.write(INFO_LUA_TEMPLATE.format(name=self.name, id=self.id))



		# Write CustomMetadata.lua
		with open(plugin_base_path/"CustomMetadata.lua", "w") as fp:

			fp.write(

				CUSTOM_METADATA_TEMPLATE.format(
					schemaVersion = self.MetadataFields.schemaVersion,
					id = self.id,
					customMetadata = self.MetadataFields.export()
				)
			)


		# Write Tagset.lua
		with open(plugin_base_path/"Tagset.lua", "w") as fp:
			fp.write(
				TAGSET_TEMPLATE.format(name = self.name, id=self.id)
			)
		return plugin_base_path

	def load(fp:str):
		with open(fp) as f:
			data = json.load(f)

		Plugin._l(data)
		
	
	def loads(string:str):
		Plugin._l(json.loads(string))

	def _l(data: dict):
		plugin = Plugin(data['name'])
		for mf in data['mfields']:
			field = Field(
					id=mf['id'],
					title=mf['title'],
					searchable=mf['searchable'],
					browsable=mf['browsable'],
					dataType=mf['dataType']
				)
			if mf['dataType'] == 'enum':
				field.allowPluginToSetOtherValues = mf['allowPluginToSetOtherValues']
				for v in mf['values']:
					field.add_value(title=v['title'], value=v['value'])
			plugin.MetadataFields.add_field(field)

		return plugin


	

if __name__ == "__main__":
	p = Plugin("Test Plugin")
	p.MetadataFields.add_field(Field("tester", "Testing Field"))
	p.MetadataFields.add_field(Field("tester2", "Testing Field 2"))
	# p.MetadataFields.add_field(Field("tester", "Testing Field"))
	# p.MetadataFields.add_field(Field("tester", "Testing Field"))
	p.export()
