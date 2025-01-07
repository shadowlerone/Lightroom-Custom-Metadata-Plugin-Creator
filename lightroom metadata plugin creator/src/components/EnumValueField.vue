<template>
	<div class="field has-addons" :class="{'has-danger': error}">
		<div class="control">
			<div class="control is-expanded">
				<input :class="{ 'is-danger': (title == '') }" required @change="update_title()" class="input"
					type="text" v-model="title" placeholder="Title">
			</div>
		</div>
		<div class="control" v-if="advanced">
			<div class="control">
				<input :class="{ 'is-danger': (value == '') }" required @change="update_value()" class="input"
					type="text" v-model="value" placeholder="value">
			</div>
		</div>
		<div class="control">
			<div class="control">
				<button type="button" class="button is-danger" @click.prevent="$emit('delete_value', index)">Delete
					Value</button>
			</div>
		</div>


	</div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUpdate, onBeforeMount } from 'vue';
import { to_id } from '../utils.js'

const props = defineProps({ 'index': Number, 'advanced': Boolean, 'uuid': Number })
const emits = defineEmits('delete_value')

let id_default = ref(true)
let title = ref(`Value ${props.uuid}`)
let value = ref(to_id(title.value))
let model = defineModel({})
let uuid = ref(props.uuid)
let error = computed(() => {
	return (value.value === "" || title.value === "")
})
let data = ref({
	'title': title,
	'value': value,
	'error': error,
	'uuid': uuid
})

let computed_id_string = computed(() => {
	return to_id(title.value)
})

function setModel() {
	model.value[props.index] = data.value
}
//  Loads parent's data, copying it to internal data
function updateModel() {
	data.title = model.value[props.index].title
	data.value = model.value[props.index].title
	data.error = model.value[props.index].error
}
onBeforeMount(() => { setModel() })

onBeforeUpdate(() => { updateModel() })

function update_title() {
	title.value = title.value.trim()
	update_from_title()
}
function update_from_title(event) {
	if (id_default.value == true) {
		value.value = computed_id_string.value
	}
}

function update_value(event) {
	value.value = to_id(value.value)
	if (value.value == "") {
		id_default.value = true
		update_from_title()
	} else {
		id_default.value = false
	}
}

</script>