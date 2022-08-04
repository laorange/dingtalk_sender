<script setup lang="ts">
import {useStore} from "../../store/useStore";
import {onMounted} from "vue";
import {AddressBook} from "../../assets/types";

const store = useStore();

onMounted(async () => {
  store.accessToken = (await (await fetch((import.meta.env.VITE_BACKEND_URL ?? "") + "/access-token/")).json())["accessToken"] as string;
  store.addressBook = await (await fetch((import.meta.env.VITE_BACKEND_URL ?? "") + "/address-book/")).json() as AddressBook;
});
</script>

<template>

</template>

<style scoped>

</style>
