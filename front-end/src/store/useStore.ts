import {defineStore} from "pinia";
import {AddressBook} from "../assets/types";
import dayjs from "dayjs";

type State = {
    accessToken: string
    addressBook: AddressBook
    senderDeptUnionId: null | string
    receiverDeptUnionIdArray: string[]
    userInputText: string

    calendar: {
        title: string
        content: string
        timeRange: [string, string]
    }
}


export const useStore = defineStore("store", {
    state: (): State => {
        return {
            accessToken: "",
            addressBook: [],
            senderDeptUnionId: null,
            receiverDeptUnionIdArray: [],
            userInputText: "",

            calendar: {
                title: "",
                content: "",
                timeRange: [dayjs().format("YYYY-MM-DD HH:mm:ss"), dayjs().add(1, "day").format("YYYY-MM-DD HH:mm:ss")],
            },
        };
    },
    getters: {},
    actions: {},
});
