import { wsaiCode } from "./wsai-code-axios";
import {
  CustomSecret,
  GetSecretsResponse,
  POSTProviderTokens,
} from "./secrets-service.types";
import { Provider, ProviderToken } from "#/types/settings";

export class SecretsService {
  static async getSecrets() {
    const { data } = await wsaiCode.get<GetSecretsResponse>("/api/secrets");
    return data.custom_secrets;
  }

  static async createSecret(name: string, value: string, description?: string) {
    const secret: CustomSecret = {
      name,
      value,
      description,
    };

    const { status } = await wsaiCode.post("/api/secrets", secret);
    return status === 201;
  }

  static async updateSecret(id: string, name: string, description?: string) {
    const secret: Omit<CustomSecret, "value"> = {
      name,
      description,
    };

    const { status } = await wsaiCode.put(`/api/secrets/${id}`, secret);
    return status === 200;
  }

  static async deleteSecret(id: string) {
    const { status } = await wsaiCode.delete<boolean>(`/api/secrets/${id}`);
    return status === 200;
  }

  static async addGitProvider(providers: Record<Provider, ProviderToken>) {
    const tokens: POSTProviderTokens = {
      provider_tokens: providers,
    };
    const { data } = await wsaiCode.post<boolean>(
      "/api/add-git-providers",
      tokens,
    );
    return data;
  }
}
