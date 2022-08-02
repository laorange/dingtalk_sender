export type UserId = string
export type UserUnionId = string
export type DepartmentId = number

export interface UserDetail {
    active: boolean;
    admin: boolean;
    avatar: string;
    boss: boolean;
    dept_id_list: DepartmentId[];
    dept_order_list: DeptOrder[];
    exclusive_account: boolean;
    hide_mobile: boolean;
    leader_in_dept: LeaderInDept[];
    name: string;
    real_authed: boolean;
    senior: boolean;
    title: string;
    unionid: UserUnionId;
    userid: UserId;
}

export interface DeptOrder {
    dept_id: DepartmentId;
    order: number;
}

export interface LeaderInDept {
    dept_id: DepartmentId;
    leader: boolean;
}

export interface DeptAddressBook {
    dept_id: DepartmentId;
    dept_name: string;
    users: UserDetail[];
}

export type AddressBook = DeptAddressBook[]
