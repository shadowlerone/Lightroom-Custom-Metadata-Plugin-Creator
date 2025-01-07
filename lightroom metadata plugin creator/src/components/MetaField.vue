<template>
	<div class="metafield panel" :class="{ 'is-danger': error }">

		<p class="panel-heading">{{ title_string || `New Field ${index + 1}` }}
			<template v-if="advanced == true">
				({{ pluginId }}.{{ id_string }}) / {{ _uuid }}
			</template>
		</p>


		<div class="panel-block">
			<div class="control">
				<div class="field is-grouped">
					<label class="label">
						Title
						<div class="control is-expanded">
							<input required @change="update_id_from_title()" class="input" type="text"
								:class="{ 'is-danger': title_string == '' }" placeholder="title" v-model="title_string">
						</div>
					</label>
					<template v-if="advanced">
						<label class="label">
							ID
							<div class="control is-expanded">
								<input :class="{ 'is-danger': id_string == '' }" required @change="update_id()"
									class="input" type="text" placeholder="id" v-model="id_string">
							</div>
						</label>
					</template>

				</div>
				<template v-if="advanced">
					<!-- searchable -->
					<div class="field is-grouped">
						<label class="checkbox">
							<input checked @change="update_searchable()" class="checkbox" name="searchable"
								type="checkbox" v-model="searchable" />
							Searchable
						</label>
						<label class="checkbox">
							<input checked class="checkbox" name="browsable" type="checkbox" v-model="browsable"
								:disabled="browsable_disabled" />
							Browsable
						</label>
					</div>


				</template>

				<!-- DataType -->
				<div class="field">
					<label class="label">
						DataType: {{ dataType }}
					</label>
					<div class="select">
						<select v-model="dataType">
							<option selected="selected" value="string">String</option>
							<option value="url">Url</option>
							<option value="enum">Enum</option>
						</select>
					</div>
				</div>
			</div>
		</div>

		<template v-if="dataType == 'enum'">
			<div class="panel-block">
				<div class="control">
					<div class="field">
						<label>
							Title for "None"
							<input class="input" v-model="noneName">
						</label>
					</div>
					<div class="field" v-if="advanced">
						<label>
							<input type="checkbox" v-model="allowPluginToSetOtherValues" />
							Allow plugin to set other values
						</label>
					</div>
					<div class="control">
						<EnumValueField :advanced="advanced" :index="i + 1" v-model="values"
							v-for="(v, i) in values.slice(1)" :key="v.value" />
						<button @click.prevent="values.push('')" class="button">Add</button>
					</div>
				</div>
				<template v-if="advanced">
					<div class="control">
						{{ values }}
					</div>
				</template>
			</div>
		</template>
		<div class="panel-block">
			<button class="button" @click.prevent="$emit('delete_field', index)">Delete</button>
		</div>
		<div class="panel-block" v-if="advanced">
			<div class="control">
				<!-- <DataDebug :data="model"/> -->
				<pre><code>{{ JSON.stringify(model[index], null, 4) }}</code></pre>
			</div>
			<div class="control">
				<pre><code>{{ JSON.stringify(id_default, null, 4) }}</code></pre>
			</div>
		</div>
	</div>
</template>

<script setup>
console.log("Redrawing")
import EnumValueField from './EnumValueField.vue'
import DataDebug from './dataDebug.vue'
import { ref, reactive, computed, onMounted, onBeforeUpdate } from 'vue';
import { sanitize, to_id } from '../utils.js'
const props = defineProps({ 'index': Number, 'pluginId': String, 'advanced': Boolean, 'uuid': Number })
const emits = defineEmits('delete_field')

let dataType = ref('string')
let searchable = ref(true)
let browsable = ref(true)
let browsable_disabled = ref(false)

let id_default = ref(true)
let title_string = ref(`New Field ${props.index + 1}`)
let allowPluginToSetOtherValues = ref(true)

let noneName = ref('None')
let values = ref([{ 'title': noneName, 'value': 'nil' }])
let id_string = ref(to_id(title_string.value))
// let uuid = ref(0)
const computed_id_string = computed(() => {
	// console.debug(`updated computed_id_string: ${to_id(title_string.value)}`)
	return to_id(title_string.value)
})
let _uuid = ref()
onMounted(() => {
	// console.log(`the component is now mounted.`)
	console.log(`props.uuid = ${props.uuid}`)
	_uuid.value = props.uuid
	// model.value[props.index].uuid = _uuid
})

onBeforeUpdate(() => {
	console.log(model.value[props.index].id)
	id_string.value = model.value[props.index].id
	title_string.value = model.value[props.index].title
	searchable.value = model.value[props.index].searchable
	browsable.value = model.value[props.index].browsable
	dataType.value = model.value[props.index].dataType
	values.value = model.value[props.index].values
	allowPluginToSetOtherValues.value = model.value[props.index].allowPluginToSetOtherValues
	error.value = model.value[props.index].error
})

let model = defineModel({
	// required: true,
})

let title_error = computed(() => {
	return title_string.value == ''
})

let id_error = computed(() => {
	return id_string.value == ''
})

