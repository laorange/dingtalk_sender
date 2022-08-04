import {createRouter, createWebHashHistory, RouteRecordRaw} from "vue-router";

import CalendarCreateForm from "../pages/CalendarCreateForm.vue";
import ResultDisplay from "../pages/ResultDisplay.vue";


const routes: RouteRecordRaw[] = [
    {
        path: "/",
        name: "index",
        component: CalendarCreateForm,
    },
    {
        path: "/result/",
        name: "result",
        component: ResultDisplay,
    },
];

export default createRouter({
    history: createWebHashHistory(),
    routes,
});
