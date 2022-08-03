<script setup lang="ts">
import {useStore} from "../store/useStore";
import {UserDetail} from "../assets/types";
import UserSelector from "./UserSelector.vue";

const store = useStore();

function parseSelectorToText() {
  let userDetails: UserDetail[] = [];
  for (const deptAddressBook of store.addressBook) {
    for (const user of deptAddressBook.users) {
      if (store.receiverDeptUnionIdArray.map(du => du.split(",")[1]).indexOf(user.unionid) > -1) {
        userDetails.push(user);
      }
    }
  }
  store.userInputText = Array.from(new Set(userDetails.map(ud => ud.name))).join("\n");
}
</script>

<template>
  <UserSelector v-model:value="store.receiverDeptUnionIdArray" label="接收者:" :required="true" placeholder="请选择接受通知的用户"/>

  <n-space align="center" justify="center">
    <n-button @click="parseSelectorToText" type="info">文字 ← 选项</n-button>
  </n-space>

</template>

<style scoped>

</style>

