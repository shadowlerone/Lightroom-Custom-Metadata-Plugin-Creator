<template>
	<div class="metafield panel">
		<template v-if="advanced == true">
			<p class="panel-heading">{{ pluginId }}.{{ id_string }}</p>
		</template>
		<template v-else>
			<p class="panel-heading">{{ title_string }}</p>
		</template>

		<div class="panel-block">
			<div class="control">
				<div class="field is-grouped">
					<label class="label">
						Title
						<div class="control is-expanded">
							<input @change="update_id_from_title()" class="input" type="text" placeholder="title"
								v-model="title_string">
						</div>
					</label>
					<template v-if="advanced">
						<label class="label">
							ID
							<div class="control is-expanded">
								<input @change="update_id()" class="input" type="text" placeholder="id"
									v-model="id_string">
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
							<input type="checkbox" v-model="allowPluginToSetOtherValues" />
							Allow plugin to set other values
						</label>
					</div>
					<div class="control">
						<template v-for="(v, i) in values" :key="i">
							<EnumValueField :advanced="advanced" :index="i" v-model="values" />
						</template>
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
	</div>
</template>

<script setup>
import EnumValueField from './EnumValueField.vue'
import { ref, reactive, computed } from 'vue';
import { sanitize, to_id } from '../utils.js'
const props = defineProps({ 'index': Number, 'pluginId': String, 'advanced': Boolean })

let dataType = ref('string')
let searchable = ref(true)
let browsable = ref(true)
let browsable_disabled = ref(false)

let id_default = ref(true)
let title_string = ref(`New Field ${props.index + 1}`)
let allowPluginToSetOtherValues = ref(true)

let values = ref([])

// let id_string = ref(sanitize(title_string.value.trim()).toLowerCase())
let id_string = ref(to_id(title_string.value))

const computed_id_string = computed(() => {
	// return sanitize(title_string.value.trim()).toLowerCase()
	return to_id(title_string.value)
})


let model = defineModel({
	// required: true,
})

model.value[props.index] = {
	'id': id_string,
	'title': title_string,
	'searchable': searchable,
	'browsable': browsable,
	'dataType': dataType,
	'values': values,
	'allowPluginToSetOtherValues': allowPluginToSetOtherValues
}


function update_id_from_title() {
	if (id_default.value == true) {
		id_string.value = computed_id_string.value
	}
}
function update_id() {
	// id_string.value = sanitize(id_string.value.trim()).toLowerCase()
	id_string.value = to_id(id_string.value)
	if (id_string.value == "") {
		id_default.value = true
		update_id_from_title()
	} else {
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