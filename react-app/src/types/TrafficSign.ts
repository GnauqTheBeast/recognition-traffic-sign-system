export interface TrafficSign {
    id: number;
    name: string;
    description: string;
    imageUrl: string;
    type: TrafficSignType;
}

export type TrafficSignType = 'WARNING' | 'PROHIBITION' | 'INFORMATION';

export interface CreateTrafficSignDTO {
    name: string;
    description: string;
    imageUrl: string;
    type: TrafficSignType;
} 
    