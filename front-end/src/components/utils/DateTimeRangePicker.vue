<script setup lang="ts">
import {zhCN, dateZhCN} from "naive-ui";
import {useStore} from "../../store/useStore";

const props = withDefaults(defineProps<{
  label: string
  required?: boolean
  validator?: () => boolean
}>(), {required: true});

const store = useStore();
</script>

<template>
  <n-form-item :label="label" :required="required" label-placement="left" :show-feedback="false"
               :validation-status="(validator?validator():true)?`success`:`error`">
    <n-config-provider :date-locale="dateZhCN" :locale="zhCN">
      <n-date-picker type="datetimerange" v-model:formatted-value="store.calendar.timeRange" :actions="['confirm']"/>
    </n-config-provider>
  </n-form-item>
</template>

<style scoped>

</style>
