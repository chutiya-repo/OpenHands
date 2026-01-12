import { WSAI CODEAction } from "./actions";
import { WSAI CODEObservation } from "./observations";
import { WSAI CODEVariance } from "./variances";

/**
 * @deprecated Will be removed once we fully transition to v1 events
 */
export type WSAI CODEParsedEvent =
  | WSAI CODEAction
  | WSAI CODEObservation
  | WSAI CODEVariance;
