@echo off
cd /d C:\Projects\eq-context
git add sks-team/gateway.md sks-team/variations.md sks-team/mops.md sks-team/clients/equinix.md sks-team/clients/schneider.md sks-team/README.md
git commit -m "sks-team: add gateway router, variations, mops, client refs — skeleton expansion"
git push origin main
echo.
echo Done. Supabase will sync within ~60s.
pause
