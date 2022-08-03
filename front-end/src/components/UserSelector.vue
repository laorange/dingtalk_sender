<script setup lang="ts">
import {computed} from "vue";
import {useStore} from "../store/useStore";
import {CascaderOption} from "naive-ui";
import {DeptAddressBook, UserDetail} from "../assets/types";

const props = withDefaults(defineProps<{
  users: string | string[],
  placeholder: string,
  label?: string,
  marginBottom?: number,
  required?: boolean,
  multiple?: boolean,
  clearable?: boolean,
  filterable?: boolean,
  clearFilterAfterSelect?: boolean
}>(), {marginBottom: 15, multiple: true, clearable: true, filterable: true, clearFilterAfterSelect: true, required: true});

const emits = defineEmits(["update:users"]);

const usersLocal = computed<string | string[]>({
  get: () => props.users,
  set: (newValue) => emits("update:users", newValue),
});

const store = useStore();

const options = computed<CascaderOption[]>(() => {
  return store.addressBook.map((dept: DeptAddressBook) => {
    return {
      label: dept.dept_name,
      value: dept.dept_id,
      children: dept.users.map((user: UserDetail) => {
        return {
          label: user.name,
          value: [dept.dept_id, user.unionid].join(","),
        };
      }),
    };
  });
});
</script>

<template>
  <div :style="{marginBottom: `${marginBottom}px`}">
    <n-form-item :label="label??''" label-placement="left" :required="required" :show-feedback="false" :show-label="!!label"
                 :validation-status="usersLocal.length?`success`:`error`">
      <n-cascader
          v-model:value="usersLocal"
          :options="options"
          :placeholder="placeholder"
          check-strategy="child"
          :max-tag-count="500"
          expand-trigger="hover"
          placement="bottom-start"
          :multiple="multiple"
          :clearable="clearable"
          :cascade="true"
          :show-path="true"
          :filterable="filterable"
          :clear-filter-after-select="clearFilterAfterSelect"
      />
    </n-form-item>
  </div>
</template>

<style scoped>

</style>
