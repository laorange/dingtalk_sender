import {defineStore} from "pinia";
import {AddressBook, UserDetail} from "../assets/types";
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

    isLoading: boolean
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

            isLoading: false,
        };
    },
    getters: {
        senderUnionId(): string {
            return this.senderDeptUnionId?.split(",")[1] ?? "";
        },
    },
    actions: {
        getUserDetailByUnionId(targetUnionId: string): UserDetail | null {
            for (const deptBookElement of this.addressBook) {
                for (const user of deptBookElement.users) {
                    if (user.unionid === targetUnionId) return user;
                }
            }
            return null;
        },
    },
});
