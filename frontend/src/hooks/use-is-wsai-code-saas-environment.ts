import { useMemo } from "react";

/**
 * Hook to check if the current domain is an All Hands SaaS environment
 * @returns True if the current domain contains "wsai-code.dev" or "wsaicode.dev" postfix
 */
export const useIsWSAICodeSaaSEnvironment = (): boolean =>
  useMemo(() => {
    const { hostname } = window.location;
    return (
      hostname.endsWith("wsai-code.dev") || hostname.endsWith("wsaicode.dev")
    );
  }, []);
