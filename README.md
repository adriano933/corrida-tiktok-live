# 🏁 Corrida Lula x Bolsonaro — VGZERATV

Jogo recreativo para TikTok LIVE, com corrida animada, presentes, OBS e painel local.

## Demonstração
Após configurar GitHub Pages (Settings > Pages > Source: GitHub Actions):
https://adriano933.github.io/corrida-tiktok-live/

A demonstração usa controles de teste; **não recebe presentes reais**.

## Uso no Windows
1. Baixe o código do repositório (Code > Download ZIP).
2. Instale Python 3.11 ou superior.
3. Execute `app/INICIAR_WINDOWS.bat`.
4. Abra o painel: http://127.0.0.1:8765/controle
5. Configure seu @ do TikTok e os presentes. Reinicie o servidor após alterar o @.
6. Inicie a transmissão TikTok LIVE.
7. OBS > Fonte > Navegador: http://127.0.0.1:8765/ (1280 × 720).

## Windows sem Python
Em Actions > Gerar aplicativo Windows > Run workflow, gere e baixe o artefato. A compilação e a integração precisam ser testadas numa máquina Windows.

## Atenção
- TikTokLive é biblioteca independente e **não oficial**; pode deixar de funcionar com alterações do TikTok.
- O GitHub Pages só exibe a demonstração, não conecta ao TikTok.
- O servidor é local e não deve ser exposto na internet.
- Presentes são pagos; divulgue as regras e não prometa premiações ou votos reais.
- Jogo de paródia recreativa, sem vínculo com políticos, campanhas ou TikTok.
