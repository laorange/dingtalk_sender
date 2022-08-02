import {defineStore} from "pinia";
import {AddressBook} from "../assets/types";

type State = {
    accessToken: string
    addressBook: AddressBook
    selectedUserUnionIdArray: string[]
    userInputText: string
}


export const useStore = defineStore("store", {
    state: (): State => {
        return {
            accessToken: "",
            addressBook: [],
            selectedUserUnionIdArray: [],
            userInputText: "",
        };
    },
    getters: {},
    actions: {},
});
