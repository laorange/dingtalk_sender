<script setup lang="ts">
import {useStore} from "../store/useStore";
import {UserDetail} from "../assets/types";
import UserSelector from "./UserSelector.vue";
import {useDialog, useMessage} from "naive-ui";

const store = useStore();
const dialog = useDialog();
const message = useMessage();

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

const handlers = {
  refreshAddressBook() {
    try {
      let ws = new WebSocket("ws://localhost:8095/refresh-address-book/");
      ws.onopen = () => {
        store.isLoading = true;
        ws.send("please refresh address book, thanks!");
      };
      ws.onmessage = (_) => {
        message.success("刷新成功");
        ws.close();
      };
      ws.onclose = () => store.isLoading = false;
    } catch (e) {
      message.error("请求数据失败！请检查后端服务是否已被关闭");
      store.isLoading = false;
    }
  },
  toRefreshAddressBook() {
    dialog.warning({
      title: `刷新成员信息可能会需要较多时间，请仅在部门成员有变动时使用该功能，确认继续？`,
      negativeText: "取消",
      positiveText: "确认",
      onPositiveClick: handlers.refreshAddressBook,
    });
  },
};
</script>

<template>
  <UserSelector v-model:value="store.receiverDeptUnionIdArray" label="接收者:" :required="true" placeholder="请选择接受通知的用户"/>

  <n-space align="center" justify="space-around">
    <n-button @click="handlers.toRefreshAddressBook" type="error">刷新部门名单</n-button>
    <n-button @click="parseSelectorToText" type="info">文字 ← 选项</n-button>
  </n-space>

</template>

<style scoped>

</style>

