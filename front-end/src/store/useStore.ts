import {defineStore} from "pinia";
import {AddressBook} from "../assets/types";

type State = {
    accessToken: string
    addressBook: AddressBook
    senderUnionId: null | string
    receiverDeptUnionIdArray: string[]
    userInputText: string

    calendar: {
        title: string
        content: string
    }
}


export const useStore = defineStore("store", {
    state: (): State => {
        return {
            accessToken: "",
            addressBook: [],
            senderUnionId: null,
            receiverDeptUnionIdArray: [],
            userInputText: "",

            calendar: {
                title: "",
                content: "",
            },
        };
    },
    getters: {},
    actions: {},
});
