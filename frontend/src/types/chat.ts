export interface Message {
  id: string;
  content: string;
  timestamp: Date;
  isUser: boolean;
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

export interface ApiRequest {
  message: string;
}

export interface ApiResponse {
  response: string;
} 