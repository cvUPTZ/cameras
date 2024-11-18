
// # types.ts
export interface Alert {
    id: string;
    timestamp: string;
    camera_id: number;
    type: string;
    message: string;
    image_url?: string;
}

export interface Camera {
    id: number;
    name: string;
    status: string;
    stream_url?: string;
}

export interface DvrConfig {
    ip: string;
    username: string;
    password: string;
}

export interface Stat {
    id: string;
    timestamp: string;
    type: string;
    value: number;
}
