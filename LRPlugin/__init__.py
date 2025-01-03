from pathlib import Path
import os

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
			self.title = value.capitalize()
		
	def export(self):
		return f"""
{{
	value = '{self.value}',
	title = '{self.title}',
}}
"""
		
class Field():
	def __init__(self, id:str, title:str = None, dataType:str = 'string', searchable:bool = True, browsable:bool = True, values:list[Value] = None):
		self.id = id
		if title:
			self.title = title
		else:
			self.title = id
		self.dataType = dataType
		self.searchable = searchable
		self.browsable = browsable
		self.values = values

	# def update_type(self, dataType):
	# 	pass


	# def 

	def export(self) -> str:
		dictionary = {
			'id': self.id,
			'title': self.title,
			'dataType': self.dataType,
			'searchable': self.searchable,
			'browsable': self.browsable,
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
	values = '{{ {value_string} }}'
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

	def export(self) -> str:
		return ",".join([f.export() for f in self.fields])


class Plugin():
	def __init__(self, name:str, SdkVersion:int = 2, metadataProvider:str = "CustomMetadata.lua", mfields:MetadataFields = None):
		self.name = name
		self.id = f"shadowlerone.{self.name}.Metadata"
		self.sdkversion = SdkVersion
		self.MetadataProvider = metadataProvider
		# self.metadataFields = 
		if mfields:
			self.MetadataFields = mfields
		else:
			self.MetadataFields = MetadataFields()

	def export(self):
		plugin_base_path = Path(f"tmp/{self.name}.lrplugin")
		plugin_base_path.mkdir(parents=True, exist_ok=True)
		# Write Info.lua
		with open(plugin_base_path/"Info.lua", "w") as fp:
			fp.write(
				INFO_LUA_TEMPLATE.format(name=self.name, id=self.id)
			)

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


	

if __name__ == "__main__":
	p = Plugin("Test Plugin")
	p.MetadataFields.add_field(Field("tester", "Testing Field"))
	p.MetadataFields.add_field(Field("tester2", "Testing Field 2"))
	# p.MetadataFields.add_field(Field("tester", "Testing Field"))
	# p.MetadataFields.add_field(Field("tester", "Testing Field"))
	p.export()
