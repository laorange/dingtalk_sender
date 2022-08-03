<script setup lang="ts">
import {useStore} from "../store/useStore";

const store = useStore();

function parseTextToSelector() {
  let userNames = store.userInputText.split(/\s/).filter(_ => !!_);
  store.selectedUserUnionIdArray = [];
  for (const deptAddressBook of store.addressBook) {
    for (const user of deptAddressBook.users) {
      if (userNames.indexOf(user.name) > -1) {
        store.selectedUserUnionIdArray.push([deptAddressBook.dept_id, user.unionid].join(","));
      }
    }
  }
}
</script>

<template>
  <div style="margin-bottom: 10px;">
    <n-input
        v-model:value="store.userInputText"
        type="textarea"
        :autosize="true"
        placeholder="请输入信息接受者，每个姓名之间以空格/回车来间隔"
        :clearable="true"
    />
  </div>

  <n-space align="center" justify="center">
    <n-button @click="parseTextToSelector" type="success">文字 → 选项</n-button>
  </n-space>

  <n-divider/>
</template>

<style scoped>

</style>
