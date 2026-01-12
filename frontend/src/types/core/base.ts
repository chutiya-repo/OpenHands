export type WSAI CODEEventType =
  | "message"
  | "system"
  | "agent_state_changed"
  | "change_agent_state"
  | "run"
  | "read"
  | "write"
  | "edit"
  | "run_ipython"
  | "delegate"
  | "browse"
  | "browse_interactive"
  | "reject"
  | "think"
  | "finish"
  | "error"
  | "recall"
  | "mcp"
  | "call_tool_mcp"
  | "task_tracking"
  | "user_rejected";

export type WSAI CODESourceType = "agent" | "user" | "environment";

interface WSAI CODEBaseEvent {
  id: number;
  source: WSAI CODESourceType;
  message: string;
  timestamp: string; // ISO 8601
}

export interface WSAI CODEActionEvent<
  T extends WSAI CODEEventType,
> extends WSAI CODEBaseEvent {
  action: T;
  args: Record<string, unknown>;
}

export interface WSAI CODEObservationEvent<
  T extends WSAI CODEEventType,
> extends WSAI CODEBaseEvent {
  cause: number;
  observation: T;
  content: string;
  extras: Record<string, unknown>;
}
