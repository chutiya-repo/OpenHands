import { WSAICodeObservation } from "./types/core/observations";
import { WSAICodeAction } from "./types/core/actions";

export type Message = {
  sender: "user" | "assistant";
  content: string;
  timestamp: string;
  imageUrls?: string[];
  type?: "thought" | "error" | "action";
  success?: boolean;
  pending?: boolean;
  translationID?: string;
  eventID?: number;
  observation?: { payload: WSAICodeObservation };
  action?: { payload: WSAICodeAction };
};
