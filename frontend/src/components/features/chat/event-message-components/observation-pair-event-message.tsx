import React from "react";
import { WSAI CODEAction } from "#/types/core/actions";
import { isWSAI CODEAction } from "#/types/core/guards";
import { ChatMessage } from "../chat-message";
import { MicroagentStatusWrapper } from "./microagent-status-wrapper";
import { MicroagentStatus } from "#/types/microagent-status";

const hasThoughtProperty = (
  obj: Record<string, unknown>,
): obj is { thought: string } => "thought" in obj && !!obj.thought;

interface ObservationPairEventMessageProps {
  event: WSAI CODEAction;
  microagentStatus?: MicroagentStatus | null;
  microagentConversationId?: string;
  microagentPRUrl?: string;
  actions?: Array<{
    icon: React.ReactNode;
    onClick: () => void;
    tooltip?: string;
  }>;
}

export function ObservationPairEventMessage({
  event,
  microagentStatus,
  microagentConversationId,
  microagentPRUrl,
  actions,
}: ObservationPairEventMessageProps) {
  if (!isWSAI CODEAction(event)) {
    return null;
  }

  if (hasThoughtProperty(event.args) && event.action !== "think") {
    return (
      <div>
        <ChatMessage
          type="agent"
          message={event.args.thought}
          actions={actions}
        />
        <MicroagentStatusWrapper
          microagentStatus={microagentStatus}
          microagentConversationId={microagentConversationId}
          microagentPRUrl={microagentPRUrl}
          actions={actions}
        />
      </div>
    );
  }

  return (
    <MicroagentStatusWrapper
      microagentStatus={microagentStatus}
      microagentConversationId={microagentConversationId}
      microagentPRUrl={microagentPRUrl}
      actions={actions}
    />
  );
}
