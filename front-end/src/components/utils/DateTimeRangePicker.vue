<script setup lang="ts">
import {computed} from "vue";
import {zhCN, dateZhCN} from "naive-ui";

const props = withDefaults(defineProps<{
  value: [string, string]
  label: string
  required?: boolean
  validator?: () => boolean
}>(), {required: true});

const emits = defineEmits(["update:value"]);

const valueLocal = computed<[string, string]>({
  get: () => props.value,
  set: (newValue) => emits("update:value", newValue),
});
</script>

<template>
  <n-form-item :label="label" :required="required" label-placement="left" :show-feedback="false"
               :validation-status="(validator?validator():true)?`success`:`error`">
    <n-config-provider :date-locale="dateZhCN" :locale="zhCN">
      <n-date-picker type="datetimerange" :default-formatted-value="valueLocal" :clearable="true"/>
    </n-config-provider>
  </n-form-item>
</template>

<style scoped>

</style>
