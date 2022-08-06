<script setup lang="ts">
import {useStore} from "../store/useStore";
import {computed} from "vue";
import {useDialog, useMessage} from "naive-ui";
import {useRouter} from "vue-router";

const store = useStore();
const router = useRouter();
const dialog = useDialog();
const message = useMessage();

const whetherCanSend = computed<boolean>(() => {
  return !!store.senderDeptUnionId
      && !!store.receiverDeptUnionIdArray.length
      && !!store.bulletin.title
      && !!store.bulletin.content;
});

const handlers = {
  async submit() {
    try {
      let url = (import.meta.env.VITE_BACKEND_URL ?? "") + "/send-bulletin/";
      let senderDetail = store.getUserDetailByUnionId(store.senderUnionId);
      let result = await (await fetch(url, {
        method: "POST",
        body: JSON.stringify({
          create_request: {
            operation_userid: senderDetail?.userid,
            private_level: 20, // whether_private ? 20 : 0
            ding: true,
            blackboard_receiver: {
              userid_list: store.receiverDeptUnionIdArray.map(du => store.getUserDetailByUnionId(du.split(",")[1])?.userid),
            },
            title: store.bulletin.title,
            content: store.bulletin.content,
            push_top: false,
            author: senderDetail?.name,
          },
        }),
      })).json();

      message.success("发送成功，请在钉钉内查看");
      console.log(result);
      await router.push({name: "home"});
    } catch (e) {
      message.error(`发送失败: ${e}`);
    }
  },
  toSubmit() {
    dialog.info({
      title: () => `确认发布？`,
      negativeText: "取消",
      positiveText: "确认",
      onPositiveClick: handlers.submit,
    });
  },
};
</script>

<template>
  <n-divider/>

  <n-space justify="center">
    <n-button @click="handlers.toSubmit()" :disabled="!whetherCanSend" :type="whetherCanSend?`success`:`warning`" size="large">发送</n-button>
    <n-button @click="router.push({name:'home'})" type="info" size="large">返回主页</n-button>
  </n-space>
</template>

<style scoped>

</style>
