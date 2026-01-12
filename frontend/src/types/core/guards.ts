import { WSAI CODEParsedEvent } from ".";
import {
  UserMessageAction,
  AssistantMessageAction,
  WSAI CODEAction,
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
  WSAI CODEObservation,
  TaskTrackingObservation,
} from "./observations";
import { StatusUpdate } from "./variances";

export const isWSAI CODEEvent = (
  event: unknown,
): event is WSAI CODEParsedEvent =>
  typeof event === "object" &&
  event !== null &&
  "id" in event &&
  "source" in event &&
  "message" in event &&
  "timestamp" in event;

export const isWSAI CODEAction = (
  event: WSAI CODEParsedEvent,
): event is WSAI CODEAction => "action" in event;

export const isWSAI CODEObservation = (
  event: WSAI CODEParsedEvent,
): event is WSAI CODEObservation => "observation" in event;

export const isUserMessage = (
  event: WSAI CODEParsedEvent,
): event is UserMessageAction =>
  isWSAI CODEAction(event) &&
  event.source === "user" &&
  event.action === "message";

export const isAssistantMessage = (
  event: WSAI CODEParsedEvent,
): event is AssistantMessageAction =>
  isWSAI CODEAction(event) &&
  event.source === "agent" &&
  (event.action === "message" || event.action === "finish");

export const isErrorObservation = (
  event: WSAI CODEParsedEvent,
): event is ErrorObservation =>
  isWSAI CODEObservation(event) && event.observation === "error";

export const isCommandAction = (
  event: WSAI CODEParsedEvent,
): event is CommandAction => isWSAI CODEAction(event) && event.action === "run";

export const isAgentStateChangeObservation = (
  event: WSAI CODEParsedEvent,
): event is AgentStateChangeObservation =>
  isWSAI CODEObservation(event) && event.observation === "agent_state_changed";

export const isCommandObservation = (
  event: WSAI CODEParsedEvent,
): event is CommandObservation =>
  isWSAI CODEObservation(event) && event.observation === "run";

export const isFinishAction = (
  event: WSAI CODEParsedEvent,
): event is FinishAction =>
  isWSAI CODEAction(event) && event.action === "finish";

export const isSystemMessage = (
  event: WSAI CODEParsedEvent,
): event is SystemMessageAction =>
  isWSAI CODEAction(event) && event.action === "system";

export const isRejectObservation = (
  event: WSAI CODEParsedEvent,
): event is WSAI CODEObservation =>
  isWSAI CODEObservation(event) && event.observation === "user_rejected";

export const isMcpObservation = (
  event: WSAI CODEParsedEvent,
): event is MCPObservation =>
  isWSAI CODEObservation(event) && event.observation === "mcp";

export const isTaskTrackingAction = (
  event: WSAI CODEParsedEvent,
): event is TaskTrackingAction =>
  isWSAI CODEAction(event) && event.action === "task_tracking";

export const isTaskTrackingObservation = (
  event: WSAI CODEParsedEvent,
): event is TaskTrackingObservation =>
  isWSAI CODEObservation(event) && event.observation === "task_tracking";

export const isStatusUpdate = (event: unknown): event is StatusUpdate =>
  typeof event === "object" &&
  event !== null &&
  "status_update" in event &&
  "type" in event &&
  "id" in event;

export const isActionOrObservation = (
  event: WSAI CODEParsedEvent,
): event is WSAI CODEAction | WSAI CODEObservation =>
  isWSAI CODEAction(event) || isWSAI CODEObservation(event);
