import {createRouter, createWebHashHistory, RouteRecordRaw} from "vue-router";

import CalendarCreateForm from "../pages/CalendarCreateForm.vue";
import ResultDisplay from "../pages/ResultDisplay.vue";


const routes: RouteRecordRaw[] = [
    {
        path: "/create-calendar/",
        name: "create-calendar",
        component: CalendarCreateForm,
        alias: "/",
    },
    {
        path: "/query-calendar/:eventId/",
        name: "query-calendar",
        component: ResultDisplay,
    },
];

export default createRouter({
    history: createWebHashHistory(),
    routes,
});
