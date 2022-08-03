<script setup lang="ts">
import {useStore} from "../../store/useStore";

const store = useStore();

function parseTextToSelector() {
  let userNames = store.userInputText.split(/\s/).filter(_ => !!_);
  store.receiverDeptUnionIdArray = [];
  for (const deptAddressBook of store.addressBook) {
    for (const user of deptAddressBook.users) {
      if (userNames.indexOf(user.name) > -1) {
        store.receiverDeptUnionIdArray.push([deptAddressBook.dept_id, user.unionid].join(","));
      }
    }
  }
}
</script>

<template>
  <div style="margin-bottom: 15px;">
    <n-form-item label="接收者:" label-placement="left" :show-feedback="false">
      <n-input
          v-model:value="store.userInputText"
          type="textarea"
          :autosize="true"
          placeholder="输入接收者，多个姓名需间隔空格/回车"
          :clearable="true"
      />
    </n-form-item>
  </div>

  <n-space align="center" justify="center">
    <n-button @click="parseTextToSelector" type="success">文字 → 选项</n-button>
  </n-space>

</template>

<style scoped>

</style>
