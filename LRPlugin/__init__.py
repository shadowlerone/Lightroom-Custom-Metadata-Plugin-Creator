from pathlib import Path
import os
from enum import IntEnum, auto
import json
from typing import Optional, Union

with open(f"{os.path.dirname(__file__)}/template.lrplugin/CustomMetadata.lua") as fp:
	CUSTOM_METADATA_TEMPLATE = fp.read()

with open(f"{os.path.dirname(__file__)}/template.lrplugin/Info.lua") as fp:
	INFO_LUA_TEMPLATE = fp.read()

with open(f"{os.path.dirname(__file__)}/template.lrplugin/Tagset.lua") as fp:
	TAGSET_TEMPLATE = fp.read()

class Value():
	"""
	Docstring for Value
	Represent possible values if Field type is DataType.Enum
	"""
	def __init__(self, value: Optional[str], title: Optional[str]= None) -> None:
		"""
		Docstring for __init__
		
		:param self: Description
		:param value: Description
		:type value: Optional[str]
		:param title: Description
		:type title: Optional[str]
		"""
		self.value = value
		if title:
			self.title = title
		else:
			if value == None:
				self.title = ""
			else:
				self.title = value.capitalize()
		
	def export(self) -> str:
		"""
		Docstring for export
		
		:param self: Description
		:return: Description
		:rtype: str
		"""
		v = self.value
		if v == None:
			v = 'nil'
		return f"""
{{
	value = '{v}',
	title = '{self.title}',
}}
"""

class DataType(IntEnum):
	"""
	DataTypes for Lightroom Field.
	
	`STRING`: String

	`URL`: URL

	`ENUM`: Options
	"""
	STRING = auto()
	URL = auto()
	ENUM = auto()

class Field():
	"""
	Docstring for Field
	"""
	def __init__(
			self, 
			id:str, 
			title:Optional[str] = None, 
			dataType:DataType = DataType.STRING, 
			searchable:bool = True, 
			browsable:bool = True, 
			values:Optional[list[Value]] = None, 
			allowPluginToSetOtherValues = True
		) -> None:
		"""
		:param id: Field id. Must be Unique.
		:type id: str
		:param title: Human friend name of Field
		:type title: Optional[str]
		:param dataType: Field Datatype
		:type dataType: DataType
		:param searchable: `True`: Field can be searched in Lightroom. `False`: Field cannot be searched in Lightroom
		:type searchable: bool
		:param browsable: TODO: Read the docs
		:type browsable: bool
		:param values: Possible values if `dataType` is `DataType.ENUM`.
		:type values: Optional[list[Value]]
		:param allowPluginToSetOtherValues: If `dataType` == `DataType.ENUM`, can the plugin logic set value to something not present in `values`
		"""
		self.update_id(id)
		self.update_title(title)
		self.update_type(dataType)
		self.searchable = searchable
		self.browseable = browsable
		if values:
			self.values = values
		else:
			self.values = []
		self.allowPluginToSetOtherValues = allowPluginToSetOtherValues

	def update_type(self, dataType: DataType) -> int:
		"""
		Update the `Field`'s type.

		**Important**: when going from `ENUM` to any other type, it **does not** delete `values`.

		:param dataType: New Datatype
		:type dataType: DataType
		:return: `1` if `dataType` == `DataType.ENUM` (for updating the UI), `0` otherwise.
		:rtype: int
		"""
		if dataType not in DataType:
			raise ValueError
		self.dataType = dataType

		if dataType == DataType.ENUM:
			return 1 # tell the controller to update the UI
		else:
			return 0

	def update_id(self, new_id:str) -> None:
		"""
		Update `Field` id. 

		:param new_id: New id
		:type new_id: str
		"""
		self.id = new_id

	def update_title(self, title:Optional[str] = None) -> None:
		"""
		Update `Field` title
			
		:param title: New `title`. If `None`: sets `title` to `id`
		:type title: Optional[str]
		"""
		if title:
			self.title = title
		else:
			self.title = self.id

	def update_searchable(self, searchable: bool) -> None:
		"""
		Updates `searchable`.
		
		:param searchable: should it be searchable. Will set to `True` if passed value is truthy, otherwise will be set to `False`.
		:type searchable: bool
		"""
		self.searchable = bool(searchable)

	def update_browseable(self, browseable: bool, strict=True) -> None:
		"""
		Updates `browseable`. 
		
		Per Lightroom documentation, `browseable` can only be `True` if `searchable` is `True`.
		
		:param browseable: New `browseable` value.
		:type browseable: bool
		:param strict: Throw an error if browseable is set to `True` while `searchable` is set to fall.
		:type strict: bool
		"""
		if browseable:
			if self.searchable:
				self.browseable = browseable
			else:
				if strict:
					raise ValueError("browsable cannot be set if searchable is false")
				else:
					self.browseable = False
		else:
			self.searchable = browseable
	
	def add_value(self, title: Optional[str] =None, value: Optional[str]=None) -> None:
		"""
		Adds possible values for `dataType` == `ENUM`.

		**Important**: Only **one** value in the list can be `None`.
		
		:param title: Human friendly name for the `value`
		:type title: Optional[str]
		:param value: Computer friendly name for the `value`.
		:type value: Optional[str]
		"""
		self.values.append(
			Value(title=title, value=value)
		)
		if value == None:
			if any([v.value == None for v in self.values ]):
				pass # warning: multiple None values. Only one allowed.
			pass
		# return len(self.values) - 1

	def remove_value(self, index:int) -> None:
		"""
		Docstring for remove_value
		
		:param self: Description
		:param index: Description
		:type index: int
		"""
		self.values.pop(index)
		pass

	def update_value(self, index:int, title:Optional[str]=None, value:Optional[str]=None) -> None:
		"""
		Update value.
		
		:param index: index of value to change
		:type index: int
		:param title: new human friendly `title`
		:type title: Optional[str]
		:param value: new computer friendly `value`
		:type value: Optional[str]
		"""
		raise NotImplementedError
		# TODO
		if title:
			pass
		if value:
			pass

	def export(self) -> str:
		"""
		Export field.
	
		:return: `str` representation of the Field for building the plugin.
		:rtype: str
		"""
		dictionary = {
			'id': self.id,
			'title': self.title,
			'dataType': str(self.dataType),
			'searchable': self.searchable,
			'browsable': self.browseable,
			'allowPluginToSetOtherValues': self.allowPluginToSetOtherValues
		}
		if self.dataType == DataType.ENUM:
			dictionary['values'] = self.values
		return Field.dict_to_string(dictionary)
	
	@staticmethod
	def dict_to_string(d: dict) -> str:
		"""
		Converts `dict` representation of `Field` to `str` (Lua code). 
		
		:param d: `dict` representation of `Field`
		:type d: dict
		:return: Lua version of `Field`
		:rtype: str
		"""
		if d['dataType'] == DataType.ENUM:
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
	"""
	Docstring for MetadataFields
	"""
	# fields:list[Field] = []
	def __init__(self, schemaVersion:int = 1, metadataFields:list[Field] = []) -> None:
		"""
		Docstring for __init__
		
		:param self: Description
		:param schemaVersion: Description
		:type schemaVersion: int
		:param metadataFields: Description
		:type metadataFields: list[Field]
		"""
		self.schemaVersion = schemaVersion
		if metadataFields:
			self.fields = metadataFields
		else:
			self.fields = []

	def add_field(self, field:Field) -> None:
		"""
		Docstring for add_field
		
		:param self: Description
		:param field: Description
		:type field: Field
		"""
		self.fields.append(field)

	def remove_field(self, index:int) -> None:
		"""
		Docstring for remove_field
		
		:param self: Description
		:param index: Description
		:type index: int
		"""
		self.fields.pop(index)

	def __getitem__(self, key):
		"""
		Docstring for __getitem__
		
		:param self: Description
		:param key: Description
		"""
		return self.fields[key]
	
	def __setitem__(self,key, newvalue):
		"""
		Docstring for __setitem__
		
		:param self: Description
		:param key: Description
		:param newvalue: Description
		"""
		self.fields[key] = newvalue

	def export(self) -> str:
		"""
		Docstring for export
		
		:param self: Description
		:return: Description
		:rtype: str
		"""
		return ",".join([f.export() for f in self.fields])


