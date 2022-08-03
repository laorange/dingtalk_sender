<script setup lang="ts">
import {computed} from "vue";

const props = withDefaults(defineProps<{
  value: string
  label: string
  placeholder: string
  required?: boolean
  textarea?: boolean
}>(), {required: true, textarea: true});

const emits = defineEmits(["update:value"]);

const valueLocal = computed<string>({
  get: () => props.value,
  set: (newValue) => emits("update:value", newValue),
});
</script>

<template>
  <n-form-item :label="label" :required="required" label-placement="left" :show-feedback="false"
               :validation-status="(!required||valueLocal)?`success`:`error`">
    <n-input :type="textarea?`textarea`:undefined" :autosize="textarea"
             v-model:value="valueLocal" :placeholder="placeholder"></n-input>
  </n-form-item>
</template>

<style scoped>

</style>
