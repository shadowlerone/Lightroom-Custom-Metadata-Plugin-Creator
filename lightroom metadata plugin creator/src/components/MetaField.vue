<template>
	<div class="metafield panel" :class="{ 'is-danger': error }">
		<p class="panel-heading">{{ title_string || `New Field ${index + 1}` }}
			<template v-if="advanced == true">
				({{ pluginId }}.{{ id_string }})
			</template>
		</p>
		<div class="panel-block">
			<div class="control">
				<div class="field" :class="{'is-grouped': advanced}">
					<label class="label">
						Title
						<div class="control is-expanded">
							<input required @change="update_title()" class="input" type="text"
								:class="{ 'is-danger': title_string == '' }" placeholder="title" v-model="title_string">
								<p class="help is-danger" v-if="title_string == ''">A blank title is not permitted</p>
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
			<div class="control" v-if="advanced">
				<pre><code>{{ JSON.stringify(model[index], null, 4) }}</code></pre>
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
						<pre><code>{{ JSON.stringify(values, null, 4) }}</code></pre>
					</div>
				</template>
			</div>
		</template>
		<div class="panel-block">
			<button class="button is-danger" @click.prevent="$emit('delete_field', index)">Delete field</button>
		</div>
	</div>
</template>

<script setup>
import EnumValueField from './EnumValueField.vue'
import { ref, computed, onMounted, onBeforeUpdate, onBeforeMount } from 'vue';
import { to_id } from '../utils.js'

const props = defineProps({ 'index': Number, 'pluginId': String, 'advanced': Boolean, 'uuid': Number })
const emits = defineEmits('delete_field')

let model = defineModel()

let dataType = ref('string')
let searchable = ref(true)
let browsable = ref(true)
let browsable_disabled = ref(false)

let id_default = ref(true)
let title_string = ref(`New Field ${props.uuid + 1}`)
let allowPluginToSetOtherValues = ref(true)

let noneName = ref('None')
let values = ref([{ 'title': noneName, 'value': 'nil' }])
let id_string = ref(to_id(title_string.value))

let uuid = ref(props.uuid)
const computed_id_string = computed(() => {
	return to_id(title_string.value)
})
const title_error = computed(() => {
	return title_string.value == ''
})
const id_error = computed(() => {
	return id_string.value == ''
})
const enum_error = computed(() => {
	var empty = (values.value.length == 0 && dataType.value == 'enum')
	var field_error = dataType.value == 'enum' && values.value.some(e => e.error)
	return empty || field_error

})

const error = computed(() => {
	return (
		title_error.value ||
		id_error.value ||
		enum_error.value
	)
})

let data = ref({
	'id': id_string,
	'title': title_string,
	'searchable': searchable,
	'browsable': browsable,
	'dataType': dataType,
	'values': values,
	'allowPluginToSetOtherValues': allowPluginToSetOtherValues,
	'error': error,
	'uuid': uuid
})
// Updates the parent's data with internal data
function setModel() {
	model.value[props.index] = data.value
}
//  Loads parent's data, copying it to internal data
function updateModel() {
	id_string.value = model.value[props.index].id
	title_string.value = model.value[props.index].title
	searchable.value = model.value[props.index].searchable
	browsable.value = model.value[props.index].browsable
	dataType.value = model.value[props.index].dataType
	values.value = model.value[props.index].values
	allowPluginToSetOtherValues.value = model.value[props.index].allowPluginToSetOtherValues
	error.value = model.value[props.index].error
}

// setModel()
// onMounted(() => { setModel() })
onBeforeMount(() => { setModel() })

onBeforeUpdate(() => { updateModel() })


function update_title() {
	title_string.value = title_string.value.trim()
	update_id_from_title()
}

function update_id_from_title() {
	if (id_default.value == true) {
		id_string.value = computed_id_string.value
	}
}
function update_id() {
	id_string.value = to_id(id_string.value)
	if (id_string.value == "") {
		id_default.value = true
		update_id_from_title()
	} else { id_default.value = false }
}

function update_searchable() {
	if (searchable.value == false) {
		browsable.value = false
		browsable_disabled.value = true
	} else {
		browsable_disabled.value = false
		browsable.value = true
	}
}
</script>

<style>
* {
	transition-property: color, background-color;
	transition-duration: 250ms;
	transition-timing-function: ease-in-out;
}
</style>