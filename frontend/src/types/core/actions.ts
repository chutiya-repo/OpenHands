import { WSAI CODEActionEvent } from "./base";
import { ActionSecurityRisk } from "#/stores/security-analyzer-store";

export interface UserMessageAction extends WSAI CODEActionEvent<"message"> {
  source: "user";
  args: {
    content: string;
    image_urls: string[];
    file_urls: string[];
  };
}

export interface SystemMessageAction extends WSAI CODEActionEvent<"system"> {
  source: "agent" | "environment";
  args: {
    content: string;
    tools: Array<Record<string, unknown>> | null;
    wsai_code_version: string | null;
    agent_class: string | null;
  };
}

export interface CommandAction extends WSAI CODEActionEvent<"run"> {
  source: "agent" | "user";
  args: {
    command: string;
    security_risk: ActionSecurityRisk;
    confirmation_state: "confirmed" | "rejected" | "awaiting_confirmation";
    thought: string;
    hidden?: boolean;
  };
}

export interface AssistantMessageAction extends WSAI CODEActionEvent<"message"> {
  source: "agent";
  args: {
    thought: string;
    image_urls: string[] | null;
    file_urls: string[];
    wait_for_response: boolean;
  };
}

export interface IPythonAction extends WSAI CODEActionEvent<"run_ipython"> {
  source: "agent";
  args: {
    code: string;
    security_risk: ActionSecurityRisk;
    confirmation_state: "confirmed" | "rejected" | "awaiting_confirmation";
    kernel_init_code: string;
    thought: string;
  };
}

export interface ThinkAction extends WSAI CODEActionEvent<"think"> {
  source: "agent";
  args: {
    thought: string;
  };
}

export interface FinishAction extends WSAI CODEActionEvent<"finish"> {
  source: "agent";
  args: {
    final_thought: string;
    outputs: Record<string, unknown>;
    thought: string;
  };
}

export interface DelegateAction extends WSAI CODEActionEvent<"delegate"> {
  source: "agent";
  timeout: number;
  args: {
    agent: "BrowsingAgent";
    inputs: Record<string, string>;
    thought: string;
  };
}

export interface BrowseAction extends WSAI CODEActionEvent<"browse"> {
  source: "agent";
  args: {
    url: string;
    thought: string;
  };
}

export interface BrowseInteractiveAction extends WSAI CODEActionEvent<"browse_interactive"> {
  source: "agent";
  timeout: number;
  args: {
    browser_actions: string;
    thought: string | null;
    browsergym_send_msg_to_user: string;
  };
}

export interface FileReadAction extends WSAI CODEActionEvent<"read"> {
  source: "agent";
  args: {
    path: string;
    thought: string;
    security_risk: ActionSecurityRisk | null;
    impl_source?: string;
    view_range?: number[] | null;
  };
}

export interface FileWriteAction extends WSAI CODEActionEvent<"write"> {
  source: "agent";
  args: {
    path: string;
    content: string;
    thought: string;
  };
}

export interface FileEditAction extends WSAI CODEActionEvent<"edit"> {
  source: "agent";
  args: {
    path: string;
    command?: string;
    file_text?: string | null;
    view_range?: number[] | null;
    old_str?: string | null;
    new_str?: string | null;
    insert_line?: number | null;
    content?: string;
    start?: number;
    end?: number;
    thought: string;
    security_risk: ActionSecurityRisk | null;
    impl_source?: string;
  };
}

export interface RejectAction extends WSAI CODEActionEvent<"reject"> {
  source: "agent";
  args: {
    thought: string;
  };
}

export interface RecallAction extends WSAI CODEActionEvent<"recall"> {
  source: "agent";
  args: {
    recall_type: "workspace_context" | "knowledge";
    query: string;
    thought: string;
  };
}

export interface MCPAction extends WSAI CODEActionEvent<"call_tool_mcp"> {
  source: "agent";
  args: {
    name: string;
    arguments: Record<string, unknown>;
    thought?: string;
  };
}

export interface TaskTrackingAction extends WSAI CODEActionEvent<"task_tracking"> {
  source: "agent";
  args: {
    command: string;
    task_list: Array<{
      id: string;
      title: string;
      status: "todo" | "in_progress" | "done";
      notes?: string;
    }>;
    thought: string;
  };
}

export type WSAI CODEAction =
  | UserMessageAction
  | AssistantMessageAction
  | SystemMessageAction
  | CommandAction
  | IPythonAction
  | ThinkAction
  | FinishAction
  | DelegateAction
  | BrowseAction
  | BrowseInteractiveAction
  | FileReadAction
  | FileEditAction
  | FileWriteAction
  | RejectAction
  | RecallAction
  | MCPAction
  | TaskTrackingAction;
