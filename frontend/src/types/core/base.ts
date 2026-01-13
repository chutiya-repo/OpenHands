export type WSAICodeEventType =
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

export type WSAICodeSourceType = "agent" | "user" | "environment";

interface WSAICodeBaseEvent {
  id: number;
  source: WSAICodeSourceType;
  message: string;
  timestamp: string; // ISO 8601
}

export interface WSAICodeActionEvent<
  T extends WSAICodeEventType,
> extends WSAICodeBaseEvent {
  action: T;
  args: Record<string, unknown>;
}

export interface WSAICodeObservationEvent<
  T extends WSAICodeEventType,
> extends WSAICodeBaseEvent {
  cause: number;
  observation: T;
  content: string;
  extras: Record<string, unknown>;
}
