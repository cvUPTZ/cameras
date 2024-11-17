export interface Alert {
  id: number;
  time: string;
  type: string;
  camera: string;
  severity: 'high' | 'medium' | 'low';
}

export interface Camera {
  id: number;
  name: string;
  status: 'active' | 'inactive';
  streamUrl?: string;
}

export interface Stat {
  label: string;
  value: string;
  icon: React.ComponentType;
}

export interface DvrConfig {
  ip: string;
  username: string;
  password: string;
}
