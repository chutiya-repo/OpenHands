import { WSAI CODEEvent } from "#/types/v1/core";

export const MAX_CONTENT_LENGTH = 1000;

export const getDefaultEventContent = (event: WSAI CODEEvent): string =>
  `\`\`\`json\n${JSON.stringify(event, null, 2)}\n\`\`\``;
