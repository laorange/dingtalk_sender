<script setup lang="ts">
import {useRoute, useRouter} from "vue-router";
import {computed, ref, watch} from "vue";
import {useStore} from "../store/useStore";
import CalendarDetail from "../assets/CalendarDetail";

const store = useStore();
const route = useRoute();
const router = useRouter();
const calendar_id = computed<string>(() => `${route.params.eventId ?? ""}`);
const senderUnionId = computed<string>(() => `${route.params.senderUnionId ?? ""}`);

const result = ref<CalendarDetail | null>(null);

const handlers = {
  async getCalendarDetail() {
    if (!calendar_id.value || !store.accessToken || !senderUnionId.value) return null;

    let url = `https://api.dingtalk.com/v1.0/calendar/users/${senderUnionId.value}/calendars/primary/events/${calendar_id.value}?maxAttendees=500`;
    return await (await fetch(url, {
      method: "GET",
      headers: {"x-acs-dingtalk-access-token": store.accessToken},
    })).json() as CalendarDetail;
  },
  async refreshResult()  {
    result.value = await handlers.getCalendarDetail();
  },
};

watch(() => [store.accessToken, calendar_id.value], handlers.refreshResult, {deep: true, immediate: true});
</script>

<template>
  <div class="calendar-detail-display-area" v-if="result">
    <h2 style="text-align: center">{{ result?.summary }}</h2>
    <n-ellipsis expand-trigger="click" :line-clamp="2" :tooltip="false" >{{ result?.description }}</n-ellipsis>
    <n-divider><n-button @click="handlers.refreshResult" type="info">刷新结果</n-button></n-divider>

    <n-grid cols="4">
      <n-gi>
        <n-space :vertical="true" justify="center" align="center">
          <div class="status-title">未读</div>
          <div class="person-status" v-for="attendee in result?.attendees.filter(a=>a.responseStatus===`needsAction`) ?? []" :key="attendee?.id">
            {{ store.getUserDetailByUnionId(attendee?.id ?? "")?.name ?? attendee?.displayName }}
          </div>
        </n-space>
      </n-gi>
      <n-gi>
        <n-space :vertical="true" justify="center" align="center">
          <div class="status-title">已拒绝</div>
          <div class="person-status" v-for="attendee in result?.attendees.filter(a=>a.responseStatus===`declined`) ?? []" :key="attendee?.id">
            {{ store.getUserDetailByUnionId(attendee?.id ?? "")?.name ?? attendee?.displayName }}
          </div>
        </n-space>
      </n-gi>
      <n-gi>
        <n-space :vertical="true" justify="center" align="center">
          <div class="status-title">暂定</div>
          <div class="person-status" v-for="attendee in result?.attendees.filter(a=>a.responseStatus===`tentative`) ?? []" :key="attendee?.id">
            {{ store.getUserDetailByUnionId(attendee?.id ?? "")?.name ?? attendee?.displayName }}
          </div>
        </n-space>
      </n-gi>
      <n-gi>
        <n-space :vertical="true" justify="center" align="center">
          <div class="status-title">已接受</div>
          <div class="person-status" v-for="attendee in result?.attendees.filter(a=>a.responseStatus===`accepted`) ?? []" :key="attendee?.id">
            {{ store.getUserDetailByUnionId(attendee?.id ?? "")?.name ?? attendee?.displayName }}
          </div>
        </n-space>
      </n-gi>
    </n-grid>
  </div>
</template>

<style scoped>
.calendar-detail-display-area {
  margin: 0 10vw;
}
</style>
