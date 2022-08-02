<script setup lang="ts">
import {computed} from "vue";
import {useStore} from "../store/useStore";
import {CascaderOption} from "naive-ui";
import {DeptAddressBook, UserDetail} from "../assets/types";


const store = useStore();

const options = computed<CascaderOption[]>(() => {
  return store.addressBook.map((dept: DeptAddressBook) => {
    return {
      label: dept.dept_name,
      value: dept.dept_id,
      children: dept.users.map(user => {
        return {
          label: user.name,
          value: user.unionid,
        };
      }),
    };
  });
});

function parseSelectorToText() {
  let userDetails: UserDetail[] = [];
  for (const deptAddressBook of store.addressBook) {
    for (const user of deptAddressBook.users) {
      if (store.selectedUserUnionIdArray.indexOf(user.unionid) > -1) {
        userDetails.push(user);
      }
    }
  }
  store.userInputText = userDetails.map(ud => ud.name).join("\n");
}
</script>

<template>
  <div style="margin-bottom: 10px;">
    <n-cascader
        v-model:value="store.selectedUserUnionIdArray"
        :options="options"
        placeholder="请选择接受通知的用户"
        check-strategy="child"
        :max-tag-count="500"
        expand-trigger="hover"
        placement="bottom-start"
        :multiple="true"
        :clearable="true"
        :cascade="true"
        :show-path="true"
        :filterable="true"
        :clear-filter-after-select="true"
    />
  </div>

  <n-space align="center" justify="center">
    <n-button @click="parseSelectorToText" type="info">文字 ← 选项</n-button>
  </n-space>

  <n-divider/>
</template>

<style scoped>

</style>
