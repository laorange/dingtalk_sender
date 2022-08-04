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

function refreshAddressBook() {
  let ws = new WebSocket("ws://localhost:8095/refresh-address-book/");
  ws.onopen = () => ws.send("please refresh address book, thanks!");
  ws.onmessage = (event) => {
    let data = event.data;
    console.log(data);
    ws.close();
  };
  console.log("正在加载！");
}
</script>

<template>
  <UserSelector v-model:value="store.receiverDeptUnionIdArray" label="接收者:" :required="true" placeholder="请选择接受通知的用户"/>

  <n-space align="center" justify="space-around">
    <n-button @click="refreshAddressBook()" type="error">刷新部门名单</n-button>
    <n-button @click="parseSelectorToText" type="info">文字 ← 选项</n-button>
  </n-space>

</template>

<style scoped>

</style>

