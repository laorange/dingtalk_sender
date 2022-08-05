<script setup lang="ts">
import {useStore} from "../store/useStore";
import dayjs from "dayjs";
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
      && !!store.calendar.title;
});

const handlers = {
  async submit() {
    try {
      let url = `https://api.dingtalk.com/v1.0/calendar/users/${store.senderUnionId}/calendars/primary/events`
      let result = await (await fetch(url, {
        method: "POST",
        headers: {"x-acs-dingtalk-access-token": store.accessToken},
        body: JSON.stringify({
          summary: store.calendar.title,
          description: store.calendar.content,
          isAllDay: false,
          start: {
            dateTime: dayjs(store.calendar.timeRange[0]).format("YYYY-MM-DDTHH:mm:ss+08:00"),
            timeZone: "Asia/Shanghai",
          },
          end: {
            dateTime: dayjs(store.calendar.timeRange[1]).format("YYYY-MM-DDTHH:mm:ss+08:00"),
            timeZone: "Asia/Shanghai",
          },
          reminders: [],
          attendees: store.receiverDeptUnionIdArray.map(du => {
            return {id: du.split(",")[1], isOptional: false};
          }),
        }),
      })).json();
      debugger
      if (result.id) {
        message.success("发送成功");
        console.log(result.id);
        await router.push({name: "query-calendar", params: {eventId: result.id}});
      } else {
        message.error(`发送失败: 未获取到有效的返回参数`);
      }
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
  </n-space>
</template>

<style scoped>

</style>
