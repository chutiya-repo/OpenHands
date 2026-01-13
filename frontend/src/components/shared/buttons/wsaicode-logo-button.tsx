import { NavLink } from "react-router";
import { useTranslation } from "react-i18next";
import WSAICodeLogo from "#/assets/branding/wsaicode-logo.svg?react";
import { I18nKey } from "#/i18n/declaration";
import { StyledTooltip } from "#/components/shared/buttons/styled-tooltip";

export function WSAICodeLogoButton() {
  const { t } = useTranslation();

  const tooltipText = t(I18nKey.BRANDING$WSAI_CODE);
  const ariaLabel = t(I18nKey.BRANDING$WSAI_CODE_LOGO);

  return (
    <StyledTooltip content={tooltipText}>
      <NavLink to="/" aria-label={ariaLabel}>
        <WSAICodeLogo width={46} height={30} />
      </NavLink>
    </StyledTooltip>
  );
}
