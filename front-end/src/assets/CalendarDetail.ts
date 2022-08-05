export default interface CalendarDetail {
    id: string;
    summary: string;
    description: string;
    status: string;
    start: Start;
    end: End;
    isAllDay: boolean;
    recurrence: Recurrence;
    attendees: Attendee[];
    organizer: Organizer;
    location: Location;
    seriesMasterId: string;
    createTime: string;
    updateTime: string;
    reminders: Reminder[];
    onlineMeetingInfo: OnlineMeetingInfo;
}

export interface Start {
    date: string;
    dateTime: string;
    timeZone: string;
}

export interface End {
    date: string;
    dateTime: string;
    timeZone: string;
}

export interface Recurrence {
    pattern: Pattern;
    range: Range;
}

export interface Pattern {
    type: string;
    dayOfMonth: number;
    daysOfWeek: string;
    index: string;
    interval: number;
}

export interface Range {
    type: string;
    endDate: string;
    numberOfOccurrences: number;
}

export interface Organizer {
    id: string;
    displayName: string;
    responseStatus: string;
    self: boolean;
}

export interface Location {
    displayName: string;
}

export interface OnlineMeetingInfo {
    type: string;
    conferenceId: string;
    url: string;
}

export interface Attendee {
    id: string;
    displayName: string;
    responseStatus: string;
    self: boolean;
    isOptional: boolean;
}

export interface Reminder {
    method: string;
    minutes: string;
}
