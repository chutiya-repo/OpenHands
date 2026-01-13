import { WSAICodeParsedEvent } from ".";
import {
  UserMessageAction,
  AssistantMessageAction,
  WSAICodeAction,
  SystemMessageAction,
  CommandAction,
  FinishAction,
  TaskTrackingAction,
} from "./actions";
import {
  AgentStateChangeObservation,
  CommandObservation,
  ErrorObservation,
  MCPObservation,
  WSAICodeObservation,
  TaskTrackingObservation,
} from "./observations";
import { StatusUpdate } from "./variances";

export const isWSAICodeEvent = (
  event: unknown,
): event is WSAICodeParsedEvent =>
  typeof event === "object" &&
  event !== null &&
  "id" in event &&
  "source" in event &&
  "message" in event &&
  "timestamp" in event;

export const isWSAICodeAction = (
  event: WSAICodeParsedEvent,
): event is WSAICodeAction => "action" in event;

export const isWSAICodeObservation = (
  event: WSAICodeParsedEvent,
): event is WSAICodeObservation => "observation" in event;

export const isUserMessage = (
  event: WSAICodeParsedEvent,
): event is UserMessageAction =>
  isWSAICodeAction(event) &&
  event.source === "user" &&
  event.action === "message";

export const isAssistantMessage = (
  event: WSAICodeParsedEvent,
): event is AssistantMessageAction =>
  isWSAICodeAction(event) &&
  event.source === "agent" &&
  (event.action === "message" || event.action === "finish");

export const isErrorObservation = (
  event: WSAICodeParsedEvent,
): event is ErrorObservation =>
  isWSAICodeObservation(event) && event.observation === "error";

export const isCommandAction = (
  event: WSAICodeParsedEvent,
): event is CommandAction => isWSAICodeAction(event) && event.action === "run";

export const isAgentStateChangeObservation = (
  event: WSAICodeParsedEvent,
): event is AgentStateChangeObservation =>
  isWSAICodeObservation(event) && event.observation === "agent_state_changed";

export const isCommandObservation = (
  event: WSAICodeParsedEvent,
): event is CommandObservation =>
  isWSAICodeObservation(event) && event.observation === "run";

export const isFinishAction = (
  event: WSAICodeParsedEvent,
): event is FinishAction =>
  isWSAICodeAction(event) && event.action === "finish";

export const isSystemMessage = (
  event: WSAICodeParsedEvent,
): event is SystemMessageAction =>
  isWSAICodeAction(event) && event.action === "system";

export const isRejectObservation = (
  event: WSAICodeParsedEvent,
): event is WSAICodeObservation =>
  isWSAICodeObservation(event) && event.observation === "user_rejected";

export const isMcpObservation = (
  event: WSAICodeParsedEvent,
): event is MCPObservation =>
  isWSAICodeObservation(event) && event.observation === "mcp";

export const isTaskTrackingAction = (
  event: WSAICodeParsedEvent,
): event is TaskTrackingAction =>
  isWSAICodeAction(event) && event.action === "task_tracking";

export const isTaskTrackingObservation = (
  event: WSAICodeParsedEvent,
): event is TaskTrackingObservation =>
  isWSAICodeObservation(event) && event.observation === "task_tracking";

export const isStatusUpdate = (event: unknown): event is StatusUpdate =>
  typeof event === "object" &&
  event !== null &&
  "status_update" in event &&
  "type" in event &&
  "id" in event;

export const isActionOrObservation = (
  event: WSAICodeParsedEvent,
): event is WSAICodeAction | WSAICodeObservation =>
  isWSAICodeAction(event) || isWSAICodeObservation(event);
