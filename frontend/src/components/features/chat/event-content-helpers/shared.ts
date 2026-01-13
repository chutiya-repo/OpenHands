import { WSAICodeAction } from "#/types/core/actions";
import { WSAICodeObservation } from "#/types/core/observations";

export const MAX_CONTENT_LENGTH = 1000;

export const getDefaultEventContent = (
  event: WSAICodeAction | WSAICodeObservation,
): string => `\`\`\`json\n${JSON.stringify(event, null, 2)}\n\`\`\``;
