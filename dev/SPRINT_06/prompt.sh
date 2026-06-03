#!/bin/bash

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Script para executar FASES do Sprint 06 — Experimentos + Visualizacao + Relatorios + Validacao
# Capitulos: 14 (Experimentos), 15 (Visualizacao), 16 (Relatorios), 17 (Validacao)
# Execucao automatizada via Claude CLI
# COM LOGGING COMPLETO para acompanhamento em tempo real
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# --- CONFIGURACOES ---
MAX_ITERATIONS=20
SPRINT_NUM="06"
SPRINT_NAME="Experimentos + Visualizacao + Relatorios + Validacao"

# --- DIRETORIO DE LOG ---
SPRINT_DIR="/home/guhaase/projetos/archbox/dev/SPRINT_${SPRINT_NUM}"
LOG_DIR="${SPRINT_DIR}/LOG"
mkdir -p "$LOG_DIR"

# Log principal com timestamp no nome
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
MAIN_LOG="${LOG_DIR}/sprint${SPRINT_NUM}_${TIMESTAMP}.log"
LATEST_LOG="${LOG_DIR}/latest.log"

# Criar link simbolico para o log mais recente
ln -sf "$MAIN_LOG" "$LATEST_LOG"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ARQUIVOS DE FASE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEMO_SPEC="/home/guhaase/projetos/archbox/dev/demo-plan.md"

FASE_FILES=(
    "${SPRINT_DIR}/FASE_01.md"
    "${SPRINT_DIR}/FASE_02.md"
    "${SPRINT_DIR}/FASE_03.md"
    "${SPRINT_DIR}/FASE_04.md"
    "${SPRINT_DIR}/FASE_05.md"
    "${SPRINT_DIR}/FASE_06.md"
)

# Cores para output no terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FUNCOES DE LOG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo -e "$msg" | tee -a "$MAIN_LOG"
}

log_file() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$MAIN_LOG"
}

log_separator() {
    local sep="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "$sep" | tee -a "$MAIN_LOG"
}

