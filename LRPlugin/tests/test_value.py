import pytest

from LRPlugin import Value


class TestPlugins:
	def test_init(self):
		t1 = 'test1'
		v = Value(t1)
		assert v.value == t1, "value was not set correctly"
		assert v.title == t1.capitalize(), "title was not automatically set to capitalized version of value"

		v2 = Value(t1, t1)
		assert v2.value == v2.title, "title was not set correctly when both value and title were set"

		v3 = Value(None, t1)
		assert v3.title == t1, "title was not set correctly when value == None and a title was provided"

		v4 = Value(None)
		assert v4.title == "", "title was not set to empty string when value == None and no title was provided"

	def test_export(self):
		t1 = 'test1'
		v = Value(t1)
		expected = f"""
{{
	value = '{v.value}',
	title = '{v.title}',
}}
"""
		assert v.export() == expected, "did not export properly"

		expected = f"""
{{
	value = '{t1}',
	title = '{t1.capitalize()}',
}}
"""
		assert v.export() == expected, "Value and title did not export properly when only value was provided"


		v = Value(t1,t1)
		expected = f"""
{{
	value = '{t1}',
	title = '{t1}',
}}
"""
		assert v.export() == expected, "Value or title did not export properly when both were provided"

		v = Value(None,t1)
		expected = f"""
{{
	value = 'nil',
	title = '{t1}',
}}
"""
		assert v.export() == expected, "Value or title did not export properly value was None and title was provided"

		v = Value(None)
		expected = f"""
{{
	value = 'nil',
	title = '',
}}
"""
		assert v.export() == expected, "Value or title did not export properly value was None and title was not provided"

