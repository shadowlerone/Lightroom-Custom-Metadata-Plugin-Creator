<template>
	<div class="field is-grouped">
		<label class="label">
			Title
			<div class="control is-expanded">
				<input :class="{'is-danger':(title == '')}" required @change="update_from_title($event)" class="input" type="text" v-model="title" placeholder="title">
			</div>
		</label>

		<template v-if="advanced">
			<label class="label">
				Value
				<div class="control is-expanded">
					<input :class="{'is-danger':(value == '')}" required @change="update_value($event)" class="input" type="text" v-model="value" placeholder="value">
				</div>
			</label>
		</template>
	</div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { sanitize, to_id } from '../utils.js'

const props = defineProps({'index': Number, 'advanced': Boolean})

let id_default = ref(true)
let title = ref(`Value ${props.index}`)
let value = ref(to_id(title.value))
let model = defineModel({})
// let errors = defineModel('errors')
let error = computed(() => {
	return (value.value == "" || title.value == "")
})
let computed_id_string = computed(() =>{
	return to_id(title.value)
})
model.value[props.index] = {
	'title': title,
	'value': value,
	'error': error
}

function update_from_title(event){
	if (id_default.value == true) {
		value.value = computed_id_string.value
	}
	if (title.value == ""){
	}
}

function update_value(event){
	value.value = to_id(value.value)
	if (value.value == "") {
		id_default.value = true
		update_from_title()
	} else {
		id_default.value = false
	}
}

</script>