<script setup>
import MetaField from "./components/MetaField.vue";
// import DataDebug from "./components/dataDebug.vue";
import { ref, reactive, computed } from 'vue';
import { sanitize, to_id } from './utils.js'
import DataDebug from "./components/dataDebug.vue";

let advanced = ref(true)

let plugin_name = ref('Test Plugin')

let plugin_id = computed(() => {
	return to_id(plugin_name.value)
})

let full_plugin_id_string = computed(() => {
	return `shadowlerone.${plugin_id.value}.Metadata`
})

let current_uuid = ref(0)
let metadata_fields = ref([current_uuid.value])
function add_field() {
	metadata_fields.value.push(current_uuid.value++)
}

// let metadata_field_count = ref(1)
let data = ref({
	'name': plugin_name,
	'mfields': metadata_fields
})

let error = computed(() => {
	return metadata_fields.value.some(e => e.error)

})

function delete_field(index) {
	// var temp = metadata_fields.value
	// metadata_fields.value.splice(index, 1)
	// for (i = 0; i<metadata_fields.value.length; i++){
	// 	temp[i] = metadata_fields[i]
	// }
	// metadata_fields.value[index] = undefined
	var j=0
	for (var i = 0; i < metadata_fields.value.length && j < metadata_fields.value.length; i++){
		if (i==index){
			j++
		}
		metadata_fields.value[i] = metadata_fields.value[i+j];
	}
	if (j > 0){
		metadata_fields.value.pop()
	}
}


async function downloadFile() {
	let headers = {
		// mode: 'cors',
		cache: 'no-cache',
		"Content-Type": "application/json",
	}
	try {
		console.debug("Sending request")
		let response = await fetch("http://localhost:5000/generate", {
			method: "POST",
			body: JSON.stringify(data.value),
			headers: headers
		})
		console.debug("attempting download")
		await forceDownload(await response.blob())
	} catch (e) {
		console.error("error occurred")
		throw new Error(e)
	}
}

async function forceDownload(blob) {
	window.console.log(blob)
	const a = document.createElement('a')
	a.style.display = 'none'
	document.body.appendChild(a)
	a.href = URL.createObjectURL(blob)
	a.setAttribute('download', `${plugin_name.value}.lrplugin.zip`)
	a.click()
	window.URL.revokeObjectURL(a.href)
	document.body.removeChild(a)
}
</script>

<template>

	<h1 class="title is-1">Lightroom Metadata Plugin Generator</h1>

	<form class="panel" :class="{ 'is-danger': error }">
		<h2 class="panel-heading"> {{ plugin_name }}
			<template v-if="advanced">(id: {{ full_plugin_id_string }})</template>
		</h2>
		<!-- <div class="panel-block">
			<div class="control">
				<div class="field">
					<label class="checkbox">
						<input class="checkbox" type="checkbox" v-model="advanced" />
						Advance Mode
					</label>
				</div>
			</div>
		</div> -->
		<div class="panel-block">
			<div class="control">
				<div class="field">
					<label class="label">
						Plugin Name
					</label>
					<div class="control">
						<input class="input" type="text" placeholder="Plugin Name" v-model="plugin_name">
					</div>
				</div>
			</div>
		</div>

		<div class="panel-block">
			<div class="control">
				<div id="metadata-fields" class="field">
					<!-- <h2 class="title is-2">Fields</h2> -->
					<label class="label">Fields</label>
					<TransitionGroup name="list">
						<MetaField 
						v-for="(v, index) in metadata_fields"
						:key="v.uuid"
						:pluginId="full_plugin_id_string" 
						:index="index" 
						:advanced="advanced"
						:uuid="current_uuid"
						v-model="metadata_fields" 
						@delete_field="delete_field"
					/>
					</TransitionGroup>
					

				</div>
				<div class="field">
					<button class="button" @click.prevent="add_field()">Add Metadata field</button>
				</div>
			</div>
		</div>



		<div class="panel-block">
			<div class="control">
				<div class="field is-grouped">
					<div class="control">
						<button @click.prevent="downloadFile()" class="button is-link">Generate</button>
					</div>
					<div class="control">
						<button class="button is-link is-light">Cancel</button>
					</div>
				</div>
			</div>
		</div>
		<div class="panel-block" v-if="advanced">
			<div class="control">
				<pre><code>{{ JSON.stringify(data, null, 4) }}</code></pre>
			</div>

		</div>

	</form>
	<!-- <template v-if="advanced == true">
		{{ data }}
	</template> -->

</template>

<style scoped>
.list-move, /* apply transition to moving elements */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* ensure leaving items are taken out of layout flow so that moving
   animations can be calculated correctly. */
.list-leave-active {
  position: absolute;
}
</style>
