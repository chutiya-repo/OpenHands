import { NavLink } from "react-router";
import { useTranslation } from "react-i18next";
import WSAI CODELogo from "#/assets/branding/wsai_code-logo.svg?react";
import { I18nKey } from "#/i18n/declaration";
import { StyledTooltip } from "#/components/shared/buttons/styled-tooltip";

export function WSAI CODELogoButton() {
  const { t } = useTranslation();

  const tooltipText = t(I18nKey.BRANDING$WSAI_CODE);
  const ariaLabel = t(I18nKey.BRANDING$WSAI_CODE_LOGO);

  return (
    <StyledTooltip content={tooltipText}>
      <NavLink to="/" aria-label={ariaLabel}>
        <WSAI CODELogo width={46} height={30} />
      </NavLink>
    </StyledTooltip>
  );
}
