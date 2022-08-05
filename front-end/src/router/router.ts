import {createRouter, createWebHashHistory, RouteRecordRaw} from "vue-router";

import HomePage from "../pages/HomePage.vue";
import CalendarCreateForm from "../pages/CalendarCreateForm.vue";
import ResultDisplay from "../pages/ResultDisplay.vue";
import BulletinCreateForm from "../pages/BulletinCreateForm.vue";


const routes: RouteRecordRaw[] = [
    {
        path: "/",
        name: "home",
        component: HomePage,
    },
    {
        path: "/create-bulletin/",
        name: "create-bulletin",
        component: BulletinCreateForm,
    },
    {
        path: "/create-calendar/",
        name: "create-calendar",
        component: CalendarCreateForm,
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