let enum_error = computed(() => {
	var empty = (values.value.length == 0 && dataType.value == 'enum')
	var field_error = dataType.value == 'enum' && values.value.some(e => e.error)
	return empty || field_error

})

let error = computed(() => {
	return (
		title_error.value ||
		id_error.value ||
		enum_error.value
	)
})

function copy_from_model(model, source_string, tmp_string) {
	// console.debug(`set ${tmp_string} = ${source_string}`)
	var _id = model;
	// console.debug(`Checking id at ${source_string}: ${_id}`)
	if (_id == undefined) {
		// console.debug(`Checking id value at model.value[props.index].id.value: ${_id.value}`) 
		// console.debug("Source is undefined. Returning")
		return false;
	}
	// console.log(`Copying (${_id})`);
	return true
}
// console.debug("======================================================================")
// if (copy_from_model(model.value[props.index].uuid, "model.value[props.index].uuid", "_uuid")) { uuid.value = model.value[props.index].uuid }
console.log(model.value)
if (typeof model.value == "number") {
	uuid.value = model.value[props.index]
}

if (copy_from_model(model.value[props.index].id, "model.value[props.index].id", "_id")) { id_string.value = model.value[props.index].id }

if (copy_from_model(model.value[props.index].title, "model.value[props.index].title", "_title")) { title_string.value = model.value[props.index].title }

if (copy_from_model(model.value[props.index].searchable, "model.value[props.index].searsearchable", "_s")) { searchable.value = model.value[props.index].searchable }

if (copy_from_model(model.value[props.index].browsable, "model.value[props.index].browsable", "_b")) { browsable.value = model.value[props.index].browsable }

if (copy_from_model(model.value[props.index].dataType, "model.value[props.index].dataType.value", "_dt")) { dataType.value = model.value[props.index].dataType }

if (copy_from_model(model.value[props.index].values, "model.value[props.index].values.value", "_v")) { values.value = model.value[props.index].values }

if (copy_from_model(model.value[props.index].allowPluginToSetOtherValues, "model.value[props.index].allowPluginToSetOtherValues", "_aptsov")) { allowPluginToSetOtherValues.value = model.value[props.index].allowPluginToSetOtherValues }

if (copy_from_model(model.value[props.index].error, "model.value[props.index].error", "_e")) { error.value = model.value[props.index].error }


// console.debug("======================================================================")

model.value[props.index] = {
	'id': id_string,
	'title': title_string,
	'searchable': searchable,
	'browsable': browsable,
	'dataType': dataType,
	'values': values,
	'allowPluginToSetOtherValues': allowPluginToSetOtherValues,
	'error': error
}
// id_default.value = id_string.value == title_string.vale
// if (model.value == '') {
// 	console.log("creating a new field")
// 	model.value = {
// 		'id': id_string,
// 		'title': title_string,
// 		'searchable': searchable,
// 		'browsable': browsable,
// 		'dataType': dataType,
// 		'values': values,
// 		'allowPluginToSetOtherValues': allowPluginToSetOtherValues,
// 		'error': error
// 	}
// } else {
// 	console.log("copying existing field")
// 	id_string = model.value.id
// 	title_string = model.value.title_string
// 	searchable = model.value.searchable
// 	browsable = model.value.browsable
// 	dataType = model.value.dataType
// 	values = model.value.values
// 	allowPluginToSetOtherValues = model.value.allowPluginToSetOtherValues
// 	error = model.value.error
// }
// model.value = {
// 	'id': id_string,
// 	'title': title_string,
// 	'searchable': searchable,
// 	'browsable': browsable,
// 	'dataType': dataType,
// 	'values': values,
// 	'allowPluginToSetOtherValues': allowPluginToSetOtherValues,
// 	'error': error
// }


function update_id_from_title() {
	console.debug("Called updated_id_from_title()")
	if (id_default.value == true) {
		console.debug("default id is true. using computed id string")
		console.debug(`Default id string: ${computed_id_string.value}`)
		id_string.value = computed_id_string.value
	}
	console.debug("End of update_id_from_title")
}
function update_id() {
	console.debug("Called update_id()")
	console.debug("Sanitizing id")
	console.debug(`id before: ${id_string.value}`)
	id_string.value = to_id(id_string.value)
	console.debug(`id before: ${id_string.value}`)
	console.debug("Checking if id is blank")
	if (id_string.value == "") {
		console.debug("id is blank, setting id_default to true")
		id_default.value = true
		console.debug("updating id based on title")
		update_id_from_title()
	} else {
		console.debug("Default id being set to false. Id is decoupled from title")
		id_default.value = false
	}
}

function update_searchable() {
	console.debug("Updating searchable");
	if (searchable.value == false) {
		console.debug("Searchable set to false.");
		browsable.value = false
		console.debug("Browsable now set to false.");
		browsable_disabled.value = true
		console.debug("Browsable now disabled.");
	} else {
		console.debug("Searchable set to true.");
		console.debug("Browsable now enabled.");
		browsable_disabled.value = false
		console.debug("Browsable set to true.");
		browsable.value = true
	}
	console.log(searchable.value)
	console.log(browsable.value)
}
</script>

<style scoped>
/* .metafield {
	border: 1px solid grey;
	padding: 2rem;
	border-radius: 5px;
} */
</style>