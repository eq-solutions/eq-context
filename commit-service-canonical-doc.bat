@echo off
REM Commits the Service-consumes-canonical design + decision record to eq-context main.
REM Supabase context server syncs from GitHub within ~60s.
cd /d "C:\Projects\eq-context"
git add "eq/canonical-readiness/service-consumes-canonical-spine-2026-06-16.md"
git commit -m "docs: ratify SoR = sks-canonical app_data; EQ Service consumes spine (design + decision record)" -m "Royce 2026-06-16: 'sks canonical is the truth.' Phased plan for EQ Service to read canonical customers/sites via security_invoker bridge views, gated on the customer-master dedupe. Companion to contract-scope-canonical-design-2026-06-15." -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
git push origin main
echo.
echo Done. Pushed to eq-context main.
pause
