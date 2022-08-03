import {defineStore} from "pinia";
import {AddressBook} from "../assets/types";

type State = {
    accessToken: string
    addressBook: AddressBook
    senderUnionId: string
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
            senderUnionId: "",
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
