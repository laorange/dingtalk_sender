from typing import TypedDict, List, Dict, Literal

UserId = str
UserName = str
UnionId = str
DepartmentId = int
DepartmentName = str
Method = Literal["GET", "POST"]

UserNameIdDict = Dict[UserName, UserId]


class UserInfoDict(TypedDict):
    name: UserName
    userid: UserId


class DepartmentDict(TypedDict):
    ext: str  # --------------------------- "ext": "{\"faceCount\":\"int\"}",
    auto_add_user: bool  # ---------------- "auto_add_user": true,
    parent_id: int  # --------------------- "parent_id": 1,
    name: DepartmentName  # --------------- "name": "xx部门",
    dept_id: DepartmentId  # -------------- "dept_id": int,
    create_dept_group: bool  # ------------ "create_dept_group": true


class Settings(TypedDict):
    AGENT_ID: str
    APP_KEY: str
    APP_SECRET: str
    PRESET_DEPARTMENTS: List[DepartmentId]
    PRESET_MEMBERS: UserNameIdDict


class AdministratorInfo(TypedDict):
    sys_level: Literal[1, 2]
    userid: UserId
