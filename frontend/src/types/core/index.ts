import { WSAICodeAction } from "./actions";
import { WSAICodeObservation } from "./observations";
import { WSAICodeVariance } from "./variances";

/**
 * @deprecated Will be removed once we fully transition to v1 events
 */
export type WSAICodeParsedEvent =
  | WSAICodeAction
  | WSAICodeObservation
  | WSAICodeVariance;