class Plugin():
	"""
	Docstring for Plugin
	"""
	def __init__(self, name:str, author
	:str = "shadowlerone", SdkVersion:int = 2, metadataProvider:str = "CustomMetadata.lua", mfields:Optional[MetadataFields] = None) -> None:
		"""
		Docstring for __init__
		
		:param self: Description
		:param name: Description
		:type name: str
		:param author: Description
		:type author: str
		:param SdkVersion: Description
		:type SdkVersion: int
		:param metadataProvider: Description
		:type metadataProvider: str
		:param mfields: Description
		:type mfields: Optional[MetadataFields]
		"""
		self.name = name
		self.id = f"{author}.{self.name}.Metadata"
		self.sdkversion = SdkVersion
		self.MetadataProvider = metadataProvider
		if mfields:
			self.MetadataFields = mfields
		else:
			self.MetadataFields = MetadataFields()
		
		self.json = None

	def export(self) -> Path:
		"""
		Docstring for export
		
		:param self: Description
		:return: Description
		:rtype: Path
		"""
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
		
		if self.json and self.json != '':
			with open(plugin_base_path/"data.json", "w") as fp:
				fp.write(self.json)
		return plugin_base_path

	@staticmethod
	def load(fp:Union[str,Path]) -> "Plugin":
		"""
		Docstring for load
		
		:param fp: Description
		:type fp: str | Path
		:return: Description
		:rtype: Plugin
		"""
		with open(fp) as f:
			data = json.load(f)

		return Plugin._l(data)
		
	@staticmethod
	def loads(string:str) -> "Plugin":
		"""
		Docstring for loads
		
		:param string: Description
		:type string: str
		:return: Description
		:rtype: Plugin
		"""
		return Plugin._l(json.loads(string))

	@staticmethod
	def _l(data: dict) -> "Plugin":
		"""
		Docstring for _l
		
		:param data: Description
		:type data: dict
		:return: Description
		:rtype: Plugin
		"""
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
		plugin.json = json.dumps(data)
		return plugin


	

if __name__ == "__main__":
	p = Plugin("Test Plugin")
	p.MetadataFields.add_field(Field("tester", "Testing Field"))
	p.MetadataFields.add_field(Field("tester2", "Testing Field 2"))
	p.export()
