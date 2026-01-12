import { SuggestedTask } from "#/utils/types";
import { wsaiCode } from "../wsai-code-axios";

export class SuggestionsService {
  static async getSuggestedTasks(): Promise<SuggestedTask[]> {
    const { data } = await wsaiCode.get("/api/user/suggested-tasks");
    return data;
  }
}
