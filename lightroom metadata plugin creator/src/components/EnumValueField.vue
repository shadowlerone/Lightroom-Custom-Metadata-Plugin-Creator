<template>
	<div class="field is-grouped">
		<label class="label">
			Title
			<div class="control is-expanded">
				<input class="input" type="text" v-model="title" placeholder="title">
			</div>
		</label>

		<template v-if="advanced">
			<label class="label">
				Value
				<div class="control is-expanded">
					<input class="input" type="text" v-model="value" placeholder="value">
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
let title = ref(`Value ${props.index+1}`)
let value = ref(to_id(title.value))
let model = defineModel({})

model.value[props.index] = {
	'title': title,
	'value': value
}

</script>