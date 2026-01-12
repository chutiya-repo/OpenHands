import { WSAI CODEAction } from "#/types/core/actions";
import { WSAI CODEEventType } from "#/types/core/base";
import {
  isCommandAction,
  isCommandObservation,
  isWSAI CODEAction,
  isWSAI CODEObservation,
} from "#/types/core/guards";
import { WSAI CODEObservation } from "#/types/core/observations";

const COMMON_NO_RENDER_LIST: WSAI CODEEventType[] = [
  "system",
  "agent_state_changed",
  "change_agent_state",
];

const ACTION_NO_RENDER_LIST: WSAI CODEEventType[] = ["recall"];

const OBSERVATION_NO_RENDER_LIST: WSAI CODEEventType[] = ["think"];

export const shouldRenderEvent = (
  event: WSAI CODEAction | WSAI CODEObservation,
) => {
  if (isWSAI CODEAction(event)) {
    if (isCommandAction(event) && event.source === "user") {
      // For user commands, we always hide them from the chat interface
      return false;
    }

    const noRenderList = COMMON_NO_RENDER_LIST.concat(ACTION_NO_RENDER_LIST);
    return !noRenderList.includes(event.action);
  }

  if (isWSAI CODEObservation(event)) {
    if (isCommandObservation(event) && event.source === "user") {
      // For user commands, we always hide them from the chat interface
      return false;
    }

    const noRenderList = COMMON_NO_RENDER_LIST.concat(
      OBSERVATION_NO_RENDER_LIST,
    );
    return !noRenderList.includes(event.observation);
  }

  return true;
};

export const hasUserEvent = (
  events: (WSAI CODEAction | WSAI CODEObservation)[],
) =>
  events.some((event) => isWSAI CODEAction(event) && event.source === "user");