update_status() {
    local status_file="${LOG_DIR}/status.txt"
    cat > "$status_file" <<EOF
=== STATUS DA EXECUCAO - SPRINT ${SPRINT_NUM} ===
Atualizado em: $(date '+%Y-%m-%d %H:%M:%S')
Sprint:        ${SPRINT_NAME}
Fase atual:    $1
Arquivo:       $2
Iteracao:      $3
Pendentes:     $4
Completos:     $5
Estado:        $6
Log completo:  $MAIN_LOG
===========================
EOF
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FUNCOES AUXILIARES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

count_pending_checkboxes() {
    local file="$1"
    local count=$(grep -c "^- \[ \]" "$file" 2>/dev/null || true)
    echo "${count:-0}"
}

count_completed_checkboxes() {
    local file="$1"
    local count=$(grep -c "^- \[x\]" "$file" 2>/dev/null || true)
    echo "${count:-0}"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GERADOR DE PROMPT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

build_prompt() {
    local fase_file="$1"
    local iteration="$2"
    local fase_basename=$(basename "$fase_file")

    cat <<PROMPT_EOF
You are creating demonstration examples for the archbox Python library (ARCH/GARCH volatility models).

## Context

- **Project**: archbox — ARCH/GARCH volatility models for financial time series
- **Library location**: \`/home/guhaase/projetos/archbox/\`
- **Target directory**: \`/home/guhaase/projetos/archbox/examples/capitulos/\`
- **Sprint**: ${SPRINT_NUM} — ${SPRINT_NAME}
- **Goal**: Create Jupyter notebooks (.ipynb), R scripts (.R), and Stata scripts (.do) demonstrating archbox features

## What archbox provides

archbox is a Python library for financial volatility modeling:
- **Univariate GARCH**: GARCH, EGARCH, GJR-GARCH, APARCH, IGARCH, FIGARCH, GARCH-M, ComponentGARCH, HAR-RV
- **Multivariate**: CCC, DCC, BEKK, GO-GARCH, DECO
- **Distributions**: Normal, Student-t, GED, Skewed-t, MixtureNormal
- **Diagnostics**: ARCH-LM, Ljung-Box, Sign Bias, Nyblom, Engle-Sheppard, Hong Spillover
- **Risk**: VaR, Expected Shortfall, EWMA, Backtesting (Kupiec, Christoffersen, Basel)
- **Regime-Switching**: MS-Mean, MS-AR, MS-GARCH, MS-VAR, Hamilton Filter, Kim Smoother, EM
- **Threshold/STAR**: TAR, SETAR, LSTAR, ESTAR, linearity tests
- **Visualization**: 15+ plot functions with themes and export
- **Reports**: HTML, LaTeX, Markdown generation
- **Datasets**: 11 built-in (sp500, bitcoin, fx_majors, us_gdp, etc.)

## Important Rules

1. **Create files at the EXACT paths specified** in the specification document.
2. **Use the Write tool** to create each file. Do NOT use echo/cat with heredoc.
3. **Use the Bash tool** ONLY for mkdir and chmod commands.
4. **Do NOT modify files outside** the target directories.
5. **Jupyter notebooks** must be valid .ipynb JSON format with alternating Markdown and Code cells.
6. **Text in Portuguese** (Brazilian), code and function names in English.
7. **R scripts** use rugarch, rmgarch, MSwM, tsDyn packages as appropriate.
8. **Stata scripts** use native arch, mgarch, mswitch commands.
9. **Mark checkboxes** as you complete each task: change \`- [ ]\` to \`- [x]\` in the specification file.
10. **Skip items already marked** \`[x]\`.
11. **Continue until ALL checkboxes are** \`[x]\`.

## Jupyter Notebook Format

Each .ipynb must follow this JSON structure:
\`\`\`json
{
 "cells": [
  {"cell_type": "markdown", "metadata": {}, "source": ["# Title\\n", "Description"]},
  {"cell_type": "code", "execution_count": null, "metadata": {}, "outputs": [], "source": ["import archbox"]}
 ],
 "metadata": {
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
  "language_info": {"name": "python", "version": "3.11.0"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
\`\`\`

## Reference: Full Demo Plan

For additional context, refer to: \`${DEMO_SPEC}\`

## Your Task: ${fase_basename}

This is iteration #${iteration}. Focus on uncompleted items (unmarked checkboxes).

---
$(cat "$fase_file")
---

REMEMBER: Mark each checkbox (\`- [ ]\` -> \`- [x]\`) in \`${fase_file}\` as you complete each task.
PROMPT_EOF
}

show_progress() {
    local pending=$1
    local completed=$2
    local fase_name=$3
    local total=$((pending + completed))
    local percentage=0
    if [ $total -gt 0 ]; then
        percentage=$((completed * 100 / total))
    fi

    log_separator
    log "PROGRESSO ${fase_name}"
    log "  Completos:  ${completed}"
    log "  Pendentes:  ${pending}"
    log "  Total:      ${total}"
    log "  Progresso:  ${percentage}%"
    log_separator
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VERIFICACAO DE PRE-REQUISITOS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

log "============================================"
log "LOG DE EXECUCAO INICIADO"
log "Modulo: SPRINT ${SPRINT_NUM} — ${SPRINT_NAME}"
log "Objetivo: Criar exemplos demonstrativos"
log "Arquivo de log: $MAIN_LOG"
log "Para acompanhar em tempo real:"
log "  tail -f $LATEST_LOG"
log "Para ver status rapido:"
log "  cat ${LOG_DIR}/status.txt"
log "============================================"

# Verificar se Claude CLI esta disponivel
if ! command -v claude &> /dev/null; then
    log "ERRO: Claude CLI nao encontrado. Instale com: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

# Verificar se todos os arquivos existem
log "Verificando arquivos de fase..."
for FASE_FILE in "${FASE_FILES[@]}"; do
    if [ ! -f "$FASE_FILE" ]; then
        log "ERRO: Arquivo $FASE_FILE nao encontrado!"
        exit 1
    fi
    log_file "  OK: $(basename "$FASE_FILE")"
done

# Verificar se o spec completo existe
if [ ! -f "$DEMO_SPEC" ]; then
    log "ERRO: Demo plan nao encontrado: $DEMO_SPEC"
    exit 1
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INICIO DA EXECUCAO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOTAL_FASES=${#FASE_FILES[@]}
EXEC_START_TIME=$(date '+%Y-%m-%d %H:%M:%S')
log "Iniciando execucao automatica de ${TOTAL_FASES} FASES"
log "Inicio: ${EXEC_START_TIME}"

# Loop externo: para cada fase
for FASE_INDEX in "${!FASE_FILES[@]}"; do
    FASE_FILE="${FASE_FILES[$FASE_INDEX]}"
    FASE_NUM=$((FASE_INDEX + 1))
    FASE_NAME="FASE ${FASE_NUM}/${TOTAL_FASES}"
    FASE_BASENAME=$(basename "$FASE_FILE")

    log ""
    log "======================================================"
    log "INICIANDO ${FASE_NAME} - ${FASE_BASENAME}"
    log "Arquivo: ${FASE_FILE}"
    log "======================================================"

    # Log especifico para cada fase
    FASE_LOG="${LOG_DIR}/sprint${SPRINT_NUM}_step${FASE_NUM}_${FASE_BASENAME%.md}_${TIMESTAMP}.log"
    log "Log desta fase: ${FASE_LOG}"

    FASE_START_TIME=$(date '+%Y-%m-%d %H:%M:%S')
    ITERATION=0

    while [ $ITERATION -lt $MAX_ITERATIONS ]; do
        ITERATION=$((ITERATION + 1))
        PENDING=$(count_pending_checkboxes "$FASE_FILE")
        COMPLETED=$(count_completed_checkboxes "$FASE_FILE")

        show_progress "$PENDING" "$COMPLETED" "$FASE_NAME"
        update_status "$FASE_NAME" "$FASE_BASENAME" "$ITERATION" "$PENDING" "$COMPLETED" "EXECUTANDO"

        if [ "$PENDING" -eq 0 ]; then
            FASE_END_TIME=$(date '+%Y-%m-%d %H:%M:%S')
            log "${GREEN}SUCESSO! ${FASE_NAME} concluida!${NC}"
            log "  Inicio: ${FASE_START_TIME}"
            log "  Fim:    ${FASE_END_TIME}"
            update_status "$FASE_NAME" "$FASE_BASENAME" "$ITERATION" "0" "$COMPLETED" "CONCLUIDA"
            break
        fi

        CLAUDE_START=$(date '+%Y-%m-%d %H:%M:%S')
        CLAUDE_START_EPOCH=$(date +%s)
        log "[CLAUDE] Iniciando chamada #${ITERATION} - ${FASE_NAME} (pendentes: ${PENDING})"
        log "[CLAUDE] Inicio da chamada: ${CLAUDE_START}"

        # Arquivos para esta iteracao
        CLAUDE_RAW="${LOG_DIR}/claude_raw_sprint${SPRINT_NUM}_step${FASE_NUM}_iter${ITERATION}.jsonl"
        CLAUDE_READABLE="${LOG_DIR}/claude_readable_sprint${SPRINT_NUM}_step${FASE_NUM}_iter${ITERATION}.log"
        > "$CLAUDE_RAW"
        > "$CLAUDE_READABLE"

        # Links simbolicos para acompanhamento em tempo real
        ln -sf "$CLAUDE_RAW" "${LOG_DIR}/claude_current_raw.jsonl"
        ln -sf "$CLAUDE_READABLE" "${LOG_DIR}/claude_current.log"

        update_status "$FASE_NAME" "$FASE_BASENAME" "$ITERATION" "$PENDING" "$COMPLETED" \
            "CLAUDE EXECUTANDO (inicio: ${CLAUDE_START}) -- tail -f ${LOG_DIR}/claude_current.log"

        # Rodar claude com prompt completo
        log "[CLAUDE] Modo: prompt completo (spec + instrucoes) - iteracao ${ITERATION} (stream-json)"
        build_prompt "$FASE_FILE" "$ITERATION" | claude -p \
            --dangerously-skip-permissions \
            --verbose \
            --output-format stream-json > "$CLAUDE_RAW" 2>&1 &
        CLAUDE_PID=$!

        # Processar stream JSONL em background -> log legivel
        (
            tail -f "$CLAUDE_RAW" --pid=$CLAUDE_PID 2>/dev/null | while IFS= read -r line; do
                TYPE=$(echo "$line" | grep -oP '"type"\s*:\s*"\K[^"]+' | head -1)

                case "$TYPE" in
                    assistant)
                        TEXT=$(echo "$line" | grep -oP '"content"\s*:\s*"\K[^"]*' | head -1)
                        if [ -n "$TEXT" ]; then
                            echo "[$(date '+%H:%M:%S')] [TEXTO] ${TEXT:0:300}" >> "$CLAUDE_READABLE"
                        fi
                        ;;
                    content_block_start)
                        TOOL=$(echo "$line" | grep -oP '"name"\s*:\s*"\K[^"]+' | head -1)
                        if [ -n "$TOOL" ]; then
                            echo "[$(date '+%H:%M:%S')] [TOOL START] $TOOL" >> "$CLAUDE_READABLE"
                        fi
                        ;;
                    content_block_delta)
                        TEXT=$(echo "$line" | grep -oP '"text"\s*:\s*"\K[^"]*' | head -1)
                        if [ -n "$TEXT" ] && [ ${#TEXT} -gt 2 ]; then
                            echo "[$(date '+%H:%M:%S')] [DELTA] ${TEXT:0:200}" >> "$CLAUDE_READABLE"
                        fi
                        ;;
                    result)
                        echo "[$(date '+%H:%M:%S')] [RESULTADO FINAL]" >> "$CLAUDE_READABLE"
                        ;;
                esac
            done
        ) &
        PARSER_PID=$!

        # Monitor: atualiza status a cada 15s enquanto claude roda
        LAST_RAW_SIZE=0
        while kill -0 $CLAUDE_PID 2>/dev/null; do
            RAW_SIZE=$(wc -c < "$CLAUDE_RAW" 2>/dev/null || echo 0)
            RAW_LINES=$(wc -l < "$CLAUDE_RAW" 2>/dev/null || echo 0)
            NOW_EPOCH=$(date +%s)
            ELAPSED_SECS=$((NOW_EPOCH - CLAUDE_START_EPOCH))
            ELAPSED_MIN=$((ELAPSED_SECS / 60))
            ELAPSED_SEC=$((ELAPSED_SECS % 60))

            LIVE_PENDING=$(count_pending_checkboxes "$FASE_FILE")
            LIVE_COMPLETED=$(count_completed_checkboxes "$FASE_FILE")
            LIVE_DONE=$((LIVE_COMPLETED - COMPLETED))

            if [ "$RAW_SIZE" -gt "$LAST_RAW_SIZE" ]; then
                ACTIVITY="ativo (stream crescendo)"
            else
                ACTIVITY="aguardando resposta API"
            fi
            LAST_RAW_SIZE=$RAW_SIZE

            update_status "$FASE_NAME" "$FASE_BASENAME" "$ITERATION" "$LIVE_PENDING" "$LIVE_COMPLETED" \
                "CLAUDE EXECUTANDO | ${ELAPSED_MIN}m${ELAPSED_SEC}s | ${RAW_LINES} eventos | ${ACTIVITY} | +${LIVE_DONE} checkboxes"

            log_file "[MONITOR] ${FASE_NAME} iter#${ITERATION} | ${ELAPSED_MIN}m${ELAPSED_SEC}s | ${RAW_LINES} eventos | ${RAW_SIZE} bytes | ${ACTIVITY} | checkboxes: ${LIVE_COMPLETED}/${LIVE_PENDING}"

            sleep 15
        done

        # Claude terminou
        wait $CLAUDE_PID
        CLAUDE_EXIT_CODE=$?

        sleep 2
        kill $PARSER_PID 2>/dev/null
        wait $PARSER_PID 2>/dev/null

        CLAUDE_END=$(date '+%Y-%m-%d %H:%M:%S')
        FINAL_RAW_LINES=$(wc -l < "$CLAUDE_RAW" 2>/dev/null || echo 0)
        FINAL_RAW_SIZE=$(wc -c < "$CLAUDE_RAW" 2>/dev/null || echo 0)
        log "[CLAUDE] Fim da chamada: ${CLAUDE_END} (exit: ${CLAUDE_EXIT_CODE}, ${FINAL_RAW_LINES} eventos JSONL, ${FINAL_RAW_SIZE} bytes)"

        # Copiar logs
        echo "--- CLAUDE READABLE: ${FASE_NAME} iter#${ITERATION} [${CLAUDE_START} -> ${CLAUDE_END}] ---" >> "$FASE_LOG"
        cat "$CLAUDE_READABLE" >> "$FASE_LOG"
        echo "--- END ---" >> "$FASE_LOG"

        echo "[$(date '+%Y-%m-%d %H:%M:%S')] [CLAUDE READABLE ${FASE_NAME} iter#${ITERATION}]" >> "$MAIN_LOG"
        cat "$CLAUDE_READABLE" >> "$MAIN_LOG"

        if [ $CLAUDE_EXIT_CODE -ne 0 ]; then
            log "${RED}[ERRO] Claude retornou codigo ${CLAUDE_EXIT_CODE}. Tentando novamente em 2s...${NC}"
            update_status "$FASE_NAME" "$FASE_BASENAME" "$ITERATION" "$PENDING" "$COMPLETED" "ERRO (code ${CLAUDE_EXIT_CODE}) - retentativa em 2s"
            sleep 2
            continue
        fi

        # Verificar progresso
        NEW_PENDING=$(count_pending_checkboxes "$FASE_FILE")
        NEW_COMPLETED=$(count_completed_checkboxes "$FASE_FILE")
        CHECKBOXES_RESOLVIDOS=$((NEW_COMPLETED - COMPLETED))

        log "[PROGRESSO] Antes: ${COMPLETED} completos, ${PENDING} pendentes"
        log "[PROGRESSO] Depois: ${NEW_COMPLETED} completos, ${NEW_PENDING} pendentes"
        log "[PROGRESSO] Checkboxes resolvidos nesta iteracao: ${CHECKBOXES_RESOLVIDOS}"

        if [ "$NEW_PENDING" -eq "$PENDING" ]; then
            log "${YELLOW}[ALERTA] Nenhum checkbox foi resolvido nesta iteracao!${NC}"
        fi

        sleep 3
    done

    if [ "$PENDING" -ne 0 ]; then
        log "${RED}LIMITE DE ITERACOES ATINGIDO para ${FASE_NAME}!${NC}"
        update_status "$FASE_NAME" "$FASE_BASENAME" "$ITERATION" "$PENDING" "$COMPLETED" "FALHA - limite de iteracoes"
        exit 1
    fi
done

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VERIFICACAO FINAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXEC_END_TIME=$(date '+%Y-%m-%d %H:%M:%S')
log ""
log "======================================================"
log "${GREEN}TODAS AS FASES CONCLUIDAS COM SUCESSO!${NC}"
log "Inicio: ${EXEC_START_TIME}"
log "Fim:    ${EXEC_END_TIME}"
log "======================================================"
log ""
log "Exemplos criados em: /home/guhaase/projetos/archbox/examples/capitulos/"
log ""
log "Capitulos deste sprint:"
log "  14_experimentos/"
log "  15_visualizacao/"
log "  16_relatorios/"
log "  17_validacao_cruzada/"
log ""

update_status "TODAS" "N/A" "N/A" "0" "N/A" "CONCLUIDO - ${EXEC_END_TIME}"
exit 0
